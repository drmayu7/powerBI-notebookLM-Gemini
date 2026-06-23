# Modul 1: Transforming Medical Statistics with Power BI

**Slot 1 — 25 Jun 2026 (Thu), 8:00 am – 11:30 am**
Presenter: Dr. Muhammad Naufal bin Nordin

This module walks you through building an interactive **COVID-19 mortality
dashboard** from scratch in **Power BI Desktop** — even if you have never
used Power BI before.

> **Haven't installed Power BI Desktop yet?** Please complete the
> [setup guide](../00-setup/) before the session.

---

## Session format

The session has two parts:

1. **Theory (30 min)** — a short slide presentation covering what Power BI
   is, why it matters for medical statistics, and the workflow you'll use.
2. **Follow-along build (~2.5 hrs)** — everyone builds the dashboard live,
   on their own laptop, alongside the facilitator. If you fall behind, get
   stuck, or miss a step, you can always rejoin from one of six checkpoint
   `.pbix` files — just ask the facilitator for the nearest one. Every step
   is also written out in the hands-on guide so you can repeat it on your
   own after the course.

---

## Slot 1 timetable

| Block | Time | Format |
| --- | --- | --- |
| Theory (slide deck) | 8:00–8:30 | Facilitator presents |
| Build Pt.1: Ingest + Power Query | 8:30–9:20 | Follow-along |
| Build Pt.2: Data model (star schema) | 9:20–9:45 | Follow-along |
| Break | 9:45–10:00 | — |
| Build Pt.3: DAX measures | 10:00–10:30 | Follow-along |
| Build Pt.4: Visuals | 10:30–11:10 | Follow-along |
| Build Pt.5: Interactivity + free explore + Q&A | 11:10–11:30 | Follow-along |

---

## What you'll build

By the end of the session, you'll have one interactive COVID-19 dashboard
page with:

- KPI cards — Total Deaths, % Unvaccinated, % With Comorbidity, Median Age
- Deaths-over-time line chart
- Deaths by state
- Deaths by age group
- Vaccination-status donut chart
- Slicers for interactive filtering

It's built on a **star schema** (`Fact_Deaths` + `Dim_Date` + `Dim_State`),
so along the way you'll also learn the modelling pattern that underlies most
real-world Power BI reports.

---

## How to follow

- **[hands-on-guide.md](hands-on-guide.md)** is your detailed, step-by-step
  safety net — every formula, every measure, and the checkpoint `.pbix`
  files are documented there. Use it to follow along live or to redo the
  build on your own afterwards.
- The **theory slide deck** is at [`../slides/module-1-power-bi.md`](../slides/module-1-power-bi.md).

---

## Datasets

The datasets live in [`data/`](data/) and are real, aggregate, open
government data — pinned as CSV files so the session doesn't depend on
internet access.

| File | Role | Source |
| --- | --- | --- |
| `covid_deaths_linelist.csv` | Fact — one row per COVID-19 death (~37,351) | data.gov.my (MOH) |
| `covid_cases.csv` | Daily new cases by state | data.gov.my (MOH) |
| `population_state.csv` | Population by state → per-100k rates | DOSM |

To regenerate the datasets from source (optional):

```bash
python data/fetch_data.py
```

---

## Data safety

All data used in this module is **open, aggregate government data** from
data.gov.my and DOSM — there is no real patient data and nothing
confidential. Never substitute these files with real patient records or
confidential hospital documents, even for practice.
