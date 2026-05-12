# Google My Maps 匯入說明

建議匯入兩份檔案：

1. `okinawa_mymaps_stays.csv`
   - 用途：看整段住宿節點與住宿移動順序

2. `okinawa_mymaps_daily.csv`
   - 用途：看每天晚上住哪裡

## 匯入步驟

1. 開啟 Google My Maps：
   - https://www.google.com/mymaps
2. 建立新地圖
3. 在左側圖層按 `匯入`
4. 上傳：
   - `C:\Users\jerry\OneDrive\文件\New project\okinawa_mymaps_stays.csv`
5. 選擇定位欄位：
   - `Address`
6. 選擇標題欄位：
   - `Name` 或 `Stay Dates`
7. 再新增第二個圖層，匯入：
   - `C:\Users\jerry\OneDrive\文件\New project\okinawa_mymaps_daily.csv`
8. 第二層同樣使用：
   - 定位欄位：`Address`
   - 標題欄位：`Date`

## 建議圖層用途

- 圖層 1：`住宿節點`
  - 看住宿換點順序：那霸 -> 名護／幸喜 -> 讀谷／殘波岬 -> 那霸

- 圖層 2：`每日住宿`
  - 看每天實際住宿位置

## 建議命名

- 地圖名稱：`2026 沖繩住宿地圖`
- 圖層一：`住宿節點`
- 圖層二：`每日住宿`
