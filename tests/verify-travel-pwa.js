const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");

const sites = [
  {
    dir: "20251129",
    name: "2025 富國島親子之旅",
    shortName: "富國島",
    cacheName: "phu-quoc-trip",
    requiredIndexMarkers: [
      'rel="manifest"',
      "beforeinstallprompt",
      "previewDate",
      "trip-state-ended",
      "navigator.serviceWorker.register",
    ],
  },
  {
    dir: "20260530",
    name: "2026 沖繩親子行程",
    shortName: "沖繩行程",
    cacheName: "okinawa-trip",
    requiredIndexMarkers: [
      'rel="manifest"',
      "countdownView",
      "endedView",
      "tripSummaryCard",
    ],
  },
];

function read(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8");
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

const failures = [];

for (const site of sites) {
  try {
    const siteRoot = path.join(root, site.dir);
    assert(fs.existsSync(path.join(siteRoot, "index.html")), `${site.dir}: missing index.html`);
    assert(fs.existsSync(path.join(siteRoot, "manifest.webmanifest")), `${site.dir}: missing manifest.webmanifest`);
    assert(fs.existsSync(path.join(siteRoot, "service-worker.js")), `${site.dir}: missing service-worker.js`);
    assert(fs.existsSync(path.join(siteRoot, "icons", "icon.svg")), `${site.dir}: missing icons/icon.svg`);

    const indexHtml = read(`${site.dir}/index.html`);
    for (const marker of site.requiredIndexMarkers) {
      assert(indexHtml.includes(marker), `${site.dir}: index.html missing marker "${marker}"`);
    }
    assert(
      indexHtml.includes("isIosDevice") || fs.existsSync(path.join(siteRoot, "app.js")) && read(`${site.dir}/app.js`).includes("isIosDevice"),
      `${site.dir}: install button should explicitly detect iOS Safari`
    );
    assert(
      indexHtml.includes("!isIosDevice") || fs.existsSync(path.join(siteRoot, "app.js")) && read(`${site.dir}/app.js`).includes("!isIosDevice"),
      `${site.dir}: install button should be hidden on iOS Safari`
    );

    const manifest = JSON.parse(read(`${site.dir}/manifest.webmanifest`));
    assert(manifest.name === site.name, `${site.dir}: manifest name mismatch`);
    assert(manifest.short_name === site.shortName, `${site.dir}: manifest short_name mismatch`);
    assert(manifest.start_url === "./index.html", `${site.dir}: manifest start_url should be ./index.html`);
    assert(manifest.scope === "./", `${site.dir}: manifest scope should be ./`);
    assert(Array.isArray(manifest.icons) && manifest.icons.length > 0, `${site.dir}: manifest icons missing`);

    const serviceWorker = read(`${site.dir}/service-worker.js`);
    assert(serviceWorker.includes(site.cacheName), `${site.dir}: service worker cache name should include ${site.cacheName}`);
    assert(serviceWorker.includes("./index.html"), `${site.dir}: service worker should cache index.html`);
    assert(serviceWorker.includes("./manifest.webmanifest"), `${site.dir}: service worker should cache manifest`);
    assert(serviceWorker.includes("./icons/icon.svg"), `${site.dir}: service worker should cache icon`);

    if (site.dir === "20260530") {
      assert(fs.existsSync(path.join(siteRoot, "data.generated.json")), `${site.dir}: missing data.generated.json`);
      assert(serviceWorker.includes("./data.generated.json"), `${site.dir}: service worker should cache generated data`);
      const stylesheet = read(`${site.dir}/styles.css`);
      assert(/\[hidden\]\s*\{[^}]*display:\s*none\s*!important\s*;?[^}]*\}/.test(stylesheet), `${site.dir}: stylesheet should preserve hidden attribute display behavior`);
      const generatedData = JSON.parse(read(`${site.dir}/data.generated.json`));
      assert(Array.isArray(generatedData.days) && generatedData.days.length > 0, `${site.dir}: generated data missing days`);
      assert(generatedData.trip?.id === "20260530-okinawa", `${site.dir}: generated trip id mismatch`);
    }
  } catch (error) {
    failures.push(error.message);
  }
}

if (failures.length > 0) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log("Travel PWA verification passed.");
