# Modul 1 Rework — Power BI Theory + COVID Live Build

**Date:** 2026-06-23
**Author:** Dr. Muhammad Naufal bin Nordin (with Claude)
**Status:** Approved design — ready for implementation planning
**Slot:** Slot 1, 25 Jun 2026 (Thu), 8:00 am – 11:30 am

---

## 1. Summary

Major rework of **Modul 1 (Power BI)**. Split the slot into a **30-minute theory
session** (slide deck) followed by a **~2.5-hour follow-along live build** in which
every participant builds an interactive COVID-19 statistics dashboard on their own
laptop, step by step with the facilitator.

The existing synthetic hospital-admissions content (7 lab files, `jana_data.py`,
BOR/ALOS framing) is **retired entirely** and replaced with a single coherent
storyline built on **real Malaysian open data** from data.gov.my / DOSM.

**Language:** All Modul 1 written materials (slides, README, hands-on guide) are in
**English**. Module 2 remains in Malay for now.

---

## 2. Goals & non-goals

### Goals
- Cleanly separate **theory** (concepts) from **hands-on** (live build).
- Teach the full Power BI workflow end-to-end: Get Data → Transform → **Model** →
  Visualize → Share.
- Explicitly teach the **data model / star schema** (a stated priority).
- Have every participant **finish a core dashboard** and experience charts, slicers,
  and cross-filtering hands-on.
- Use **real, locally relevant, safe-to-share** open data.

### Non-goals
- No Power BI Service / publishing to cloud (Desktop only).
- No real patient data (open aggregate/anonymised data only).
- No maintenance of the old synthetic-admissions labs.
- Module 2 language/content is out of scope.

---

## 3. Audience & format decisions (locked)

| Decision | Choice |
|---|---|
| Participation | **Follow-along** — everyone builds on their own laptop |
| Data model depth | **Full star schema**: Deaths fact + Date + State (+ population) |
| Old content | **Replaced entirely** |
| Dashboard scope | **Standard core + optional showcase extras if pace allows** |
| Slide language | English |
| All Modul 1 docs | English |

Implications of follow-along: per-stage **checkpoints** with fallback `.pbix`
files, **pre-downloaded data** (no reliance on live internet in the room), and a
**written hands-on guide** so stragglers can catch up.

---

## 4. Slot 1 timetable (3.5 hrs)

| Block | Time | Mins | Format |
|---|---|---|---|
| Theory | 8:00–8:30 | 30 | Slide deck (facilitator presents) |
| Build Pt.1: Ingest + Power Query | 8:30–9:20 | 50 | Follow-along |
| Build Pt.2: Data model (star schema) | 9:20–9:45 | 25 | Follow-along |
| **Break** | 9:45–10:00 | 15 | — |
| Build Pt.3: DAX measures | 10:00–10:30 | 30 | Follow-along |
| Build Pt.4: Visuals | 10:30–11:10 | 40 | Follow-along |
| Build Pt.5: Interactivity + free explore + Q&A | 11:10–11:30 | 20 | Follow-along + optional extras |

Each build part ends at a **checkpoint** (`00-start` → `05-final`) with a fallback
`.pbix` so anyone stuck can reload and rejoin.

---

## 5. Theory deck (30 min, ~14 slides, English)

1. Title
2. What is BI / Power BI?
3. **The 5 types of analytics** — Descriptive (*what happened?* — today's dashboard),
   Diagnostic (*why?* — slicing/drill, today), Predictive (*what will happen?* —
   teaser for Module 2 / AI), Prescriptive (*what should we do?*), Continuous
   (real-time, always-on). Frames where dashboards sit and bridges to Module 2.
4. Why it matters for KKM (manual Excel → automated, always-current dashboards)
5. The workflow: Get Data → Transform → **Model** → Visualize → Share
6. The 3 views (Report / Data / Model)
7. **What is a data model?** Fact vs dimension, star schema — plain language, the
   "one big flat table vs related tables" intuition
8. **What is a measure (DAX)?** vs a column — quick intuition
9. Today's data: data.gov.my open data + the COVID deaths linelist (what one row is)
10. Open-data ethics — why this is safe to use; contrast with the patient-data
    security rule
11. Preview of the dashboard we'll build (screenshot of finished result)
12. Ground rules for follow-along (checkpoints, "raise hand if stuck", file location)
13. → To the build
14. (buffer / section divider)

---

## 6. Data & ingestion plan

All source files are **pre-downloaded into the repo** so the training room never
depends on live internet.

| Role | File | Source |
|---|---|---|
| Fact | `covid_deaths_linelist.parquet` | `https://storage.data.gov.my/healthcare/covid_deaths_linelist.parquet` |
| Dimension input | `population_state.parquet` | `https://storage.dosm.gov.my/population/population_state.parquet` |
| Optional context | `covid_cases.parquet` | `https://storage.data.gov.my/healthcare/covid_cases.parquet` |

**Teaching approach:** the facilitator demos **Get Data → Web** (URL ingestion) once
on screen, then everyone loads the **local copies** in `modul-1-power-bi/data/` as
the reliable path. A `data/fetch_data.py` script (using duckdb/httpfs) regenerates
the local files.

### Source data profile (validated with duckdb)
- `covid_deaths_linelist`: **37,351 rows**, one per death, 2020-03-17 → 2024-05-18,
  16 states. Columns: `date`, `date_announced`, `date_positive`,
  `date_dose1/2/3`, `brand1/2/3`, `state`, `age`, `male` (0/1), `bid` (0/1),
  `malaysian` (0/1), `comorb` (0/1).
- `population_state` (DOSM): `state`, `date` (year, Jan 1), `sex`, `age`,
  `ethnicity`, `population` (thousands). Filter to `sex=both`, `age=overall`,
  `ethnicity=overall`. State names match the deaths table exactly.
- `covid_cases`: daily new cases by state (optional, for case-fatality angle).

---

## 7. Star schema (data model)

```
        Dim_Date ────┐
                     │  (1-to-many on Date)
   Dim_State ────────┤
   (+ Region,        Fact_Deaths
    + Population)     (1 row per death)
```

- **Fact_Deaths** — cleaned deaths linelist at death-event grain.
- **Dim_Date** — calendar table via DAX `CALENDAR`, "Mark as date table" → unlocks
  time intelligence.
- **Dim_State** — state + **Region** (Semenanjung / Borneo) + **Population**.

### Population design decision
Rather than a separate `state × year` population table (which needs a painful
composite-key relationship for beginners), **fold a single representative-year
(2024) population into `Dim_State`**. This yields a clean `Deaths per 100k` measure
with one simple 1-to-many relationship, while still teaching the intended concept
(a dimension enriching the fact to compute a rate). The separate-population-table
approach is mentioned as an "advanced" note only.

This fulfils the "Deaths + Date + State + Population" star-schema goal; population
simply lives inside the State dimension.

**Validated rate teaching moment:** W.P. Labuan has the highest deaths-per-100k
(small population) while Selangor has the highest raw count — a built-in lesson on
**rates vs counts**.

---

## 8. Power Query transforms (teachable cleaning steps)

On **Fact_Deaths**:
- Promote headers; set data types.
- `Sex` = from `male` (1 → Male, 0 → Female).
- `Age_Group` = age bands (0–17, 18–39, 40–59, 60–79, 80+).
- `Vaccination_Status` = compare `date_dose2` / `date_dose1` to `date` →
  **Fully vaccinated (≥2 doses)** / **Partial (1 dose)** / **Unvaccinated**.
  *(The "wow" derived column.)*
- `Comorbidity`, `Citizenship`, `BID` = flags (1/0) → Yes/No text.

Build **Dim_State**: filter `population_state` to both/overall/overall, 2024; add the
Region grouping; convert population (thousands → persons).

**Validated derivation:** Vaccination status at death → **60.2% Unvaccinated**,
24.8% Fully vaccinated, 15.0% Partial. A striking, real public-health finding.

---

## 9. DAX measures

**Core**
- `Total Deaths`
- `% Brought-in-Dead`
- `% With Comorbidity`
- `% Unvaccinated`
- `Median Age`
- `Deaths per 100k` (uses Dim_State population)

**Time intelligence**
- `Deaths YTD` (showcases Dim_Date)

**Included (from `covid_cases`)**
- `Case Fatality %` — total deaths ÷ total cases (facilitator may drop if time tight)

---

## 10. Dashboard (one page)

### Core (everyone finishes)
- **4 KPI cards:** Total Deaths · % Unvaccinated · % With Comorbidity · Median Age
- **Line chart:** deaths over time (the COVID waves — visually dramatic)
- **Bar (primary) / Map:** deaths by state
- **Column:** deaths by age group
- **Donut:** vaccination status at death
- **Slicers:** State, Sex, Comorbidity, Date range

### Optional showcase (only if pace is good)
- Deaths-per-100k filled map
- Decomposition tree (age → comorbidity → vaccination status)
- Drillthrough page per state

### Risk: map visuals
Power BI map visuals require internet + Bing and may be disabled on government
tenants. **The core uses a bar chart by state** (always works); the map is an
optional/showcase swap.

### Interactivity teaching
Cross-filtering between visuals, slicer behaviour, drill-down, tooltips.

---

## 11. Deliverables & repo changes

### New / rewritten
- `slides/modul-1-power-bi.md` — rewritten theory deck (English, ~14 slides).
- `modul-1-power-bi/README.md` — rewritten (English: theory + build overview).
- `modul-1-power-bi/hands-on-guide.md` — written follow-along guide (English;
  stragglers' safety net mirroring the live steps).
- `modul-1-power-bi/data/` — pre-downloaded parquet/CSV + `fetch_data.py`.
- Facilitator pacing notes + checkpoint list.

### Checkpoint `.pbix` files
`.pbix` are binary and must be built by the facilitator in Power BI Desktop. The
repo provides the data + step guide so each checkpoint (`00-start` → `05-final`)
can be regenerated. The checkpoint sequence is documented in the hands-on guide.

### Retired
- `modul-1-power-bi/lab/01–07`
- `data/jana_data.py` and synthetic CSVs
- BOR/ALOS framing

---

## 12. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Room internet unreliable | Pre-download all data into repo; URL ingestion is a one-time demo only |
| Laptops without Power BI Desktop | Reinforce `00-persediaan/` prerequisite; have a spare install plan |
| Map visuals blocked on govt tenant | Core dashboard uses bar-by-state; map is optional swap |
| Participants fall behind | Per-stage checkpoint `.pbix` + written hands-on guide to rejoin |
| Build overruns 3.5 hrs | Showcase extras are explicitly optional; core is sized to finish |
| State-name / data drift in source | `fetch_data.py` pins/refreshes local copies; validated names match |

---

## 13. Open items for the implementation plan
- **Age bands (decided):** 0–17 / 18–39 / 40–59 / 60–79 / 80+.
- **`covid_cases` (decided):** include it for now (enables `Case Fatality %`);
  the facilitator may drop it later if time is tight.
- Final slide visual assets (finished-dashboard screenshot) — produced after the
  first `.pbix` is built.
- Marp rendering check for the English deck (reuse existing Marp setup).
