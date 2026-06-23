# Hands-on Guide — Build a COVID-19 Dashboard in Power BI

This guide walks you, step by step, through building an interactive COVID-19 mortality dashboard in Power BI Desktop, using real (anonymised) Malaysian COVID-19 data. It is your safety net: the facilitator will demo each step live, but if you fall behind, get stuck, or need to double-check a formula, everything you need is written out here — including the exact custom-column formulas, DAX measures, and checkpoint files you can use to rejoin the class at any point.

## Ground rules

1. **Bring your own laptop** with Power BI Desktop installed (Windows only — there is no Mac version). Confirm it opens before the session starts.
2. **Use the local CSV files**, not the internet. All three datasets you need are already in `modul-1-power-bi/data/`:
   - `covid_deaths_linelist.csv` — one row per COVID-19 death (~37,351 rows). Will become table **Fact_Deaths**.
   - `covid_cases.csv` — daily new cases by state. Will become table **covid_cases**.
   - `population_state.csv` — population by state. Will become table **Dim_State**.
3. The facilitator will demo **Get Data → Web** once, pointed at the data.gov.my open data catalogue, just to show you what URL-based ingestion looks like. **You do not need to do this.** Web ingestion depends on internet stability and government proxy/firewall settings, which can fail mid-class — so everyone builds from the local CSVs for reliability.
4. **Save your file regularly** (Ctrl+S) and give it a sensible name, e.g. `MyName-covid-dashboard.pbix`.
5. **Checkpoints**: at six points in this guide, the facilitator has a matching saved `.pbix` checkpoint file. If you fall behind or something breaks, do not panic — ask for the nearest checkpoint file, open it, and continue from there. The checkpoints are:
   - `00-start.pbix` — the 3 CSVs loaded, nothing transformed yet
   - `01-powerquery.pbix` — after all Power Query transforms (custom columns + Dim_State)
   - `02-model.pbix` — after Dim_Date, Mark as date table, and the 4 relationships
   - `03-dax.pbix` — after all 10 measures are created
   - `04-visuals.pbix` — after the 6 core visuals
   - `05-final.pbix` — after slicers/interactivity (+ any optional showcase)
6. If you are ever unsure which menu to click, the exact button names are given in **bold** throughout this guide.

---

## Part 1 — Ingest + Power Query

**Goal at the end of this part:** all three tables loaded and transformed, reaching checkpoint `01-powerquery`.

### 1.1 Load the three CSV files

1. Open Power BI Desktop. Go to **Home → Get Data → Text/CSV**.
2. Browse to `modul-1-power-bi/data/covid_deaths_linelist.csv` and select it. Click **Transform Data** (not Load) so it opens in Power Query Editor.
3. Repeat **Home → Get Data → Text/CSV** for `covid_cases.csv` and for `population_state.csv`. Click **Transform Data** for each, so all three open as queries in the same Power Query Editor window.

You should now have three queries listed on the left: `covid_deaths_linelist`, `covid_cases`, `population_state`.

> This is checkpoint **`00-start`** — three CSVs loaded, nothing transformed yet.

### 1.2 Rename the deaths table to Fact_Deaths

1. In the Queries pane, right-click `covid_deaths_linelist` → **Rename**.
2. Rename it to `Fact_Deaths`.

`covid_cases` keeps its name as-is.

### 1.3 Add custom columns on Fact_Deaths

With `Fact_Deaths` selected, use **Add Column → Custom Column** for each of the columns below. Type the column name exactly, and paste the formula into the formula box exactly as shown (these are valid Power Query M expressions).

**Sex**

```
if [male] = 1 then "Male" else "Female"
```

**Age_Group**

You may build this using **Add Column → Conditional Column** if you prefer the dialog, but the underlying logic — and the exact formula to type if you use Custom Column — is:

```
if [age] <= 17 then "0–17"
else if [age] <= 39 then "18–39"
else if [age] <= 59 then "40–59"
else if [age] <= 79 then "60–79"
else "80+"
```

**Vaccination_Status**

```
if [date_dose2] <> null and [date_dose2] <= [date] then "Fully vaccinated (≥2 doses)"
else if [date_dose1] <> null and [date_dose1] <= [date] then "Partial (1 dose)"
else "Unvaccinated"
```

**Comorbidity**

```
if [comorb] = 1 then "Yes" else "No"
```

**Citizenship**

```
if [malaysian] = 1 then "Malaysian" else "Non-citizen"
```

**BID_Label**

```
if [bid] = 1 then "Yes" else "No"
```

After adding all six, check the Applied Steps pane on the right — you should see six new "Added Custom" / "Added Conditional Column" steps, in addition to the original "Changed Type" step.

> **Tip:** if you make a typo, click the gear icon next to the relevant step in Applied Steps to edit the formula again, rather than deleting and redoing it.

### 1.4 Build Dim_State from population_state

1. Select the `population_state` query. Right-click → **Rename** → `Dim_State`.
2. Filter the rows: click the filter arrow on the `date` column → **Date Filters** (or use **Add Column → Custom Column** with a filter step) to keep only rows where the year is 2024. In practice: use the column filter dropdown and keep rows where `Date.Year([date]) = 2024`.
   - Note: in a fuller open-data extract you would also filter `sex = "both"`, `age = "overall"`, `ethnicity = "overall"` — but the local `population_state.csv` is **already pre-filtered** to those breakdowns (it only has columns `state, date, population`), so filtering by year 2024 is all that's needed here.
3. Add **Add Column → Custom Column** named `Population`:
   ```
   [population] * 1000
   ```
   (the source `population` column is in thousands, so multiplying by 1000 gives actual head-count).
4. Add another **Add Column → Custom Column** named `Region`:
   ```
   if List.Contains({"Sabah","Sarawak","W.P. Labuan"}, [state]) then "Borneo" else "Semenanjung"
   ```
5. Remove columns you no longer need so that `Dim_State` ends with just three columns: `state`, `Region`, `Population`. Right-click any extra column → **Remove Columns**, or use **Choose Columns** to keep only these three.
6. Confirm the result is 16 rows (one per Malaysian state).

### 1.5 Load everything

Click **Home → Close & Apply** to load the transformed tables into the data model.

> This is checkpoint **`01-powerquery`** — all Power Query transforms done (custom columns on Fact_Deaths, Dim_State built).

---

## Part 2 — Data model

**Goal at the end of this part:** a working star schema with a date dimension, marked as a date table, and 4 relationships wired up — reaching checkpoint `02-model`.

### 2.1 Create the Dim_Date table

1. Go to **Modeling → New table**.
2. Type the table name and paste this DAX formula exactly:

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

3. Press Enter. A new `Dim_Date` table appears in the Fields pane with columns `Date`, `Year`, `MonthNo`, `MonthName`, `YearMonth`.

### 2.2 Mark Dim_Date as the official date table

1. Switch to **Model view** (or Table view) on the left-hand navigation.
2. Select the `Dim_Date` table.
3. Go to **Table tools → Mark as date table** (or right-click the table → **Mark as date table**).
4. In the dialog, choose `Dim_Date[Date]` as the date column and confirm.

This step is required for time-intelligence functions like `TOTALYTD` to work correctly later.

### 2.3 Create the relationships

Switch to **Model view**. Drag to create each relationship (or use **Modeling → Manage relationships → New**). All four are **many-to-one**, single cross-filter direction (from the "many" side filtering the "one" side):

| From (many) | To (one) |
|---|---|
| `Fact_Deaths[date]` | `Dim_Date[Date]` |
| `Fact_Deaths[state]` | `Dim_State[state]` |
| `covid_cases[date]` | `Dim_Date[Date]` |
| `covid_cases[state]` | `Dim_State[state]` |

After this, your model view should show `Dim_Date` and `Dim_State` in the middle as dimension tables, with `Fact_Deaths` and `covid_cases` both connected to them — a star schema.

> This is checkpoint **`02-model`** — Dim_Date created, marked as date table, and all 4 relationships wired up.

---

## Break (15 minutes)

Stretch, grab a drink, ask the facilitator any questions one-on-one. If your model isn't quite right yet, this is a good time to load checkpoint `02-model.pbix` so you start Part 3 on solid ground.

---

## Part 3 — DAX measures

**Goal at the end of this part:** all 10 measures created, reaching checkpoint `03-dax`.

For each measure: select the `Fact_Deaths` table in the Fields pane (or whichever table is noted), go to **Modeling → New measure**, and type the formula exactly as shown. Press Enter to confirm.

```DAX
Total Deaths        = COUNTROWS ( 'Fact_Deaths' )
% Brought-in-Dead   = DIVIDE ( SUM ( 'Fact_Deaths'[bid] ), [Total Deaths] )
% With Comorbidity  = DIVIDE ( SUM ( 'Fact_Deaths'[comorb] ), [Total Deaths] )
% Unvaccinated      = DIVIDE (
                          CALCULATE ( [Total Deaths], 'Fact_Deaths'[Vaccination_Status] = "Unvaccinated" ),
                          [Total Deaths] )
Median Age          = MEDIAN ( 'Fact_Deaths'[age] )
Total Population    = SUM ( 'Dim_State'[Population] )
Deaths per 100k      = DIVIDE ( [Total Deaths], [Total Population] ) * 100000
Deaths YTD           = TOTALYTD ( [Total Deaths], 'Dim_Date'[Date] )
Total Cases          = SUM ( 'covid_cases'[cases_new] )
Case Fatality %      = DIVIDE ( [Total Deaths], [Total Cases] )
```

Notes:
- `Total Population` should be created with `Dim_State` selected (it sums `Dim_State[Population]`).
- `Total Cases` should be created with `covid_cases` selected (it sums `covid_cases[cases_new]`).
- All other measures can live on `Fact_Deaths`.
- `Deaths YTD` only works correctly because `Dim_Date` was marked as the date table in Part 2.

### 3.1 Format the measures

1. Select each `% …` measure (`% Brought-in-Dead`, `% With Comorbidity`, `% Unvaccinated`, `Case Fatality %`) and on the **Measure tools** ribbon, set the format to **Percentage** with 1–2 decimal places.
2. Select `Deaths per 100k` and set its format to a **Decimal number** with 1 decimal place.

> This is checkpoint **`03-dax`** — all 10 measures created and formatted.

---

## Part 4 — Visuals

**Goal at the end of this part:** the 6 core visuals on the report canvas, reaching checkpoint `04-visuals`.

Switch to the **Report view**. Build the following on the canvas (use **Insert visual** from the Visualizations pane, or drag fields onto a blank canvas area which auto-suggests a visual):

1. **4 KPI cards** — insert a **Card** visual for each of:
   - `Total Deaths`
   - `% Unvaccinated`
   - `% With Comorbidity`
   - `Median Age`
2. **Line chart** — X-axis `Dim_Date[Date]`, Values `Total Deaths`. This shows the COVID-19 waves over time.
3. **Bar chart** (clustered bar) — Axis `Dim_State[state]`, Values `Total Deaths`.
4. **Column chart** (clustered column) — Axis `Age_Group`, Values `Total Deaths`.
5. **Donut chart** — Legend `Vaccination_Status`, Values `Total Deaths`.

Arrange the cards along the top of the canvas, and the four charts in a 2x2 grid below them. Resize and align so nothing overlaps.

> This is checkpoint **`04-visuals`** — the 6 core visuals are placed on the canvas.

---

## Part 5 — Interactivity + optional showcase

**Goal at the end of this part:** slicers wired up (and, time permitting, showcase visuals added), reaching checkpoint `05-final`.

### 5.1 Add the 4 slicers

Insert a **Slicer** visual for each of the following fields:

1. `Dim_State[state]`
2. `Sex`
3. `Comorbidity`
4. `Dim_Date[Date]` — set this slicer's format to **Between** (a date range slider) via the Slicer settings in the Format pane.

Place all four slicers along one side of the canvas (e.g. the top or left) so they filter every visual at once. Click through a state and a vaccination category to confirm the cards and charts respond.

### 5.2 Optional showcase (only if your group is keeping pace)

If you have time left, add any of the following. If you are behind schedule, skip this whole section and go straight to wrap-up.

- **Filled map** — Location `Dim_State[state]`, Color saturation `Deaths per 100k`.
  - **Important:** Power BI's map visuals require an internet connection and use the Bing Maps service, which is sometimes **disabled on government tenants/networks**. If the map visual fails to render or shows an error, this is expected on some KKM machines — the **bar chart by state from Part 4 is the reliable, core default**, and the filled map is only an optional swap-in when maps are available.
- **Decomposition tree** — Analyze `Total Deaths`, Explain by `Age_Group` → `Comorbidity` → `Vaccination_Status`.
- **Per-state drillthrough page** — create a new page, set `Dim_State[state]` as a drillthrough filter, and right-click a state bar on the main page → **Drillthrough**.
- A **`Case Fatality %` card** (this uses the `covid_cases` table via the `Total Cases` measure).

> This is checkpoint **`05-final`** — slicers added and working (plus any optional showcase visuals you had time for).

---

## Facilitator pacing

| Block | Time | Mins | Checkpoint reached |
|---|---|---|---|
| Theory (slides) | 8:00–8:30 | 30 | — |
| Part 1 Ingest + Power Query | 8:30–9:20 | 50 | 00-start, 01-powerquery |
| Part 2 Data model | 9:20–9:45 | 25 | 02-model |
| Break | 9:45–10:00 | 15 | — |
| Part 3 DAX measures | 10:00–10:30 | 30 | 03-dax |
| Part 4 Visuals | 10:30–11:10 | 40 | 04-visuals |
| Part 5 Interactivity + free explore + Q&A | 11:10–11:30 | 20 | 05-final |

If you fall behind, open the nearest checkpoint `.pbix` and rejoin; skip optional showcase items first when short on time.
