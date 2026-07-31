# Travel PWA 統一架構設計

## 背景

目前 `triphelper` 站內有兩個旅行子站：

- `20251129/`：2025 富國島親子之旅，現況為單一 `index.html`，使用 React UMD + Babel inline script，尚未具備 PWA 基礎資源。
- `20260530/`：2026 沖繩親子自由行，現況已具備 `manifest.webmanifest`、`service-worker.js`、`icons/icon.svg` 與靜態資產，屬於可安裝的 PWA 雛形。

需求是將兩個子站統一為 PWA 架構，並為兩者加入一致的旅程狀態切換規則。狀態以日期自動切換，不依賴後端或手動操作。

## 目標

本次設計要達成以下目標：

1. `20251129/` 補齊 PWA 所需資源與註冊流程。
2. `20260530/` 保留既有 PWA 結構，但新增開始前倒數頁與結束頁。
3. 兩個站統一使用同一套旅程狀態模型：
   - `countdown`：旅程開始前
   - `active`：旅程進行中
   - `ended`：旅程結束後
4. 狀態判斷完全由前端依日期自動切換，部署方式維持 GitHub Pages 靜態站。
5. 保留各站原有內容風格，不做大幅重寫。

## 非目標

本次不處理以下內容：

- 不導入後端 API、資料庫或排程系統。
- 不把兩個子站重構成單一前端框架專案。
- 不更動 `triphelper` 根入口頁的資訊架構。
- 不新增相簿、花費統計或旅遊回顧內容，只預留結束頁入口文案與按鈕。

## 核心設計

### 1. 統一旅程狀態模型

每個子站定義自己的旅程設定：

- `tripName`
- `startAt`
- `endAt`
- `timezone`
- `countdownTitle`
- `countdownBody`
- `endedTitle`
- `endedBody`
- `primaryActionLabel`
- `primaryActionHref`

前端在載入時使用旅程設定與當前時間計算狀態：

- 當前時間 `< startAt`：`countdown`
- `startAt <= 當前時間 <= endAt`：`active`
- `當前時間 > endAt`：`ended`

時區統一以 `Asia/Taipei` 為基準，避免使用者裝置位於其他國家時導致旅程切換日錯誤。

### 2. 倒數邏輯

在 `countdown` 狀態顯示：

- 距離出發剩餘天數、時、分
- 出發日期與返程日期
- 旅程亮點摘要
- PWA 安裝按鈕
- 「預覽完整行程」或「查看旅程重點」按鈕

倒數為純前端計算，畫面更新週期為每分鐘一次即可，不追求秒級刷新，以降低不必要重繪。

### 3. 旅程中邏輯

在 `active` 狀態顯示原有主要行程內容，並額外補充一個簡潔狀態摘要：

- 今天是旅程第幾天
- 距離返程剩餘幾天
- 當前日期對應的旅程範圍

這個摘要是疊加在原畫面上的狀態資訊，不改變原本內容主體。

### 4. 結束頁邏輯

在 `ended` 狀態顯示：

- 旅程已結束主標題
- 一段簡短回顧型文案
- 「重新查看完整行程」按鈕
- 視覺上弱化即時行程感，改成回顧落版

結束頁不移除原本內容，而是將原本內容收斂為次要入口，避免旅程過後仍直接落在臨時操作型頁面。

## 各站實作設計

### `20251129/` 富國島站

#### 現況

- 所有內容集中於單一 `index.html`
- 使用 React 18 UMD、ReactDOM UMD 與 Babel inline script
- 目前沒有 `manifest`、`service worker`、`icons`

#### 設計

1. 新增 PWA 檔案：
   - `20251129/manifest.webmanifest`
   - `20251129/service-worker.js`
   - `20251129/icons/icon.svg`

2. 更新 `20251129/index.html`：
   - 補 `theme-color`
   - 補 `description`
   - 補 `manifest` / `icon` / `apple-touch-icon`
   - 補 service worker 註冊 script

3. 狀態殼層策略：
   - 優先採用「外層控制顯示區塊」方式，不全面拆散原本 React 行程內容
   - 新增頂層容器負責切換 `countdown / active / ended`
   - `active` 時渲染原本富國島主畫面
   - `countdown` / `ended` 時顯示新的狀態頁內容

4. 日期設定
   - 起始日：`2025-11-29T00:00:00+08:00`
   - 結束日：`2025-12-06T23:59:59+08:00`

#### 風險

- `index.html` 內含大型 inline React/Babel script，若直接大改容易引入語法錯誤。
- 因此本次優先用「最小侵入」方式包裝現有畫面，不做激進重構。

### `20260530/` 沖繩站

#### 現況

- 已有 `index.html`、`app.js`、`styles.css`
- 已有 `manifest.webmanifest`、`service-worker.js`、`icons/icon.svg`
- 目前直接呈現旅程中型頁面，沒有開始前與結束後狀態

#### 設計

1. 在 `app.js` 加入旅程設定與狀態判斷函式。
2. 在 `index.html` 補結構節點：
   - 倒數區塊容器
   - 旅程中摘要區塊
   - 結束頁容器
3. 在 `styles.css` 新增兩組版面：
   - 開始前倒數 hero / countdown card
   - 結束頁 summary / revisit CTA
4. `active` 狀態下維持既有逐日行程、住宿、早餐與雨天切換內容。

#### 風險

- 目前 `app.js` 以單檔組裝內容為主，新增狀態判斷時要避免和既有 `renderTabs`、`renderDays` 等函式互相踩狀態。
- 解法是將狀態判斷放在初始化流程最前面，並明確控制哪些區塊在不同狀態下顯示或隱藏。

## 共用 PWA 策略

兩站都統一採用：

- 相對路徑 `./` 為基礎的 `manifest` 與 service worker 註冊方式
- 快取本站必要資源：
  - `./`
  - `./index.html`
  - `./manifest.webmanifest`
  - `./service-worker.js`
  - `./icons/icon.svg`
  - 各站 CSS / JS

快取策略採用：

- install 時預先 cache 核心殼層資源
- fetch 時先查 cache，再 fallback 到網路
- 離線時至少能打開站點殼層與主要靜態內容

不在本次引入更複雜的版本管理或 stale-while-revalidate 策略，以維持行為可預期。

## 測試與驗證設計

### 1. 檔案層驗證

- 檢查 `20251129` 的 `manifest`、`service-worker.js`、`icons` 是否存在
- 檢查 `20260530` 的新增狀態區塊與既有資源是否完整

### 2. HTTP 驗證

以本地靜態伺服器驗證以下 URL 回傳 `200`：

- `/20251129/`
- `/20251129/manifest.webmanifest`
- `/20251129/service-worker.js`
- `/20260530/`
- `/20260530/manifest.webmanifest`
- `/20260530/service-worker.js`

### 3. 狀態切換驗證

透過可注入或可覆蓋的目前時間值進行三種狀態驗證：

- 開始前：確認倒數頁出現
- 旅程中：確認主行程畫面出現
- 結束後：確認結束頁出現

若現有程式結構不利於單元測試，則提供一個明確的 query string 覆蓋參數，例如 `?previewDate=2025-11-28T12:00:00+08:00`，只用於本地驗證三種時間狀態。正式使用時仍以真實目前時間為準，覆蓋參數不影響一般使用者流程。

## 實作步驟

1. 盤點 `20251129` 內旅程開始與結束日期，寫入固定設定值。
2. 新增 `20251129` PWA 基礎資源。
3. 為 `20251129/index.html` 加入旅程狀態殼層與倒數/結束頁。
4. 為 `20260530` 加入同型狀態判斷與 UI 區塊。
5. 本地啟動靜態伺服器，驗證兩站資源與畫面。
6. 驗證 GitHub Pages 子目錄相容性後提交。

## 主要風險與對策

### 1. 舊頁面過大且為 inline Babel

風險：修改 `20251129/index.html` 容易發生小語法錯誤導致整頁無法載入。  
對策：只做必要外層包裝與最少插入點調整，避免重整整體程式結構。

### 2. 時區導致日期判斷錯誤

風險：旅遊當地時間與台灣時間不同時，若直接吃裝置本地時間，切換點可能不符合需求。  
對策：所有狀態判斷固定以 `Asia/Taipei` 為基準。

### 3. Service worker 更新快取殘留

風險：使用者已安裝舊版時，可能看到舊畫面。  
對策：更新 cache name 並清理舊 cache，確保新版本能接手。

## 成功標準

當以下條件成立，視為本次需求完成：

1. `20251129` 與 `20260530` 都可作為 PWA 安裝。
2. 兩站都會依日期自動切換 `countdown / active / ended`。
3. `20260530` 新增開始倒數與結束頁，且原本旅程中內容可正常運作。
4. `20251129` 保留原本主體內容，同時補齊 PWA 與狀態頁能力。
5. 在 GitHub Pages 子目錄下仍可正常載入。
