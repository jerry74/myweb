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

let days = [
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

let breakfasts = [
  ["5/31", "5/30 那霸便利店買好。"],
  ["6/1", "5/31 AEON 名護或便利店買好。"],
  ["6/2", "6/1 名護超市或便利店買好。"],
  ["6/3", "6/2 恩納／讀谷周邊便利店買好。"],
  ["6/4", "6/3 恩納／讀谷周邊便利店買好。"],
  ["6/5", "6/4 那霸市區便利店買好。"],
  ["6/6", "6/5 Costco 或便利店留好。"],
];

let rainRules = [
  ["5/31", "美國村縮短或取消，改到 6/3 傍晚補。"],
  ["6/2", "古宇利島取消或短停，Neo Park 保留。"],
  ["6/3", "飯店室內設施與餐廳為主，美國村只作補位。"],
  ["6/5", "知念岬取消，文化王國縮短，Costco 保留。"],
];

let breakfastMap = new Map(breakfasts);
let stayDetailsMap = new Map([
  ["5/30", {
    name: "東急 Stay 沖繩那霸（Tokyu Stay Okinawa Naha / 東急ステイ沖縄那覇）",
    mapUrl: mapUrl("Tokyu Stay Okinawa Naha"),
  }],
  ["5/31", {
    name: "名護／幸喜住宿（Nago / Kouki / 名護・幸喜）",
    mapUrl: mapUrl("Kouki Beach Nago Okinawa"),
  }],
  ["6/1", {
    name: "名護／幸喜住宿（Nago / Kouki / 名護・幸喜）",
    mapUrl: mapUrl("Kouki Beach Nago Okinawa"),
  }],
  ["6/2", {
    name: "沖繩殘波岬美爵度假酒店（Grand Mercure Okinawa Cape Zanpa Resort / グランドメルキュール沖縄残波岬リゾート）",
    mapUrl: mapUrl("Grand Mercure Okinawa Cape Zanpa Resort"),
  }],
  ["6/3", {
    name: "沖繩殘波岬美爵度假酒店（Grand Mercure Okinawa Cape Zanpa Resort / グランドメルキュール沖縄残波岬リゾート）",
    mapUrl: mapUrl("Grand Mercure Okinawa Cape Zanpa Resort"),
  }],
  ["6/4", {
    name: "那霸單軌沿線住宿（建議旭橋／縣廳前／小祿／赤嶺）",
    mapUrl: mapUrl("Asahibashi Station Naha"),
  }],
  ["6/5", {
    name: "那霸單軌沿線住宿（建議旭橋／縣廳前／小祿／赤嶺）",
    mapUrl: mapUrl("Asahibashi Station Naha"),
  }],
  ["6/6", {
    name: "回程日",
    mapUrl: mapUrl("Naha Airport"),
  }],
]);
let tripConfig = {
  startAt: "2026-05-30T00:00:00+08:00",
  departureAt: "2026-05-30T12:00:00+08:00",
  endAt: "2026-06-06T23:59:59+08:00",
};

const dayList = document.querySelector("#dayList");
const dayTabs = document.querySelector("#dayTabs");
const todayHeroTitle = document.querySelector("#todayHeroTitle");
const todayHeroLead = document.querySelector("#todayHeroLead");
const todayHeroMeta = document.querySelector("#todayHeroMeta");
const todayHeroNextStop = document.querySelector("#todayHeroNextStop");
const tripSummaryCard = document.querySelector("#tripSummaryCard");
const mealCard = document.querySelector("#mealCard");
const rainDecisionCard = document.querySelector("#rainDecisionCard");
const shoppingBackupCard = document.querySelector("#shoppingBackupCard");
const todayNextStopAction = document.querySelector("#todayNextStopAction");
const tripDateRange = document.querySelector("#tripDateRange");
const countdownView = document.querySelector("#countdownView");
const endedView = document.querySelector("#endedView");
const appHeader = document.querySelector("#appHeader");
const appContent = document.querySelector("#appContent");
const bottomTabs = document.querySelector("#bottomTabs");
const countdownDays = document.querySelector("#countdownDays");
const countdownHours = document.querySelector("#countdownHours");
const countdownMinutes = document.querySelector("#countdownMinutes");
const previewTripButton = document.querySelector("#previewTripButton");
const revisitTripButton = document.querySelector("#revisitTripButton");
let activeDayIndex = 0;
let forceShowItinerary = false;

function linkPills(links) {
  if (!links.length) return "";
  return `<div class="link-row">${links.map(([label, url]) => `<a class="link-pill" href="${url}" target="_blank" rel="noreferrer">${label}</a>`).join("")}</div>`;
}

function isMapLink(label) {
  return label.includes("地圖") || label.includes("Google Maps") || label === "Costco";
}

function mealLinkType(label) {
  return isMapLink(label) ? "map" : "reference";
}

function mealPlaceName(label, fallbackName = "相關資訊") {
  return label
    .replace(/Google Maps/g, fallbackName)
    .replace(/地圖|介紹|評價|參考|遊記|官方資訊/g, "")
    .trim() || fallbackName;
}

function mealLinkPill([label, url]) {
  const type = mealLinkType(label);
  const buttonLabel = type === "map" ? "地圖" : label.replace(/^.+?(介紹|評價|參考|遊記|官方資訊)$/, "$1");

  return `<a class="link-pill meal-link-pill ${type === "map" ? "map-link" : "reference-link"}" href="${url}" target="_blank" rel="noreferrer">${buttonLabel}</a>`;
}

function groupedMealLinks(links) {
  if (!links.length) return "";
  const places = [];

  links.forEach((link) => {
    const [label] = link;
    const placeName = mealPlaceName(label, places[places.length - 1]?.name);
    let place = places.find((entry) => entry.name === placeName);

    if (!place) {
      place = { name: placeName, map: null, reference: null, extras: [] };
      places.push(place);
    }

    const type = mealLinkType(label);
    if (type === "map" && !place.map) {
      place.map = link;
    } else if (type === "reference" && !place.reference) {
      place.reference = link;
    } else {
      place.extras.push(link);
    }
  });

  return `
    <div class="meal-link-places">
      ${places.map((place) => `
        <div class="meal-link-place">
          <span class="meal-link-place-name">${place.name}</span>
          <div class="meal-link-actions">
            ${place.map ? mealLinkPill(place.map) : ""}
            ${place.reference ? mealLinkPill(place.reference) : ""}
            ${place.extras.map((link) => mealLinkPill(link)).join("")}
          </div>
        </div>
      `).join("")}
    </div>
  `;
}

function getEntryMeta(entry) {
  const text = entry.text || "";
  const isWeatherSwitch = entry.time.includes("雨天") || text.includes("若雨") || text.includes("下雨") || text.includes("取消");
  const isOptional = text.includes("視天氣") || text.includes("若 ") || text.includes("若雨") || text.includes("短停") || text.includes("補");

  return {
    weatherSensitive: isWeatherSwitch || text.includes("戶外") || text.includes("景觀") || text.includes("散步"),
    optional: isOptional,
    isWeatherSwitch,
  };
}

function getPreviewDate() {
  const value = new URLSearchParams(window.location.search).get("previewDate");
  const previewDate = value ? new Date(value) : null;
  return previewDate && !Number.isNaN(previewDate.getTime()) ? previewDate : null;
}

function getCurrentDate() {
  return getPreviewDate() || new Date();
}

function getTripState(currentDate) {
  const start = new Date(tripConfig.startAt);
  const end = new Date(tripConfig.endAt);
  if (currentDate < start) return "countdown";
  if (currentDate > end) return "ended";
  return "active";
}

function getActiveTripDayIndex(currentDate) {
  const start = new Date(tripConfig.startAt);
  const day = Math.floor((currentDate - start) / (1000 * 60 * 60 * 24));
  return Math.min(Math.max(day, 0), days.length - 1);
}

function getCountdownParts(targetDate, currentDate) {
  const diff = Math.max(targetDate - currentDate, 0);
  return {
    days: Math.floor(diff / (1000 * 60 * 60 * 24)),
    hours: Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
    minutes: Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60)),
  };
}

function setHidden(element, hidden) {
  if (!element) return;
  element.classList.toggle("is-hidden", hidden);
}

function getEntryStartMinutes(entry) {
  const time = entry.time || "";
  const clockMatch = time.match(/^(\d{1,2}):(\d{2})$/);

  if (clockMatch) {
    return Number(clockMatch[1]) * 60 + Number(clockMatch[2]);
  }

  const timeSlots = [
    ["清晨", 5 * 60],
    ["上午", 9 * 60],
    ["中午", 12 * 60],
    ["下午後段", 16 * 60],
    ["下午", 14 * 60],
    ["傍晚", 17 * 60 + 30],
    ["晚上", 19 * 60],
  ];
  const matchedSlot = timeSlots.find(([label]) => time.includes(label));
  return matchedSlot ? matchedSlot[1] : null;
}

function getCurrentMinutes(currentDate) {
  return currentDate.getHours() * 60 + currentDate.getMinutes();
}

function getNavigableEntries(day) {
  return day.schedule
    .map((entry, index) => ({
      entry,
      index,
      startMinutes: getEntryStartMinutes(entry),
    }))
    .filter(({ startMinutes }) => startMinutes !== null)
    .sort((a, b) => a.startMinutes - b.startMinutes || a.index - b.index);
}

function getNextStopForCurrentTime(day, currentDate) {
  const timedEntries = getNavigableEntries(day);
  if (!timedEntries.length) return day.schedule[0];

  const nowMinutes = getCurrentMinutes(currentDate);
  const upcoming = timedEntries.find(({ startMinutes }) => startMinutes >= nowMinutes);
  return upcoming ? upcoming.entry : null;
}

function shouldUseTimeBasedNextStop(day, currentDate) {
  return getTripState(currentDate) === "active"
    && days.indexOf(day) === getActiveTripDayIndex(currentDate);
}

function getPlaceNameFromText(text) {
  return (text || "")
    .split(/[（(，,。]/)[0]
    .replace(/^(晴天短停|若.+補|視天氣|單軌或短程交通前往)/, "")
    .trim();
}

function getNavigationDestination(entry) {
  if (!entry || !entry.links?.length) return "查看行程細節";
  const [label, url] = entry.links[0];
  if (!url.startsWith("http")) return "查看行程細節";
  if (label.includes("地圖") || label.includes("Google Maps")) {
    return getPlaceNameFromText(entry.text) || label;
  }
  return label;
}

function getTimelineCards(day, currentDate = getCurrentDate()) {
  const nextStop = shouldUseTimeBasedNextStop(day, currentDate)
    ? getNextStopForCurrentTime(day, currentDate)
    : day.schedule[0];
  return day.schedule.map((entry, index) => {
    const meta = getEntryMeta(entry);
    const badges = [];

    if (entry === nextStop) {
      badges.push("下一步");
    }

    if (meta.isWeatherSwitch) {
      badges.push("雨天切換");
    } else if (meta.weatherSensitive) {
      badges.push("雨天敏感");
    }

    badges.push(meta.optional ? "可彈性調整" : "固定行程");

    return {
      ...entry,
      isNext: entry === nextStop,
      badges,
    };
  });
}

function getActiveDayViewModel() {
  const day = days[activeDayIndex];
  const timelineCards = getTimelineCards(day);
  const nextStop = timelineCards.find((entry) => entry.isNext) || null;

  return {
    dayNumber: activeDayIndex + 1,
    totalDays: days.length,
    dateLabel: `${day.date}（${day.weekday}）`,
    title: day.title,
    stay: day.stay,
    lead: `${day.date}（${day.weekday}）｜住宿：${day.stay}`,
    nextStop,
    navigationDestination: getNavigationDestination(nextStop),
  };
}

function getTodayMealViewModel(day) {
  return {
    entries: day.food,
  };
}

function getTripSummaryViewModel(day) {
  const stayDetails = stayDetailsMap.get(day.date);

  return {
    dayLabel: `Day ${activeDayIndex + 1} / ${days.length}`,
    stay: stayDetails?.name || day.stay,
    remainingDays: Math.max(days.length - activeDayIndex - 1, 0),
    transferLabel: day.tags.includes("drive") ? "今天有移動" : "今天定點活動",
  };
}

function getRainDecisionViewModel(day) {
  const tags = [];

  if (day.tags.includes("rain")) {
    tags.push("保留部分室內點", "戶外可取消", "視天氣延後");
  } else {
    tags.push("照原行程", "低天氣風險");
  }

  return {
    title: "雨天切換",
    summary: day.rainPlan,
    decisionTags: tags,
  };
}

function getShoppingBackupViewModel(day) {
  return day.shoppingBackup || [];
}

function getDaySupportDetails(day) {
  const stayDetails = stayDetailsMap.get(day.date);

  return {
    stay: day.stay,
    stayName: stayDetails?.name || day.stay,
    stayAddress: stayDetails?.address || "",
    stayPhone: stayDetails?.phone || "",
    stayMapUrl: stayDetails?.mapUrl || mapUrl(day.stay),
    breakfast: breakfastMap.get(day.date) || "依照當天住宿與前一站行程彈性準備早餐。",
  };
}

function renderTodayHero() {
  const model = getActiveDayViewModel();
  const nextStopLink = model.nextStop && model.nextStop.links.length ? model.nextStop.links[0][1] : "#todayTimeline";

  todayHeroTitle.textContent = model.title;
  todayHeroLead.textContent = model.lead;
  todayHeroMeta.innerHTML = `
    <span>Day ${model.dayNumber} / ${model.totalDays}</span>
    <strong>${model.dateLabel}</strong>
    <small>今天主題：${model.title}</small>
  `;
  todayHeroNextStop.innerHTML = `
    <span>下一站｜${model.nextStop ? model.nextStop.time : "自由調整"}</span>
    <strong>${model.nextStop ? model.nextStop.text : "今天自由調整"}</strong>
    <small>導航到：${model.navigationDestination}</small>
  `;
  todayHeroNextStop.classList.toggle("has-map-link", nextStopLink.startsWith("http"));
  todayNextStopAction.href = nextStopLink;
  todayNextStopAction.target = nextStopLink.startsWith("http") ? "_blank" : "_self";
  todayNextStopAction.rel = nextStopLink.startsWith("http") ? "noreferrer" : "";
}

function renderTripSummary() {
  const day = days[activeDayIndex];
  const model = getTripSummaryViewModel(day);

  tripSummaryCard.innerHTML = `
    <p class="eyebrow">Trip Summary</p>
    <h2>${model.dayLabel}</h2>
    <div class="summary-metrics">
      <div class="summary-item">
        <span>今天節奏</span>
        <strong>${model.transferLabel}</strong>
      </div>
      <div class="summary-item">
        <span>目前住宿</span>
        <strong>${model.stay}</strong>
      </div>
      <div class="summary-item">
        <span>距離返程</span>
        <strong>${model.remainingDays} 天</strong>
      </div>
    </div>
  `;
}

function renderSupportCards() {
  const day = days[activeDayIndex];
  const mealModel = getTodayMealViewModel(day);
  const rainModel = getRainDecisionViewModel(day);
  const shoppingModel = getShoppingBackupViewModel(day);

  mealCard.innerHTML = `
    <p class="eyebrow">Meals & Supply</p>
    <h2>今天吃什麼</h2>
    <div class="support-stack">
      ${mealModel.entries.map((entry) => `
        <div class="support-item">
          <span class="compact-meta">${entry.title}</span>
          <strong>${entry.text}</strong>
          ${groupedMealLinks(entry.links)}
        </div>
      `).join("")}
    </div>
  `;

  rainDecisionCard.innerHTML = `
    <p class="eyebrow">Weather Switch</p>
    <h2>${rainModel.title}</h2>
    <p class="support-copy">${rainModel.summary}</p>
    <div class="decision-tags">
      ${rainModel.decisionTags.map((tag) => `<span class="decision-tag">${tag}</span>`).join("")}
    </div>
  `;

  shoppingBackupCard.innerHTML = `
    <p class="eyebrow">Shopping Backup</p>
    <h2>購物備案</h2>
    ${shoppingModel.length ? `
      <div class="support-stack">
        ${shoppingModel.map((entry) => `
          <div class="support-item shopping-support-item">
            <div class="shopping-support-top">
              <strong>${entry.name}</strong>
              <div class="shopping-tag-row">
                ${(entry.tags || []).map((tag) => `<span class="shopping-tag">${tag}</span>`).join("")}
              </div>
            </div>
            <p class="support-copy">${entry.note || ""}</p>
            ${linkPills(entry.links || [])}
          </div>
        `).join("")}
      </div>
    ` : `
      <p class="support-copy">這一天沒有特別整理大型商場備案，維持主行程或附近便利店採買即可。</p>
    `}
  `;
}

function renderDays() {
  const visibleDays = [days[activeDayIndex]];

  dayList.innerHTML = visibleDays.map((day) => `
    <article class="timeline-day">
      <header class="timeline-day-header">
        <div>
          <p class="eyebrow">Day Focus</p>
          <h3>${day.date}（${day.weekday}）${day.title}</h3>
          <p class="compact-meta">住宿：${day.stay}</p>
        </div>
      </header>
      <div class="day-support-strip">
        <div class="day-support-card">
          <span class="compact-meta">今晚住宿</span>
          ${(() => {
            const details = getDaySupportDetails(day);
            return `
              <strong>${details.stayName}</strong>
              ${details.stayAddress ? `<small>${details.stayAddress}</small>` : ""}
              ${details.stayPhone ? `<small>${details.stayPhone}</small>` : ""}
              <a class="support-link" href="${details.stayMapUrl}" target="_blank" rel="noreferrer">Google Maps</a>
            `;
          })()}
        </div>
        <div class="day-support-card">
          <span class="compact-meta">早餐準備</span>
          <strong>${getDaySupportDetails(day).breakfast}</strong>
        </div>
      </div>
      ${day.shoppingBackup?.length ? `
        <section class="shopping-backup-panel" aria-label="購物備案">
          <span class="compact-meta">購物備案</span>
          <div class="shopping-backup-grid">
            ${day.shoppingBackup.map((entry) => `
              <div class="shopping-backup-item">
                <strong>${entry.name}</strong>
              </div>
            `).join("")}
          </div>
        </section>
      ` : ""}
      <div class="timeline-cards">
        ${getTimelineCards(day).map((entry) => `
          <section class="timeline-card ${entry.isNext ? "is-next" : ""}">
            <div class="timeline-card-top">
              <b>${entry.time}</b>
              <div class="timeline-badges">
                ${entry.badges.map((badge) => `<span class="timeline-badge">${badge}</span>`).join("")}
              </div>
            </div>
            <p>${entry.text}</p>
            ${linkPills(entry.links)}
          </section>
        `).join("")}
      </div>
    </article>
  `).join("");
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
      <span>${day.weekday}｜${day.title}</span>
    </button>
  `).join("");

  dayTabs.querySelectorAll(".day-tab").forEach((button) => {
    button.addEventListener("click", () => {
      activeDayIndex = Number(button.dataset.dayIndex);
      renderDashboard();
    });
  });

  scrollActiveDayTabIntoView();
}

function scrollActiveDayTabIntoView() {
  const activeTab = dayTabs.querySelector(".day-tab.active");
  if (!activeTab) return;
  activeTab.scrollIntoView({ block: "nearest", inline: "center" });
}

function renderDashboard() {
  renderTodayHero();
  renderTripSummary();
  renderSupportCards();
  renderTabs();
  renderDays();
}

let deferredPrompt;
const installButtons = document.querySelectorAll(".install-button");
const isIosDevice = /iPad|iPhone|iPod/.test(window.navigator.userAgent)
  || (window.navigator.platform === "MacIntel" && window.navigator.maxTouchPoints > 1);

function isStandaloneMode() {
  return window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
}

function updateInstallButtons() {
  const canUseInstallPrompt = Boolean(deferredPrompt) && !isIosDevice && !isStandaloneMode();
  installButtons.forEach((button) => {
    button.hidden = !canUseInstallPrompt;
  });
}

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredPrompt = event;
  updateInstallButtons();
});

installButtons.forEach((button) => {
  button.addEventListener("click", async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    await deferredPrompt.userChoice;
    deferredPrompt = null;
    updateInstallButtons();
  });
});

window.addEventListener("appinstalled", () => {
  deferredPrompt = null;
  updateInstallButtons();
});

updateInstallButtons();

const appUpdatePrompt = document.querySelector("#appUpdatePrompt");
const appUpdateButton = document.querySelector("#appUpdateButton");
let waitingServiceWorker = null;
let updateReloadRequested = false;

function showAppUpdatePrompt(worker) {
  waitingServiceWorker = worker;
  if (appUpdatePrompt) {
    appUpdatePrompt.hidden = false;
  }
}

if (appUpdateButton) {
  appUpdateButton.addEventListener("click", () => {
    if (!waitingServiceWorker) return;
    updateReloadRequested = true;
    waitingServiceWorker.postMessage({ type: "SKIP_WAITING" });
  });
}

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./service-worker.js").then((registration) => {
      if (registration.waiting && navigator.serviceWorker.controller) {
        showAppUpdatePrompt(registration.waiting);
      }

      registration.addEventListener("updatefound", () => {
        const installingWorker = registration.installing;
        if (!installingWorker) return;

        installingWorker.addEventListener("statechange", () => {
          if (installingWorker.state === "installed" && navigator.serviceWorker.controller) {
            showAppUpdatePrompt(installingWorker);
          }
        });
      });
    });
  });

  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (!updateReloadRequested) return;
    window.location.reload();
  });
}

async function loadGeneratedTripData() {
  try {
    const response = await fetch("./data.generated.json", { cache: "no-store" });
    if (!response.ok) return;
    const data = await response.json();
    const trip = data.trip || {};

    days = data.days || days;
    breakfasts = Object.entries(data.breakfasts || {});
    rainRules = Object.entries(data.rainRules || {});
    breakfastMap = new Map(breakfasts);
    stayDetailsMap = new Map(Object.entries(data.stays || {}));
    tripConfig = {
      startAt: trip.startAt || tripConfig.startAt,
      departureAt: trip.departureAt || tripConfig.departureAt,
      endAt: trip.endAt || tripConfig.endAt,
    };

    if (tripDateRange && trip.dateRange) {
      tripDateRange.textContent = trip.dateRange;
    }
  } catch (error) {
    console.warn("Using bundled trip fallback data.", error);
  }
}

function renderTripState() {
  const now = getCurrentDate();
  const state = getTripState(now);

  if (forceShowItinerary) {
    setHidden(countdownView, true);
    setHidden(endedView, true);
    setHidden(appHeader, false);
    setHidden(appContent, false);
    setHidden(bottomTabs, false);
    if (state === "ended") {
      activeDayIndex = days.length - 1;
    } else if (state === "countdown") {
      activeDayIndex = 0;
    }
    return;
  }

  setHidden(countdownView, state !== "countdown");
  setHidden(endedView, state !== "ended");
  setHidden(appHeader, state !== "active");
  setHidden(appContent, state !== "active");
  setHidden(bottomTabs, state !== "active");

  if (state === "countdown") {
    const parts = getCountdownParts(new Date(tripConfig.departureAt), now);
    countdownDays.textContent = parts.days;
    countdownHours.textContent = parts.hours;
    countdownMinutes.textContent = parts.minutes;
  }

  if (state === "active") {
    activeDayIndex = getActiveTripDayIndex(now);
  }

  if (state === "ended") {
    activeDayIndex = days.length - 1;
  }
}

function showItineraryFromStatePage(event) {
  event.preventDefault();
  forceShowItinerary = true;
  renderTripState();
  renderDashboard();
  const timeline = document.querySelector("#todayTimeline");
  if (timeline) {
    timeline.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

previewTripButton.addEventListener("click", showItineraryFromStatePage);
revisitTripButton.addEventListener("click", showItineraryFromStatePage);

async function initApp() {
  await loadGeneratedTripData();
  renderTripState();
  renderDashboard();
  setInterval(() => {
    renderTripState();
    if (!countdownView.classList.contains("is-hidden") || !endedView.classList.contains("is-hidden")) {
      return;
    }
    renderDashboard();
  }, 60000);
}

initApp();

