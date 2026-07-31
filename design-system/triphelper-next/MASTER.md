# TripHelper Next Design System

本檔是未來新增行程頁面的視覺 Source of Truth。所有風格共用同一份 HTML、資料模型、互動與 PWA 行為，只透過 `trip.style` 和 CSS token 改變視覺語彙。

快速挑選可直接開啟 `previews/index.html`；原始截圖與檔名規則見 `previews/README.md`。

## Shared Product Direction

- 核心：手機先看「今天、下一站、時間線」，桌機再展開住宿、餐食與雨備摘要。
- 共用骨架：Hero、日期軌道、時間線、旅程摘要、安裝與更新提示。
- 共用視覺：24 套風格皆使用旅行繪本卡骨架——目的地主色框、場景式 Hero、彩色圖章日期、圓角時間線卡與清楚的下一站 CTA；每套再以自己的色票、底紋、字體節奏與形狀區分。
- 參考策略：吸收使用者提供的多目的地手機卡構圖與 `20251129/` 的藍綠漸層、白色圓卡、多彩分類節奏；不得直接複製參考插畫、角色、地標組合或品牌畫面。
- 禁止：複製目的地專屬 HTML、旅遊照片 hero、emoji 圖示、外部字型、CDN、框架或破壞離線能力的資產。
- 預設風格：`editorial-wayfinder`；未指定或舊資料缺少 `trip.style` 時使用此風格。

## Style Profiles

| Style ID | 中文名稱 | 適合行程 | 視覺語彙 |
|---|---|---|---|
| `editorial-wayfinder` | 城市編輯風 | 城市散步、交通密集、親子綜合行程 | 紙本導引、壓縮大標、鈷藍與訊號橘、圓形日期軌道 |
| `coastal-breeze` | 海島微風 | 海島、海灘、渡假村、親子放鬆 | 海水藍、珊瑚橘、沙色表面、柔和不對稱曲線 |
| `alpine-field-notes` | 山野手帳 | 自駕、登山、露營、自然觀察 | 森林綠、土壤橘、筆記橫線、方形路標與襯線標題 |
| `neon-metro` | 都會霓虹 | 夜間城市、購物、美食、展演 | 紫紅漸層、青綠高光、城市網格、切角幾何 |
| `heritage-ink` | 文化紙本 | 古城、寺社、博物館、慢旅行 | 宣紙色、赭紅、棕墨、細紋紙面與低圓角排版 |
| `candy-postcard` | 糖果明信片 | 咖啡甜點、閨蜜旅行、購物、拍照景點 | 莓粉、紫色、圓潤糖果卡與柔和點點底紋 |
| `cloud-storybook` | 雲朵繪本 | 親子、主題樂園、動物園、童話小鎮 | 天空藍、暖黃色、雲朵底紋與繪本式大圓角 |
| `sticker-playground` | 貼紙玩樂 | 樂園、追星、動漫、青春城市旅行 | 桃紅、藍綠、黃色貼紙感、粗框與硬陰影 |
| `berry-picnic` | 莓果野餐 | 花季、農場、野餐、鄉村與輕旅行 | 莓果紅、葉綠、奶油底色與細緻格紋 |
| `comic-panel` | 漫畫分鏡 | 樂園、城市闖關、運動賽事、親子冒險 | 紅藍黃原色、漫畫網點、粗黑框與硬陰影 |
| `cel-adventure` | 動畫冒險 | 自駕、戶外探索、家庭旅行、海陸移動 | 青綠、冒險橘、賽璐璐色塊與動態切角 |
| `retro-toon` | 復古卡通 | 老街、鐵道、懷舊餐廳、公路旅行 | 復古青綠、珊瑚紅、奶油紙與膠囊曲線 |
| `doodle-notebook` | 塗鴉手帳 | 校外旅行、市集、DIY、親子自由行 | 筆記格線、手繪虛線、不規則圓角與藍綠墨色 |
| `travel-toon-cards` | 旅行繪本卡 | 海島、賞花、親子、美食與多主題城市旅行 | 目的地主色框、繪本場景感、彩色圖章、白色圓卡與輕快層次 |
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

各風格的完整意圖、配色與限制位於 `styles/`。新增風格必須更新 CLI 白名單、CSS token、測試與此表，不得新增另一份頁面模板。

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
