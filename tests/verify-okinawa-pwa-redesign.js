const fs = require("fs");
const path = require("path");

function assertIncludes(haystack, needle, label) {
  if (!haystack.includes(needle)) {
    throw new Error(`Missing ${label}: ${needle}`);
  }
}

const root = process.cwd();
const html = fs.readFileSync(path.join(root, "okinawa-pwa", "index.html"), "utf8");
const js = fs.readFileSync(path.join(root, "okinawa-pwa", "app.js"), "utf8");

assertIncludes(html, 'id="todayHero"', "today hero container");
assertIncludes(html, 'id="tripSummaryCard"', "trip summary card");
assertIncludes(html, 'id="mealCard"', "meal card");
assertIncludes(html, 'id="rainDecisionCard"', "rain decision card");
assertIncludes(js, "function getActiveDayViewModel()", "day view model helper");
assertIncludes(js, "function renderTodayHero()", "today hero renderer");
assertIncludes(js, "function renderSupportCards()", "support cards renderer");

console.log("verify-okinawa-pwa-redesign: PASS");
