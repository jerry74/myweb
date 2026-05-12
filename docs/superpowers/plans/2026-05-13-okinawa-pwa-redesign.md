# Okinawa PWA Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `okinawa-pwa/` into a today-first travel dashboard that keeps the existing data and PWA behavior while making the page faster to scan and use on mobile.

**Architecture:** Keep the app as a static HTML/CSS/vanilla JS site. Replace the current section layout with a dashboard shell in `index.html`, add derived-view helpers in `app.js` to produce today-card, summary, timeline, meal, and rain-decision data from existing arrays, and restyle the interface with a new card hierarchy and responsive token system in `styles.css`.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, existing service worker/PWA install flow, Node.js for verification.

---

## File Map

- Modify: `okinawa-pwa/index.html`
- Modify: `okinawa-pwa/styles.css`
- Modify: `okinawa-pwa/app.js`
- Create: `tests/verify-okinawa-pwa-redesign.js`

## Task 1: Add A Redesign Verification Harness

**Files:**
- Create: `tests/verify-okinawa-pwa-redesign.js`

- [ ] **Step 1: Write the failing verification script**

Create a Node script that checks the redesigned dashboard markers exist in `okinawa-pwa/index.html`, and that `app.js` contains the new rendering entry points we plan to add.

```js
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
```

- [ ] **Step 2: Run the verification script to confirm it fails**

Run: `node tests/verify-okinawa-pwa-redesign.js`

Expected: FAIL with at least one missing marker such as `today hero container` because the redesign structure does not exist yet.

- [ ] **Step 3: Keep this script as the regression check**

Do not delete the script after implementation. We will use the same command at the end of the work and expect:

```text
verify-okinawa-pwa-redesign: PASS
```

- [ ] **Step 4: Commit the failing test harness**

```bash
git add tests/verify-okinawa-pwa-redesign.js
git commit -m "test: add okinawa pwa redesign verifier"
```

## Task 2: Replace The HTML Shell With A Dashboard Layout

**Files:**
- Modify: `okinawa-pwa/index.html`

- [ ] **Step 1: Add the new dashboard shell markup**

Replace the current main layout sections with a dashboard structure that includes the hero, summary card, timeline section, and support cards while preserving install button, search input, and bottom tabs.

```html
<header class="app-header">
  <div class="header-media" aria-hidden="true"></div>
  <div class="header-content dashboard-header">
    <div class="hero-kicker">
      <p class="eyebrow">Okinawa Family Trip</p>
      <span id="tripDateRange">2026/05/30 - 2026/06/06</span>
    </div>
    <div class="hero-grid">
      <section id="todayHero" class="hero-card" aria-labelledby="todayHeroTitle">
        <div class="hero-card-copy">
          <p class="eyebrow">Today First</p>
          <h1 id="todayHeroTitle">今天主卡</h1>
          <p id="todayHeroLead" class="lead"></p>
        </div>
        <div id="todayHeroActions" class="hero-actions"></div>
      </section>
      <aside id="tripSummaryCard" class="summary-card" aria-label="旅程摘要"></aside>
    </div>
  </div>
</header>

<main class="dashboard-main">
  <section class="status-strip" aria-label="旅程重點">
    ...
  </section>

  <section class="tools-bar" aria-label="行程篩選">
    ...
  </section>

  <section id="todayTimeline" class="section">
    <div class="section-heading">
      <p class="eyebrow">Today Timeline</p>
      <h2>今天行程</h2>
    </div>
    <div id="dayList" class="timeline-list"></div>
  </section>

  <section class="section support-grid" aria-label="支援資訊">
    <article id="mealCard" class="support-card"></article>
    <article id="rainDecisionCard" class="support-card"></article>
  </section>

  <section class="section utility-grid">
    <article class="panel">
      <h2>住宿總覽</h2>
      <div id="stayList" class="compact-list"></div>
    </article>
    <article class="panel">
      <h2>早餐採買規則</h2>
      <div id="breakfastList" class="compact-list"></div>
    </article>
  </section>
</main>
```

- [ ] **Step 2: Preserve the install CTA and search affordance**

Keep the existing install button and search input in the new shell. Ensure the install button still exists with the same `id`:

```html
<button id="installButton" class="primary-button" type="button" hidden>安裝到手機</button>
```

And keep the search field:

```html
<input id="searchInput" type="search" placeholder="輸入地點、餐廳、日期">
```

- [ ] **Step 3: Add anchors for the new app.js render targets**

Make sure these exact ids exist in `index.html` because the new rendering logic depends on them:

```html
<section id="todayHero" class="hero-card"></section>
<aside id="tripSummaryCard" class="summary-card"></aside>
<article id="mealCard" class="support-card"></article>
<article id="rainDecisionCard" class="support-card"></article>
```

- [ ] **Step 4: Re-run the verifier and confirm it still fails on JS markers**

Run: `node tests/verify-okinawa-pwa-redesign.js`

Expected: FAIL, but now only on missing JavaScript helpers such as `function getActiveDayViewModel()`.

- [ ] **Step 5: Commit the HTML shell change**

```bash
git add okinawa-pwa/index.html tests/verify-okinawa-pwa-redesign.js
git commit -m "feat: add okinawa dashboard html shell"
```

## Task 3: Add View-Model Helpers For Today-First Rendering

**Files:**
- Modify: `okinawa-pwa/app.js`

- [ ] **Step 1: Add failing helper names and wiring targets**

Introduce the helper function stubs near the DOM queries so the verifier starts targeting the real API surface.

```js
const todayHero = document.querySelector("#todayHero");
const tripSummaryCard = document.querySelector("#tripSummaryCard");
const mealCard = document.querySelector("#mealCard");
const rainDecisionCard = document.querySelector("#rainDecisionCard");

function getEntryMeta(entry) {
  const [, , slug, flags = {}] = entry;
  return {
    slug,
    weatherSensitive: Boolean(flags.weatherSensitive),
    optional: Boolean(flags.optional),
  };
}

function getActiveDayViewModel() {
  const day = days[activeDayIndex];
  return {
    dayNumber: activeDayIndex + 1,
    totalDays: days.length,
    dateLabel: `${day.date}（${day.weekday}）`,
    title: day.title,
    stay: day.stay,
  };
}

function getTodayMealViewModel(day) {
  return {
    spotlight: day.food.slice(0, 2),
    backup: day.food.slice(2),
  };
}
```

- [ ] **Step 2: Add timeline support helpers from existing schedule data**

Create a helper that decorates the raw schedule items with status badges and next-stop detection.

```js
function getTimelineCards(day) {
  return day.schedule.map((entry, index) => {
    const meta = getEntryMeta(entry);
    return {
      time: entry.time,
      text: entry.text,
      links: entry.links,
      isNext: index === 0,
      badges: [
        meta.weatherSensitive ? "雨天敏感" : null,
        meta.optional ? "可彈性調整" : "固定行程",
      ].filter(Boolean),
    };
  });
}
```

- [ ] **Step 3: Add support-card derivation helpers**

Use the existing rain rule and meal data instead of inventing a new data source.

```js
function getRainDecisionViewModel(day) {
  return {
    title: "雨天切換",
    summary: day.rainPlan,
    decisionTags: day.tags.includes("rain")
      ? ["保留部分室內點", "戶外可取消", "視天氣延後"]
      : ["照原行程", "低天氣風險"],
  };
}

function getTripSummaryViewModel(day) {
  return {
    dayLabel: `Day ${activeDayIndex + 1} / ${days.length}`,
    stay: day.stay,
    remainingDays: days.length - activeDayIndex - 1,
    transferLabel: day.tags.includes("drive") ? "今天有移動" : "今天定點活動",
  };
}
```

- [ ] **Step 4: Re-run the verifier and confirm it now fails on renderer functions**

Run: `node tests/verify-okinawa-pwa-redesign.js`

Expected: FAIL on missing render functions such as `function renderTodayHero()`.

- [ ] **Step 5: Commit the view-model helper layer**

```bash
git add okinawa-pwa/app.js tests/verify-okinawa-pwa-redesign.js
git commit -m "feat: add okinawa dashboard view models"
```

## Task 4: Render The Today Hero, Summary, Timeline, And Support Cards

**Files:**
- Modify: `okinawa-pwa/app.js`

- [ ] **Step 1: Render the today hero card**

Add a renderer that writes the hero content from the active day view model.

```js
function renderTodayHero() {
  const model = getActiveDayViewModel();
  const timeline = getTimelineCards(days[activeDayIndex]);
  const nextStop = timeline.find((entry) => entry.isNext) || timeline[0];

  todayHero.innerHTML = `
    <div class="hero-card-copy">
      <p class="eyebrow">Today First</p>
      <h1>${model.title}</h1>
      <p class="lead">${model.dateLabel}｜住宿：${model.stay}</p>
      <div class="hero-next-stop">
        <span>下一站</span>
        <strong>${nextStop ? nextStop.text : "今天自由調整"}</strong>
      </div>
    </div>
    <div class="hero-actions">
      <a class="primary-button" href="#todayTimeline">看今天行程</a>
      <button class="ghost-button" type="button" data-jump="next-link">查看下一站</button>
      <a class="ghost-button" href="#rainDecisionCard">雨天備案</a>
    </div>
  `;
}
```

- [ ] **Step 2: Render the summary and support cards**

Add dedicated renderers for the summary, meals, and rain-decision modules.

```js
function renderTripSummary() {
  const day = days[activeDayIndex];
  const model = getTripSummaryViewModel(day);

  tripSummaryCard.innerHTML = `
    <p class="eyebrow">Trip Summary</p>
    <div class="summary-metrics">
      <div><span>${model.dayLabel}</span><strong>${model.transferLabel}</strong></div>
      <div><span>目前住宿</span><strong>${model.stay}</strong></div>
      <div><span>距離返程</span><strong>${model.remainingDays} 天</strong></div>
    </div>
  `;
}

function renderSupportCards() {
  const day = days[activeDayIndex];
  const mealModel = getTodayMealViewModel(day);
  const rainModel = getRainDecisionViewModel(day);

  mealCard.innerHTML = `
    <p class="eyebrow">Meals & Supply</p>
    <h3>今天吃什麼</h3>
    <div class="support-stack">
      ${mealModel.spotlight.map((entry) => `
        <div class="support-item">
          <strong>${entry.title}</strong>
          <p>${entry.text}</p>
          ${linkPills(entry.links)}
        </div>
      `).join("")}
    </div>
  `;

  rainDecisionCard.innerHTML = `
    <p class="eyebrow">Weather Switch</p>
    <h3>${rainModel.title}</h3>
    <p>${rainModel.summary}</p>
    <div class="decision-tags">
      ${rainModel.decisionTags.map((tag) => `<span class="decision-tag">${tag}</span>`).join("")}
    </div>
  `;
}
```

- [ ] **Step 3: Replace the old day-card renderer with timeline cards**

Update `renderDays()` so it renders a single-day, card-based timeline with badges rather than the previous two-column article layout.

```js
function renderDays() {
  const query = searchInput.value.trim().toLowerCase();
  const visibleDays = query
    ? days.filter((day) => JSON.stringify(day).toLowerCase().includes(query))
    : [days[activeDayIndex]];

  dayList.innerHTML = visibleDays.map((day) => `
    <article class="timeline-day">
      <header class="timeline-day-header">
        <div>
          <p class="eyebrow">Day Focus</p>
          <h3>${day.date}（${day.weekday}）${day.title}</h3>
          <p class="compact-meta">住宿：${day.stay}</p>
        </div>
      </header>
      <div class="timeline-cards">
        ${getTimelineCards(day).map((entry) => `
          <section class="timeline-card">
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
```

- [ ] **Step 4: Update the tab click flow to refresh every dashboard region**

Make tab clicks and startup invoke the new renderers in one place.

```js
function renderDashboard() {
  renderTodayHero();
  renderTripSummary();
  renderSupportCards();
  renderTabs();
  renderDays();
  renderCompactLists();
}

dayTabs.querySelectorAll(".day-tab").forEach((button) => {
  button.addEventListener("click", () => {
    activeDayIndex = Number(button.dataset.dayIndex);
    searchInput.value = "";
    renderDashboard();
  });
});
```

- [ ] **Step 5: Make the verifier pass for JavaScript markers**

Run: `node tests/verify-okinawa-pwa-redesign.js`

Expected:

```text
verify-okinawa-pwa-redesign: PASS
```

- [ ] **Step 6: Commit the rendering implementation**

```bash
git add okinawa-pwa/app.js tests/verify-okinawa-pwa-redesign.js
git commit -m "feat: render okinawa travel dashboard"
```

## Task 5: Replace The Visual System And Responsive Layout

**Files:**
- Modify: `okinawa-pwa/styles.css`

- [ ] **Step 1: Replace the root tokens with the new travel-dashboard palette**

Update the root variables to move away from the current generic blue-green look.

```css
:root {
  --bg: #f6f1e7;
  --surface: rgba(255, 252, 246, 0.92);
  --surface-strong: #ffffff;
  --ink: #143042;
  --muted: #5d7180;
  --line: rgba(20, 48, 66, 0.10);
  --sea: #0f766e;
  --sea-deep: #155e75;
  --sand: #f5e8cf;
  --coral: #f97316;
  --leaf: #2f855a;
  --shadow-lg: 0 24px 60px rgba(20, 48, 66, 0.12);
  --shadow-md: 0 14px 32px rgba(20, 48, 66, 0.08);
}
```

- [ ] **Step 2: Add new hero, summary, and support-card layout styles**

Define the new shell classes introduced in `index.html`.

```css
.dashboard-header {
  padding: 52px 0 36px;
}

.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr);
  gap: 18px;
  margin-top: 22px;
}

.hero-card,
.summary-card,
.support-card {
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(18px);
}

.hero-card {
  padding: 24px;
  box-shadow: 0 20px 44px rgba(15, 23, 42, 0.18);
}

.summary-card {
  padding: 22px;
}
```

- [ ] **Step 3: Replace old day-card rules with timeline card rules**

Swap out `.day-card`, `.day-top`, `.day-body`, and `.time-row` focused styles for timeline-card styles.

```css
.timeline-list,
.timeline-cards,
.support-grid {
  display: grid;
  gap: 16px;
}

.timeline-day {
  display: grid;
  gap: 16px;
}

.timeline-card {
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: 24px;
  background: var(--surface-strong);
  box-shadow: var(--shadow-md);
}

.timeline-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.timeline-badge,
.decision-tag {
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 800;
}
```

- [ ] **Step 4: Add mobile-first stacking and desktop breathing room**

Introduce responsive rules for the new dashboard layout.

```css
@media (max-width: 820px) {
  .hero-grid,
  .support-grid,
  .utility-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 560px) {
  .hero-card,
  .summary-card,
  .support-card,
  .timeline-card {
    border-radius: 22px;
  }

  .hero-actions {
    flex-direction: column;
    align-items: stretch;
  }
}
```

- [ ] **Step 5: Verify the page still contains the new dashboard regions**

Run: `node tests/verify-okinawa-pwa-redesign.js`

Expected:

```text
verify-okinawa-pwa-redesign: PASS
```

- [ ] **Step 6: Commit the visual redesign**

```bash
git add okinawa-pwa/styles.css okinawa-pwa/index.html okinawa-pwa/app.js tests/verify-okinawa-pwa-redesign.js
git commit -m "feat: restyle okinawa pwa as travel dashboard"
```

## Task 6: Polish, Manual Verification, And Handoff

**Files:**
- Modify: `okinawa-pwa/index.html`
- Modify: `okinawa-pwa/styles.css`
- Modify: `okinawa-pwa/app.js`
- Modify: `tests/verify-okinawa-pwa-redesign.js`

- [ ] **Step 1: Run the automated verifier**

Run: `node tests/verify-okinawa-pwa-redesign.js`

Expected:

```text
verify-okinawa-pwa-redesign: PASS
```

- [ ] **Step 2: Start a local static server and verify the page loads**

Run from repo root:

```bash
python -m http.server 4173
```

Open `http://127.0.0.1:4173/okinawa-pwa/` and verify:

- the page loads without console-blocking errors
- the hero shows today-first content
- day tabs switch the hero, summary, support cards, and timeline together

- [ ] **Step 3: Verify mobile behavior**

Use browser responsive mode or a narrow window and confirm:

- no horizontal scrolling at 375px width
- hero actions remain tappable
- support cards stack cleanly
- bottom tabs remain usable

- [ ] **Step 4: Verify PWA affordances still work**

Confirm:

- install button appears when `beforeinstallprompt` fires
- external guide/map links still open
- service worker registration still succeeds without changing the registration path

- [ ] **Step 5: Commit final polish**

```bash
git add okinawa-pwa/index.html okinawa-pwa/styles.css okinawa-pwa/app.js tests/verify-okinawa-pwa-redesign.js
git commit -m "chore: polish okinawa pwa redesign"
```

## Self-Review

### Spec coverage

- Today-first dashboard shell: covered by Task 2 and Task 5
- Today hero, summary, timeline, meals, rain decision modules: covered by Task 3 and Task 4
- Mobile-first responsive behavior: covered by Task 5 and Task 6
- Preserve PWA/install/external link behavior: covered by Task 2 and Task 6
- Keep existing data model and derive display state from it: covered by Task 3

No uncovered spec sections remain.

### Placeholder scan

- No `TODO`, `TBD`, or deferred implementation language remains.
- Each implementation task names exact files and concrete commands.
- Verification commands and expected outputs are included.

### Type consistency

- `getActiveDayViewModel()`, `renderTodayHero()`, and `renderSupportCards()` are referenced consistently across Tasks 3 and 4.
- Render targets use the same ids in the HTML and JavaScript tasks: `todayHero`, `tripSummaryCard`, `mealCard`, `rainDecisionCard`.

