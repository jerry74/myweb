"""TripHelper 新行程頁面工作流。

常用指令（皆在 repo 根目錄執行）：

    python scripts/trip-page.py styles 海島            # 依關鍵字挑風格
    python scripts/trip-page.py create --id 20270403-kyoto --name "2027 京都親子行程" \\
        --start-date 2027-04-03 --end-date 2027-04-06 --style sakura-promenade --timezone +09:00
    python scripts/trip-page.py build --id 20270403-kyoto   # 改完 YAML 後重新產生
    python scripts/trip-page.py verify --id 20270403-kyoto  # 加 --strict 會擋下仍有「待補」的行程
    python scripts/trip-page.py gallery                     # 產生即時風格廊（不需重拍截圖）
    python scripts/trip-page.py new-style --id my-style --label "我的風格" --base coastal-breeze
"""

import argparse
import hashlib
import html
import importlib.util
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = Path("templates") / "trip-pwa"
DESIGN_DIR = Path("design-system") / "triphelper-next"
REGISTRY_FILE = DESIGN_DIR / "styles.json"
TEMPLATE_ROOT = ROOT / TEMPLATE_DIR
TRIP_ID_PATTERN = re.compile(r"^(?P<date>\d{8})-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$")
STYLE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)+$")
TIMEZONE_PATTERN = re.compile(r"^[+-](?:0\d|1[0-4]):[0-5]\d$")
TIME_PATTERN = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
STYLE_SELECTOR_PATTERN = re.compile(r'data-style="([^"]+)"')
PLACEHOLDER_PATTERN = re.compile(r"待補|待確認|待規劃")
WEEKDAYS = "一二三四五六日"
CARD_START = "<!-- TRIP-PAGES:START -->"
CARD_END = "<!-- TRIP-PAGES:END -->"
SITE_ASSETS = ("index.html", "styles.css", "app.js", "data.generated.json", "data.fallback.js", "manifest.webmanifest")


class WorkflowError(RuntimeError):
    pass


# ---------------------------------------------------------------------------
# Style registry: design-system/triphelper-next/styles.json is the only list.
# ---------------------------------------------------------------------------


def load_style_registry(root: Path = ROOT) -> tuple[str, dict[str, dict[str, str]]]:
    path = root / REGISTRY_FILE
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise WorkflowError(f"無法讀取風格登錄檔：{path}（{error}）") from error
    profiles: dict[str, dict[str, str]] = {}
    for entry in document.get("styles", []):
        profiles[entry["id"]] = {
            "label": entry["label"],
            "fits": entry.get("fits", ""),
            "vibe": entry.get("vibe", ""),
            "background_color": entry["backgroundColor"],
            "theme_color": entry["themeColor"],
        }
    default = document.get("default")
    if default not in profiles:
        raise WorkflowError(f"風格登錄檔的 default 不在清單中：{default}")
    return default, profiles


DEFAULT_STYLE, STYLE_PROFILES = load_style_registry()


def get_style_profile(style_id: str | None) -> tuple[str, dict[str, str]]:
    resolved = style_id or DEFAULT_STYLE
    profile = STYLE_PROFILES.get(resolved)
    if profile is None:
        hint = "；用 `python scripts/trip-page.py styles` 查看可用風格"
        close = [sid for sid in STYLE_PROFILES if resolved.split("-")[0] in sid]
        suggestion = f"，是不是指 {', '.join(close[:3])}" if close else ""
        raise WorkflowError(f"未知的行程風格：{resolved}{suggestion}{hint}")
    return resolved, profile


# ---------------------------------------------------------------------------
# CSS: split the shared stylesheet into top-level rules so a trip page only
# ships the base tokens/components plus its own style profile.
# ---------------------------------------------------------------------------


def split_css_rules(text: str) -> tuple[list[tuple[str, str]], str]:
    """Return ([(selector, segment)], tail). Each segment keeps its leading comments/whitespace."""
    rules: list[tuple[str, str]] = []
    depth = 0
    index = 0
    segment_start = 0
    selector_start: int | None = None
    quote: str | None = None
    length = len(text)
    while index < length:
        char = text[index]
        if quote:
            if char == "\\":
                index += 2
                continue
            if char == quote:
                quote = None
        elif text.startswith("/*", index):
            end = text.find("*/", index + 2)
            if end < 0:
                raise WorkflowError("styles.css 有未結束的註解")
            index = end + 2
            continue
        elif char in "\"'":
            quote = char
        elif char == "{":
            if depth == 0:
                selector_start = segment_start
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                raise WorkflowError("styles.css 大括號不成對")
            if depth == 0:
                segment = text[segment_start : index + 1]
                prelude = segment[: segment.index("{")] if selector_start is not None else ""
                selector = re.sub(r"/\*.*?\*/", "", prelude, flags=re.DOTALL).strip()
                rules.append((selector, segment))
                segment_start = index + 1
                selector_start = None
        index += 1
    if depth != 0:
        raise WorkflowError("styles.css 大括號不成對")
    return rules, text[segment_start:]


def strip_leading_trivia(segment: str) -> str:
    """Drop the whitespace and comments that precede a rule's selector."""
    text = segment.lstrip()
    while text.startswith("/*"):
        text = text[text.index("*/") + 2 :].lstrip()
    return text


def rule_styles(selector: str) -> set[str]:
    return set(STYLE_SELECTOR_PATTERN.findall(selector))


def render_stylesheet(style: str, template_root: Path = TEMPLATE_ROOT) -> str:
    source = (template_root / "styles.css").read_text(encoding="utf-8")
    rules, tail = split_css_rules(source)
    kept = []
    for selector, segment in rules:
        styles = rule_styles(selector)
        if styles and style not in styles:
            continue
        kept.append(segment)
    header = f"/* Generated by scripts/trip-page.py from templates/trip-pwa/styles.css (style: {style}). Do not edit. */\n"
    return header + "".join(kept).lstrip("\n") + tail


# ---------------------------------------------------------------------------
# Trip data
# ---------------------------------------------------------------------------


def load_trip_builder():
    builder_path = ROOT / "scripts" / "build-trip.py"
    spec = importlib.util.spec_from_file_location("triphelper_build_trip", builder_path)
    if spec is None or spec.loader is None:
        raise WorkflowError(f"無法載入產生器：{builder_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_iso_date(value: str, label: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise WorkflowError(f"{label} 必須是 YYYY-MM-DD：{value}") from error


def validate_identity(trip_id: str, start_date: date, end_date: date) -> tuple[str, str]:
    match = TRIP_ID_PATTERN.fullmatch(trip_id)
    if not match:
        raise WorkflowError("--id 必須使用 YYYYMMDD-slug（小寫英數與連字號），例如 20270403-kyoto")
    site_dir = match.group("date")
    if site_dir != start_date.strftime("%Y%m%d"):
        raise WorkflowError(f"--id 的日期前綴必須等於 --start-date；可改用 {start_date:%Y%m%d}-{match.group('slug')}")
    if end_date < start_date:
        raise WorkflowError("--end-date 不可早於 --start-date")
    if (end_date - start_date).days > 45:
        raise WorkflowError("單一行程不可超過 46 天")
    return site_dir, match.group("slug")


def format_date_range(start_date: date, end_date: date) -> str:
    return f"{start_date:%Y/%m/%d} - {end_date:%Y/%m/%d}"


def make_trip_data(
    trip_id: str,
    name: str,
    short_name: str,
    start_date: date,
    end_date: date,
    summary: str,
    style: str = DEFAULT_STYLE,
    timezone: str = "+08:00",
    departure_time: str = "09:00",
) -> dict:
    days = []
    breakfasts = {}
    rain_rules = {}
    stays = {}
    current = start_date
    day_number = 1

    while current <= end_date:
        iso_date = current.isoformat()
        days.append(
            {
                "date": iso_date,
                "weekday": WEEKDAYS[current.weekday()],
                "title": f"Day {day_number} 行程待規劃",
                "stay": "住宿待確認",
                "tags": [],
                "rainPlan": "待補雨天替代方案。",
                "schedule": [
                    {"time": "09:00", "text": "待補上午行程。", "links": []},
                    {"time": "14:00", "text": "待補下午行程。", "links": []},
                    {"time": "18:00", "text": "待補晚間行程。", "links": []},
                ],
                "food": [
                    {"title": "早餐", "text": "待補。", "links": []},
                    {"title": "午餐", "text": "待補。", "links": []},
                    {"title": "晚餐", "text": "待補。", "links": []},
                ],
            }
        )
        breakfasts[iso_date] = "待補前一晚或當天早餐安排。"
        rain_rules[iso_date] = "待補雨天切換原則。"
        stays[iso_date] = {"name": "住宿待確認", "mapUrl": ""}
        current += timedelta(days=1)
        day_number += 1

    return {
        "trip": {
            "id": trip_id,
            "name": name,
            "shortName": short_name,
            "description": summary,
            "style": style,
            "dateRange": format_date_range(start_date, end_date),
            "flights": "待補",
            "carRental": "待補",
            "rainFocus": "待補",
            "startAt": f"{start_date.isoformat()}T00:00:00{timezone}",
            "departureAt": f"{start_date.isoformat()}T{departure_time}:00{timezone}",
            "endAt": f"{end_date.isoformat()}T23:59:59{timezone}",
        },
        "links": {},
        "days": days,
        "breakfasts": breakfasts,
        "rainRules": rain_rules,
        "stays": stays,
    }


def _parse_datetime(value, path: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str):
        errors.append(f"{path} 必須是 ISO 時間字串，例如 '2027-04-03T09:00:00+09:00'")
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        errors.append(f"{path} 不是有效的 ISO 時間：{value}")
        return None


def _check_time(value, path: str, errors: list[str]) -> None:
    if isinstance(value, int) and not isinstance(value, bool):
        hours, minutes = divmod(value, 60)
        errors.append(f"{path} 被 YAML 解析成數字 {value}，請加引號寫成 '{hours:02d}:{minutes:02d}'")
    elif not isinstance(value, str) or not value.strip():
        errors.append(f"{path} 必須是文字，例如 '09:30' 或「上午」")


def _check_links(links, path: str, errors: list[str]) -> None:
    if links is None:
        return
    if not isinstance(links, list):
        errors.append(f"{path} 必須是清單")
        return
    for index, link in enumerate(links):
        item_path = f"{path}[{index}]"
        if isinstance(link, list) and len(link) == 2:
            label, url = link
        elif isinstance(link, dict):
            label, url = link.get("label"), link.get("url")
        else:
            errors.append(f"{item_path} 必須是 [名稱, 網址] 或 {{label, url}}")
            continue
        if not isinstance(label, str) or not label.strip():
            errors.append(f"{item_path} 缺少連結名稱")
        if not isinstance(url, str) or not re.match(r"^(https?://|tel:|mailto:)", url):
            errors.append(f"{item_path} 的網址必須以 https:// 開頭：{url}")


def validate_trip_data(data, trip_id: str) -> list[str]:
    """Return human-readable problems; an empty list means the YAML is publishable."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["YAML 最外層必須是物件（trip / days / stays …）"]
    trip = data.get("trip")
    if not isinstance(trip, dict):
        return ["缺少 trip 區塊"]
    if trip.get("id") != trip_id:
        errors.append(f"trip.id 必須是 {trip_id}，目前是 {trip.get('id')}")
    for key in ("name", "shortName", "dateRange"):
        if not isinstance(trip.get(key), str) or not trip[key].strip():
            errors.append(f"trip.{key} 必須是非空文字")
    start = _parse_datetime(trip.get("startAt"), "trip.startAt", errors)
    end = _parse_datetime(trip.get("endAt"), "trip.endAt", errors)
    if "departureAt" in trip:
        _parse_datetime(trip.get("departureAt"), "trip.departureAt", errors)
    if start and end and end < start:
        errors.append("trip.endAt 不可早於 trip.startAt")

    days = data.get("days")
    if not isinstance(days, list) or not days:
        errors.append("days 至少需要一天")
        days = []
    seen_dates: set[str] = set()
    for day_index, day in enumerate(days):
        path = f"days[{day_index}]"
        if not isinstance(day, dict):
            errors.append(f"{path} 必須是物件")
            continue
        day_date = day.get("date")
        if not isinstance(day_date, str):
            errors.append(f"{path}.date 必須加引號寫成 '2027-04-03'")
        else:
            if day_date in seen_dates:
                errors.append(f"{path}.date 重複：{day_date}")
            seen_dates.add(day_date)
            try:
                parsed = date.fromisoformat(day_date)
            except ValueError:
                parsed = None
            if parsed is not None:
                if start and end and not (start.date() <= parsed <= end.date()):
                    errors.append(f"{path}.date {day_date} 不在 trip.startAt～endAt 之間")
                expected = WEEKDAYS[parsed.weekday()]
                if day.get("weekday") != expected:
                    errors.append(f"{path}.weekday 應為「{expected}」（{day_date}）")
        if not isinstance(day.get("title"), str) or not day["title"].strip():
            errors.append(f"{path}.title 必須是非空文字")
        schedule = day.get("schedule", [])
        if not isinstance(schedule, list):
            errors.append(f"{path}.schedule 必須是清單")
            schedule = []
        for entry_index, entry in enumerate(schedule):
            entry_path = f"{path}.schedule[{entry_index}]"
            if not isinstance(entry, dict):
                errors.append(f"{entry_path} 必須是物件（time / text / links）")
                continue
            _check_time(entry.get("time"), f"{entry_path}.time", errors)
            if not isinstance(entry.get("text"), str) or not entry["text"].strip():
                errors.append(f"{entry_path}.text 必須是非空文字")
            _check_links(entry.get("links"), f"{entry_path}.links", errors)
        for meal_index, meal in enumerate(day.get("food", []) or []):
            meal_path = f"{path}.food[{meal_index}]"
            if not isinstance(meal, dict) or not isinstance(meal.get("title"), str):
                errors.append(f"{meal_path} 必須有 title 與 text")
                continue
            _check_links(meal.get("links"), f"{meal_path}.links", errors)
        for item_index, item in enumerate(day.get("shoppingBackup", []) or []):
            _check_links(item.get("links") if isinstance(item, dict) else None, f"{path}.shoppingBackup[{item_index}].links", errors)
        tags = day.get("tags", [])
        if tags is not None and (not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags)):
            errors.append(f"{path}.tags 必須是文字清單")

    stays = data.get("stays", {}) or {}
    if not isinstance(stays, dict):
        errors.append("stays 必須是以日期為 key 的物件")
    else:
        for key, stay in stays.items():
            if str(key) not in seen_dates:
                errors.append(f"stays 的日期 {key} 不在 days 中")
            if not isinstance(stay, dict) or not isinstance(stay.get("name"), str):
                errors.append(f"stays.{key}.name 必須是文字")
            elif stay.get("mapUrl") and not str(stay["mapUrl"]).startswith("http"):
                errors.append(f"stays.{key}.mapUrl 必須以 https:// 開頭")
    return errors


def find_placeholders(value, path: str = "") -> list[str]:
    if isinstance(value, str):
        return [path] if PLACEHOLDER_PATTERN.search(value) else []
    if isinstance(value, dict):
        found = []
        for key, item in value.items():
            found += find_placeholders(item, f"{path}.{key}" if path else str(key))
        return found
    if isinstance(value, list):
        found = []
        for index, item in enumerate(value):
            found += find_placeholders(item, f"{path}[{index}]")
        return found
    return []


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def render_template(name: str, replacements: dict[str, str], template_root: Path = TEMPLATE_ROOT) -> str:
    template_path = template_root / name
    if not template_path.is_file():
        raise WorkflowError(f"缺少頁面範本：{template_path}")
    content = template_path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    unresolved = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", content)))
    if unresolved:
        raise WorkflowError(f"範本仍有未填欄位：{', '.join(unresolved)}")
    return content


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as file:
        yaml.safe_dump(data, file, allow_unicode=True, sort_keys=False, width=120)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def make_manifest(trip: dict, style_profile: dict[str, str]) -> dict:
    return {
        "name": trip["name"],
        "short_name": trip["shortName"],
        "description": trip.get("description", "可離線使用的旅遊行程。"),
        "start_url": "./index.html",
        "scope": "./",
        "display": "standalone",
        "background_color": style_profile["background_color"],
        "theme_color": style_profile["theme_color"],
        "orientation": "portrait-primary",
        "icons": [
            {"src": "./icons/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}
        ],
    }


def build_cache_name(slug: str, site_root: Path) -> str:
    digest = hashlib.sha256()
    for name in SITE_ASSETS:
        digest.update((site_root / name).read_bytes())
    return f"trip-{slug}-{digest.hexdigest()[:12]}"


def render_site(site_root: Path, markdown_path: Path | None, data: dict, slug: str, full_stylesheet: bool = False) -> None:
    """Render every generated asset from the shared template + YAML data."""
    trip = data["trip"]
    style, style_profile = get_style_profile(trip.get("style"))
    summary = trip.get("description") or "可離線使用的旅遊行程。"
    replacements = {
        "TRIP_NAME": html.escape(trip["name"]),
        "SHORT_NAME": html.escape(trip["shortName"]),
        "SUMMARY": html.escape(summary),
        "DATE_RANGE": html.escape(trip["dateRange"]),
        "BUILD_DATE": datetime.now().date().isoformat(),
        "STYLE": style,
        "THEME_COLOR": style_profile["theme_color"],
    }
    builder = load_trip_builder()
    if markdown_path is not None:
        builder.write_markdown(data, markdown_path)
    builder.write_json(data, site_root / "data.generated.json")
    write_text(site_root / "data.fallback.js", "window.TRIP_FALLBACK = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")
    write_text(site_root / "index.html", render_template("index.html", replacements))
    stylesheet = (TEMPLATE_ROOT / "styles.css").read_text(encoding="utf-8") if full_stylesheet else render_stylesheet(style)
    write_text(site_root / "styles.css", stylesheet)
    write_text(site_root / "app.js", render_template("app.js", {}))
    write_text(site_root / "icons" / "icon.svg", render_template("icon.svg", {}))
    write_json(site_root / "manifest.webmanifest", make_manifest(trip, style_profile))
    cache_name = build_cache_name(slug, site_root)
    write_text(site_root / "service-worker.js", render_template("service-worker.js", {"CACHE_NAME": cache_name}))


def render_home_card(site_dir: str, trip: dict) -> str:
    style, profile = get_style_profile(trip.get("style"))
    summary = trip.get("description") or "可離線使用的旅遊行程。"
    return (
        f'      <a class="card" href="./{site_dir}/" data-trip="{site_dir}" style="--card-accent: {profile["theme_color"]}">\n'
        f'        <span class="badge">{html.escape(site_dir[:4])} {html.escape(trip["shortName"])}</span>\n'
        f'        <h2>{html.escape(trip["name"])}</h2>\n'
        f'        <p>{html.escape(summary)}</p>\n'
        f'        <div class="meta">\n'
        f'          <span>{html.escape(trip["dateRange"])}</span>\n'
        f'          <span>{html.escape(profile["label"])} · PWA</span>\n'
        f'        </div>\n'
        f'      </a>\n'
    )


def upsert_home_card(project_root: Path, site_dir: str, trip: dict, *, create: bool) -> None:
    index_path = project_root / "index.html"
    if not index_path.is_file():
        raise WorkflowError(f"缺少首頁：{index_path}")
    content = index_path.read_text(encoding="utf-8")
    if CARD_START not in content or CARD_END not in content:
        raise WorkflowError("首頁缺少 TRIP-PAGES 標記，無法安全新增入口")
    card = render_home_card(site_dir, trip)
    managed = re.compile(rf'      <a class="card" href="\./{site_dir}/" data-trip="{site_dir}"[^>]*>.*?</a>\n', re.DOTALL)
    if managed.search(content):
        content = managed.sub(lambda _: card, content, count=1)
    elif create:
        if f'href="./{site_dir}/"' in content:
            raise WorkflowError(f"首頁已存在 {site_dir} 入口")
        content = content.replace(f"      {CARD_END}", f"{card}      {CARD_END}")
    else:
        return
    write_text(index_path, content)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def create_trip(args: argparse.Namespace) -> None:
    start_date = parse_iso_date(args.start_date, "--start-date")
    end_date = parse_iso_date(args.end_date, "--end-date")
    site_dir, slug = validate_identity(args.id, start_date, end_date)
    if not TIMEZONE_PATTERN.fullmatch(args.timezone):
        raise WorkflowError("--timezone 必須像 +09:00 或 -05:00")
    if not TIME_PATTERN.fullmatch(args.departure_time):
        raise WorkflowError("--departure-time 必須是 HH:MM，例如 07:45")
    project_root = Path(args.project_root).resolve()
    source_path = project_root / "data" / "trips" / f"{args.id}.yaml"
    markdown_path = project_root / "trips" / f"{args.id}.md"
    site_root = project_root / site_dir

    conflicts = [path for path in (source_path, markdown_path, site_root) if path.exists()]
    if conflicts:
        display = ", ".join(str(path) for path in conflicts)
        raise WorkflowError(f"拒絕覆寫既有行程：{display}")

    style, _ = get_style_profile(args.style)
    short_name = args.short_name or args.name
    data = make_trip_data(
        args.id, args.name, short_name, start_date, end_date, args.summary, style, args.timezone, args.departure_time
    )
    write_yaml(source_path, data)
    render_site(site_root, markdown_path, data, slug)
    upsert_home_card(project_root, site_dir, data["trip"], create=True)
    print(f"Created {args.id}: {site_root}")
    print("下一步：")
    print(f"  1. 編輯 {source_path.relative_to(project_root)}（把「待補」換成實際行程）")
    print(f"  2. python scripts/trip-page.py build --id {args.id}")
    print(f"  3. python scripts/trip-page.py verify --id {args.id} --strict")
    print(f"  4. python -m http.server 4173 後開 http://127.0.0.1:4173/{site_dir}/?previewDate={start_date.isoformat()}T10:00")


def existing_trip_paths(project_root: Path, trip_id: str) -> tuple[Path, Path, Path, str]:
    match = TRIP_ID_PATTERN.fullmatch(trip_id)
    if not match:
        raise WorkflowError("--id 必須使用 YYYYMMDD-slug，例如 20270403-kyoto")
    source_path = project_root / "data" / "trips" / f"{trip_id}.yaml"
    markdown_path = project_root / "trips" / f"{trip_id}.md"
    site_root = project_root / match.group("date")
    if not source_path.is_file():
        raise WorkflowError(f"找不到行程來源：{source_path}")
    if not site_root.is_dir():
        raise WorkflowError(f"找不到行程頁面：{site_root}")
    return source_path, markdown_path, site_root, match.group("slug")


def load_valid_source(source_path: Path, trip_id: str) -> dict:
    try:
        data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise WorkflowError(f"YAML 語法錯誤：{error}") from error
    problems = validate_trip_data(data, trip_id)
    if problems:
        listing = "\n  - ".join(problems[:20])
        more = f"\n  …另有 {len(problems) - 20} 項" if len(problems) > 20 else ""
        raise WorkflowError(f"{source_path.name} 有 {len(problems)} 個問題：\n  - {listing}{more}")
    return data


def report_placeholders(data: dict, strict: bool) -> None:
    placeholders = find_placeholders(data)
    if not placeholders:
        return
    sample = "、".join(placeholders[:5])
    message = f"尚有 {len(placeholders)} 處「待補／待確認」內容，例如 {sample}"
    if strict:
        raise WorkflowError(message + "；發布前請補齊，或拿掉 --strict 先預覽")
    print(f"提醒：{message}", file=sys.stderr)


def build_existing_trip(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).resolve()
    source_path, markdown_path, site_root, slug = existing_trip_paths(project_root, args.id)
    data = load_valid_source(source_path, args.id)
    get_style_profile(data["trip"].get("style"))
    render_site(site_root, markdown_path, data, slug)
    upsert_home_card(project_root, site_root.name, data["trip"], create=False)
    print(f"Built {args.id}: {site_root}")
    report_placeholders(data, strict=False)


def load_fallback(path: Path) -> dict:
    content = path.read_text(encoding="utf-8").strip()
    prefix = "window.TRIP_FALLBACK = "
    if not content.startswith(prefix) or not content.endswith(";"):
        raise WorkflowError("data.fallback.js 格式不正確")
    return json.loads(content[len(prefix) : -1])


def verify_existing_trip(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).resolve()
    source_path, markdown_path, site_root, slug = existing_trip_paths(project_root, args.id)
    required = [
        markdown_path,
        site_root / "index.html",
        site_root / "styles.css",
        site_root / "app.js",
        site_root / "data.generated.json",
        site_root / "data.fallback.js",
        site_root / "manifest.webmanifest",
        site_root / "service-worker.js",
        site_root / "icons" / "icon.svg",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise WorkflowError("缺少必要檔案：" + ", ".join(missing))

    source = load_valid_source(source_path, args.id)
    generated = json.loads((site_root / "data.generated.json").read_text(encoding="utf-8"))
    fallback = load_fallback(site_root / "data.fallback.js")
    manifest = json.loads((site_root / "manifest.webmanifest").read_text(encoding="utf-8"))
    page = (site_root / "index.html").read_text(encoding="utf-8")
    stylesheet = (site_root / "styles.css").read_text(encoding="utf-8")
    app = (site_root / "app.js").read_text(encoding="utf-8")
    service_worker = (site_root / "service-worker.js").read_text(encoding="utf-8")
    markdown = markdown_path.read_text(encoding="utf-8")

    if generated != source or fallback != source:
        raise WorkflowError("YAML、JSON 與離線 fallback 尚未同步，請先執行 build")
    trip = source["trip"]
    style, style_profile = get_style_profile(trip.get("style"))
    if manifest.get("name") != trip.get("name") or manifest.get("short_name") != trip.get("shortName"):
        raise WorkflowError("manifest 名稱尚未與 YAML 同步，請先執行 build")
    if manifest.get("background_color") != style_profile["background_color"] or manifest.get("theme_color") != style_profile["theme_color"]:
        raise WorkflowError("manifest 配色尚未與行程風格同步，請先執行 build")
    if 'data-ui="trip-wayfinder"' not in page or f'data-style="{style}"' not in page or "{{" in page:
        raise WorkflowError("index.html 不是完整的 Trip Wayfinder 頁面，請先執行 build")
    if f"<title>{html.escape(trip['name'])}</title>" not in page:
        raise WorkflowError("index.html 標題尚未與 YAML 同步，請先執行 build")
    if "--primitive-primary" not in stylesheet or "--next-stop-background" not in stylesheet or "prefers-reduced-motion" not in stylesheet:
        raise WorkflowError("styles.css 缺少設計 token 或 reduced-motion 支援")
    if f':root[data-style="{style}"]' not in stylesheet:
        raise WorkflowError(f"styles.css 缺少 {style} 的淺色風格 token")
    if style != DEFAULT_STYLE and f':root[data-theme="dark"][data-style="{style}"]' not in stylesheet:
        raise WorkflowError(f"styles.css 缺少 {style} 的深色風格 token")
    foreign = {sid for sid in STYLE_SELECTOR_PATTERN.findall(stylesheet) if sid != style}
    if foreign:
        raise WorkflowError(f"styles.css 含有其他風格的 token（{', '.join(sorted(foreign)[:3])}），請先執行 build")
    if "window.TRIP_FALLBACK" not in app or "previewDate" not in app:
        raise WorkflowError("app.js 缺少資料 fallback 或預覽日期功能")
    for asset in ("./index.html", "./styles.css", "./app.js", "./data.generated.json", "./data.fallback.js", "./manifest.webmanifest", "./icons/icon.svg"):
        if asset not in service_worker:
            raise WorkflowError(f"service worker 未快取 {asset}")
    if f'"{build_cache_name(slug, site_root)}"' not in service_worker:
        raise WorkflowError("service worker cache 名稱與目前資產內容不符，請先執行 build")
    if trip.get("name") not in markdown:
        raise WorkflowError("Markdown 缺少行程名稱")
    report_placeholders(source, strict=args.strict)
    print(f"Verified {args.id}: {len(source['days'])} days, style {style}")


def list_styles(args: argparse.Namespace) -> None:
    keywords = [keyword.lower() for keyword in args.keywords]
    matches = []
    for style_id, profile in STYLE_PROFILES.items():
        haystack = " ".join((style_id, profile["label"], profile["fits"], profile["vibe"])).lower()
        if all(keyword in haystack for keyword in keywords):
            matches.append((style_id, profile))
    if not matches:
        raise WorkflowError(f"沒有符合「{' '.join(args.keywords)}」的風格；不帶關鍵字可列出全部")
    width = max(len(style_id) for style_id, _ in matches)
    for style_id, profile in matches:
        marker = "*" if style_id == DEFAULT_STYLE else " "
        print(f"{marker} {style_id.ljust(width)}  {profile['label']}｜{profile['fits']}")
    print(f"\n共 {len(matches)} 套；* 為預設。執行 `python scripts/trip-page.py gallery` 可即時比較所有風格。")


# ---------------------------------------------------------------------------
# Live style gallery
# ---------------------------------------------------------------------------


def make_gallery_data() -> dict:
    maps = "https://www.google.com/maps/search/?api=1&query="
    data = make_trip_data(
        "20300403-gallery",
        "京都春日親子散步",
        "京都散步",
        date(2030, 4, 3),
        date(2030, 4, 5),
        "三天兩夜的寺社、河岸與市場散步，示範每套風格的實際版面。",
        DEFAULT_STYLE,
        "+09:00",
        "08:30",
    )
    trip = data["trip"]
    trip.update({"flights": "BR132 / BR131", "carRental": "不租車，搭地鐵與巴士", "rainFocus": "京都水族館・錦市場・京都車站"})
    hotel = {"name": "京都四條河原町飯店", "address": "京都市下京區河原町通四條下", "phone": "+81-75-000-0000", "mapUrl": maps + "Shijo%20Kawaramachi%20Kyoto"}
    days = [
        ("抵達京都，沿鴨川散步", ["交通日", "輕鬆"], [
            ("10:40", "關西機場搭 HARUKA 到京都車站。", [["地圖", maps + "Kyoto%20Station"]]),
            ("14:00", "入住後到鴨川河岸散步，傍晚逛先斗町。", [["鴨川地圖", maps + "Kamogawa%20Kyoto"]]),
            ("18:30", "錦市場周邊晚餐，買隔天早餐。", []),
        ]),
        ("伏見稻荷與東山", ["寺社", "步行多"], [
            ("08:30", "伏見稻荷大社千本鳥居，早點出發避開人潮。", [["地圖", maps + "Fushimi%20Inari"], ["攻略", "https://example.com/inari"]]),
            ("13:00", "清水寺、二年坂與三年坂散步。", [["地圖", maps + "Kiyomizu-dera"]]),
            ("17:30", "八坂神社與祇園白川夜景。", []),
        ]),
        ("嵐山與回程", ["自然", "回程"], [
            ("09:00", "嵐山竹林與渡月橋。", [["地圖", maps + "Arashiyama"]]),
            ("13:30", "待補午後彈性行程。", []),
            ("17:00", "回京都車站搭 HARUKA 前往機場。", []),
        ]),
    ]
    for day, (title, tags, schedule) in zip(data["days"], days):
        day["title"] = title
        day["stay"] = hotel["name"]
        day["tags"] = tags
        day["rainPlan"] = "改去京都水族館或京都車站地下街。"
        day["schedule"] = [{"time": time, "text": text, "links": links} for time, text, links in schedule]
        day["food"] = [
            {"title": "早餐", "text": "飯店附近麵包店。", "links": []},
            {"title": "午餐", "text": "烏龍麵或丼飯。", "links": []},
            {"title": "晚餐", "text": "錦市場周邊居酒屋。", "links": []},
        ]
        data["stays"][day["date"]] = dict(hotel)
        data["rainRules"][day["date"]] = "雨大時改室內行程。"
        data["breakfasts"][day["date"]] = "前一晚超商買好。"
    data["days"][1]["shoppingBackup"] = [{"name": "京都車站 Porta 地下街", "note": "下雨時的購物備案", "links": [["地圖", maps + "Kyoto%20Porta"]]}]
    return data


GALLERY_PAGE = """<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TripHelper 即時風格廊</title>
  <style>
    :root { color-scheme: light dark; --ink: #1d232b; --muted: #5b6470; --paper: #f4f1ea; --card: #fff; --line: #d9d3c8; --accent: #2457d6; }
    @media (prefers-color-scheme: dark) { :root { --ink: #eef1f5; --muted: #a8b0bb; --paper: #12151a; --card: #1b1f26; --line: #313844; --accent: #8fb0ff; } }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: "Segoe UI Variable", "Noto Sans TC", "Microsoft JhengHei UI", sans-serif; color: var(--ink); background: var(--paper); }
    header { position: sticky; top: 0; z-index: 2; display: flex; flex-wrap: wrap; gap: 12px 20px; align-items: center; padding: 14px 20px; border-bottom: 1px solid var(--line); background: color-mix(in srgb, var(--paper) 92%, transparent); backdrop-filter: blur(8px); }
    h1 { margin: 0; font-size: 1.1rem; }
    .controls { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
    input[type=search] { min-width: 220px; padding: 8px 12px; border: 1px solid var(--line); border-radius: 999px; background: var(--card); color: inherit; font: inherit; }
    .toggle { display: inline-flex; border: 1px solid var(--line); border-radius: 999px; overflow: hidden; }
    .toggle button { padding: 7px 14px; border: 0; background: transparent; color: inherit; font: inherit; cursor: pointer; }
    .toggle button[aria-pressed=true] { background: var(--accent); color: var(--paper); }
    button:focus-visible, input:focus-visible, a:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
    main { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, var(--frame-width, 390px)), 1fr)); gap: 24px; padding: 24px 20px 48px; }
    article { display: grid; gap: 10px; align-content: start; }
    .meta { display: flex; justify-content: space-between; gap: 10px; align-items: baseline; }
    .meta strong { font-size: 1rem; }
    .meta code { color: var(--muted); font-size: 0.8rem; }
    .meta p { margin: 2px 0 0; color: var(--muted); font-size: 0.82rem; }
    .swatch { flex: 0 0 auto; width: 14px; height: 14px; border-radius: 50%; }
    .frame { overflow: hidden; width: var(--frame-width, 390px); max-width: 100%; height: var(--frame-height, 720px); border: 1px solid var(--line); border-radius: 18px; background: var(--card); }
    iframe { display: block; width: var(--frame-inner, 390px); height: calc(var(--frame-height, 720px) / var(--frame-scale, 1)); border: 0; transform: scale(var(--frame-scale, 1)); transform-origin: 0 0; }
    .copy { padding: 4px 10px; border: 1px solid var(--line); border-radius: 999px; background: var(--card); color: inherit; font: inherit; font-size: 0.78rem; cursor: pointer; }
    [hidden] { display: none !important; }
  </style>
</head>
<body>
  <header>
    <h1>TripHelper 即時風格廊 <small id="count"></small></h1>
    <div class="controls">
      <input type="search" id="filter" placeholder="篩選：海島、親子、夜景…" aria-label="篩選風格">
      <div class="toggle" role="group" aria-label="顯示模式">
        <button type="button" data-theme-choice="light" aria-pressed="true">淺色</button>
        <button type="button" data-theme-choice="dark" aria-pressed="false">深色</button>
      </div>
      <div class="toggle" role="group" aria-label="裝置寬度">
        <button type="button" data-device="mobile" aria-pressed="true">手機</button>
        <button type="button" data-device="desktop" aria-pressed="false">桌機</button>
      </div>
    </div>
  </header>
  <main id="grid"></main>
  <script>
    const STYLES = __STYLES__;
    const PREVIEW_DATE = "__PREVIEW_DATE__";
    const grid = document.querySelector("#grid");
    let theme = "light";
    let device = "mobile";
    const devices = { mobile: { inner: 390, scale: 1, width: 390, height: 720 }, desktop: { inner: 1280, scale: 0.42, width: 538, height: 470 } };

    function src(style) {
      const params = new URLSearchParams({ previewStyle: style, previewTheme: theme, previewDate: PREVIEW_DATE });
      return `./sample/index.html?${params}`;
    }

    function render() {
      const size = devices[device];
      document.body.style.setProperty("--frame-inner", `${size.inner}px`);
      document.body.style.setProperty("--frame-scale", size.scale);
      document.body.style.setProperty("--frame-width", `${size.width}px`);
      document.body.style.setProperty("--frame-height", `${size.height}px`);
      grid.querySelectorAll("iframe").forEach((frame) => { frame.src = src(frame.dataset.style); });
    }

    STYLES.forEach((style) => {
      const article = document.createElement("article");
      article.dataset.search = `${style.id} ${style.label} ${style.fits} ${style.vibe}`.toLowerCase();
      article.innerHTML = `
        <div class="meta">
          <div><strong></strong> <code></code><p></p></div>
          <span class="swatch" aria-hidden="true"></span>
        </div>
        <div class="frame"><iframe loading="lazy"></iframe></div>
        <div><button class="copy" type="button">複製 --style</button></div>`;
      article.querySelector("strong").textContent = style.label;
      article.querySelector("code").textContent = style.id;
      article.querySelector("p").textContent = style.fits;
      article.querySelector(".swatch").style.background = style.themeColor;
      const frame = article.querySelector("iframe");
      frame.dataset.style = style.id;
      frame.title = `${style.label} 預覽`;
      const copy = article.querySelector(".copy");
      copy.addEventListener("click", async () => {
        try { await navigator.clipboard.writeText(`--style ${style.id}`); copy.textContent = "已複製"; }
        catch { copy.textContent = `--style ${style.id}`; }
      });
      grid.append(article);
    });

    document.querySelector("#filter").addEventListener("input", (event) => {
      const words = event.target.value.toLowerCase().split(/\\s+/).filter(Boolean);
      let shown = 0;
      grid.querySelectorAll("article").forEach((article) => {
        article.hidden = !words.every((word) => article.dataset.search.includes(word));
        if (!article.hidden) shown += 1;
      });
      document.querySelector("#count").textContent = `${shown}/${STYLES.length}`;
    });
    document.querySelectorAll("[data-theme-choice]").forEach((button) => button.addEventListener("click", () => {
      theme = button.dataset.themeChoice;
      document.querySelectorAll("[data-theme-choice]").forEach((other) => other.setAttribute("aria-pressed", String(other === button)));
      render();
    }));
    document.querySelectorAll("[data-device]").forEach((button) => button.addEventListener("click", () => {
      device = button.dataset.device;
      document.querySelectorAll("[data-device]").forEach((other) => other.setAttribute("aria-pressed", String(other === button)));
      render();
    }));
    document.querySelector("#count").textContent = `${STYLES.length}/${STYLES.length}`;
    render();
  </script>
</body>
</html>
"""


def build_gallery(args: argparse.Namespace) -> None:
    out_dir = Path(args.out).resolve()
    sample_root = out_dir / "sample"
    data = make_gallery_data()
    render_site(sample_root, None, data, "gallery", full_stylesheet=True)
    styles = [
        {"id": sid, "label": p["label"], "fits": p["fits"], "vibe": p["vibe"], "themeColor": p["theme_color"]}
        for sid, p in STYLE_PROFILES.items()
    ]
    page = GALLERY_PAGE.replace("__STYLES__", json.dumps(styles, ensure_ascii=False)).replace("__PREVIEW_DATE__", "2030-04-04T10:30:00")
    write_text(out_dir / "index.html", page)
    print(f"Gallery: {out_dir / 'index.html'}（{len(styles)} 套風格）")
    try:
        relative = out_dir.relative_to(ROOT).as_posix()
        print(f"預覽：python -m http.server 4173 後開 http://127.0.0.1:4173/{relative}/")
    except ValueError:
        print(f"預覽：在 {out_dir} 執行 python -m http.server 4173 後開 http://127.0.0.1:4173/")


# ---------------------------------------------------------------------------
# New style scaffold
# ---------------------------------------------------------------------------


STYLE_DOC_TEMPLATE = """# {title} / {label}

- Style ID：`{style_id}`
- 適用：{fits}。
- 感受：{vibe}。
- 來源：由 `{base}` 複製後調整；請在 `templates/trip-pwa/styles.css` 搜尋 `data-style="{style_id}"` 修改色票與元件 token。
- Light：paper `{background}`、primary `{theme}`；其餘色票待調整。
- Dark：沿用 `{base}` 深色色票，待調整。
- 避免：低對比文字、只靠顏色傳達狀態、無限動畫與外部字型。
"""


def create_style(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).resolve()
    style_id = args.id
    if not STYLE_ID_PATTERN.fullmatch(style_id):
        raise WorkflowError("--id 必須是小寫 kebab-case，且至少兩段，例如 harbor-lights")
    registry_path = project_root / REGISTRY_FILE
    stylesheet_path = project_root / TEMPLATE_DIR / "styles.css"
    doc_path = project_root / DESIGN_DIR / "styles" / f"{style_id}.md"
    master_path = project_root / DESIGN_DIR / "MASTER.md"
    default, profiles = load_style_registry(project_root)
    if style_id in profiles or doc_path.exists():
        raise WorkflowError(f"風格 {style_id} 已存在")
    if args.base not in profiles:
        raise WorkflowError(f"--base 必須是既有風格：{args.base}")
    for color_arg in (args.theme_color, args.background_color):
        if color_arg and not re.fullmatch(r"#[0-9a-fA-F]{6}", color_arg):
            raise WorkflowError(f"顏色必須是 #RRGGBB：{color_arg}")

    base = profiles[args.base]
    theme_color = (args.theme_color or base["theme_color"]).lower()
    background_color = (args.background_color or base["background_color"]).lower()
    fits = args.fits or "待補適合行程"
    vibe = args.vibe or "待補視覺語彙"

    stylesheet = stylesheet_path.read_text(encoding="utf-8")
    rules, tail = split_css_rules(stylesheet)
    overrides = []
    if args.background_color:
        overrides.append(f"  --primitive-paper: {background_color};")
    if args.theme_color:
        overrides.append(f"  --primitive-primary: {theme_color};")
    pieces: list[str] = []
    cloned = 0
    injected = False
    for selector, segment in rules:
        pieces.append(segment)
        if args.base in rule_styles(selector):
            body = strip_leading_trivia(segment).replace(f'data-style="{args.base}"', f'data-style="{style_id}"')
            if overrides and not injected and 'data-theme="dark"' not in selector:
                closing = body.rstrip().rfind("}")
                body = body[:closing].rstrip() + "\n" + "\n".join(overrides) + "\n}"
                injected = True
            pieces.append(f"\n\n/* {style_id}: cloned from {args.base}; adjust tokens below. */\n{body}")
            cloned += 1
    if cloned == 0:
        raise WorkflowError(f"styles.css 找不到 {args.base} 的 token 區塊")
    write_text(stylesheet_path, "".join(pieces) + tail)

    document = json.loads(registry_path.read_text(encoding="utf-8"))
    document["styles"].append(
        {
            "id": style_id,
            "label": args.label,
            "fits": fits,
            "vibe": vibe,
            "backgroundColor": background_color,
            "themeColor": theme_color,
        }
    )
    write_json(registry_path, document)

    title = " ".join(part.capitalize() for part in style_id.split("-"))
    write_text(
        doc_path,
        STYLE_DOC_TEMPLATE.format(
            title=title, label=args.label, style_id=style_id, fits=fits, vibe=vibe, base=args.base,
            background=background_color.upper(), theme=theme_color.upper(),
        ),
    )

    if master_path.is_file():
        master = master_path.read_text(encoding="utf-8")
        rows = list(re.finditer(r"^\| `[^`]+` \|.*\|\n", master, flags=re.MULTILINE))
        if rows:
            row = f"| `{style_id}` | {args.label} | {fits} | {vibe} |\n"
            insert_at = rows[-1].end()
            write_text(master_path, master[:insert_at] + row + master[insert_at:])

    print(f"Created style {style_id}（複製 {args.base}，共 {cloned} 個 CSS 區塊）")
    print("下一步：")
    print(f'  1. 在 {TEMPLATE_DIR.as_posix()}/styles.css 搜尋 data-style="{style_id}"，調整色票、底紋與形狀 token')
    print(f"  2. 補完 {doc_path.relative_to(project_root).as_posix()} 的設計意圖")
    print("  3. python scripts/trip-page.py gallery，用即時風格廊檢查淺色／深色與手機／桌機")
    print("  4. python tests/verify-trip-page-workflow.py")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create and maintain TripHelper itinerary pages.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Create a new data-driven itinerary PWA.")
    create.add_argument("--id", required=True, help="Trip id in YYYYMMDD-slug format.")
    create.add_argument("--name", required=True)
    create.add_argument("--short-name", help="Home-screen name; defaults to --name.")
    create.add_argument("--start-date", required=True)
    create.add_argument("--end-date", required=True)
    create.add_argument("--summary", default="可離線使用的旅遊行程。")
    create.add_argument("--style", default=DEFAULT_STYLE, help="Style id; list with `styles`.")
    create.add_argument("--timezone", default="+08:00", help="UTC offset at the destination, e.g. +09:00.")
    create.add_argument("--departure-time", default="09:00", help="Departure time on the first day (HH:MM).")
    create.add_argument("--project-root", default=str(ROOT), help=argparse.SUPPRESS)
    create.set_defaults(handler=create_trip)

    build = subparsers.add_parser("build", help="Regenerate an itinerary page from YAML and the shared template.")
    build.add_argument("--id", required=True, help="Trip id in YYYYMMDD-slug format.")
    build.add_argument("--project-root", default=str(ROOT), help=argparse.SUPPRESS)
    build.set_defaults(handler=build_existing_trip)

    verify = subparsers.add_parser("verify", help="Verify generated data and offline assets.")
    verify.add_argument("--id", required=True, help="Trip id in YYYYMMDD-slug format.")
    verify.add_argument("--strict", action="store_true", help="Fail when placeholder text (待補) remains.")
    verify.add_argument("--project-root", default=str(ROOT), help=argparse.SUPPRESS)
    verify.set_defaults(handler=verify_existing_trip)

    styles = subparsers.add_parser("styles", help="List style profiles, optionally filtered by keywords.")
    styles.add_argument("keywords", nargs="*", help="Keywords such as 海島 親子.")
    styles.set_defaults(handler=list_styles)

    gallery = subparsers.add_parser("gallery", help="Build a live gallery that renders every style from the template.")
    gallery.add_argument("--out", default=str(ROOT / DESIGN_DIR / "previews" / "live"))
    gallery.set_defaults(handler=build_gallery)

    new_style = subparsers.add_parser("new-style", help="Scaffold a new style profile by cloning an existing one.")
    new_style.add_argument("--id", required=True, help="kebab-case style id, e.g. harbor-lights.")
    new_style.add_argument("--label", required=True, help="中文名稱")
    new_style.add_argument("--base", default=DEFAULT_STYLE, help="Existing style to clone.")
    new_style.add_argument("--fits", help="適合行程")
    new_style.add_argument("--vibe", help="視覺語彙")
    new_style.add_argument("--theme-color", help="#RRGGBB used for primary and manifest theme_color.")
    new_style.add_argument("--background-color", help="#RRGGBB used for paper and manifest background_color.")
    new_style.add_argument("--project-root", default=str(ROOT), help=argparse.SUPPRESS)
    new_style.set_defaults(handler=create_style)
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.handler(args)
    except WorkflowError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
