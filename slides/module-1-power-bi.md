---
marp: true
theme: gaia
paginate: true
footer: 'Kursus Lanjutan KKM 2026 · Dr. Muhammad Naufal bin Nordin'
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Transforming Medical Statistics with Power BI

**Slot 1 — 25 Jun 2026 (Thursday)**
Kursus Lanjutan (Advanced) — Pegawai Tadbir (Rekod Perubatan) & Penolong
KKM 2026

Dr. Muhammad Naufal bin Nordin

<!--
Welcome. This is Slot 1 — using Power BI to transform medical statistics. In the next 30 minutes I'll cover the core concepts, then we build a real COVID-19 dashboard together, step by step, on your own laptops. No prior Power BI experience is needed — if you can use Excel, you can do this.
-->

---

## What is Power BI?

- A **business intelligence** tool from Microsoft.
- Turns raw data (Excel, CSV, databases) into interactive **dashboards** & **reports**.
- For Medical Records: move from **manual Excel statistics** → **automatic dashboards** that are always up to date.

<!--
Power BI is Microsoft's business-intelligence tool. It takes raw data — Excel, CSV, databases — and turns it into interactive dashboards and reports. For Medical Records, the shift is from tallying statistics by hand in Excel to dashboards that refresh automatically and are always current. Build it once; reuse it every month.
-->

---

## The 5 types of analytics

- **Descriptive** — what happened? (counts, trends → *today's dashboard*)
- **Diagnostic** — why did it happen? (slicing, drill-down → *also today*)
- **Predictive** — what will happen? (forecasting → *Module 2 / AI*)
- **Prescriptive** — what should we do? (recommendations)
- **Continuous** — real-time, always-on automated analytics

<!--
Analytics comes in five levels. Descriptive — what happened — and diagnostic — why did it happen — are where dashboards live, and that's today's focus. Predictive and prescriptive look ahead and recommend action; that's where the AI tools in Module 2 begin to help. Continuous means real-time, always-on. We master the first two well today, because everything else builds on them.
-->

---

## Why it matters for KKM

- **Automate** counts and rates — no more manual tallying.
- **Filter** by state, age group, or vaccination status in one click.
- **Share** consistent figures with management — everyone sees the same numbers.

<!--
Three concrete wins for our work. First, automate counts and rates — no more manual tallying at month-end. Second, filter by state, age group, or vaccination status in a single click, instead of rebuilding a pivot table each time. Third, share one consistent set of figures, so management isn't comparing three spreadsheets with three different numbers.
-->

---

## The Power BI workflow

```
Get Data → Transform → Model → Visualize → Share
```

1. **Get Data** — import CSV/Excel/database.
2. **Transform** — clean & shape the data (Power Query).
3. **Model** — define relationships between tables.
4. **Visualize** — build charts & dashboards.
5. **Share** — publish/export to others.

<!--
Every Power BI project follows the same five steps. Get Data — import your files. Transform — clean and shape the data in Power Query. Model — define how the tables relate. Visualize — build the charts. Share — publish or export. We'll walk this exact path together in the hands-on session, in this order.
-->

---

## A quick tour: 3 views

Three views on the left side of Power BI Desktop:

- **Report view** — canvas for building visuals & dashboards.
- **Data view** — inspect tables (rows & columns).
- **Model view** — manage relationships between tables.

<!--
On the left edge of Power BI Desktop are three views you'll switch between constantly. Report view is the canvas where you build visuals. Data view shows the underlying tables, row by row. And Model view is where you manage relationships between tables. Get familiar with these three icons — we'll move between them all morning.
-->

---

## What is a data model?

![bg left:60% fit](../module-1-power-bi/img/03-model-star.png)

- **Fact:** `Fact_Deaths`
- **Dimensions:** `Dim_Date`, `Dim_State`
- **Relationships** join them
- → a **star schema**

<!--
A data model is simply how our tables relate to each other. In the middle is the fact table, Fact_Deaths — one row for every COVID-19 death; this is the "what happened", the events we count. Around it sit the dimension tables — the context we slice by: Dim_Date is a calendar, Dim_State holds each state and its population. The lines are relationships: one-to-many — one state has many deaths, one date has many deaths. That linkage is the magic: click a state in a slicer and every chart filters automatically. We could have used one big flat table, but this shape — a star schema, one fact surrounded by dimensions — is cleaner and faster, avoids repeating the same state and date text on 37,000 rows, and lets us add context like population once, in Dim_State, then reuse it — which is how we'll later compute deaths per 100,000.
-->

---

## What is a measure (DAX)?

- **Column** — a stored value, fixed per row (e.g. *State*, *Age*).
- **Measure** — a calculation evaluated **in context**, using DAX (e.g. *Total Deaths*, *Deaths per 100k*).
- Measures recalculate automatically as you filter or slice the report.

<!--
Two things people often confuse. A column is a stored value, fixed for each row — like State or Age. A measure is a calculation evaluated in context, written in a language called DAX — like Total Deaths or Deaths per 100k. The key difference: a measure recalculates automatically every time you filter or slice. Pick one state and Total Deaths updates instantly. We'll write a few simple measures today — they're short, often a single line.
-->

---

## Today's data

- Source: **data.gov.my** — open government data.
- Dataset: **COVID-19 deaths line-list**.
- **One row = one death.**
- ~37,000 deaths, **2020–2024**, by state, age, sex, comorbidity, and vaccination status.

<!--
Our data is real and public, from data.gov.my, the government's open-data portal. It's the COVID-19 deaths line-list — one row per death, about 37,000 of them, spanning 2020 to 2024, with state, age, sex, comorbidity, and vaccination status. Using real Malaysian data makes the exercise far more meaningful than a made-up sample — and it's a portal you can keep using afterwards.
-->

---

## Is this safe to use?

- Open, **aggregate / de-identified** government data → safe to share, publish, and teach with.
- **Never** upload real patient records or confidential documents to any cloud/AI tool.
- This rule applies beyond today's class — it's a standing data-security principle.

<!--
Yes — because this is open, aggregated, de-identified government data, it's safe to share, publish, and teach with. But the rule for your real work stands: never upload actual patient records or confidential documents to any cloud or AI tool. Today's safety comes from the data being public; your daily data is not. That principle applies well beyond this class.
-->

---

## What we'll build today

A one-page dashboard with:

- **KPI cards** — total deaths, key summary numbers.
- **Line chart** — deaths over time.
- **Bar chart** — deaths by state.
- **Breakdown by age group.**
- **Donut chart** — vaccination status.
- **Slicers** — to filter everything above interactively.

<!--
Here's the plan for the hands-on session — a single-page dashboard: KPI cards for the headline numbers, a line chart for deaths over time, a bar chart by state, an age-group breakdown, a vaccination-status donut, and slicers to filter everything interactively. Don't worry about building it now — just get a feel for the target; we'll construct each piece together.
-->

---

## The finished dashboard

![w:880](../module-1-power-bi/img/05-cards-visuals.png)

<!--
This is exactly what you'll have built by the end of the morning. Notice the headline numbers — about 37,000 deaths, just over 60% unvaccinated, median age 64 — and how the pandemic waves stand out in the line chart, peaking in 2021. Try clicking a state or the Sex slicer and watch every visual update at once. By late morning, this will be your own file.
-->

---

## Follow-along ground rules

- Everyone builds on their **own laptop**.
- Data files are in `module-1-power-bi/data/`.
- **Raise your hand** if you get stuck — don't wait.
- We save **checkpoints** along the way so you can rejoin at any point.

<!--
A few ground rules before we start. Everyone builds on their own laptop — this is hands-on, not watch-only. The data files are already in the module-1 data folder. Raise your hand the moment you get stuck; don't suffer in silence while we move ahead. And we save checkpoints along the way, so if you fall behind you can open the nearest saved file and rejoin instantly.
-->

---

<!-- _class: lead -->

# Let's build → hands-on-guide

<!--
That's the theory. Let's open Power BI Desktop and start building — we'll follow the hands-on guide together from here, one step at a time. Make sure your Power BI Desktop is open and the data folder is handy.
-->
