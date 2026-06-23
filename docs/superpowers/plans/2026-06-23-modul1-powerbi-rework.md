# Modul 1 Power BI Rework — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers-extended-cc:subagent-driven-development (recommended) or superpowers-extended-cc:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Modul 1's synthetic-admissions content with a 30-min English theory deck plus a follow-along live build of an interactive COVID-19 dashboard on real data.gov.my data, taught via a star schema.

**Architecture:** Content/data deliverables in a training repo — no application code. A Python `fetch_data.py` (duckdb) pins three open datasets to local CSV; a Marp slide deck delivers theory; a single `hands-on-guide.md` drives the follow-along build (Power Query → star schema → DAX → visuals) with facilitator-built checkpoint `.pbix` files (gitignored). Old synthetic labs are deleted.

**Tech Stack:** Markdown, Marp CLI (`@marp-team/marp-cli` via npx), Python 3.13 + duckdb, Power BI Desktop (consumed by participants, not built in CI), data.gov.my / DOSM open parquet.

**User decisions (already made):**
- "Follow-along — everyone builds on their own laptop."
- "Full star: Deaths + Date + State + Population."
- "Replace entirely with COVID build" (retire old synthetic labs/data/BOR-ALOS).
- Dashboard scope: "Standard core + optional showcase extras if pace allows."
- "Everything in Module 1 English" (slides, README, hands-on guide). Module 2 stays Malay.
- Theory deck adds a "5 types of analytics" slide.
- Age bands: 0–17 / 18–39 / 40–59 / 60–79 / 80+.
- Include `covid_cases` for now (Case Fatality measure); may drop later.

**Reference spec:** `docs/superpowers/specs/2026-06-23-modul1-powerbi-rework-design.md`

---

## File Structure

| Path | Responsibility | Action |
|---|---|---|
| `pyproject.toml` | add `duckdb` dependency | Modify |
| `modul-1-power-bi/data/fetch_data.py` | download + pin 3 datasets to CSV | Create |
| `modul-1-power-bi/data/covid_deaths_linelist.csv` | fact data (committed) | Generated |
| `modul-1-power-bi/data/covid_cases.csv` | cases context (committed) | Generated |
| `modul-1-power-bi/data/population_state.csv` | population dim input (committed) | Generated |
| `slides/modul-1-power-bi.md` | theory deck (English Marp) | Rewrite |
| `slides/build/modul-1-power-bi.pdf` | rendered deck (committed) | Regenerate |
| `slides/README.md` | fix Slot 1 timing/language note | Modify |
| `modul-1-power-bi/README.md` | English module overview | Rewrite |
| `modul-1-power-bi/hands-on-guide.md` | follow-along build guide | Create |
| `docs/SCREENSHOTS.md` | Modul 1 screenshot manifest | Modify |
| `modul-1-power-bi/lab/**`, `data/jana_data.py`, synthetic CSVs | old content | Delete |
| `modul-1-power-bi/img/.gitkeep` | screenshot folder for new guide | Create |

**Canonical technical artifacts** (single source of truth — every task that needs these uses these exact strings; do not improvise variants):

### Power Query custom columns on `Fact_Deaths`
```
Sex                = if [male] = 1 then "Male" else "Female"
Age_Group          = if [age] <= 17 then "0–17"
                     else if [age] <= 39 then "18–39"
                     else if [age] <= 59 then "40–59"
                     else if [age] <= 79 then "60–79"
                     else "80+"
Vaccination_Status = if [date_dose2] <> null and [date_dose2] <= [date] then "Fully vaccinated (≥2 doses)"
                     else if [date_dose1] <> null and [date_dose1] <= [date] then "Partial (1 dose)"
                     else "Unvaccinated"
Comorbidity        = if [comorb] = 1 then "Yes" else "No"
Citizenship        = if [malaysian] = 1 then "Malaysian" else "Non-citizen"
BID_Label          = if [bid] = 1 then "Yes" else "No"
```

### `Dim_State` (from population_state, in Power Query)
- Filter to `sex = "both"`, `age = "overall"`, `ethnicity = "overall"`, `Date.Year([date]) = 2024`.
- `Population = [population] * 1000` (source is in thousands).
- `Region = if List.Contains({"Sabah","Sarawak","W.P. Labuan"}, [state]) then "Borneo" else "Semenanjung"`.
- Keep columns: `state`, `Region`, `Population` (16 rows).

### `Dim_Date` (DAX calculated table)
```DAX
Dim_Date =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2020, 1, 1 ), DATE ( 2024, 12, 31 ) ),
    "Year", YEAR ( [Date] ),
    "MonthNo", MONTH ( [Date] ),
    "MonthName", FORMAT ( [Date], "mmm" ),
    "YearMonth", FORMAT ( [Date], "YYYY-MM" )
)
```
Then **Model view → Mark as date table** on `Dim_Date[Date]`.

### Relationships (all many-to-one, single direction)
- `Fact_Deaths[date]`  → `Dim_Date[Date]`
- `Fact_Deaths[state]` → `Dim_State[state]`
- `covid_cases[date]`  → `Dim_Date[Date]`
- `covid_cases[state]` → `Dim_State[state]`

### DAX measures
```DAX
Total Deaths        = COUNTROWS ( 'Fact_Deaths' )
% Brought-in-Dead   = DIVIDE ( SUM ( 'Fact_Deaths'[bid] ), [Total Deaths] )
% With Comorbidity  = DIVIDE ( SUM ( 'Fact_Deaths'[comorb] ), [Total Deaths] )
% Unvaccinated      = DIVIDE (
                          CALCULATE ( [Total Deaths], 'Fact_Deaths'[Vaccination_Status] = "Unvaccinated" ),
                          [Total Deaths] )
Median Age          = MEDIAN ( 'Fact_Deaths'[age] )
Total Population    = SUM ( 'Dim_State'[Population] )
Deaths per 100k     = DIVIDE ( [Total Deaths], [Total Population] ) * 100000
Deaths YTD          = TOTALYTD ( [Total Deaths], 'Dim_Date'[Date] )
Total Cases         = SUM ( 'covid_cases'[cases_new] )
Case Fatality %     = DIVIDE ( [Total Deaths], [Total Cases] )
```
Format `% …` measures as Percentage; `Deaths per 100k` as 1 decimal.

### Dashboard visuals
**Core:** 4 cards (Total Deaths · % Unvaccinated · % With Comorbidity · Median Age) · line chart `Dim_Date[Date]` × `Total Deaths` · bar chart `Dim_State[state]` × `Total Deaths` · column chart `Age_Group` × `Total Deaths` · donut `Vaccination_Status` · slicers (`Dim_State[state]`, `Sex`, `Comorbidity`, `Dim_Date[Date]` range).
**Optional showcase:** filled map `Dim_State[state]` × `Deaths per 100k` · decomposition tree (`Total Deaths` by Age_Group → Comorbidity → Vaccination_Status) · per-state drillthrough page · Case Fatality card.

### Checkpoint `.pbix` sequence (facilitator-built; gitignored)
`00-start` (data loaded) → `01-powerquery` (transforms) → `02-model` (Dim_Date, Dim_State, relationships) → `03-dax` (measures) → `04-visuals` (core visuals) → `05-final` (interactivity + optional extras).

---

## Task 1: Retire old synthetic Modul 1 content

**Goal:** Remove the synthetic-admissions labs, generator, and CSVs so only the new COVID storyline remains.

**Files:**
- Delete: `modul-1-power-bi/lab/01-import-data.md` … `07-eksport-simpan.md` (all 7)
- Delete: `modul-1-power-bi/lab/img/.gitkeep` (and the now-empty `lab/` dir)
- Delete: `modul-1-power-bi/data/jana_data.py`
- Delete: `modul-1-power-bi/data/disiplin.csv`, `kemasukan.csv`, `tarikh.csv`, `wad.csv`
- Create: `modul-1-power-bi/img/.gitkeep` (folder for new guide screenshots)

**Acceptance Criteria:**
- [ ] `modul-1-power-bi/lab/` no longer exists.
- [ ] No synthetic CSVs or `jana_data.py` remain under `modul-1-power-bi/data/`.
- [ ] `modul-1-power-bi/img/.gitkeep` exists.

**Verify:** `ls modul-1-power-bi/lab 2>/dev/null; ls modul-1-power-bi/data` → `lab` absent; `data` shows no `kemasukan.csv`/`jana_data.py`.

**Steps:**

- [ ] **Step 1: Delete old content**
```bash
cd /d/Dev/training/powerBI-notebookLM-Gemini
git rm -r modul-1-power-bi/lab
git rm modul-1-power-bi/data/jana_data.py modul-1-power-bi/data/disiplin.csv \
       modul-1-power-bi/data/kemasukan.csv modul-1-power-bi/data/tarikh.csv \
       modul-1-power-bi/data/wad.csv
mkdir -p modul-1-power-bi/img && touch modul-1-power-bi/img/.gitkeep
git add modul-1-power-bi/img/.gitkeep
```

- [ ] **Step 2: Verify**
```bash
ls modul-1-power-bi/lab 2>/dev/null && echo "STILL THERE" || echo "lab removed"
ls modul-1-power-bi/data
```
Expected: `lab removed`; `data` listing contains no synthetic CSVs.

- [ ] **Step 3: Commit**
```bash
git commit -m "chore: retire synthetic Modul 1 labs and data"
```

---

## Task 2: Data fetch script + pinned local datasets

**Goal:** A reproducible `fetch_data.py` that downloads the three datasets to committed CSVs, with row counts validated.

**Files:**
- Modify: `pyproject.toml` (add `duckdb` dependency)
- Create: `modul-1-power-bi/data/fetch_data.py`
- Generated (commit): `modul-1-power-bi/data/covid_deaths_linelist.csv`, `covid_cases.csv`, `population_state.csv`

**Acceptance Criteria:**
- [ ] `fetch_data.py` runs to completion and writes 3 CSVs.
- [ ] `covid_deaths_linelist.csv` has 37,351 data rows.
- [ ] `population_state.csv` is pre-filtered to `sex=both, age=overall, ethnicity=overall` (16 rows per year, one row per state-year).
- [ ] Script prints a row-count summary per file.

**Verify:** `python modul-1-power-bi/data/fetch_data.py` → prints `covid_deaths_linelist: 37351 rows` (plus the other two counts) and exits 0.

**Steps:**

- [ ] **Step 1: Add duckdb dependency**

In `pyproject.toml`, change:
```toml
dependencies = []
```
to:
```toml
dependencies = ["duckdb>=1.0"]
```
Then install: `pip install duckdb` (or `uv pip install duckdb` if using uv).

- [ ] **Step 2: Write `fetch_data.py`**
```python
"""Download and pin the open datasets used by Modul 1 to local CSV.

Source: data.gov.my (MOH) and DOSM open data. Run from anywhere:
    python modul-1-power-bi/data/fetch_data.py
"""
from pathlib import Path
import duckdb

OUT = Path(__file__).parent
SOURCES = {
    "covid_deaths_linelist":
        "https://storage.data.gov.my/healthcare/covid_deaths_linelist.parquet",
    "covid_cases":
        "https://storage.data.gov.my/healthcare/covid_cases.parquet",
}
POP_URL = "https://storage.dosm.gov.my/population/population_state.parquet"

def main() -> None:
    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs;")

    for name, url in SOURCES.items():
        dest = OUT / f"{name}.csv"
        con.execute(f"COPY (SELECT * FROM read_parquet('{url}')) "
                    f"TO '{dest.as_posix()}' (HEADER, DELIMITER ',')")
        n = con.execute(f"SELECT count(*) FROM read_parquet('{url}')").fetchone()[0]
        print(f"{name}: {n} rows -> {dest.name}")

    # Population: pre-filter to the 'overall' state totals (one row per state-year).
    pop_dest = OUT / "population_state.csv"
    con.execute(f"""
        COPY (
            SELECT state, date, population
            FROM read_parquet('{POP_URL}')
            WHERE sex = 'both' AND age = 'overall' AND ethnicity = 'overall'
            ORDER BY date, state
        ) TO '{pop_dest.as_posix()}' (HEADER, DELIMITER ',')
    """)
    n = con.execute(f"""
        SELECT count(*) FROM read_parquet('{POP_URL}')
        WHERE sex='both' AND age='overall' AND ethnicity='overall'
    """).fetchone()[0]
    print(f"population_state (filtered): {n} rows -> {pop_dest.name}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run and verify counts**
```bash
cd /d/Dev/training/powerBI-notebookLM-Gemini
python modul-1-power-bi/data/fetch_data.py
```
Expected output includes `covid_deaths_linelist: 37351 rows -> covid_deaths_linelist.csv`.

- [ ] **Step 4: Commit script + data**
```bash
git add pyproject.toml modul-1-power-bi/data/fetch_data.py \
        modul-1-power-bi/data/covid_deaths_linelist.csv \
        modul-1-power-bi/data/covid_cases.csv \
        modul-1-power-bi/data/population_state.csv
git commit -m "feat: fetch script + pinned COVID/population datasets for Modul 1"
```

---

## Task 3: Theory slide deck (English, Marp)

**Goal:** Rewrite `slides/modul-1-power-bi.md` in English (~14 slides incl. the 5-types-of-analytics slide), render the PDF, and fix the slides README note.

**Files:**
- Rewrite: `slides/modul-1-power-bi.md`
- Regenerate (commit): `slides/build/modul-1-power-bi.pdf`
- Modify: `slides/README.md` (Slot 1 line: ~30 min, note English)

**Acceptance Criteria:**
- [ ] Deck is in English, keeps the Marp front-matter (`marp: true`, `theme: gaia`, footer).
- [ ] Includes a dedicated "5 types of analytics" slide (Descriptive/Diagnostic/Predictive/Prescriptive/Continuous).
- [ ] Includes slides for: what is BI, why for KKM, the workflow, the 3 views, what is a data model, what is a measure, today's data + open-data ethics, dashboard preview, follow-along ground rules.
- [ ] Marp renders to PDF with no error.

**Verify:** `npx -y @marp-team/marp-cli slides/modul-1-power-bi.md --pdf -o slides/build/modul-1-power-bi.pdf` → exits 0 and writes the PDF.

**Steps:**

- [ ] **Step 1: Rewrite the deck** following the Section 5 outline of the spec. Keep front-matter:
```markdown
---
marp: true
theme: gaia
paginate: true
footer: 'Kursus Lanjutan KKM 2026 · Dr. Muhammad Naufal bin Nordin'
---
```
Slides (one `---`-separated section each): Title → What is Power BI → **5 types of analytics** → Why it matters for KKM → Workflow (Get Data→Transform→Model→Visualize→Share) → The 3 views → What is a data model (fact vs dimension, star schema) → What is a measure (DAX) vs a column → Today's data (data.gov.my COVID linelist; one row = one death) → Open-data ethics (safe vs patient-data rule) → Dashboard preview (screenshot placeholder) → Follow-along ground rules → "Let's build → hands-on-guide".

The analytics slide content:
```markdown
## The 5 types of analytics

- **Descriptive** — what happened? (counts, trends → *today's dashboard*)
- **Diagnostic** — why did it happen? (slicing, drill-down → *also today*)
- **Predictive** — what will happen? (forecasting → *Module 2 / AI*)
- **Prescriptive** — what should we do? (recommendations)
- **Continuous** — real-time, always-on automated analytics
```

- [ ] **Step 2: Render PDF**
```bash
npx -y @marp-team/marp-cli slides/modul-1-power-bi.md --pdf -o slides/build/modul-1-power-bi.pdf
```
Expected: exit 0, PDF updated.

- [ ] **Step 3: Update `slides/README.md`** — change the Slot 1 row to `Slot 1 — Power BI (~30 min, English)`.

- [ ] **Step 4: Commit**
```bash
git add slides/modul-1-power-bi.md slides/build/modul-1-power-bi.pdf slides/README.md
git commit -m "feat: English theory deck for Modul 1 (adds analytics types)"
```

---

## Task 4: Hands-on follow-along guide

**Goal:** Create `modul-1-power-bi/hands-on-guide.md` — the complete English follow-along build, using the canonical artifacts above, organized by the 5 build parts with checkpoints and a facilitator pacing note.

**Files:**
- Create: `modul-1-power-bi/hands-on-guide.md`

**Acceptance Criteria:**
- [ ] Sections cover, in order: Part 1 Ingest + Power Query, Part 2 Data model, Break, Part 3 DAX, Part 4 Visuals, Part 5 Interactivity + optional showcase.
- [ ] Power Query section contains the exact `Sex`, `Age_Group`, `Vaccination_Status`, `Comorbidity`, `Citizenship`, `BID_Label` formulas from the canonical block.
- [ ] Data model section contains the `Dim_State` filter/Region logic, the `Dim_Date` DAX table, "Mark as date table", and the 4 relationships.
- [ ] DAX section lists all 10 measures verbatim from the canonical block.
- [ ] Visuals section lists the 6 core visuals + 4 slicers, and the optional showcase items.
- [ ] Each of the 6 checkpoints (`00-start`…`05-final`) is named with what state it represents.
- [ ] A short "Facilitator pacing" note maps the timetable (Section 4 of spec) to checkpoints.

**Verify:** `grep -c "Vaccination_Status" modul-1-power-bi/hands-on-guide.md` ≥ 2 AND `grep -c "Deaths per 100k" modul-1-power-bi/hands-on-guide.md` ≥ 1 AND `grep -c "Mark as date table" modul-1-power-bi/hands-on-guide.md` ≥ 1.

**Steps:**

- [ ] **Step 1: Write the guide** with these sections (embed the canonical artifacts verbatim):
  1. **Intro & ground rules** — files in `modul-1-power-bi/data/`, raise hand if stuck, reload nearest checkpoint to rejoin.
  2. **Part 1 — Ingest + Power Query** (8:30–9:20): Get Data → Text/CSV for the 3 CSVs; note the one-time "Get Data → Web" demo of the data.gov.my catalogue; open Power Query; set types; add the 6 custom columns (exact formulas); build `Dim_State` from `population_state` (filter + Population×1000 + Region). Checkpoint `01-powerquery`.
  3. **Part 2 — Data model** (9:20–9:45): add `Dim_Date` DAX table; Mark as date table; create the 4 relationships in Model view; explain star schema vs one-big-table. Checkpoint `02-model`.
  4. **Break** (9:45–10:00).
  5. **Part 3 — DAX measures** (10:00–10:30): create all 10 measures (exact code); set format strings. Checkpoint `03-dax`.
  6. **Part 4 — Visuals** (10:30–11:10): 4 cards, line, bar-by-state, column-by-age, donut-by-vaccination. Checkpoint `04-visuals`.
  7. **Part 5 — Interactivity + showcase** (11:10–11:30): add 4 slicers; demo cross-filtering/drill/tooltips; optional filled map (per-100k), decomposition tree, drillthrough, Case Fatality card. Note the map-visual internet/tenant risk and the bar-chart fallback. Checkpoint `05-final`.
  8. **Facilitator pacing** — table mapping timetable blocks to checkpoints; "if behind, reload checkpoint and skip optional extras."

- [ ] **Step 2: Verify required content present**
```bash
cd /d/Dev/training/powerBI-notebookLM-Gemini
grep -c "Vaccination_Status" modul-1-power-bi/hands-on-guide.md
grep -c "Deaths per 100k" modul-1-power-bi/hands-on-guide.md
grep -c "Mark as date table" modul-1-power-bi/hands-on-guide.md
```
Expected: first ≥ 2, others ≥ 1.

- [ ] **Step 3: Commit**
```bash
git add modul-1-power-bi/hands-on-guide.md
git commit -m "feat: COVID dashboard follow-along hands-on guide"
```

---

## Task 5: Rewrite Modul 1 README (English)

**Goal:** Rewrite `modul-1-power-bi/README.md` in English to describe the new theory + follow-along structure, dataset, and how to fetch data.

**Files:**
- Rewrite: `modul-1-power-bi/README.md`

**Acceptance Criteria:**
- [ ] English. Describes the 30-min theory + ~2.5-hr follow-along split and the Slot 1 timetable.
- [ ] Documents the 3 datasets + `python data/fetch_data.py` to (re)generate them.
- [ ] Links to `hands-on-guide.md` and the slide deck.
- [ ] States data is open/aggregate (no real patient data) and links the prerequisite `../00-persediaan/`.
- [ ] No references to the deleted synthetic labs / `jana_data.py` / BOR-ALOS.

**Verify:** `grep -i "jana_data\|kemasukan\|BOR\|ALOS" modul-1-power-bi/README.md` → no matches; `grep -c "hands-on-guide" modul-1-power-bi/README.md` ≥ 1.

**Steps:**

- [ ] **Step 1: Rewrite** with sections: title + slot line; what you'll build (one-line dashboard description); Slot 1 timetable table (from spec Section 4); Datasets table (3 files + sources) and `python data/fetch_data.py`; how to follow (`hands-on-guide.md`, checkpoints); slide deck link (`../slides/modul-1-power-bi.md`); data-safety note; prerequisite link.

- [ ] **Step 2: Verify**
```bash
cd /d/Dev/training/powerBI-notebookLM-Gemini
grep -i "jana_data\|kemasukan\|BOR\|ALOS" modul-1-power-bi/README.md && echo "STALE REF" || echo "clean"
grep -c "hands-on-guide" modul-1-power-bi/README.md
```
Expected: `clean`; count ≥ 1.

- [ ] **Step 3: Commit**
```bash
git add modul-1-power-bi/README.md
git commit -m "docs: rewrite Modul 1 README for COVID build (English)"
```

---

## Task 6: Update screenshot manifest for new build

**Goal:** Replace the Modul 1 section of `docs/SCREENSHOTS.md` so it lists screenshots for the new follow-along guide (stored in `modul-1-power-bi/img/`), removing references to deleted labs.

**Files:**
- Modify: `docs/SCREENSHOTS.md` (Modul 1 table only; leave Modul 2 untouched)

**Acceptance Criteria:**
- [ ] Modul 1 table points at `modul-1-power-bi/img/` (not `lab/img/`).
- [ ] Rows correspond to the new build steps (e.g. get-data CSV, Power Query custom column, model/relationships, new measure, core visuals, slicers/dashboard, optional map).
- [ ] No rows reference old lab numbers/filenames (`01-get-data` admissions context, `kemasukan`, etc.).

**Verify:** `grep -n "lab/img\|kemasukan\|Tempoh_Tinggal" docs/SCREENSHOTS.md` → no matches in the Modul 1 section.

**Steps:**

- [ ] **Step 1: Replace the Modul 1 table** with rows mapping the new guide (folder `modul-1-power-bi/img/`). Suggested rows:
  `01-get-data-csv.png` (Get Data → Text/CSV), `02-custom-column-agegroup.png` (Age_Group conditional), `02-custom-column-vaccine.png` (Vaccination_Status), `03-model-star.png` (Model view, 4 relationships), `03-mark-date-table.png`, `04-new-measure.png` (Deaths per 100k), `05-cards-visuals.png` (core visuals), `06-slicers-dashboard.png` (slicers + cross-filter), `07-map-per100k.png` (optional filled map).

- [ ] **Step 2: Verify**
```bash
cd /d/Dev/training/powerBI-notebookLM-Gemini
grep -n "lab/img\|kemasukan\|Tempoh_Tinggal" docs/SCREENSHOTS.md || echo "clean"
```
Expected: `clean`.

- [ ] **Step 3: Commit**
```bash
git add docs/SCREENSHOTS.md
git commit -m "docs: refresh Modul 1 screenshot manifest for COVID build"
```

---

## Self-Review

- **Spec coverage:** timetable (Task 4 pacing + Task 5 README) ✓; theory deck incl. analytics types (Task 3) ✓; data + ingestion + fetch script (Task 2) ✓; star schema + population-in-Dim_State (canonical block, Task 4) ✓; Power Query transforms incl. age bands + vaccination status (Task 4) ✓; DAX incl. per-100k + Case Fatality (Task 4) ✓; dashboard core + optional (Task 4) ✓; map risk/fallback (Task 4) ✓; retire old content (Task 1) ✓; English everywhere (Tasks 3–5) ✓; screenshot manifest (Task 6) ✓; checkpoint `.pbix` sequence documented, gitignored (Task 4) ✓.
- **Placeholders:** none — all DAX/M/relationships given verbatim in the canonical block.
- **Type consistency:** column/measure/table names (`Fact_Deaths`, `Dim_State`, `Dim_Date`, `Vaccination_Status`, `Deaths per 100k`) are identical across all tasks.

**Note on `.pbix`:** binary and gitignored; built by the facilitator from the guide. The plan deliberately produces no `.pbix` in CI — the guide + pinned data make them reproducible.
