# TripHelper Next Design System

本檔是未來新增行程頁面的視覺 Source of Truth。它採用 `ui-ux-pro-max` 的 editorial、單欄優先、清楚層級與高對比建議，並依本專案的離線 PWA、繁體中文與純靜態架構調整。

## Design Direction

- 名稱：Editorial Wayfinder。
- 感受：旅程手冊、交通導引、紙本行程單；俐落但不冷淡。
- 核心：手機先看「今天、下一站、時間線」，桌機再展開住宿、餐食與雨備摘要。
- 禁止：沖繩舊版的青綠卡片堆疊、玻璃擬態、旅遊照片 hero、emoji 圖示、過度圓角與大面積漸層。

## Tokens

| Role | Light | Dark | Usage |
|---|---|---|---|
| Ink | `#171717` | `#F6F2E9` | 標題、主要文字 |
| Paper | `#F3F0E8` | `#101318` | 頁面背景 |
| Surface | `#FFFDF8` | `#181C23` | 浮動導覽、摘要 |
| Cobalt | `#2457D6` | `#7DA2FF` | 下一站、連結、主要互動 |
| Signal | `#E7522C` | `#FF7958` | 狀態、日期標記、雨備 |
| Lime | `#D9EF57` | `#C8DF4A` | 當前節點、確認狀態 |

- 字體只用離線系統字型：`Segoe UI Variable`、`Noto Sans TC`、`Microsoft JhengHei UI`。
- 間距以 4/8px 為基準；主要頁寬 `1240px`。
- 小／中／大圓角為 `8px / 16px / 28px`；一般內容不用每段都包卡片。
- 動畫限 150–200ms 顏色與透明度；不得用 hover 位移或大幅縮放。

## Layout and Components

- Hero：超大緊縮標題＋簡短摘要；桌機右側放高對比「下一站」面板。
- Day rail：黏性水平日期軌道；目前日期使用 ink/paper 反白，鍵盤可操作。
- Timeline：時間欄、垂直路線與節點；當前下一站用 lime 強調。
- Briefing：住宿、三餐、雨備集中在次欄；手機落到時間線下方。
- Icons：只用一致的 24px stroke SVG；所有 icon-only button 都要有 `aria-label`。
- Theme：支援 light/dark、自動偵測與手動切換；不得依賴外部字型或 CDN。

## Accessibility and Responsive Rules

- 正文對比至少 4.5:1；focus ring 使用 `#FFB703` 且不可被移除。
- 提供 skip link、連續 heading hierarchy、語意化 `nav/main/section/aside/ol`。
- 支援 `prefers-reduced-motion`；不做 parallax、scroll-jacking 或無限動畫。
- 必測 375、768、1024、1440px；不得水平溢出，黏性導覽不得遮住內容。
- PWA 離線 fallback、安裝按鈕、service worker 更新提示與 `previewDate` 必須保留。

## Delivery Checklist

- [ ] 無 emoji icon、外部字型、框架或 CDN。
- [ ] 點擊、hover、focus、keyboard 都有清楚回饋。
- [ ] Light/dark 皆有可讀對比。
- [ ] 375/768/1024/1440px 無水平捲動。
- [ ] `prefers-reduced-motion` 生效。
- [ ] YAML、JSON、fallback、manifest 與 service worker cache 同步。
