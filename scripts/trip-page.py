import argparse
import hashlib
import html
import importlib.util
import json
import re
import shutil
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "templates" / "trip-pwa"
TRIP_ID_PATTERN = re.compile(r"^(?P<date>\d{8})-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$")
WEEKDAYS = "一二三四五六日"
CARD_START = "<!-- TRIP-PAGES:START -->"
CARD_END = "<!-- TRIP-PAGES:END -->"


class WorkflowError(RuntimeError):
    pass


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
        raise WorkflowError("--id 必須使用 YYYYMMDD-slug，例如 20270403-kyoto")
    site_dir = match.group("date")
    if site_dir != start_date.strftime("%Y%m%d"):
        raise WorkflowError("--id 的日期前綴必須等於 --start-date")
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

    timezone = "+08:00"
    return {
        "trip": {
            "id": trip_id,
            "name": name,
            "shortName": short_name,
            "description": summary,
            "dateRange": format_date_range(start_date, end_date),
            "flights": "待補",
            "carRental": "待補",
            "rainFocus": "待補",
            "startAt": f"{start_date.isoformat()}T00:00:00{timezone}",
            "departureAt": f"{start_date.isoformat()}T09:00:00{timezone}",
            "endAt": f"{end_date.isoformat()}T23:59:59{timezone}",
        },
        "links": {},
        "days": days,
        "breakfasts": breakfasts,
        "rainRules": rain_rules,
        "stays": stays,
    }


def render_template(name: str, replacements: dict[str, str]) -> str:
    template_path = TEMPLATE_ROOT / name
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


def build_cache_name(slug: str, site_root: Path) -> str:
    digest = hashlib.sha256()
    for name in ("index.html", "styles.css", "app.js", "data.generated.json", "data.fallback.js", "manifest.webmanifest"):
        digest.update((site_root / name).read_bytes())
    return f"trip-{slug}-{digest.hexdigest()[:12]}"


def add_home_card(project_root: Path, site_dir: str, trip: dict, summary: str) -> None:
    index_path = project_root / "index.html"
    if not index_path.is_file():
        raise WorkflowError(f"缺少首頁：{index_path}")
    content = index_path.read_text(encoding="utf-8")
    if CARD_START not in content or CARD_END not in content:
        raise WorkflowError("首頁缺少 TRIP-PAGES 標記，無法安全新增入口")
    href = f'href="./{site_dir}/"'
    if href in content:
        raise WorkflowError(f"首頁已存在 {site_dir} 入口")

    year = site_dir[:4]
    card = f'''      <a class="card" href="./{site_dir}/">
        <span class="badge">{html.escape(year)} {html.escape(trip["shortName"])}</span>
        <h2>{html.escape(trip["name"])}</h2>
        <p>{html.escape(summary)}</p>
        <div class="meta">
          <span>路徑：`/{site_dir}/`</span>
          <span>型態：PWA</span>
        </div>
      </a>
'''
    content = content.replace(f"      {CARD_END}", f"{card}      {CARD_END}")
    write_text(index_path, content)


def create_trip(args: argparse.Namespace) -> None:
    start_date = parse_iso_date(args.start_date, "--start-date")
    end_date = parse_iso_date(args.end_date, "--end-date")
    site_dir, slug = validate_identity(args.id, start_date, end_date)
    project_root = Path(args.project_root).resolve()
    source_path = project_root / "data" / "trips" / f"{args.id}.yaml"
    markdown_path = project_root / "trips" / f"{args.id}.md"
    site_root = project_root / site_dir

    conflicts = [path for path in (source_path, markdown_path, site_root) if path.exists()]
    if conflicts:
        display = ", ".join(str(path) for path in conflicts)
        raise WorkflowError(f"拒絕覆寫既有行程：{display}")

    data = make_trip_data(args.id, args.name, args.short_name, start_date, end_date, args.summary)
    trip = data["trip"]
    replacements = {
        "TRIP_NAME": html.escape(args.name),
        "SHORT_NAME": html.escape(args.short_name),
        "SUMMARY": html.escape(args.summary),
        "DATE_RANGE": html.escape(trip["dateRange"]),
        "BUILD_DATE": datetime.now().date().isoformat(),
    }

    write_yaml(source_path, data)
    builder = load_trip_builder()
    builder.write_markdown(data, markdown_path)
    builder.write_json(data, site_root / "data.generated.json")
    write_text(site_root / "data.fallback.js", "window.TRIP_FALLBACK = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")
    write_text(site_root / "index.html", render_template("index.html", replacements))
    write_text(site_root / "styles.css", render_template("styles.css", {}))
    write_text(site_root / "app.js", render_template("app.js", {}))
    write_text(site_root / "icons" / "icon.svg", render_template("icon.svg", {}))

    manifest = {
        "name": args.name,
        "short_name": args.short_name,
        "description": args.summary,
        "start_url": "./index.html",
        "scope": "./",
        "display": "standalone",
        "background_color": "#f3f0e8",
        "theme_color": "#2457d6",
        "orientation": "portrait-primary",
        "icons": [
            {"src": "./icons/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}
        ],
    }
    write_json(site_root / "manifest.webmanifest", manifest)
    cache_name = build_cache_name(slug, site_root)
    write_text(site_root / "service-worker.js", render_template("service-worker.js", {"CACHE_NAME": cache_name}))
    add_home_card(project_root, site_dir, trip, args.summary)
    print(f"Created {args.id}: {site_root}")


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


def build_existing_trip(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).resolve()
    source_path, markdown_path, site_root, slug = existing_trip_paths(project_root, args.id)
    data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    if data.get("trip", {}).get("id") != args.id:
        raise WorkflowError("YAML 的 trip.id 與 --id 不一致")

    builder = load_trip_builder()
    builder.write_markdown(data, markdown_path)
    builder.write_json(data, site_root / "data.generated.json")
    write_text(site_root / "data.fallback.js", "window.TRIP_FALLBACK = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")

    trip = data["trip"]
    manifest = {
        "name": trip["name"],
        "short_name": trip["shortName"],
        "description": trip.get("description", "可離線使用的旅遊行程。"),
        "start_url": "./index.html",
        "scope": "./",
        "display": "standalone",
        "background_color": "#f3f0e8",
        "theme_color": "#2457d6",
        "orientation": "portrait-primary",
        "icons": [
            {"src": "./icons/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}
        ],
    }
    write_json(site_root / "manifest.webmanifest", manifest)
    cache_name = build_cache_name(slug, site_root)
    write_text(site_root / "service-worker.js", render_template("service-worker.js", {"CACHE_NAME": cache_name}))
    print(f"Built {args.id}: {site_root}")


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

    source = yaml.safe_load(source_path.read_text(encoding="utf-8"))
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
    trip = source.get("trip", {})
    if trip.get("id") != args.id:
        raise WorkflowError("trip.id 與檔名不一致")
    if not isinstance(source.get("days"), list) or not source["days"]:
        raise WorkflowError("行程至少需要一天")
    if manifest.get("name") != trip.get("name") or manifest.get("short_name") != trip.get("shortName"):
        raise WorkflowError("manifest 名稱尚未與 YAML 同步")
    if 'data-ui="trip-wayfinder"' not in page or "{{" in page:
        raise WorkflowError("index.html 不是完整的 Trip Wayfinder 頁面")
    if "--color-cobalt" not in stylesheet or "prefers-reduced-motion" not in stylesheet:
        raise WorkflowError("styles.css 缺少設計 token 或 reduced-motion 支援")
    if "window.TRIP_FALLBACK" not in app or "previewDate" not in app:
        raise WorkflowError("app.js 缺少資料 fallback 或預覽日期功能")
    for asset in ("./index.html", "./styles.css", "./app.js", "./data.generated.json", "./data.fallback.js", "./manifest.webmanifest", "./icons/icon.svg"):
        if asset not in service_worker:
            raise WorkflowError(f"service worker 未快取 {asset}")
    if f"trip-{slug}-" not in service_worker or "{{CACHE_NAME}}" in service_worker:
        raise WorkflowError("service worker cache 名稱未正確產生")
    if trip.get("name") not in markdown:
        raise WorkflowError("Markdown 缺少行程名稱")
    print(f"Verified {args.id}: {len(source['days'])} days")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create and maintain TripHelper itinerary pages.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser("create", help="Create a new data-driven itinerary PWA.")
    create.add_argument("--id", required=True, help="Trip id in YYYYMMDD-slug format.")
    create.add_argument("--name", required=True)
    create.add_argument("--short-name", required=True)
    create.add_argument("--start-date", required=True)
    create.add_argument("--end-date", required=True)
    create.add_argument("--summary", default="可離線使用的旅遊行程。")
    create.add_argument("--project-root", default=str(ROOT), help=argparse.SUPPRESS)
    create.set_defaults(handler=create_trip)

    build = subparsers.add_parser("build", help="Regenerate an itinerary page from YAML.")
    build.add_argument("--id", required=True, help="Trip id in YYYYMMDD-slug format.")
    build.add_argument("--project-root", default=str(ROOT), help=argparse.SUPPRESS)
    build.set_defaults(handler=build_existing_trip)

    verify = subparsers.add_parser("verify", help="Verify generated data and offline assets.")
    verify.add_argument("--id", required=True, help="Trip id in YYYYMMDD-slug format.")
    verify.add_argument("--project-root", default=str(ROOT), help=argparse.SUPPRESS)
    verify.set_defaults(handler=verify_existing_trip)
    return parser


def main() -> int:
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
