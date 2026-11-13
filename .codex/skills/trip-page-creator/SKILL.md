---
name: trip-page-creator
description: Create, scaffold, rebuild, or verify a new TripHelper itinerary PWA page from trip metadata and YAML. Use when adding a new destination or travel-date page, cloning an itinerary structure without copying the old Okinawa UI, regenerating a new page after YAML edits, or checking its offline assets and generated data.
---

# Trip Page Creator

Create new itinerary pages through the repository CLI. Keep `data/trips/<trip-id>.yaml` as the editable source and use the TripHelper Next template; never clone `20260530/` by hand.

## Create

1. Read the root `AGENTS.md`, inspect `git status`, and preserve unrelated changes.
2. Collect or infer:
   - id: `YYYYMMDD-destination-slug`（日期 = 出發日）
   - full name（short name 可省略，預設同 full name）
   - start/end dates in `YYYY-MM-DD`
   - destination UTC offset（例如日本 `+09:00`；預設 `+08:00`）
   - one-sentence summary
   - style profile：`python scripts/trip-page.py styles 海島 親子` 以關鍵字篩選；要比較實際畫面時執行 `python scripts/trip-page.py gallery`，用 `python -m http.server 4173` 開 `http://127.0.0.1:4173/design-system/triphelper-next/previews/live/`
3. Run from the repository root:

```powershell
python scripts/trip-page.py create `
  --id 20270403-kyoto `
  --name "2027 京都親子行程" `
  --start-date 2027-04-03 `
  --end-date 2027-04-05 `
  --timezone +09:00 `
  --style heritage-ink `
  --summary "三天兩夜的京都散步與親子體驗。"
```

The command creates the YAML source, Markdown, date-directory PWA, embedded offline fallback, manifest, content-hashed service worker, SVG icon, and root-page card, then prints the next steps. It refuses existing targets; do not bypass that safeguard by deleting or overwriting files.

## Maintain

Edit only `data/trips/<trip-id>.yaml`, then run:

```powershell
python scripts/trip-page.py build --id 20270403-kyoto
python scripts/trip-page.py verify --id 20270403-kyoto --strict
```

- `build` validates the YAML first（例如未加引號的 `time: 14:00`、星期錯誤、連結格式），列出 `days[0].schedule[1].time` 這類路徑後停止；修正 YAML 再重跑。
- `build` re-renders every page asset from `templates/trip-pwa/`, so template upgrades, name/date changes and `trip.style` changes all propagate. The page only ships the CSS of its own style.
- `verify` warns about remaining 「待補／待確認」; `--strict` fails on them and is the publish gate.
- Do not hand-edit generated Markdown, JSON, fallback data, HTML, CSS, manifest, or service-worker cache names.

## UI Rules

- Read `design-system/triphelper-next/MASTER.md` before changing the template.
- Use `templates/trip-pwa/` as the shared template source.
- Preserve the shared Wayfinder layout, light/dark themes, keyboard focus, reduced motion, `previewDate`/`previewStyle`/`previewTheme`, install flow, offline fallback, and update prompt.
- Use inline stroke SVG icons and system fonts only. Do not add emoji icons, external fonts, CDN assets, Tailwind, or another framework.

## Styles

風格清單只存在 `design-system/triphelper-next/styles.json`；不要在文件或測試中再手抄一份。

- 列出／篩選：`python scripts/trip-page.py styles [關鍵字…]`
- 即時比較：`python scripts/trip-page.py gallery`（輸出到已 gitignore 的 `previews/live/`）
- 更換既有行程風格：改 YAML 的 `trip.style`，再 `build` + `verify`
- 新增風格：

```powershell
python scripts/trip-page.py new-style --id harbor-lights --label "港灣燈火" `
  --base coastal-breeze --fits "港口、夜景、渡輪" --vibe "海港藍、燈塔黃、航線虛線" `
  --theme-color "#1a5f8a" --background-color "#eef6fb"
```

它會複製 base 風格的所有 CSS 區塊（淺色、場景、深色）、加入登錄檔、建立 `styles/<id>.md` 並在 MASTER 表格加一列。之後只需在 `styles.css` 搜尋 `data-style="<id>"` 調整 token，並用 gallery 檢查淺色／深色與手機／桌機。靜態截圖（`previews/<id>/*.png`）是選配。

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
