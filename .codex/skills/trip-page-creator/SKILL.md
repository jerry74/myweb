---
name: trip-page-creator
description: Create, scaffold, rebuild, or verify a new TripHelper itinerary PWA page from trip metadata and YAML. Use when adding a new destination or travel-date page, cloning an itinerary structure without copying the old Okinawa UI, regenerating a new page after YAML edits, or checking its offline assets and generated data.
---

# Trip Page Creator

Create new itinerary pages through the repository CLI. Keep `data/trips/<trip-id>.yaml` as the editable source and use the TripHelper Next template; never clone `20260530/` by hand.

## Create

1. Read the root `AGENTS.md`, inspect `git status`, and preserve unrelated changes.
2. Collect or infer:
   - id: `YYYYMMDD-destination-slug`
   - full and short names
   - start/end dates in `YYYY-MM-DD`
   - one-sentence summary
3. Run from the repository root:

```powershell
python scripts/trip-page.py create `
  --id 20270403-kyoto `
  --name "2027 京都親子行程" `
  --short-name "京都行程" `
  --start-date 2027-04-03 `
  --end-date 2027-04-05 `
  --summary "三天兩夜的京都散步與親子體驗。"
```

The command must create the YAML source, Markdown, date-directory PWA, embedded offline fallback, manifest, content-hashed service worker, SVG icon, and root-page card. It refuses existing targets; do not bypass that safeguard by deleting or overwriting files.

## Maintain

Edit only `data/trips/<trip-id>.yaml`, then run:

```powershell
python scripts/trip-page.py build --id 20270403-kyoto
python scripts/trip-page.py verify --id 20270403-kyoto
```

Do not hand-edit generated Markdown, JSON, fallback data, manifest, or service-worker cache names.

## UI Rules

- Read `design-system/triphelper-next/MASTER.md` before changing the template.
- Use `templates/trip-pwa/` as the shared template source.
- Preserve the Editorial Wayfinder layout, light/dark themes, keyboard focus, reduced motion, `previewDate`, install flow, offline fallback, and update prompt.
- Use inline stroke SVG icons and system fonts only. Do not add emoji icons, external fonts, CDN assets, Tailwind, or another framework.

## Validate

Run the workflow regression plus existing project gates:

```powershell
python tests/verify-trip-page-workflow.py
python tests/verify-trip-pipeline.py
node tests/verify-travel-pwa.js
python -m py_compile scripts/trip-page.py
node --check templates/trip-pwa/app.js
git diff --check
```

For UI changes, generate a disposable sample outside product directories, serve it over local HTTP, and verify 375, 768, 1024, and 1440px layouts, theme switching, date selection, console errors, and required PWA assets. Do not commit, push, or deploy unless explicitly requested.
