import argparse
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_trip(source: Path) -> dict:
    with source.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def write_json(trip: dict, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(trip, file, ensure_ascii=False, indent=2)
        file.write("\n")


def link_label(link: dict | list) -> str:
    return link["label"] if isinstance(link, dict) else link[0]


def link_url(link: dict | list) -> str:
    return link["url"] if isinstance(link, dict) else link[1]


def link_list(links: list[dict | list]) -> str:
    if not links:
        return ""
    return " / ".join(f"[{link_label(link)}]({link_url(link)})" for link in links)


def render_markdown(trip: dict) -> str:
    meta = trip["trip"]
    lines = [
        f"# {meta['name']}",
        "",
        f"- 日期：{meta['dateRange']}",
        f"- 航班：{meta['flights']}",
        f"- 租車：{meta['carRental']}",
        f"- 雨天核心：{meta['rainFocus']}",
        "",
        "## 每日行程",
        "",
    ]

    for index, day in enumerate(trip["days"], start=1):
        stay = trip["stays"].get(day["date"], {})
        breakfast = trip["breakfasts"].get(day["date"], "依照當天住宿與前一站行程彈性準備早餐。")
        lines.extend([
            f"### Day {index}｜{day['date']}（{day['weekday']}）{day['title']}",
            "",
            f"- 住宿：{stay.get('name', day['stay'])}",
            f"- 早餐準備：{breakfast}",
            f"- 雨天備案：{day['rainPlan']}",
            "",
            "#### 時間軸",
            "",
        ])

        for entry in day["schedule"]:
            links = link_list(entry.get("links", []))
            suffix = f"（{links}）" if links else ""
            lines.append(f"- **{entry['time']}**：{entry['text']}{suffix}")

        lines.extend(["", "#### 三餐與採買", ""])

        for entry in day["food"]:
            links = link_list(entry.get("links", []))
            suffix = f"（{links}）" if links else ""
            lines.append(f"- **{entry['title']}**：{entry['text']}{suffix}")

        lines.append("")

    lines.extend(["## 住宿整理", ""])
    for date, stay in trip["stays"].items():
        lines.append(f"- **{date}**：{stay['name']}（[Google Maps]({stay['mapUrl']})）")

    lines.extend(["", "## 早餐準備整理", ""])
    for date, text in trip["breakfasts"].items():
        lines.append(f"- **{date}**：{text}")

    lines.extend(["", "## 雨天切換摘要", ""])
    for date, text in trip["rainRules"].items():
        lines.append(f"- **{date}**：{text}")

    lines.append("")
    return "\n".join(lines)


def write_markdown(trip: dict, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(trip), encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build trip Markdown and PWA data from YAML.")
    parser.add_argument("--source", default="data/trips/20260530-okinawa.yaml")
    parser.add_argument("--markdown", default="trips/20260530-okinawa.md")
    parser.add_argument("--json", default="20260530/data.generated.json")
    parser.add_argument("--markdown-only", action="store_true")
    args = parser.parse_args()

    trip = load_trip(ROOT / args.source)
    write_markdown(trip, ROOT / args.markdown)
    if not args.markdown_only:
        write_json(trip, ROOT / args.json)


if __name__ == "__main__":
    main()
