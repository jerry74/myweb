---
name: trip-itinerary-maintainer
description: Use when updating the 20260530 Okinawa trip itinerary, changing travel days, meals, stays, rain plans, links, or publishing itinerary changes to the PWA site.
---

# Trip Itinerary Maintainer

Use this skill for the `20260530` Okinawa itinerary.

## Source of Truth

- Edit `data/trips/20260530-okinawa.yaml` for itinerary content.
- Do not edit generated outputs by hand:
  - `trips/20260530-okinawa.md`
  - `20260530/data.generated.json`
- `20260530/app.js` renders from `20260530/data.generated.json` when available.

## Daily Edit Workflow

When the user asks to change itinerary content but does not ask to publish:

1. Update only `data/trips/20260530-okinawa.yaml`.
2. Run:

```powershell
python scripts\build-trip.py --markdown-only
```

3. Review the diff for the YAML and Markdown.
4. Report the changed day, field, and Markdown path.
5. Do not update `20260530/data.generated.json`.

## Publish Workflow

When the user asks to publish, sync, update the PWA, or push the itinerary to the website:

1. Run:

```powershell
python scripts\build-trip.py
```

2. Confirm `20260530/data.generated.json` changed if itinerary data changed.
3. If PWA data changed, bump `CACHE_NAME` in `20260530/service-worker.js`.
4. Run verification:

```powershell
node --check 20260530\app.js
node tests\verify-travel-pwa.js
```

5. Commit and push when requested.

## Ambiguous Requests

If a requested itinerary change is unclear, summarize the intended YAML edit before changing files. Keep questions narrow and concrete.
