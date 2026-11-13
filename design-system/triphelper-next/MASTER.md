# TripHelper Next Design System

本檔是未來新增行程頁面的視覺 Source of Truth。所有風格共用同一份 HTML、資料模型、互動與 PWA 行為，只透過 `trip.style` 和 CSS token 改變視覺語彙。

挑選風格：`python scripts/trip-page.py styles 關鍵字` 篩選；`python scripts/trip-page.py gallery` 產生以目前 CSS 即時渲染的風格廊（永遠與範本同步）。`previews/index.html` 是靜態截圖目錄，可能落後於最新 token。

## Shared Product Direction

- 核心：手機先看「今天、下一站、時間線」，桌機再展開住宿、餐食與雨備摘要。
- 共用骨架：Hero、日期軌道、時間線、旅程摘要、安裝與更新提示。
- 共用視覺：30 套風格皆使用旅行繪本卡骨架——目的地主色框、場景式 Hero、彩色圖章日期、圓角時間線卡與清楚的下一站 CTA；每套再以自己的色票、底紋、字體節奏與形狀區分。
- 參考策略：吸收使用者提供的多目的地手機卡構圖與 `20251129/` 的藍綠漸層、白色圓卡、多彩分類節奏；不得直接複製參考插畫、角色、地標組合或品牌畫面。
- 禁止：複製目的地專屬 HTML、旅遊照片 hero、emoji 圖示、外部字型、CDN、框架或破壞離線能力的資產。
- 預設風格：`editorial-wayfinder`；未指定或舊資料缺少 `trip.style` 時使用此風格。

## Style Profiles

| Style ID | 中文名稱 | 適合行程 | 視覺語彙 |
|---|---|---|---|
| `editorial-wayfinder` | 城市編輯風 | 城市散步、交通密集、親子綜合行程 | 路線貼紙、分層街廓、鈷藍訊號橘與手繪硬陰影 |
| `coastal-breeze` | 海島微風 | 海島、海灘、渡假村、親子放鬆 | 海岸波浪、泡泡點紋、珊瑚潟湖與圓潤日期章 |
| `alpine-field-notes` | 山野手帳 | 自駕、登山、露營、自然觀察 | 雪峰場景、斜向步道、森林綠與土壤橘 |
| `neon-metro` | 都會霓虹 | 夜間城市、購物、美食、展演 | 霓虹樓群、光帶路線、城市網格與發光 CTA |
| `heritage-ink` | 文化紙本 | 古城、寺社、博物館、慢旅行 | 柱廊場景、印章圓章、赭紅棕墨與雙線框 |
| `candy-postcard` | 糖果明信片 | 咖啡甜點、閨蜜旅行、購物、拍照景點 | 糖果泡泡、莓粉紫色、彩色圓章與柔和厚陰影 |
| `cloud-storybook` | 雲朵繪本 | 親子、主題樂園、動物園、童話小鎮 | 雲丘場景、暖黃點綴、超大圓角與繪本軌道 |
| `sticker-playground` | 貼紙玩樂 | 樂園、追星、動漫、青春城市旅行 | 斜切街景、貼紙圓章、彩色帶狀 CTA 與硬陰影 |
| `berry-picnic` | 莓果野餐 | 花季、農場、野餐、鄉村與輕旅行 | 野餐格紋、果實丘陵、莓果紅葉綠與圓形日期章 |
| `comic-panel` | 漫畫分鏡 | 樂園、城市闖關、運動賽事、親子冒險 | 速度線、印刷網點、對話框 CTA 與厚黑框卡片 |
| `cel-adventure` | 動畫冒險 | 自駕、戶外探索、家庭旅行、海陸移動 | 斜向冒險場景、速度帶、青綠橘色塊與動態節點 |
| `retro-toon` | 復古卡通 | 老街、鐵道、懷舊餐廳、公路旅行 | 復古街景、道路條紋、青綠珊瑚紅與膠囊曲線 |
| `doodle-notebook` | 塗鴉手帳 | 校外旅行、市集、DIY、親子自由行 | 剪貼簿紙膠帶、彩色筆刷、波浪路線與手繪硬陰影 |
| `travel-toon-cards` | 旅行繪本卡 | 海島、賞花、親子、美食與多主題城市旅行 | 旅行貼紙明信片、海岸波浪、郵票圓章與珊瑚潟湖層次 |
| `aurora-frost` | 極光冰原 | 冰島、雪地、溫泉、極光追尋 | 深海藍、冰霜青、極光綠、雪峰幾何與星點底紋 |
| `savanna-safari` | 草原遊獵 | 非洲草原、動物觀察、越野與親子探險 | 夕照金、土棕、草原綠、足跡點紋與有機曲線 |
| `ancient-odyssey` | 古文明漫遊 | 古羅馬、希臘、遺址與博物館 | 石灰金、赭紅、柱廊幾何、雙線框與襯線標題 |
| `tokyo-pulse` | 東京潮流 | 東京夜景、動漫、購物、科技與美食 | 午夜藍、霓虹粉與青、城市網格、切角街廓與高能量對比 |
| `coral-dive` | 珊瑚潛旅 | 潛水、浮潛、珊瑚礁與海島生態 | 潟湖青、珊瑚紅、氣泡點紋、海底弧線與圓潤卡片 |
| `sakura-promenade` | 櫻花漫遊 | 賞櫻、寺社、春日街區與和風散步 | 櫻花粉、春芽綠、花瓣點紋、鳥居場景與柔和圓角 |
| `tropical-lagoon` | 熱帶潟湖 | 峇里島、衝浪、沙灘與渡假 | 潟湖藍綠、珊瑚橘、日光黃、波紋與島嶼曲線 |
| `golden-boulevard` | 金色街廓 | 巴黎、歐洲古都、咖啡與建築散步 | 蜂蜜金、磚紅、街廓格線、遮棚條紋與典雅襯線字 |
| `alpine-railway` | 高山鐵道 | 瑞士、景觀列車、山屋與湖山健行 | 森林綠、天空藍、雪峰幾何、鐵道路線與明信片卡 |
| `sunset-street-food` | 夕陽街頭食趣 | 泰國、夜市、寺廟、嘟嘟車與美食探索 | 夕陽橘、辣椒紅、青綠點綴、攤棚條紋與街屋色塊 |
| `desert-caravan` | 沙漠星旅 | 摩洛哥、沙漠露營、古城與駱駝旅程 | 香料橘、靛青、沙丘波線、帳篷剪影與夜空星點 |
| `nordic-fjord` | 北歐峽灣 | 挪威、峽灣、公路、瀑布與木屋旅行 | 冰河青、松林綠、分層山谷、瀑布線與清爽留白 |
| `carnival-parade` | 嘉年華遊行 | 巴西、節慶、音樂、舞蹈與朋友旅行 | 莓紅、亮黃、熱帶綠、彩旗節奏與紙花碎片 |
| `forest-fairytale` | 森林童話 | 親子森林、童話村、動物園與露營 | 苔蘚綠、莓果紅、蘑菇圓點、樹冠剪影與柔軟卡片 |
| `cosmic-camp` | 宇宙露營 | 天文館、觀星、科技館與科學親子旅行 | 深空靛、星雲紫、電光藍、軌道圓環與星球幾何 |
| `treasure-island` | 尋寶海島 | 海島跳島、船旅、親子探險與尋寶闖關 | 海圖米色、潟湖青、寶箱紅、航線虛線與島嶼輪廓 |
| `bund-wonderland` | 外灘樂遊 | 上海、江南古鎮、主題樂園、外灘夜景與親子城市行 | 黛藍夜空、豫園朱紅、燈籠金、天際線剪影與雲朵圓角 |

各風格的完整意圖、配色與限制位於 `styles/`。風格清單的唯一來源是 `styles.json`（id、名稱、適合行程、視覺語彙、manifest 色碼）；CLI、測試與即時風格廊都讀它。

### 新增風格

1. `python scripts/trip-page.py new-style --id <kebab-id> --label "中文名稱" --base <最接近的既有風格> --fits "…" --vibe "…" --theme-color "#RRGGBB" --background-color "#RRGGBB"`：自動複製 base 的淺色／場景／深色 CSS 區塊、寫入 `styles.json`、建立 `styles/<id>.md`、在上表加一列。
2. 在 `templates/trip-pwa/styles.css` 搜尋 `data-style="<id>"`，只改 primitive 與 component token；不得新增另一份頁面模板或元件 selector。
3. `python scripts/trip-page.py gallery` 產生即時風格廊（`previews/live/`，已 gitignore），檢查淺色／深色、手機／桌機與對比。
4. `python tests/verify-trip-page-workflow.py`。靜態截圖（`previews/<id>/*.png`）是選配，只有要更新離線選型目錄時才需要。

## Three-layer Tokens

1. Primitive：`--primitive-*` 保存原始色票，例如 ink、paper、primary、signal、highlight。
2. Semantic：`--color-*` 表達跨風格意義，例如文字、表面、主互動、警示、focus。
3. Component：`--hero-*`、`--next-stop-*`、`--day-*`、`--timeline-*`、`--brief-*` 決定元件字體、形狀、陰影與背景。

元件 CSS 只能使用 semantic 或 component token。風格 selector 以 `:root[data-style="..."]` 覆寫 primitive 或 component token；dark mode 以 `:root[data-theme="dark"][data-style="..."]` 覆寫 primitive token。不得在元件 selector 直接放目的地專屬色碼。

## Shared Layout and Components

- Hero：目的地主色場景卡＋主標題＋簡短摘要；用 CSS 幾何雲朵、太陽與色塊營造插畫層次，桌機右側放高對比「下一站」面板。
- Day rail：黏性水平日期軌道；目前日期使用漸層圖章卡與文字雙重標示，鍵盤可操作。
- Timeline：時間欄、垂直路線、白色圓角資訊卡與多彩節點；當前下一站仍使用 highlight token，不只靠顏色辨識。
- Briefing：住宿、三餐、雨備使用帶分類色的浮層卡，桌機集中於次欄，手機落到時間線下方。
- 旅程資訊：`trip.flights`、`trip.carRental`、`trip.rainFocus` 有實際內容時，在 Briefing 最後顯示「旅程資訊」卡；仍是「待補」則隱藏。
- 當日標籤：`day.tags` 以 chip 顯示在當日標題下方，形狀沿用 `--day-tab-radius`。
- 待補狀態：含「待補／待確認／待規劃」的文字自動加 `.is-pending`，以淡化文字與虛線時間線卡呈現，讓剛建立的行程一眼看出還缺什麼。
- Icons：只用一致的 24px stroke SVG；所有 icon-only button 都要有 `aria-label`。
- Theme：支援 light/dark、自動偵測與手動切換；風格不可鎖死顯示模式。

## Typography and Motion

- 字體只用可離線的系統字型：`Segoe UI Variable`、`Noto Sans TC`、`Microsoft JhengHei UI`、Georgia 等。
- 間距以 4/8px 為基準；主要頁寬 `1240px`。
- 動畫限 150–200ms 顏色與透明度；不得用 hover 位移、大幅縮放、parallax 或無限動畫。
- 風格差異優先由色彩、字體節奏、底紋、圓角與陰影形成，不改變資訊架構。

## Accessibility and Responsive Rules

- 正文對比至少 4.5:1；focus ring 必須清楚且不可被移除。
- 提供 skip link、連續 heading hierarchy、語意化 `nav/main/section/aside/ol`。
- 支援 `prefers-reduced-motion`；按鈕和連結保留 hover、focus、keyboard 回饋。
- 必測 375、768、1024、1440px；不得水平溢出，黏性導覽不得遮住內容。
- PWA 離線 fallback、安裝按鈕、service worker 更新提示與 `previewDate` 必須保留。

## Delivery Checklist

- [ ] `trip.style` 是 CLI 支援的 style ID，HTML 與 manifest 已同步。
- [ ] 無 emoji icon、外部字型、框架或 CDN。
- [ ] light/dark 皆有可讀對比與 visible focus。
- [ ] 375/768/1024/1440px 無水平捲動。
- [ ] `prefers-reduced-motion` 生效。
- [ ] YAML、JSON、fallback、manifest 與 service worker cache 同步。
