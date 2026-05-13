import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "trips" / "20260530-okinawa.yaml"
MARKDOWN = ROOT / "trips" / "20260530-okinawa.md"
GENERATED = ROOT / "20260530" / "data.generated.json"


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


trip = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))
generated = json.loads(GENERATED.read_text(encoding="utf-8"))
markdown = MARKDOWN.read_text(encoding="utf-8")

assert_true(trip["trip"]["id"] == "20260530-okinawa", "source trip id mismatch")
assert_true(generated["trip"]["id"] == trip["trip"]["id"], "generated trip id mismatch")
assert_true(generated["days"] == trip["days"], "generated days are not synced with YAML")
assert_true(len(trip["days"]) == 8, "expected 8 itinerary days")
assert_true(trip["trip"]["name"] in markdown, "markdown missing trip name")

for index, day in enumerate(trip["days"], start=1):
    heading = f"Day {index}｜{day['date']}（{day['weekday']}）{day['title']}"
    assert_true(heading in markdown, f"markdown missing heading: {heading}")

print("Trip pipeline verification passed.")
