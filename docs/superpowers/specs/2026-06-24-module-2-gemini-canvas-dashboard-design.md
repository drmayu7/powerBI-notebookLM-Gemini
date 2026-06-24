# Module 2 — Gemini Canvas COVID Dashboard Lab (Design)

**Date:** 2026-06-24
**Author:** Dr. Muhammad Naufal bin Nordin (with Claude)
**Status:** Approved design → ready for implementation plan

## Summary

Add a new hands-on workflow to Module 2 in which trainees take the COVID-19
mortality data they built a Power BI dashboard from in Module 1, and have
**Gemini Canvas** generate a polished web dashboard ("Malaysia Covid Insights")
from the same numbers. This bridges Module 1 (build it yourself in Power BI)
and Module 2 (let AI build it), reinforcing that the *data* is the asset and AI
is a fast presentation layer.

The data is pre-aggregated by a small reproducible Python script into five tiny
tables, which the trainee pastes inline into Gemini together with a fixed
Malay "hero" prompt.

## Goals

- A reproducible aggregation that reads Module 1's deaths line-list and emits
  the exact figures shown in the Module 1 dashboard screenshot.
- A self-contained lab: everything pastes inline into Gemini Canvas, no file
  upload (reliable on government networks/tenants).
- The generated dashboard recomputes correctly when filtered by gender, with
  no client-side aggregation needed.

## Non-goals

- Building the dashboard HTML/JS ourselves — Gemini Canvas generates it from
  the prompt.
- Month-level or daily trend granularity — year only.
- Changing any Module 1 content or data.

## Reference: what the dashboard must reproduce

The Module 1 dashboard (`module-1-power-bi/img/05-cards-visuals.png`) is the
source of truth for values. The Gemini prompt maps 1:1 onto it:

| Module 1 visual | Reference value | Gemini element |
|---|---|---|
| Total Deaths | ~37K | KPI: Jumlah kematian |
| % Unvaccinated | 60.2% | KPI: Peratus tanpa vaksin |
| % With Comorbidity | 78.8% | KPI: Peratus komorbiditi |
| Median Age | 64.00 | KPI: Median umur kematian |
| Deaths by Year | 2020→2024 curve | Trend dim: tahun |
| Deaths by state | Selangor highest | Trend dim: negeri |
| Deaths by Age_Group | 60–79 peak | Trend dim: kumpulan umur |
| Deaths by Vaccination_Status | 60.2 / 24.8 / 15.0 donut | Trend dim: status vaksinasi |
| Sex slicer | Female / Male | Filter: jantina |

## Deliverables

| File | Action |
|---|---|
| `module-2-notebooklm-gemini/data/aggregate_dashboard_data.py` | New — aggregation script |
| `module-2-notebooklm-gemini/data/covid_dashboard_aggregated.csv` | New — source-of-truth aggregated output (long format) |
| `module-2-notebooklm-gemini/lab/05-gemini-canvas-dashboard.md` | New — the lab |
| `module-2-notebooklm-gemini/lab/06-explore-further.md` | Renamed from `05-explore-further.md` |
| `module-2-notebooklm-gemini/README.md` | Edited — lab map adds Workflow 4, renumbers |

## Component 1 — Aggregation script

`aggregate_dashboard_data.py` mirrors the style of Module 1's `fetch_data.py`.

**Input:** Module 1's deaths line-list (relative path
`../../module-1-power-bi/data/covid_deaths_linelist.csv`). The KPIs and all four
breakdowns derive solely from this file; `covid_cases.csv` and
`population_state.csv` are not needed (no cases or per-100k visuals here).

**Derived columns (identical to Module 1 `hands-on-guide.md`):**
- `Sex` = "Male" if `male==1` else "Female"
- `Age_Group`: ≤17 "0–17", ≤39 "18–39", ≤59 "40–59", ≤79 "60–79", else "80+"
- `Vaccination_Status`: "Fully vaccinated (≥2 doses)" if `date_dose2` ≤ `date`;
  else "Partial (1 dose)" if `date_dose1` ≤ `date`; else "Unvaccinated"
- `Comorbidity`: "Yes" if `comorb==1` else "No"
- `year` = year of `date`

**Pre-computation rule:** every output table is fully computed for
`sex ∈ {All, Male, Female}`. `All` is the unfiltered population; `Male`/`Female`
are the gender slices. The dashboard's gender filter then *selects* a
precomputed slice rather than aggregating — so Gemini never does arithmetic at
runtime. Median age is computed per slice (it cannot be summed).

**Outputs — five logical tables** (all written into one long-format
`covid_dashboard_aggregated.csv` with a `table` column, and also rendered by the
script as ready-to-paste blocks for the lab so there is no manual drift):

1. **kpi** — `sex, total_deaths, pct_unvaccinated, pct_comorbidity, median_age`
   (3 rows). Percentages rounded to 1 dp; median to 2 dp.
2. **deaths_by_year** — `year, sex, deaths` (5 × 3 = 15 rows)
3. **deaths_by_state** — `state, sex, deaths` (16 × 3 = 48 rows)
4. **deaths_by_age_group** — `age_group, sex, deaths` (5 × 3 = 15 rows)
5. **deaths_by_vacc_status** — `vacc_status, sex, deaths` (3 × 3 = 9 rows)

Total ≈ 90 rows — small enough to paste inline.

## Component 2 — Lab file (`05-gemini-canvas-dashboard.md`)

English instructions + Malay hero prompt, matching the existing
`06-explore-further.md` convention. Structure:

1. **Goal + bridge intro** — "In Module 1 you built this dashboard by hand in
   Power BI. Now you'll give the same numbers to Gemini and have it generate a
   web dashboard in seconds."
2. **Step 1 — Open Gemini Canvas** (gemini.google.com → Canvas).
3. **Step 2 — Paste the five data tables**, each under a clear heading
   (KPI / Deaths by year / by state / by age group / by vaccination status).
   Values come verbatim from the script output.
4. **Step 3 — Paste the hero prompt** (the user's Malay prompt, verbatim, in a
   code block).
5. **Step 4 — Iterate** — a couple of follow-up refinement prompts
   (e.g. adjust colours, fix a KPI, add the gender filter behaviour).
6. **Expected outcome** — a working "Malaysia Covid Insights" dashboard whose
   `All` figures match the Module 1 dashboard, filterable by gender.

The hero prompt (verbatim, Malay):

> Cipta sebuah dashboard web analitik kesihatan bertaraf antarabangsa bernama
> Malaysia Covid Insights dengan reka bentuk futuristik, profesional, premium,
> AI-powered, glassmorphism dan responsive, menggunakan tema warna hijau
> emerald, cyan dan putih, memaparkan AI Insight Banner, KPI utama (Jumlah
> kematian, Peratus kematian tanpa mendapat vaksin, Peratus kematian dengan
> komorbiditi, Median umur kematian), carta interaktif trend jumlah kematian
> mengikut tarikh (tahun), negeri, kumpulan umur, dan status vaksinasi, filter
> interaktif utama adalah berdasarkan jantina, lengkap dengan animasi moden,
> ikon futuristik, kad statistik premium, grafik interaktif, visualisasi data
> masa nyata, AI recommendation engine, predictive analytics, smart insights,
> dan reka bentuk setanding Microsoft Power BI, Tableau, Google Analytics 4 dan
> Government Digital Service UK, sesuai digunakan oleh Kementerian Kesihatan
> Malaysia sebagai COVID Command Center Dashboard, dengan susun atur bersih,
> kemas, moden, mudah dibaca, berimpak tinggi dan memberikan pengalaman
> pengguna yang elegan serta berteknologi tinggi.

## Component 3 — README update

`module-2-notebooklm-gemini/README.md` lab map:
- Add a "Workflow 4: Build a dashboard in Gemini Canvas" entry as step 5.
- Renumber "Explore further" to step 6.
- Add the new workflow to the "Main Workflows" list (now 4 workflows).

## Verification

Before declaring done, run the script and confirm the `All` slice matches the
Module 1 screenshot:
- Total Deaths ≈ 37,000 (37K rounded)
- % Unvaccinated = 60.2%
- % With Comorbidity = 78.8%
- Median Age = 64.00
- Vaccination donut split ≈ 60.2 / 24.8 / 15.0

If any figure diverges, reconcile the derived-column logic against
`module-1-power-bi/hands-on-guide.md` before proceeding.

## Decisions log

- Inline paste (not file upload) — reliability on government networks.
- Approach A (five labeled tables) over a single long/wide CSV — most robust
  for Gemini to map to the right visual during a live demo.
- Year-only trend granularity — matches the prompt and Module 1.
- Pre-computed All/Male/Female slices — gender filter selects, never aggregates.
- Malay hero prompt verbatim, English surrounding instructions.
- No synthetic-data caveat — the COVID dataset is public/real (Module 1 treats
  it as real anonymised data); the repo's synthetic warning concerns uploaded
  documents, not this dataset.
