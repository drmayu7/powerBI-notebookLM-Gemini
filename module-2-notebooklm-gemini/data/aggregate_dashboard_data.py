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
