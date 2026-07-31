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
   - style profile；依旅遊類型從下方 Style Guide 選擇
   - 如果使用者尚未決定風格，先開啟 `design-system/triphelper-next/previews/index.html` 比較實際截圖
3. Run from the repository root:

```powershell
python scripts/trip-page.py create `
  --id 20270403-kyoto `
  --name "2027 京都親子行程" `
  --short-name "京都行程" `
  --start-date 2027-04-03 `
  --end-date 2027-04-05 `
  --style heritage-ink `
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
- Preserve the shared Wayfinder layout, light/dark themes, keyboard focus, reduced motion, `previewDate`, install flow, offline fallback, and update prompt.
- Use inline stroke SVG icons and system fonts only. Do not add emoji icons, external fonts, CDN assets, Tailwind, or another framework.

## Style Guide

- `editorial-wayfinder`：城市散步、跨區交通、資訊密集的綜合行程；也是預設值。
- `coastal-breeze`：海島、海灘、渡假村與親子放鬆。
- `alpine-field-notes`：自駕、登山、露營與自然觀察。
- `neon-metro`：夜間城市、購物、美食與展演。
- `heritage-ink`：古城、寺社、博物館與慢旅行。
- `candy-postcard`：咖啡甜點、閨蜜旅行、購物與拍照景點。
- `cloud-storybook`：親子、主題樂園、動物園與童話小鎮。
- `sticker-playground`：樂園、追星、動漫與青春城市旅行。
- `berry-picnic`：花季、農場、野餐與鄉村輕旅行。
- `comic-panel`：樂園、城市闖關、運動賽事與親子冒險。
- `cel-adventure`：自駕、戶外探索、家庭旅行與海陸移動。
- `retro-toon`：老街、鐵道、懷舊餐廳與公路旅行。
- `doodle-notebook`：校外旅行、市集、DIY 與親子自由行。
- `travel-toon-cards`：海島、賞花、親子、美食與多主題城市旅行；活潑旅行繪本卡風格。
- `aurora-frost`：冰島、雪地、溫泉、極光追尋與冬季自然旅行。
- `savanna-safari`：非洲草原、野生動物觀察、越野與親子探險。
- `ancient-odyssey`：古羅馬、希臘、考古遺址、博物館與文明巡禮。
- `tokyo-pulse`：東京夜景、動漫、購物、科技、美食與高密度都會旅行。
- `coral-dive`：潛水、浮潛、珊瑚礁、海洋生態與海島探險。
- `sakura-promenade`：賞櫻、寺社、春日街區、和風散步與花季旅行。
- `tropical-lagoon`：峇里島、衝浪、沙灘、渡假村與熱帶放鬆行程。
- `golden-boulevard`：巴黎、歐洲古都、咖啡館、建築與藝術散步。
- `alpine-railway`：瑞士、景觀列車、山屋、湖山健行與鐵道旅行。
- `sunset-street-food`：泰國、夜市、寺廟、嘟嘟車與街頭美食探索。

要更換既有新行程的風格，修改 YAML 的 `trip.style` 後執行 `build` 與 `verify`。不要手改生成頁面的 `data-style` 或 manifest 色碼。新增風格時必須沿用 primitive → semantic → component 三層 token，並同步更新 `STYLE_PROFILES`、共享 CSS、設計文件與每風格回歸測試。

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
