# Travel PWA Unification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `20251129/` and `20260530/` both work as date-aware PWAs with automatic countdown, active-trip, and ended-trip states.

**Architecture:** Keep both sub-sites as static GitHub Pages folders. Add small, local helper scripts per site instead of introducing a build system. Use a `?previewDate=` query parameter for deterministic verification of countdown, active, and ended states.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, existing React UMD/Babel page in `20251129/`, service worker cache APIs, PowerShell HTTP verification.

---

## File Map

- Create: `20251129/manifest.webmanifest`
- Create: `20251129/service-worker.js`
- Create: `20251129/icons/icon.svg`
- Modify: `20251129/index.html`
- Modify: `20260530/index.html`
- Modify: `20260530/app.js`
- Modify: `20260530/styles.css`
- Modify: `20260530/service-worker.js`
- Create: `tests/verify-travel-pwa.js`

## Task 1: Verification Harness

**Files:**
- Create: `tests/verify-travel-pwa.js`

- [ ] **Step 1: Write failing verification script**

Create a Node script that checks required files, manifest fields, service worker assets, and static HTML markers for both travel sites.

- [ ] **Step 2: Run verification before implementation**

Run: `node tests/verify-travel-pwa.js`
Expected: FAIL because `20251129/manifest.webmanifest` and `20251129/service-worker.js` do not exist yet.

- [ ] **Step 3: Keep script as regression verification**

After implementation, the same command must exit `0`.

## Task 2: `20251129` PWA Foundation

**Files:**
- Create: `20251129/manifest.webmanifest`
- Create: `20251129/service-worker.js`
- Create: `20251129/icons/icon.svg`
- Modify: `20251129/index.html`

- [ ] **Step 1: Add PWA head metadata**

Add `theme-color`, `description`, manifest link, icon link, and apple touch icon to `20251129/index.html`.

- [ ] **Step 2: Add install button wiring**

Use existing React state to listen for `beforeinstallprompt`, expose an install CTA in the welcome/countdown screen, and hide it after prompt completion.

- [ ] **Step 3: Register service worker**

Register `./service-worker.js` on window load when `navigator.serviceWorker` exists.

- [ ] **Step 4: Add PWA resources**

Create a manifest scoped to `./`, cache the core page resources, and use a cache-first fetch fallback for offline access.

## Task 3: `20251129` Date States

**Files:**
- Modify: `20251129/index.html`

- [ ] **Step 1: Add trip configuration**

Define start date `2025-11-29T00:00:00+08:00`, end date `2025-12-06T23:59:59+08:00`, and `previewDate` parsing.

- [ ] **Step 2: Preserve existing welcome flow as countdown**

Use the existing `WelcomeScreen` as the countdown state before the trip starts.

- [ ] **Step 3: Add active trip summary**

Show trip day and return countdown inside the existing hero while the trip is active.

- [ ] **Step 4: Add ended page**

When current time is after the configured end date, show a review-style page with a button to reopen the full itinerary.

## Task 4: `20260530` Date States

**Files:**
- Modify: `20260530/index.html`
- Modify: `20260530/app.js`
- Modify: `20260530/styles.css`
- Modify: `20260530/service-worker.js`

- [ ] **Step 1: Add state containers**

Add countdown, active summary, ended, and main content containers in `index.html`.

- [ ] **Step 2: Add trip state logic**

Add trip config for `2026-05-30T00:00:00+08:00` through `2026-06-06T23:59:59+08:00`, parse `previewDate`, and calculate countdown/active/ended state.

- [ ] **Step 3: Render countdown and ended pages**

Render countdown metrics before the trip and ended content after the trip, while keeping existing daily itinerary rendering for active mode.

- [ ] **Step 4: Style new state views**

Add responsive CSS for countdown cards, active summary, ended page, and hidden state helpers.

- [ ] **Step 5: Bump service worker cache**

Update the cache name so existing clients receive the new app shell.

## Task 5: Verification And Commit

**Files:**
- All changed files

- [ ] **Step 1: Run Node verification**

Run: `node tests/verify-travel-pwa.js`
Expected: PASS.

- [ ] **Step 2: Run local HTTP verification**

Start or reuse a static server at `triphelper`, then verify `/20251129/`, `/20251129/manifest.webmanifest`, `/20251129/service-worker.js`, `/20260530/`, `/20260530/manifest.webmanifest`, and `/20260530/service-worker.js` return `200`.

- [ ] **Step 3: Verify preview states**

Request both sites with preview dates before, during, and after each trip and confirm the expected HTML/JS markers are present.

- [ ] **Step 4: Commit and push**

Commit with message `Unify travel pages as date-aware PWAs`, then push `main` to GitHub.
