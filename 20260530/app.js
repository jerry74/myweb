const mapUrl = (query) => `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}`;

const guideLinks = {
  kokusai: "https://edgechen.photography/kokusai-dori/",
  americanVillage: "https://yusuke.com.tw/blog/post/okinawa-american-village",
  aquarium: "https://okinawa.letsgojp.com/archives/17071/",
  kouri: "https://www.jeepe.jp/zh_TW/articles/kouri-island-travel-guide-1477",
  neoPark: "https://twobunny.tw/neo-park/",
  okinawaWorld: "https://okinawa.letsgojp.com/archives/757370/",
  chinen: "https://mimihan.tw/chinenmisaki-park/",
  costco: "https://ksk.tw/okinawa-costco/",
  steak88: "https://twobunny.tw/steak-house-88/",
  sandsDiner: "https://twobunny.tw/sands-diner/",
  yataimura: "https://mimigo.tw/okinawa-yatai/",
  potama: "https://www.gltjp.com/zh-hant/article/item/21034/",
  kapuka: "https://fupo.tw/blog/post/wagyu-cafe-kapuka",
  califKitchen: "https://gogojp.tw/the-calif-kitchen-r/",
  hamaya: "https://mimigo.tw/okinawa-americanvillage/",
  aeonNago: "https://world.aeon-ryukyu.jp/en/store/aeon/aeon_nago/",
  matsuKominka: "https://twobunny.tw/matsu-no-kominka/",
  nagoSteak: "https://www.tripadvisor.com/Restaurant_Review-g1023465-d15710026-Reviews-Nago_Steak-Nago_Okinawa_Prefecture_Kyushu.html",
  flipper: "https://www.tripadvisor.com/Restaurant_Review-g1023465-d1179034-Reviews-Restaurant_Flipper-Nago_Okinawa_Prefecture_Kyushu.html",
  hamanoya: "https://mimihan.tw/hamanoya/",
  kinjichi: "https://tw.ecob.okinawa/okinawa-noodle-kinchichi-onna-tw/",
  shogunBurger: "https://www.markting.com.tw/577/",
  garlicShrimp: "https://www.markting.com.tw/564/",
  konazu: "https://www.google.com/maps/search/?api=1&query=Konazu+Coffee+Naha+Shintoshin",
  kurukuma: "https://rocky.tw/cafe-kurukuma/",
  yabusachi: "https://www.totalokinawa.com/cafe-yabusachi/",
};

const foodLinks = {
  nahaDinner: [["牛排館88地圖", mapUrl("Steak House 88 Kokusai Dori")], ["牛排館88介紹", guideLinks.steak88], ["Sand's 地圖", mapUrl("Sand's Diner Naha")], ["Sand's 介紹", guideLinks.sandsDiner], ["屋台村地圖", mapUrl("Kokusai Dori Yatai Mura")], ["屋台村介紹", guideLinks.yataimura]],
  americanLunch: [["Kapuka 地圖", mapUrl("WaGyu Cafe Kapuka")], ["Kapuka 介紹", guideLinks.kapuka], ["加州廚房地圖", mapUrl("THE CALIF KITCHEN Okinawa")], ["加州廚房介紹", guideLinks.califKitchen], ["濱屋地圖", mapUrl("Hamaya Soba Okinawa")], ["濱屋介紹", guideLinks.hamaya]],
  aeonNago: [["AEON 名護地圖", mapUrl("AEON Nago Shopping Center")], ["官方資訊", guideLinks.aeonNago]],
  nagoDinner: [["松之古民家地圖", mapUrl("Matsu no Kominka Nago")], ["松之古民家介紹", guideLinks.matsuKominka], ["名護牛排地圖", mapUrl("Nago Steak Okinawa")], ["名護牛排評價", guideLinks.nagoSteak], ["Flipper 地圖", mapUrl("Restaurant Flipper Nago")], ["Flipper 評價", guideLinks.flipper]],
  onnaDinner: [["濱之家地圖", mapUrl("Hamanoya Onna Okinawa")], ["濱之家介紹", guideLinks.hamanoya], ["金月地圖", mapUrl("Kinjichi Soba Onna")], ["金月介紹", guideLinks.kinjichi], ["將軍漢堡地圖", mapUrl("SHOGUN BURGER Onna")], ["將軍漢堡介紹", guideLinks.shogunBurger]],
  resortLunch: [["蒜香蝦地圖", mapUrl("THE GARLIC SHRIMP Okinawa")], ["蒜香蝦介紹", guideLinks.garlicShrimp], ["金月地圖", mapUrl("Kinjichi Soba Onna")], ["金月介紹", guideLinks.kinjichi]],
  americanDinner: [["加州廚房地圖", mapUrl("THE CALIF KITCHEN Okinawa")], ["加州廚房介紹", guideLinks.califKitchen], ["Kapuka 地圖", mapUrl("WaGyu Cafe Kapuka")], ["Kapuka 介紹", guideLinks.kapuka]],
  nahaShoppingLunch: [["Konazu 地圖", mapUrl("Konazu Coffee Naha Shintoshin")], ["Konazu 參考", guideLinks.konazu]],
  nahaShoppingDinner: [["屋台村地圖", mapUrl("Kokusai Dori Yatai Mura")], ["屋台村介紹", guideLinks.yataimura], ["牛排館88地圖", mapUrl("Steak House 88 Kokusai Dori")], ["牛排館88介紹", guideLinks.steak88], ["Potama 地圖", mapUrl("Potama Makishi Market")], ["Potama 介紹", guideLinks.potama]],
  southLunch: [["Kurukuma 地圖", mapUrl("Cafe Kurukuma Okinawa")], ["Kurukuma 介紹", guideLinks.kurukuma], ["Yabusachi 地圖", mapUrl("Cafe Yabusachi Okinawa")], ["Yabusachi 介紹", guideLinks.yabusachi]],
  costcoDinner: [["Costco 地圖", mapUrl("Costco Okinawa Nanjo Warehouse")], ["Costco 遊記", guideLinks.costco]],
};

const item = (time, text, links = []) => ({
  time,
  text,
  links,
});

const foodItem = (title, text, links = []) => ({ title, text, links });

const days = [
  {
    date: "5/30",
    weekday: "六",
    title: "抵達那霸，不租車",
    stay: "那霸市區",
    tags: ["food"],
    rainPlan: "這天不排戶外遠點；若下雨，直接縮短國際通散步，改成飯店休息與便利店採買。",
    schedule: [
      item("中午", "抵達那霸機場（Naha Airport / 那覇空港），進市區入住休息。", [["Google Maps", mapUrl("Naha Airport")]], "naha-airport"),
      item("傍晚", "國際通（Kokusai Street / 国際通り）散步、晚餐、採買隔天早餐。", [["地圖", mapUrl("Kokusai Dori Naha")], ["中文攻略", guideLinks.kokusai]], "kokusai-dori", { weatherSensitive: true }),
      item("晚上", "平和通商店街（Heiwa-dori / 平和通り）短逛，早點回飯店。", [["地圖", mapUrl("Heiwa dori Naha")]], "heiwa-dori", { weatherSensitive: true }),
    ],
    food: [
      foodItem("早餐", "飛機上或機場簡單吃。"),
      foodItem("午餐", "抵達後以機場或那霸市區簡餐為主。"),
      foodItem("晚餐", "牛排館 88 國際通店、山地沙丘餐酒館或國際通屋台村。", foodLinks.nahaDinner),
      foodItem("採買", "便利店買飯糰、麵包、優格、牛奶、水果。"),
    ],
  },
  {
    date: "5/31",
    weekday: "日",
    title: "取車，美國村，北上名護",
    stay: "名護／幸喜",
    tags: ["drive", "rain", "food"],
    rainPlan: "小雨照去美國村，以餐廳與室內店鋪為主；大雨就縮短或取消，把美國村移到 6/3 傍晚補。",
    schedule: [
      item("上午", "退房後在那霸取車，開始自駕。"),
      item("中午", "美國村（American Village / アメリカンビレッジ）午餐與逛街。", [["地圖", mapUrl("American Village Okinawa")], ["中文攻略", guideLinks.americanVillage]], "american-village", { weatherSensitive: true }),
      item("下午", "視天氣散步、購物，之後北上名護／幸喜入住。", [["幸喜海灘", mapUrl("Kouki Beach Nago Okinawa")]], "kouki-beach"),
      item("雨天", "美國村縮短成吃飯短停；若雨太大，移到 6/3 傍晚補。"),
    ],
    food: [
      foodItem("早餐", "前一晚便利店早餐。"),
      foodItem("午餐", "和牛咖啡 Kapuka、加州廚房、濱屋沖繩麵。", foodLinks.americanLunch),
      foodItem("晚餐", "AEON 名護購物中心或名護市區簡餐，順便補貨。", foodLinks.aeonNago),
    ],
  },
  {
    date: "6/1",
    weekday: "一",
    title: "水族館與海洋博公園",
    stay: "名護／幸喜",
    tags: ["drive", "rain", "food"],
    rainPlan: "這天是雨天友善日；下雨時保留水族館，縮短海洋博公園戶外散步。",
    schedule: [
      item("上午", "沖繩美麗海水族館（Okinawa Churaumi Aquarium / 沖縄美ら海水族館），停留 2.5 到 3 小時。", [["地圖", mapUrl("Okinawa Churaumi Aquarium")], ["中文攻略", guideLinks.aquarium]], "churaumi-aquarium"),
      item("中午", "海洋博公園（Ocean Expo Park / 海洋博公園）周邊午餐。", [["地圖", mapUrl("Ocean Expo Park Okinawa")]], "ocean-expo-park"),
      item("下午", "海洋博公園散步，雨天縮短戶外，水族館照跑。", [], "ocean-expo-park", { optional: true, weatherSensitive: true }),
      item("晚上", "回名護／幸喜晚餐與休息。"),
    ],
    food: [
      foodItem("早餐", "前一晚採買。"),
      foodItem("午餐", "園區或周邊簡單吃。"),
      foodItem("晚餐", "松之古民家、名護牛排、法蘭彼餐廳，或 AEON 名護。", foodLinks.nagoDinner),
    ],
  },
  {
    date: "6/2",
    weekday: "二",
    title: "古宇利島，Neo Park，南下殘波岬",
    stay: "讀谷／殘波岬",
    tags: ["drive", "rain", "food"],
    rainPlan: "古宇利島最吃天氣；大雨取消古宇利，改以 Neo Park 為主，提早入住飯店。",
    schedule: [
      item("上午", "古宇利島（Kouri Island / 古宇利島），晴天停留 1.5 到 2 小時。", [["地圖", mapUrl("Kouri Island Okinawa")], ["中文攻略", guideLinks.kouri]], "kouri-island", { weatherSensitive: true }),
      item("中午", "古宇利或名護沿線午餐。"),
      item("下午", "名護動植物園（Neo Park Okinawa / ネオパークオキナワ），再南下入住殘波岬。", [["地圖", mapUrl("Neo Park Okinawa")], ["中文攻略", guideLinks.neoPark]], "neo-park"),
      item("雨天", "古宇利島取消或短停；Neo Park 保留，提早入住飯店。"),
    ],
    food: [
      foodItem("早餐", "前一晚採買。"),
      foodItem("午餐", "北部簡餐、沖繩麵或咖啡輕食。"),
      foodItem("晚餐", "濱之家海鮮料理、金月沖繩麵、將軍漢堡恩納村店。", foodLinks.onnaDinner),
    ],
  },
  {
    date: "6/3",
    weekday: "三",
    title: "渡假飯店放空，美國村補位",
    stay: "讀谷／殘波岬",
    tags: ["rain", "food"],
    rainPlan: "雨天以飯店室內設施、餐廳、休息為主；只有 5/31 沒去成美國村時才補位。",
    schedule: [
      item("上午", "飯店泳池、沙灘、親子放空。", [["飯店地圖", mapUrl("Grand Mercure Okinawa Cape Zanpa Resort")]], "grand-mercure-zanpa"),
      item("中午", "飯店內或讀谷／恩納周邊午餐。"),
      item("下午", "回房午睡或繼續飯店設施。"),
      item("傍晚", "若 5/31 美國村受雨影響，這天補美國村；否則維持純放鬆。", [["美國村", mapUrl("American Village Okinawa")]], "american-village", { optional: true, weatherSensitive: true }),
    ],
    food: [
      foodItem("早餐", "前一晚便利店或飯店附近採買。"),
      foodItem("午餐", "蒜香蝦餐廳、金月沖繩麵，或飯店內解決。", foodLinks.resortLunch),
      foodItem("晚餐", "飯店餐廳；若補美國村，選加州廚房或和牛咖啡 Kapuka。", foodLinks.americanDinner),
    ],
  },
  {
    date: "6/4",
    weekday: "四",
    title: "回那霸，市區採買",
    stay: "那霸市區",
    tags: ["drive", "food"],
    rainPlan: "市區日受雨影響小；下雨就選新都心、DFS、商場、餐廳，縮短國際通戶外步行。",
    schedule: [
      item("上午", "退房後自駕回那霸，飯店寄放行李或入住。"),
      item("下午", "新都心（Omoromachi / おもろまち）、DFS 沖繩或國際通擇一。", [["新都心", mapUrl("Omoromachi Naha")], ["DFS", mapUrl("T Galleria Okinawa by DFS")], ["國際通", mapUrl("Kokusai Dori Naha")]], "naha-shopping", { weatherSensitive: true }),
      item("晚上", "那霸市區晚餐、採買、整理行李。"),
    ],
    food: [
      foodItem("早餐", "前一晚採買。"),
      foodItem("午餐", "可納滋咖啡新都心店或商場簡餐。", foodLinks.nahaShoppingLunch),
      foodItem("晚餐", "國際通屋台村、牛排館 88、豬肉蛋飯糰牧志市場店。", foodLinks.nahaShoppingDinner),
    ],
  },
  {
    date: "6/5",
    weekday: "五",
    title: "南部收尾，文化王國，知念岬，Costco",
    stay: "那霸市區",
    tags: ["drive", "rain", "food"],
    rainPlan: "小雨保留文化王國與 Costco，知念岬縮短；大雨取消知念岬，文化王國只跑玉泉洞與室內區。",
    schedule: [
      item("上午", "沖繩世界文化王國（Okinawa World / おきなわワールド），停留 2.5 到 4 小時。", [["地圖", mapUrl("Okinawa World")], ["中文攻略", guideLinks.okinawaWorld]], "okinawa-world"),
      item("中午", "南城市景觀午餐。"),
      item("下午", "晴天短停知念岬公園（Cape Chinen Park / 知念岬公園），再去 Costco。", [["知念岬", mapUrl("Cape Chinen Park")], ["知念攻略", guideLinks.chinen], ["Costco", mapUrl("Costco Okinawa Nanjo Warehouse")], ["Costco 遊記", guideLinks.costco]], "chinen-cape", { weatherSensitive: true }),
      item("下午後段", "好市多沖繩南城倉庫店採買晚餐與隔天早餐。", [["Costco", mapUrl("Costco Okinawa Nanjo Warehouse")], ["Costco 遊記", guideLinks.costco]], "costco-nanjo"),
      item("雨天", "知念岬取消；文化王國縮短成玉泉洞與室內區；Costco 保留。"),
    ],
    food: [
      foodItem("早餐", "前一晚便利店早餐。"),
      foodItem("午餐", "海景香料餐廳 Kurukuma 或海景咖啡 Yabusachi。", foodLinks.southLunch),
      foodItem("晚餐", "Costco 熟食：壽司、烤雞、沙拉、Pizza、麵包。", foodLinks.costcoDinner),
    ],
  },
  {
    date: "6/6",
    weekday: "六",
    title: "清晨回台北",
    stay: "回程",
    tags: ["food"],
    rainPlan: "早班機日不安排景點；下雨只影響出門時間，建議更早出發。",
    schedule: [
      item("清晨", "單軌或短程交通前往那霸機場（Naha Airport / 那覇空港）。", [["地圖", mapUrl("Naha Airport")]], "naha-airport"),
      item("08:30", "NU301 那霸起飛。"),
      item("09:05", "抵達桃園機場。"),
    ],
    food: [
      foodItem("早餐", "Costco 麵包、便利店飯糰、牛奶，快速出門。"),
    ],
  },
];

const stays = [
  ["5/30", "東急 Stay 沖繩那霸（Tokyu Stay Okinawa Naha / 東急ステイ沖縄那覇）", mapUrl("Tokyu Stay Okinawa Naha")],
  ["5/31-6/1", "名護／幸喜住宿（Nago / Kouki / 名護・幸喜）", mapUrl("Kouki Beach Nago Okinawa")],
  ["6/2-6/3", "沖繩殘波岬美爵度假酒店（Grand Mercure Okinawa Cape Zanpa Resort / グランドメルキュール沖縄残波岬リゾート）", mapUrl("Grand Mercure Okinawa Cape Zanpa Resort")],
  ["6/4-6/5", "那霸單軌沿線，建議旭橋／縣廳前／小祿／赤嶺", mapUrl("Asahibashi Station Naha")],
];

const breakfasts = [
  ["5/31", "5/30 那霸便利店買好。"],
  ["6/1", "5/31 AEON 名護或便利店買好。"],
  ["6/2", "6/1 名護超市或便利店買好。"],
  ["6/3", "6/2 恩納／讀谷周邊便利店買好。"],
  ["6/4", "6/3 恩納／讀谷周邊便利店買好。"],
  ["6/5", "6/4 那霸市區便利店買好。"],
  ["6/6", "6/5 Costco 或便利店留好。"],
];

const rainRules = [
  ["5/31", "美國村縮短或取消，改到 6/3 傍晚補。"],
  ["6/2", "古宇利島取消或短停，Neo Park 保留。"],
  ["6/3", "飯店室內設施與餐廳為主，美國村只作補位。"],
  ["6/5", "知念岬取消，文化王國縮短，Costco 保留。"],
];

const dayList = document.querySelector("#dayList");
const dayTabs = document.querySelector("#dayTabs");
const stayList = document.querySelector("#stayList");
const breakfastList = document.querySelector("#breakfastList");
const rainList = document.querySelector("#rainList");
const searchInput = document.querySelector("#searchInput");
const activeDaySummary = document.querySelector("#activeDaySummary");
let activeDayIndex = 0;

function linkPills(links) {
  if (!links.length) return "";
  return `<div class="link-row">${links.map(([label, url]) => `<a class="link-pill" href="${url}" target="_blank" rel="noreferrer">${label}</a>`).join("")}</div>`;
}

function renderDays() {
  const query = searchInput.value.trim().toLowerCase();
  dayList.innerHTML = "";

  const visibleDays = query
    ? days.filter((day) => JSON.stringify(day).toLowerCase().includes(query))
    : [days[activeDayIndex]];

  visibleDays
    .forEach((day) => {
      const card = document.createElement("article");
      card.className = "day-card";
      card.innerHTML = `
        <div class="day-top">
          <div class="date-badge">
            <span class="tag">${day.weekday}</span>
            <strong>${day.date}</strong>
          </div>
          <div>
            <h3>${day.title}</h3>
            <span class="compact-meta">住宿：${day.stay}</span>
          </div>
        </div>
        <div class="day-body">
          <div class="schedule">
            <div class="rain-note">
              <strong>雨天切換</strong>
              <p>${day.rainPlan}</p>
            </div>
            ${day.schedule.map((entry) => `
              <div class="time-row">
                <b>${entry.time}</b>
                <div>
                  <div class="row-copy">
                    <span>${entry.text}</span>
                  </div>
                  ${linkPills(entry.links)}
                </div>
              </div>
            `).join("")}
          </div>
          <aside class="food-panel">
            <h3>三餐與採買</h3>
            <div class="food-list">
              ${day.food.map((entry) => `
                <div class="food-item">
                  <strong>${entry.title}</strong>
                  <p>${entry.text}</p>
                  ${linkPills(entry.links)}
                </div>
              `).join("")}
            </div>
          </aside>
        </div>
      `;
      dayList.appendChild(card);
    });
}

function renderTabs() {
  dayTabs.innerHTML = days.map((day, index) => `
    <button
      class="day-tab ${index === activeDayIndex ? "active" : ""}"
      type="button"
      role="tab"
      aria-selected="${index === activeDayIndex}"
      data-day-index="${index}"
    >
      <span class="day-label">Day ${index + 1}</span>
      <strong>${day.date}</strong>
      <span>${day.weekday}｜${day.stay}</span>
    </button>
  `).join("");

  const activeDay = days[activeDayIndex];
  activeDaySummary.innerHTML = `
    <span>Day ${activeDayIndex + 1} / ${days.length}</span>
    <strong>${activeDay.date}（${activeDay.weekday}）${activeDay.title}</strong>
    <small>住宿：${activeDay.stay}</small>
  `;

  dayTabs.querySelectorAll(".day-tab").forEach((button) => {
    button.addEventListener("click", () => {
      activeDayIndex = Number(button.dataset.dayIndex);
      searchInput.value = "";
      renderTabs();
      renderDays();
    });
  });
}

function renderCompactLists() {
  stayList.innerHTML = stays.map(([date, text, url]) => `
    <div class="compact-item">
      <span class="compact-meta">${date}</span>
      <strong>${text}</strong>
      <a href="${url}" target="_blank" rel="noreferrer">Google Maps</a>
    </div>
  `).join("");

  breakfastList.innerHTML = breakfasts.map(([date, text]) => `
    <div class="compact-item">
      <span class="compact-meta">${date}</span>
      <strong>${text}</strong>
    </div>
  `).join("");

  rainList.innerHTML = rainRules.map(([date, text]) => `
    <article class="rain-card">
      <strong>${date}</strong>
      <p>${text}</p>
    </article>
  `).join("");
}

searchInput.addEventListener("input", renderDays);

let deferredPrompt;
const installButton = document.querySelector("#installButton");

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredPrompt = event;
  installButton.hidden = false;
});

installButton.addEventListener("click", async () => {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  await deferredPrompt.userChoice;
  deferredPrompt = null;
  installButton.hidden = true;
});

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./service-worker.js");
  });
}

renderCompactLists();
renderTabs();
renderDays();
