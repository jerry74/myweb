const fallbackData = window.TRIP_FALLBACK || null;

const elements = {
  tripName: document.querySelector("#tripName"),
  brandShortName: document.querySelector("#brandShortName"),
  tripSummary: document.querySelector("#tripSummary"),
  tripDateRange: document.querySelector("#tripDateRange"),
  tripStatus: document.querySelector("#tripStatus"),
  countdown: document.querySelector("#countdown"),
  countdownValue: document.querySelector("#countdownValue"),
  dayRail: document.querySelector("#dayRail"),
  dayNumber: document.querySelector("#dayNumber"),
  dayTitle: document.querySelector("#dayTitle"),
  dayStayInline: document.querySelector("#dayStayInline"),
  timeline: document.querySelector("#timeline"),
  stayDetails: document.querySelector("#stayDetails"),
  mealList: document.querySelector("#mealList"),
  rainPlan: document.querySelector("#rainPlan"),
  shoppingBlock: document.querySelector("#shoppingBlock"),
  shoppingList: document.querySelector("#shoppingList"),
  nextStopTime: document.querySelector("#nextStopTime"),
  nextStopTitle: document.querySelector("#nextStopTitle"),
  nextStopLink: document.querySelector("#nextStopLink"),
  themeButton: document.querySelector("#themeButton"),
  installButton: document.querySelector("#installButton"),
  appUpdatePrompt: document.querySelector("#appUpdatePrompt"),
  appUpdateButton: document.querySelector("#appUpdateButton"),
};

let tripData = fallbackData;
let activeDayIndex = 0;
let deferredInstallPrompt = null;
let waitingServiceWorker = null;
let reloadForUpdate = false;

function getPreviewDate() {
  const value = new URLSearchParams(window.location.search).get("previewDate");
  if (!value) return null;
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function getCurrentDate() {
  return getPreviewDate() || new Date();
}

function dateKey(value) {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function normalizeDayDate(day, trip) {
  if (/^\d{4}-\d{2}-\d{2}$/.test(day.date)) return day.date;
  const match = /^(\d{1,2})\/(\d{1,2})$/.exec(day.date || "");
  if (!match) return day.date;
  const year = new Date(trip.startAt).getFullYear();
  return `${year}-${match[1].padStart(2, "0")}-${match[2].padStart(2, "0")}`;
}

function displayDate(day) {
  const match = /^(?:\d{4}-)?(\d{2})-(\d{2})$/.exec(day.date || "");
  if (match) return `${Number(match[1])}/${Number(match[2])}`;
  return day.date || "—";
}

function getTripState(now, trip) {
  const departure = new Date(trip.departureAt || trip.startAt);
  const end = new Date(trip.endAt);
  if (now < departure) return "countdown";
  if (now > end) return "ended";
  return "active";
}

function getInitialDayIndex(now) {
  const trip = tripData.trip;
  const today = dateKey(now);
  const exact = tripData.days.findIndex((day) => normalizeDayDate(day, trip) === today);
  if (exact >= 0) return exact;
  if (now > new Date(trip.endAt)) return tripData.days.length - 1;
  return 0;
}

function getCountdownText(now, departure) {
  const remaining = Math.max(0, departure.getTime() - now.getTime());
  const totalMinutes = Math.floor(remaining / 60000);
  const days = Math.floor(totalMinutes / 1440);
  const hours = Math.floor((totalMinutes % 1440) / 60);
  const minutes = totalMinutes % 60;
  if (days > 0) return `${days} 天 ${hours} 小時`;
  if (hours > 0) return `${hours} 小時 ${minutes} 分`;
  return `${minutes} 分鐘`;
}

function parseStartMinutes(label) {
  const match = /(?:^|\s)([01]?\d|2[0-3]):([0-5]\d)/.exec(label || "");
  if (!match) return null;
  return Number(match[1]) * 60 + Number(match[2]);
}

function linkParts(link) {
  if (Array.isArray(link)) return { label: link[0], url: link[1] };
  return { label: link?.label, url: link?.url };
}

function getNextEntry(day, now, isToday) {
  if (!isToday) return day.schedule?.[0] || null;
  const currentMinutes = now.getHours() * 60 + now.getMinutes();
  const timedEntries = (day.schedule || [])
    .map((entry, index) => ({ entry, index, minutes: parseStartMinutes(entry.time) }))
    .filter((candidate) => candidate.minutes !== null);
  if (!timedEntries.length) return day.schedule?.[0] || null;
  const upcoming = timedEntries.find((candidate) => candidate.minutes >= currentMinutes);
  return upcoming?.entry || null;
}

function renderTripHeader(now) {
  const trip = tripData.trip;
  const state = getTripState(now, trip);
  elements.tripName.textContent = trip.name;
  elements.brandShortName.textContent = trip.shortName || trip.name;
  document.title = trip.name;
  const descriptionMeta = document.querySelector('meta[name="description"]');
  if (descriptionMeta && trip.description) descriptionMeta.content = trip.description;
  elements.tripSummary.textContent = trip.description || "把每天的移動、吃飯與休息安排在同一張旅程地圖上。";
  elements.tripDateRange.textContent = trip.dateRange;
  elements.tripStatus.textContent = state === "active" ? "旅途中" : state === "ended" ? "旅程已結束" : "行程準備中";
  elements.countdown.hidden = state !== "countdown";
  if (state === "countdown") {
    elements.countdownValue.textContent = getCountdownText(now, new Date(trip.departureAt || trip.startAt));
  }
}

function renderDayRail() {
  elements.dayRail.replaceChildren();
  tripData.days.forEach((day, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "day-tab";
    button.setAttribute("aria-label", `第 ${index + 1} 天，${day.date}，${day.title}`);
    if (index === activeDayIndex) button.setAttribute("aria-current", "date");

    const date = document.createElement("strong");
    date.textContent = displayDate(day);
    const weekday = document.createElement("span");
    weekday.textContent = `週${day.weekday || "—"}`;
    button.append(date, weekday);
    button.addEventListener("click", () => {
      activeDayIndex = index;
      renderDay(getCurrentDate());
      button.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
    });
    elements.dayRail.append(button);
  });
}

function createLink(link, className) {
  const { label, url } = linkParts(link);
  if (!label || !url) return null;
  const anchor = document.createElement("a");
  anchor.className = className;
  anchor.href = url;
  anchor.target = "_blank";
  anchor.rel = "noreferrer noopener";
  anchor.textContent = label;
  return anchor;
}

function renderTimeline(day, nextEntry) {
  elements.timeline.replaceChildren();
  (day.schedule || []).forEach((entry) => {
    const item = document.createElement("li");
    item.className = "timeline-item";
    if (entry === nextEntry) item.classList.add("is-next");

    const time = document.createElement("time");
    time.className = "timeline-time";
    time.textContent = entry.time || "彈性";

    const content = document.createElement("div");
    content.className = "timeline-content";
    const text = document.createElement("p");
    text.textContent = entry.text || "待補行程。";
    content.append(text);

    const links = (entry.links || []).map((link) => createLink(link, "timeline-link")).filter(Boolean);
    if (links.length) {
      const linkList = document.createElement("div");
      linkList.className = "timeline-links";
      linkList.append(...links);
      content.append(linkList);
    }

    item.append(time, content);
    elements.timeline.append(item);
  });
}

function renderStay(day) {
  elements.stayDetails.replaceChildren();
  const details = tripData.stays?.[day.date] || { name: day.stay };
  const name = document.createElement("p");
  name.textContent = details.name || day.stay || "住宿待確認";
  elements.stayDetails.append(name);
  if (details.address) {
    const address = document.createElement("p");
    address.textContent = details.address;
    elements.stayDetails.append(address);
  }
  if (details.mapUrl) {
    const mapLink = createLink({ label: "查看住宿地圖", url: details.mapUrl }, "stay-link");
    if (mapLink) elements.stayDetails.append(mapLink);
  }
}

function renderMeals(day) {
  elements.mealList.replaceChildren();
  (day.food || []).forEach((meal) => {
    const item = document.createElement("div");
    item.className = "meal-item";
    const title = document.createElement("strong");
    title.textContent = meal.title || "餐食";
    const text = document.createElement("p");
    text.textContent = meal.text || "待補。";
    item.append(title, text);
    elements.mealList.append(item);
  });
}

function renderShopping(day) {
  const entries = day.shoppingBackup || [];
  elements.shoppingBlock.hidden = entries.length === 0;
  elements.shoppingList.replaceChildren();
  entries.forEach((entry) => {
    const item = document.createElement("div");
    item.className = "shopping-item";
    const name = document.createElement("strong");
    name.textContent = entry.name || "備選地點";
    const note = document.createElement("p");
    note.textContent = entry.note || (entry.tags || []).join(" · ");
    item.append(name, note);
    const links = (entry.links || []).map((link) => createLink(link, "timeline-link")).filter(Boolean);
    if (links.length) {
      const linkList = document.createElement("div");
      linkList.className = "timeline-links";
      linkList.append(...links);
      item.append(linkList);
    }
    elements.shoppingList.append(item);
  });
}

function renderNextStop(day, nextEntry, now) {
  const today = normalizeDayDate(day, tripData.trip) === dateKey(now);
  if (!nextEntry) {
    elements.nextStopTime.textContent = today ? "今日行程已完成" : `DAY ${String(activeDayIndex + 1).padStart(2, "0")}`;
    elements.nextStopTitle.textContent = today ? "好好休息，準備下一天" : day.title;
    elements.nextStopLink.hidden = true;
    return;
  }

  elements.nextStopTime.textContent = nextEntry.time || `DAY ${String(activeDayIndex + 1).padStart(2, "0")}`;
  elements.nextStopTitle.textContent = nextEntry.text || day.title;
  const route = (nextEntry.links || []).map(linkParts).find((link) => link.url && /google\.[^/]+\/maps|maps\.app\.goo\.gl/i.test(link.url));
  elements.nextStopLink.hidden = !route;
  if (route) {
    elements.nextStopLink.href = route.url;
    elements.nextStopLink.target = "_blank";
    elements.nextStopLink.rel = "noreferrer noopener";
  }
}

function renderDay(now) {
  const day = tripData.days[activeDayIndex];
  if (!day) return;
  renderDayRail();
  elements.dayNumber.textContent = `DAY ${String(activeDayIndex + 1).padStart(2, "0")} · ${displayDate(day)} 週${day.weekday || "—"}`;
  elements.dayTitle.textContent = day.title || "今日行程";
  elements.dayStayInline.textContent = day.stay ? `今晚住：${day.stay}` : "";
  const isToday = normalizeDayDate(day, tripData.trip) === dateKey(now);
  const nextEntry = getNextEntry(day, now, isToday);
  renderTimeline(day, nextEntry);
  renderStay(day);
  renderMeals(day);
  renderShopping(day);
  elements.rainPlan.textContent = day.rainPlan || tripData.rainRules?.[day.date] || "依現場天氣彈性調整。";
  renderNextStop(day, nextEntry, now);
}

async function loadTripData() {
  try {
    const response = await fetch("./data.generated.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const generated = await response.json();
    if (!generated.trip || !Array.isArray(generated.days) || generated.days.length === 0) {
      throw new Error("invalid trip data");
    }
    tripData = generated;
  } catch (error) {
    if (!fallbackData) throw error;
    console.warn("Using embedded itinerary data.", error);
    tripData = fallbackData;
  }
}

function setupTheme() {
  let savedTheme = null;
  try {
    savedTheme = localStorage.getItem("triphelper-theme");
  } catch (error) {
    console.warn("Theme preference is unavailable.", error);
  }
  const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)").matches;
  document.documentElement.dataset.theme = savedTheme || (prefersDark ? "dark" : "light");
  elements.themeButton.addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    elements.themeButton.setAttribute("aria-label", next === "dark" ? "切換淺色模式" : "切換深色模式");
    try {
      localStorage.setItem("triphelper-theme", next);
    } catch (error) {
      console.warn("Theme preference could not be saved.", error);
    }
  });
}

function setupInstallPrompt() {
  const isIosDevice = /iphone|ipad|ipod/i.test(navigator.userAgent);
  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    deferredInstallPrompt = event;
    if (!isIosDevice) elements.installButton.hidden = false;
  });
  elements.installButton.addEventListener("click", async () => {
    if (!deferredInstallPrompt) return;
    deferredInstallPrompt.prompt();
    await deferredInstallPrompt.userChoice;
    deferredInstallPrompt = null;
    elements.installButton.hidden = true;
  });
  window.addEventListener("appinstalled", () => {
    deferredInstallPrompt = null;
    elements.installButton.hidden = true;
  });
}

function showUpdatePrompt(worker) {
  waitingServiceWorker = worker;
  elements.appUpdatePrompt.hidden = false;
}

function setupServiceWorker() {
  if (!("serviceWorker" in navigator)) return;
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./service-worker.js").then((registration) => {
      if (registration.waiting && navigator.serviceWorker.controller) showUpdatePrompt(registration.waiting);
      registration.addEventListener("updatefound", () => {
        const worker = registration.installing;
        if (!worker) return;
        worker.addEventListener("statechange", () => {
          if (worker.state === "installed" && navigator.serviceWorker.controller) showUpdatePrompt(worker);
        });
      });
    }).catch((error) => console.warn("Service worker registration failed.", error));
  });

  elements.appUpdateButton.addEventListener("click", () => {
    if (!waitingServiceWorker) return;
    reloadForUpdate = true;
    waitingServiceWorker.postMessage({ type: "SKIP_WAITING" });
  });
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (reloadForUpdate) window.location.reload();
  });
}

async function init() {
  setupTheme();
  setupInstallPrompt();
  setupServiceWorker();
  await loadTripData();
  document.documentElement.dataset.style = tripData.trip.style || "editorial-wayfinder";
  const now = getCurrentDate();
  activeDayIndex = getInitialDayIndex(now);
  renderTripHeader(now);
  renderDay(now);
}

init().catch((error) => {
  console.error("Trip page failed to initialize.", error);
  elements.dayTitle.textContent = "行程資料暫時無法載入";
});
