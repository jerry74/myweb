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
      "activeTripSummary",
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
  } catch (error) {
    failures.push(error.message);
  }
}

if (failures.length > 0) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log("Travel PWA verification passed.");
