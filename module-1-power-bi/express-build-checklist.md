# Express Build Checklist — Screenshot-Ready COVID Dashboard

A condensed (~20-minute) sequence to build a presentable dashboard in Power BI
Desktop, aimed at producing the two screenshots used by the slide deck and the
catch-up manifest. It skips formatting polish, optional visuals, and the
`covid_cases` table. For the full teaching version, use
[`hands-on-guide.md`](hands-on-guide.md).

**Produces:**
- `img/03-model-star.png` — the Model view star schema
- `img/05-cards-visuals.png` — the finished one-page dashboard

**Data:** in [`data/`](data/) — `covid_deaths_linelist.csv`, `population_state.csv`.

---

## Part A — Load + transform (~7 min)

1. **Home → Get Data → Text/CSV** → load `data/covid_deaths_linelist.csv` → **Transform Data**.
2. Repeat for `data/population_state.csv` → **Transform Data**. (Skip `covid_cases` — not needed here.)
3. Rename query `covid_deaths_linelist` → **`Fact_Deaths`** (right-click → Rename).
4. **Fix date types first (important — avoids the error below).** With `Fact_Deaths`
   selected, click the `date_dose1` header, then **Ctrl-click** `date_dose2` and
   `date_dose3` (include `date` too — harmless). **Transform → Data Type → Date**;
   if prompted, choose **Replace current**. This turns empty cells into real
   `null` instead of text `""`.
   > If a locale parse error appears, use **Transform → Data Type → Using Locale… →
   > Date → English (United States)** (the CSV stores dates as `YYYY-MM-DD`).
5. **Add Column → Custom Column** three times on `Fact_Deaths` (exact name + formula):

   **`Age_Group`**
   ```
   if [age] <= 17 then "0–17"
   else if [age] <= 39 then "18–39"
   else if [age] <= 59 then "40–59"
   else if [age] <= 79 then "60–79"
   else "80+"
   ```
   **`Vaccination_Status`**
   ```
   if [date_dose2] <> null and [date_dose2] <= [date] then "Fully vaccinated (≥2 doses)"
   else if [date_dose1] <> null and [date_dose1] <= [date] then "Partial (1 dose)"
   else "Unvaccinated"
   ```
   **`Sex`** (for a slicer)
   ```
   if [male] = 1 then "Male" else "Female"
   ```
6. Select `population_state` → rename to **`Dim_State`**. Filter the `date` column to
   keep only **2024** (filter dropdown → Date Filters → Year = 2024). Then
   **Add Column → Custom Column** named **`Population`**: `[population] * 1000`.
   > Tidy (optional but recommended): **Home → Choose Columns** and keep only
   > `state` and `Population`. If a stray `Population.1` appears (because a
   > `population` column already existed), remove the old one and rename the new
   > custom column to `Population`.
7. **Home → Close & Apply.**

## Part B — Model (~4 min)

8. **Modeling → New table**, paste:
   ```DAX
   Dim_Date =
   ADDCOLUMNS (
       CALENDAR ( DATE ( 2020, 1, 1 ), DATE ( 2024, 12, 31 ) ),
       "Year", YEAR ( [Date] ),
       "MonthName", FORMAT ( [Date], "mmm" ),
       "YearMonth", FORMAT ( [Date], "YYYY-MM" )
   )
   ```
9. Switch to **Model view**. Create 2 relationships by dragging:
   - `Fact_Deaths[date]` → `Dim_Date[Date]`
   - `Fact_Deaths[state]` → `Dim_State[state]`
10. Drag the three tables into a tidy **star layout**: `Dim_Date` and `Dim_State` on
    the sides, `Fact_Deaths` in the middle. *(This is screenshot #1 — see Part D.)*

## Part C — Measures + visuals (~7 min)

11. **Modeling → New measure** ×4. Create them **one at a time**: type the name,
    press Enter, then paste the formula after `=`. **Do not paste the whole block
    into one box** (that causes a "circular dependency" error).
    ```DAX
    Total Deaths       = COUNTROWS ( 'Fact_Deaths' )
    % Unvaccinated     = DIVIDE ( CALCULATE ( [Total Deaths], 'Fact_Deaths'[Vaccination_Status] = "Unvaccinated" ), [Total Deaths] )
    % With Comorbidity = DIVIDE ( SUM ( 'Fact_Deaths'[comorb] ), [Total Deaths] )
    Median Age         = MEDIAN ( 'Fact_Deaths'[age] )
    ```
    > Circular-dependency error? Click the `Total Deaths` measure and confirm its
    > formula bar reads exactly `Total Deaths = COUNTROWS('Fact_Deaths')` — if it
    > holds any `DIVIDE`/`CALCULATE` or a `[Total Deaths]` reference, the wrong
    > formula was pasted into it; overwrite it.

    Select the two `%` measures → **Measure tools → Format → Percentage** (1 decimal).
12. **Report view** — build these (click a visual in the Visualizations pane, then
    drag fields):
    - **4 Cards:** `Total Deaths`, `% Unvaccinated`, `% With Comorbidity`, `Median Age` → row across the top.
    - **Line chart:** X = `Dim_Date[Date]`, Y = `Total Deaths`.
    - **Clustered bar:** Y = `Dim_State[state]`, X = `Total Deaths`.
    - **Clustered column:** X = `Age_Group`, Y = `Total Deaths`.
    - **Donut:** Legend = `Vaccination_Status`, Values = `Total Deaths`.
    - *(Optional)* **Slicer:** `Sex`.
13. Arrange the 4 charts in a 2×2 grid under the cards; resize so nothing overlaps.

## Part D — Capture (~2 min)

Use **Win + Shift + S** (Snipping Tool), rectangular snip:

- **Model view** → snip the diagram area → save as `img/03-model-star.png`.
- **Report view** → snip just the report canvas (not the menus/panes) → save as
  `img/05-cards-visuals.png`.

> Tip: collapse the Filters/Visualizations panes before snipping the dashboard for
> a cleaner frame; a 16:9-ish crop matches the slides best.

Optionally save the file as a checkpoint `.pbix` while you're here.

---

## After capturing

Re-render the deck so the images embed:
```bash
npx -y @marp-team/marp-cli slides/module-1-power-bi.md --pdf  -o slides/build/module-1-power-bi.pdf  --allow-local-files
npx -y @marp-team/marp-cli slides/module-1-power-bi.md --pptx -o slides/build/module-1-power-bi.pptx --allow-local-files
```
