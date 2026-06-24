# Module 2 Gemini Canvas Dashboard Lab — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers-extended-cc:subagent-driven-development (recommended) or superpowers-extended-cc:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Module 2 hands-on lab where trainees feed Module 1's COVID figures into Gemini Canvas (via a fixed Malay prompt) to generate a "Malaysia Covid Insights" web dashboard.

**Architecture:** A duckdb script aggregates Module 1's deaths line-list into five tiny tables, pre-computed for sex = All/Male/Female, and self-verifies the All slice against the Module 1 dashboard screenshot. A new lab file embeds those tables inline plus the verbatim Malay hero prompt. The existing `05-explore-further.md` is renumbered to `06`, and the README lab map is updated.

**Tech Stack:** Python 3.13 + duckdb (run via `uv run`), Markdown.

**User decisions (already made):**
- "Approach A works, go with it" — five labeled tables, one per chart.
- Data delivery = "Paste inline in prompt" (no file upload).
- Lab placement = "Insert as new 05, bump explore-further to 06".
- Trend granularity = "Year".
- "the covid data provided is public dataset, so no worries" — no synthetic-data caveat.
- Hero prompt stays Malay verbatim; surrounding instructions in English.
- Values must match the Module 1 images (`05-cards-visuals.png`): 37K / 60.2% / 78.8% / 64.00.

**Spec:** `docs/superpowers/specs/2026-06-24-module-2-gemini-canvas-dashboard-design.md`

---

## File Structure

| File | Responsibility |
|---|---|
| `module-2-notebooklm-gemini/data/aggregate_dashboard_data.py` | Reads Module 1 deaths CSV; emits aggregated CSV + paste blocks; self-verifies vs screenshot |
| `module-2-notebooklm-gemini/data/covid_dashboard_aggregated.csv` | Generated source-of-truth (long format: `table,sex,category,value`) |
| `module-2-notebooklm-gemini/lab/05-gemini-canvas-dashboard.md` | The new hands-on lab |
| `module-2-notebooklm-gemini/lab/06-explore-further.md` | Renamed from `05-explore-further.md` (content unchanged) |
| `module-2-notebooklm-gemini/README.md` | Lab map + Main Workflows updated |

---

## Task 1: Aggregation script + verified source CSV

**Goal:** A duckdb script that aggregates the Module 1 deaths line-list into five tables (pre-computed for All/Male/Female), writes the source CSV, prints copy-paste blocks, and fails loudly if the All slice does not match the Module 1 dashboard screenshot.

> **USER-ORDERED GATE — NON-SKIPPABLE.** This task was requested by the user in the current conversation. It MUST NOT be closed by walking around it, by declaring it "verified inline", or by substituting a cheaper check. Close only after every item in `acceptanceCriteria` has been re-validated independently, with output captured.

**Files:**
- Create: `module-2-notebooklm-gemini/data/aggregate_dashboard_data.py`
- Generate (by running): `module-2-notebooklm-gemini/data/covid_dashboard_aggregated.csv`

**Acceptance Criteria:**
- [ ] Script runs clean: `uv run python module-2-notebooklm-gemini/data/aggregate_dashboard_data.py`
- [ ] Prints `VERIFICATION PASSED` — All slice: `total_deaths=37351`, `pct_unvaccinated≈60.2`, `pct_comorbidity≈78.8`, `median_age≈64.0`
- [ ] Writes `covid_dashboard_aggregated.csv` with header `table,sex,category,value` and rows for all five tables × {All, Male, Female}
- [ ] Prints five labeled paste blocks (KPI + four breakdowns) to stdout

**Verify:** `uv run python module-2-notebooklm-gemini/data/aggregate_dashboard_data.py` → ends with `VERIFICATION PASSED` and exit code 0; `head -1 module-2-notebooklm-gemini/data/covid_dashboard_aggregated.csv` → `table,sex,category,value`

**Steps:**

- [ ] **Step 1: Write the script**

Create `module-2-notebooklm-gemini/data/aggregate_dashboard_data.py`:

```python
"""Aggregate Module 1's COVID deaths line-list into the small tables the
Module 2 Gemini Canvas dashboard lab pastes into Gemini.

Derived-column logic is identical to module-1-power-bi/hands-on-guide.md, so
the figures tie out to the Module 1 dashboard screenshot
(module-1-power-bi/img/05-cards-visuals.png).

Run:
    uv run python module-2-notebooklm-gemini/data/aggregate_dashboard_data.py
"""
from pathlib import Path
import csv
import duckdb

HERE = Path(__file__).parent
SRC = (HERE.parent.parent / "module-1-power-bi" / "data"
       / "covid_deaths_linelist.csv")
OUT = HERE / "covid_dashboard_aggregated.csv"

# All-slice targets from the Module 1 dashboard screenshot.
TARGETS = {"total_deaths": 37351, "pct_unvaccinated": 60.2,
           "pct_comorbidity": 78.8, "median_age": 64.0}

DERIVED = f"""
CREATE OR REPLACE VIEW deaths AS
SELECT *,
    CASE WHEN male = 1 THEN 'Male' ELSE 'Female' END AS Sex,
    CASE WHEN age <= 17 THEN '0–17'
         WHEN age <= 39 THEN '18–39'
         WHEN age <= 59 THEN '40–59'
         WHEN age <= 79 THEN '60–79'
         ELSE '80+' END AS Age_Group,
    CASE WHEN date_dose2 IS NOT NULL AND date_dose2 <= "date"
              THEN 'Fully vaccinated (≥2 doses)'
         WHEN date_dose1 IS NOT NULL AND date_dose1 <= "date"
              THEN 'Partial (1 dose)'
         ELSE 'Unvaccinated' END AS Vaccination_Status,
    CAST(year("date") AS VARCHAR) AS yr
FROM read_csv_auto('{SRC.as_posix()}', nullstr='', sample_size=-1);
"""

KPI_SQL = """
SELECT coalesce(Sex, 'All') AS sex,
       count(*) AS total_deaths,
       round(100.0 * count(*) FILTER (WHERE Vaccination_Status = 'Unvaccinated')
             / count(*), 1) AS pct_unvaccinated,
       round(100.0 * sum(comorb) / count(*), 1) AS pct_comorbidity,
       round(median(age), 2) AS median_age
FROM deaths
GROUP BY GROUPING SETS ((Sex), ())
ORDER BY (sex = 'All') DESC, sex;
"""


def by_dim(con, col, by_deaths=False):
    """Deaths per category × {All, Male, Female} for one breakdown column."""
    order = "deaths DESC" if by_deaths else "category"
    sql = f"""
    SELECT coalesce(Sex, 'All') AS sex, CAST({col} AS VARCHAR) AS category,
           count(*) AS deaths
    FROM deaths
    GROUP BY GROUPING SETS ((Sex, {col}), ({col}))
    ORDER BY (sex = 'All') DESC, sex, {order};
    """
    return con.execute(sql).fetchall()


def pivot(rows):
    """rows: (sex, category, deaths) -> ordered categories + {category: {sex: n}}."""
    cats, table = [], {}
    for sex, category, deaths in rows:
        if category not in table:
            cats.append(category)
            table[category] = {}
        table[category][sex] = deaths
    return cats, table


def print_block(title, header, lines):
    print(f"\n### {title}")
    print("```")
    print(header)
    for ln in lines:
        print(ln)
    print("```")


def main():
    con = duckdb.connect()
    con.execute(DERIVED)

    kpi = con.execute(KPI_SQL).fetchall()
    years = by_dim(con, "yr")
    states = by_dim(con, "state", by_deaths=True)
    ages = by_dim(con, "Age_Group", by_deaths=True)
    vacc = by_dim(con, "Vaccination_Status", by_deaths=True)

    # --- Verification gate (All slice vs Module 1 screenshot) ---
    all_row = next(r for r in kpi if r[0] == "All")
    got = {"total_deaths": all_row[1], "pct_unvaccinated": all_row[2],
           "pct_comorbidity": all_row[3], "median_age": all_row[4]}
    tol = {"total_deaths": 0, "pct_unvaccinated": 0.1,
           "pct_comorbidity": 0.1, "median_age": 0.5}
    print("Verification (All slice vs Module 1 screenshot):")
    ok = True
    for k, want in TARGETS.items():
        passed = abs(got[k] - want) <= tol[k]
        ok = ok and passed
        print(f"  {k:18} got={str(got[k]):>10}  want={str(want):>8}  "
              f"{'OK' if passed else 'FAIL'}")
    if not ok:
        raise SystemExit("VERIFICATION FAILED — reconcile derived-column logic "
                         "against module-1-power-bi/hands-on-guide.md")
    print("VERIFICATION PASSED")

    # --- Write the long-format source-of-truth CSV ---
    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["table", "sex", "category", "value"])
        for sex, total, unvacc, comorb, med in kpi:
            w.writerow(["kpi", sex, "total_deaths", total])
            w.writerow(["kpi", sex, "pct_unvaccinated", unvacc])
            w.writerow(["kpi", sex, "pct_comorbidity", comorb])
            w.writerow(["kpi", sex, "median_age", med])
        for name, rows in [("deaths_by_year", years),
                           ("deaths_by_state", states),
                           ("deaths_by_age_group", ages),
                           ("deaths_by_vacc_status", vacc)]:
            for sex, category, deaths in rows:
                w.writerow([name, sex, category, deaths])
    print(f"\nWrote {OUT.relative_to(HERE.parent.parent)}")

    # --- Print copy-paste blocks for the lab ---
    print("\n" + "=" * 60)
    print("PASTE BLOCKS FOR THE LAB (copy each into 05-gemini-canvas-dashboard.md)")
    print("=" * 60)

    print_block(
        "KPI table", "sex,total_deaths,pct_unvaccinated,pct_comorbidity,median_age",
        [f"{s},{t},{u},{c},{m}" for s, t, u, c, m in kpi])

    for title, rows in [("Deaths by year", years),
                        ("Deaths by state", states),
                        ("Deaths by age group", ages),
                        ("Deaths by vaccination status", vacc)]:
        cats, table = pivot(rows)
        header = "category,All,Male,Female"
        lines = [f"{cat},{table[cat].get('All', 0)},"
                 f"{table[cat].get('Male', 0)},{table[cat].get('Female', 0)}"
                 for cat in cats]
        print_block(title, header, lines)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the script and confirm verification passes**

Run: `uv run python module-2-notebooklm-gemini/data/aggregate_dashboard_data.py`
Expected: a `Verification (...)` block where every line ends `OK`, then `VERIFICATION PASSED`, then `Wrote module-2-notebooklm-gemini/data/covid_dashboard_aggregated.csv`, then the five labeled paste blocks. Exit code 0.

If any line says `FAIL`: the derived-column logic diverged from Module 1. Compare the `CASE` expressions against `module-1-power-bi/hands-on-guide.md` §1.3 (Sex/Age_Group/Vaccination_Status) before continuing. Do NOT loosen `TARGETS` or `tol` to force a pass.

- [ ] **Step 3: Capture the stdout paste blocks**

Re-run and save the output for Task 2 (the lab embeds these verbatim):
Run: `uv run python module-2-notebooklm-gemini/data/aggregate_dashboard_data.py > /tmp/paste-blocks.txt`
Keep `/tmp/paste-blocks.txt` — Task 2 copies the five blocks from it.

- [ ] **Step 4: Commit**

```bash
git add module-2-notebooklm-gemini/data/aggregate_dashboard_data.py \
        module-2-notebooklm-gemini/data/covid_dashboard_aggregated.csv
git commit -m "feat(m2): aggregate Module 1 deaths into dashboard CSV + paste blocks

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: New lab file + renumber explore-further

**Goal:** Create `05-gemini-canvas-dashboard.md` (bridge intro → paste the five tables → paste the Malay hero prompt → iterate → expected outcome) and rename the existing closing lab from `05` to `06`.

**Files:**
- Rename: `module-2-notebooklm-gemini/lab/05-explore-further.md` → `module-2-notebooklm-gemini/lab/06-explore-further.md`
- Create: `module-2-notebooklm-gemini/lab/05-gemini-canvas-dashboard.md`

**Acceptance Criteria:**
- [ ] `06-explore-further.md` exists with content identical to the old `05-explore-further.md`; old `05-explore-further.md` no longer exists
- [ ] `05-gemini-canvas-dashboard.md` contains: goal, a Module 1→2 bridge intro, the five data paste blocks (verbatim from Task 1 stdout), the Malay hero prompt verbatim in a code block, an iterate step, and an expected-outcome section
- [ ] The five paste blocks' All-slice KPI values read 37351 / 60.2 / 78.8 / 64.0
- [ ] No file-upload step (inline paste only)

**Verify:** `ls module-2-notebooklm-gemini/lab/` shows `05-gemini-canvas-dashboard.md` and `06-explore-further.md` (no `05-explore-further.md`); `grep -c "Malaysia Covid Insights" module-2-notebooklm-gemini/lab/05-gemini-canvas-dashboard.md` ≥ 1

**Steps:**

- [ ] **Step 1: Rename the explore-further lab (preserve history)**

```bash
git mv module-2-notebooklm-gemini/lab/05-explore-further.md \
       module-2-notebooklm-gemini/lab/06-explore-further.md
```

- [ ] **Step 2: Create the new lab file**

Create `module-2-notebooklm-gemini/lab/05-gemini-canvas-dashboard.md`. Replace each `<<< paste block: ... >>>` marker with the matching block from `/tmp/paste-blocks.txt` (Task 1 stdout). Use the exact structure below:

````markdown
# Lab 5: Build a Dashboard in Gemini Canvas

**Goal:** Turn the COVID-19 figures from Module 1 into a polished, interactive
web dashboard — generated by **Gemini Canvas** from a single prompt.

---

## From Power BI to AI in one step

In **Module 1** you built a COVID-19 mortality dashboard by hand in Power BI:
ingest, model, write DAX, lay out visuals. In this lab you give the *same
numbers* to Gemini and let it generate a web dashboard for you in seconds.

The point is not that AI replaces Power BI — it is that once you have clean,
aggregated data, AI is a fast way to produce a polished presentation layer for
sharing or prototyping.

> The numbers below are pre-aggregated from the public MOH COVID-19 deaths
> line-list (the same dataset used in Module 1). Source aggregation script:
> [`../data/aggregate_dashboard_data.py`](../data/aggregate_dashboard_data.py).

---

## Step 1 — Open Gemini Canvas

1. Go to [gemini.google.com](https://gemini.google.com).
2. In the prompt box, enable **Canvas** (the Canvas tool turns Gemini's reply
   into a live, editable web app preview alongside the chat).

---

## Step 2 — Give Gemini the data

Paste the five tables below into the Gemini prompt box (you will add the design
prompt in Step 3). Each table is already split by gender (`All`, `Male`,
`Female`) so the dashboard's gender filter just selects a slice.

**KPI table**

```
<<< paste block: KPI table >>>
```

**Deaths by year**

```
<<< paste block: Deaths by year >>>
```

**Deaths by state**

```
<<< paste block: Deaths by state >>>
```

**Deaths by age group**

```
<<< paste block: Deaths by age group >>>
```

**Deaths by vaccination status**

```
<<< paste block: Deaths by vaccination status >>>
```

---

## Step 3 — Paste the design prompt

After the data, paste this prompt (in Malay) and send:

```
Cipta sebuah dashboard web analitik kesihatan bertaraf antarabangsa bernama Malaysia Covid Insights dengan reka bentuk futuristik, profesional, premium, AI-powered, glassmorphism dan responsive, menggunakan tema warna hijau emerald, cyan dan putih, memaparkan AI Insight Banner, KPI utama (Jumlah kematian, Peratus kematian tanpa mendapat vaksin, Peratus kematian dengan komorbiditi, Median umur kematian), carta interaktif trend jumlah kematian mengikut tarikh (tahun), negeri, kumpulan umur, dan status vaksinasi, filter interaktif utama adalah berdasarkan jantina, lengkap dengan animasi moden, ikon futuristik, kad statistik premium, grafik interaktif, visualisasi data masa nyata, AI recommendation engine, predictive analytics, smart insights, dan reka bentuk setanding Microsoft Power BI, Tableau, Google Analytics 4 dan Government Digital Service UK, sesuai digunakan oleh Kementerian Kesihatan Malaysia sebagai COVID Command Center Dashboard, dengan susun atur bersih, kemas, moden, mudah dibaca, berimpak tinggi dan memberikan pengalaman pengguna yang elegan serta berteknologi tinggi.
```

Gemini will build the dashboard in the Canvas panel. Give it a few seconds to
render.

---

## Step 4 — Iterate

Canvas is interactive — refine with short follow-up prompts, for example:

- ```
  Pastikan KPI dan semua carta dikemas kini apabila penapis jantina ditukar
  (All / Male / Female).
  ```
- ```
  Jadikan carta trend boleh tukar paparan antara: tahun, negeri, kumpulan umur,
  dan status vaksinasi.
  ```
- ```
  Tukar tema warna supaya lebih kontras dan mudah dibaca pada skrin pembentangan.
  ```

---

## Expected outcome

You have a working **Malaysia Covid Insights** dashboard in Gemini Canvas whose
default (`All`) figures match the Module 1 dashboard — Total Deaths ~37K,
% Unvaccinated 60.2%, % With Comorbidity 78.8%, Median Age 64 — and that
re-filters by gender.

> Compare it to the Power BI dashboard from Module 1: same data, two very
> different ways to build a dashboard.

➡️ Next: [Explore further](06-explore-further.md).
````

- [ ] **Step 3: Fill in the paste blocks**

Open `/tmp/paste-blocks.txt`. For each `<<< paste block: TITLE >>>` marker, replace it with the lines under the matching `### TITLE` block from the script output (the CSV lines only — not the ``` fences or the `### ` heading). Confirm the KPI block's `All` row reads `All,37351,60.2,78.8,64.0`.

- [ ] **Step 4: Verify no markers remain**

Run: `grep -n "paste block" module-2-notebooklm-gemini/lab/05-gemini-canvas-dashboard.md`
Expected: no output (all markers replaced).

- [ ] **Step 5: Commit**

```bash
git add module-2-notebooklm-gemini/lab/05-gemini-canvas-dashboard.md \
        module-2-notebooklm-gemini/lab/06-explore-further.md
git commit -m "feat(m2): add Gemini Canvas dashboard lab; renumber explore-further to 06

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: Update Module 2 README lab map

**Goal:** Reflect the new four-workflow structure and the renumbered files in the Module 2 README.

**Files:**
- Modify: `module-2-notebooklm-gemini/README.md`

**Acceptance Criteria:**
- [ ] "3 Main Workflows" section becomes four workflows, adding "Build a dashboard in Gemini Canvas"
- [ ] Lab Map table has six rows; row 5 links to `lab/05-gemini-canvas-dashboard.md`, row 6 links to `lab/06-explore-further.md`
- [ ] No remaining link to `lab/05-explore-further.md`

**Verify:** `grep -n "05-gemini-canvas-dashboard.md\|06-explore-further.md" module-2-notebooklm-gemini/README.md` shows both; `grep -c "05-explore-further.md" module-2-notebooklm-gemini/README.md` → 0

**Steps:**

- [ ] **Step 1: Update the "Main Workflows" heading and list**

In `module-2-notebooklm-gemini/README.md`, change the `## 3 Main Workflows` heading to `## 4 Main Workflows` and add a fourth list item after the "Meeting audio → minutes" item:

```markdown
4. **Build a dashboard in Gemini Canvas** — turn Module 1's aggregated COVID
   figures into a polished web dashboard from a single prompt.
```

- [ ] **Step 2: Update the Lab Map table**

Replace the Lab Map table rows so it reads:

```markdown
| Step | File | Estimated time |
| --- | --- | --- |
| 1 | [Set up the notebook](lab/01-set-up-notebook.md) | 20 min |
| 2 | [Workflow 1: Query the corpus](lab/02-query-the-corpus.md) | 30 min |
| 3 | [Workflow 2: Project paper → slides](lab/03-project-paper-to-slides.md) | 35 min |
| 4 | [Workflow 3: Audio → meeting minutes](lab/04-meeting-audio-to-minutes.md) | 35 min |
| 5 | [Workflow 4: Build a dashboard in Gemini Canvas](lab/05-gemini-canvas-dashboard.md) | 25 min |
| 6 | [Explore further](lab/06-explore-further.md) | 20 min |
```

- [ ] **Step 3: Verify links resolve**

Run: `grep -c "05-explore-further.md" module-2-notebooklm-gemini/README.md`
Expected: `0`
Run: `ls module-2-notebooklm-gemini/lab/05-gemini-canvas-dashboard.md module-2-notebooklm-gemini/lab/06-explore-further.md`
Expected: both paths listed (exist).

- [ ] **Step 4: Commit**

```bash
git add module-2-notebooklm-gemini/README.md
git commit -m "docs(m2): add Gemini Canvas workflow to README lab map

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Self-Review

- **Spec coverage:** Deliverables 1–2 (script + CSV) → Task 1; lab file + rename (3–4) → Task 2; README (5) → Task 3. Aggregation spec (Component 1), pre-computed All/Male/Female, median-per-slice, verification gate → Task 1. Lab structure + verbatim Malay prompt (Component 2) → Task 2. README update (Component 3) → Task 3. All spec sections covered.
- **Placeholder scan:** The only intentional markers are `<<< paste block: ... >>>` in Task 2, which are explicitly resolved from Task 1's real stdout in Step 3 — not placeholders left for the engineer to invent.
- **Type/name consistency:** CSV schema `table,sex,category,value` is used identically in Task 1 (write) and referenced in Task 2. KPI paste header `sex,total_deaths,pct_unvaccinated,pct_comorbidity,median_age` matches the script's `print_block` call. Filenames `05-gemini-canvas-dashboard.md` / `06-explore-further.md` consistent across Tasks 2 and 3.
