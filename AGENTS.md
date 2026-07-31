# TripHelper Repository Guidelines

本文件適用於 `D:\WorkSpace\TripHelper` 根目錄及其子目錄。以目前工作樹、程式碼與可驗證結果為準；舊計畫文件只代表設計意圖，不得覆蓋目前實作狀態。

# Project Overview

TripHelper 是以 GitHub Pages 發布的靜態旅遊行程網站，包含可離線使用的 PWA。主要維護中的產品是 `20260530/` 沖繩親子行程，旅行日期為 2026/05/30–2026/06/06；`20251129/` 是保留中的富國島舊行程 PWA。

目前階段是「行程資料維護、生成與發布」：以 YAML 維護行程，生成 Markdown 與 PWA JSON，再以靜態檔案發布。專案沒有 Node bundler、後端服務或 TypeScript build pipeline。

# Source of Truth

- 行程內容：`data/trips/20260530-okinawa.yaml`。
- 生成流程：`scripts/build-trip.py`。
- 新行程頁面流程：`scripts/trip-page.py`，以 `templates/trip-pwa/` 與 `design-system/triphelper-next/MASTER.md` 建立、重建及驗證獨立 PWA；不要複製沖繩頁面當新範本。
- 生成結果：`trips/20260530-okinawa.md` 與 `20260530/data.generated.json`。修改行程時先改 YAML，再執行 build；不要手動只改生成檔。
- PWA 行為與版面：`20260530/index.html`、`20260530/styles.css`、`20260530/app.js`、`20260530/service-worker.js`、`20260530/manifest.webmanifest` 及 `20260530/icons/`。
- 舊行程執行檔：`20251129/`；除非任務明確指定，維持其現狀。
- `docs/superpowers/` 是設計與實作紀錄；若與實際程式碼衝突，以程式碼、設定、測試與 Git 狀態為準。

# Repository Structure

- `20260530/`：目前發布的沖繩 PWA，包含頁面、樣式、前端邏輯、manifest、service worker、圖示與生成資料。
- `20251129/`：舊的富國島 PWA，獨立維護其靜態資產與 service worker。
- `data/trips/`：可編輯的行程來源資料。
- `trips/`：由來源資料生成的 Markdown 行程文件。
- `scripts/`：資料生成與匯出工具；主要發布資料入口是 `build-trip.py`。目前未追蹤的 `export-my-maps.py` 僅用於產生 Google My Maps 匯入檔，不是 PWA build 依賴。
- `tests/`：Python pipeline 驗證與 Node.js 靜態 PWA 驗證。
- `docs/superpowers/`：設計規格與歷史實作計畫。
- `.codex/skills/`：此專案使用的本地 Codex skills，不是產品執行時依賴。
- `templates/trip-pwa/`：未來行程頁面的通用 Wayfinder PWA 範本；以 `trip.style` 選擇視覺風格，不複製頁面模板。
- `design-system/triphelper-next/`：新行程頁面的設計 token、版面、互動與無障礙規則。
- `design-system/triphelper-next/previews/`：24 套 style ID 的瀏覽器截圖與離線選型目錄；只供設計挑選，不是 PWA 執行期資產。
- `myweb/`：目前工作樹中的巢狀 Git 工作副本，未納入根 repo 追蹤；不可當作根 repo 的發布來源，也不可在未指定時批次修改或提交。
- `exports/` 與根目錄的研究、匯出、暫存檔：除非任務明確要求，視為工作產物，不得加入產品提交。

# Commands

- 安裝：`python -m pip install PyYAML`。目前沒有 `requirements.txt`、`pyproject.toml` 或 `package.json`；Node.js 僅用於驗證腳本。
- 開發：在 repo 根目錄執行 `python -m http.server 4173`，瀏覽 `http://127.0.0.1:4173/20260530/`。
- 測試：`python tests/verify-trip-pipeline.py`；`node tests/verify-travel-pwa.js`。
- Typecheck：不適用，本專案沒有 TypeScript。可執行語法檢查：`python -m py_compile scripts/build-trip.py tests/verify-trip-pipeline.py` 與 `node --check 20260530/app.js`。
- Build：`python scripts/build-trip.py`。預設會重新生成 Markdown 與 `20260530/data.generated.json`。
- 新增行程頁面：`python scripts/trip-page.py create --id YYYYMMDD-slug --name "完整名稱" --short-name "短名稱" --start-date YYYY-MM-DD --end-date YYYY-MM-DD --style <style-id> --summary "摘要"`；style ID 見 `design-system/triphelper-next/MASTER.md`。
- 維護新行程：先改 `data/trips/<trip-id>.yaml`，再執行 `python scripts/trip-page.py build --id <trip-id>` 與 `python scripts/trip-page.py verify --id <trip-id>`。
- 新行程流程測試：`python tests/verify-trip-page-workflow.py`。
- 選用地圖匯出：`python scripts/export-my-maps.py`。預設輸出到 `exports/`；此工具與輸出目前都不是發布鏈或必要完成條件。
- 完整驗證：先執行 Build，再執行上述兩個測試、Python/Node 語法檢查及 `git diff --check`；若有 UI 或 PWA 資產變更，再以本地 HTTP server 檢查兩個站點與其 manifest、service worker、生成 JSON 均回應 `200`。

`tests/verify-okinawa-pwa-redesign.js` 仍引用目前空的 `okinawa-pwa/` 路徑，缺少其預期的 `index.html` 與 `app.js`，不是有效驗證入口；除非先修正測試目標，不把它列為完成條件。

# Architecture Rules

- 維持靜態 GitHub Pages 架構；除非任務明確要求，不引入後端、資料庫、bundler 或新的框架。
- 行程資料流固定為 `YAML -> scripts/build-trip.py -> Markdown/JSON -> 20260530 PWA`。發布行程時，來源 YAML 與生成檔必須同時更新且通過同步測試。
- 新行程資料流固定為 `create -> YAML -> trip-page.py build -> Markdown/JSON/fallback/manifest/service worker -> verify`；`create` 拒絕覆寫既有 id 或日期目錄。
- 新行程 UI 固定使用 `templates/trip-pwa/` 與 TripHelper Next 設計系統；風格只由 `trip.style` 與三層 token 切換，並保留純靜態、離線 fallback、內容雜湊 cache、`previewDate`、light/dark、鍵盤操作及 reduced-motion。
- 保留 `20260530/data.generated.json` 的載入與 `app.js` 內建 fallback；生成 JSON 無法取得時，PWA 仍應能離線或以 fallback 渲染。
- 維持 `trip.id = 20260530-okinawa`、日期順序、每日行程結構與 `startAt`/`departureAt`/`endAt` 語意。若資料模型需要變更，必須同步修改 generator、PWA、測試與文件。
- 兩個 PWA 是各自獨立的子目錄；manifest、scope、相對 URL 與 service worker cache 不得依賴另一個站點的路徑。
- `20260530/service-worker.js` 的 cache asset 清單必須涵蓋實際需要的資產；修改可快取資產或生成資料時，更新 cache 版本並完成新舊 service worker 更新流程驗證。
- 行程狀態、倒數、當日選擇與下一站判斷由前端依行程日期處理；不要以當前開發日期硬編碼結果。需要可重現檢查時，使用既有的 `previewDate` 機制。

# Safety Boundaries

- 禁止在未指定時修改、刪除或重置既有使用者變更；目前髒工作樹中的 `20260530/`、`data/`、`scripts/`、`tests/`、`docs/`、`trips/` 變更，以及未追蹤的 `myweb/`、`exports/`、地圖匯出工具與研究文件都必須保留。
- 禁止直接手改生成 JSON/Markdown 取代 YAML；禁止以 `git add -A` 把研究檔、匯出檔或巢狀 repo 一起提交。只 stage 任務明確涉及的檔案。
- 禁止未經明確授權執行 force push、`git reset --hard`、大量刪除、覆寫其他工作副本、commit、push、建立 PR 或部署。
- 禁止把 token、cookie、密碼、私鑰、`.env`、API 回應中的完整憑證或 GitHub/Pages secret 放入 repo、文件、測試輸出或 commit。此專案目前不需要執行期秘密；未來若需要，僅使用 Bitwarden/CI secret 或程序環境注入，且不得存放在 `D:\WorkSpace\TripHelper`。
- 不要把 `myweb/` 當成可安全覆蓋的備份；若任務指定操作它，先以 `git -C myweb status` 確認其獨立工作樹。

# Definition of Done

完成修改時必須符合：

- 修改範圍與任務一致，且未覆蓋不相關工作；`git diff` 與 `git status` 已人工檢查。
- 行程變更已由 YAML 重新生成，`python tests/verify-trip-pipeline.py` 通過。
- PWA 資產、manifest、service worker、生成資料與必要 UI markers 通過 `node tests/verify-travel-pwa.js`。
- 相關 Python/JavaScript 語法檢查與 `git diff --check` 通過；本專案沒有額外 Typecheck 或 lint。
- 新行程工作流或範本變更已通過 `python tests/verify-trip-page-workflow.py`、`python -m py_compile scripts/trip-page.py` 與 `node --check templates/trip-pwa/app.js`。
- UI/PWA 修改已用本地 HTTP server 驗證目錄、資產、`previewDate` 狀態與必要的 service worker 更新行為。
- 若是發布修改，生成檔與 cache 版本已包含在同一個有意識的變更中；若改變資料模型，相關測試與文件也已更新。
- 未提交秘密、暫存檔、匯出檔、巢狀 repo 或不相關檔案。

# Deployment

- 目前發布來源是根 repo 的 `main` 分支，遠端為 `https://github.com/jerry74/myweb.git`；GitHub Pages 以 repo 靜態檔案發布，不能只以本地測試或 GitHub Actions 狀態判定完成。
- 部署前必須完成 Build、兩個有效驗證腳本、語法檢查、`git diff --check`、變更範圍檢查與 service worker cache 版本檢查；只有明確授權後才 commit/push `main`。
- 正式環境目前入口為 `https://jerry74.github.io/myweb/`。發布後至少檢查 `/20251129/`、`/20260530/`、`/20260530/index.html`、`/20260530/manifest.webmanifest`、`/20260530/service-worker.js` 與 `/20260530/data.generated.json` 回應 `200`，並確認 HTML/JSON/快取內容是本次版本。
- PWA 部署後須確認 service worker 能取得新版本；若瀏覽器仍使用舊 cache，使用頁面提供的更新提示完成更新，再檢查生成資料與當日行程。
- 回滾以 Git 可追溯版本為準：找出上一個已驗證的 commit，使用 `git revert <問題commit>` 建立反向提交並重新發布；禁止以 force push 或直接刪除正式檔案回滾。回滾後重新執行正式環境 smoke test。
