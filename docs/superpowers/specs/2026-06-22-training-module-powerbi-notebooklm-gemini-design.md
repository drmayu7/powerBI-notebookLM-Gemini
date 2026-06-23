# Design: Power BI + NotebookLM & Gemini Training Module

**Date:** 2026-06-22
**Presenter:** Dr. Muhammad Naufal bin Nordin (Senior Principal Assistant Director, Planning Division, KKM)
**Course:** Advanced Course — Administrative Officer (Medical Records) & Assistant Administrative Officer, National Level KKM 2026
**Slot:** 25 June 2026 (Thursday)

## 1. Context & Goals

A public GitHub repository containing training modules for course participants to reference. Two training slots by the presenter on 25 June 2026:

1. **8:00 am – 11:30 am** (break 10:00–10:30) — *Medical Statistics Transformation using Power BI* (~3 hours)
2. **11:30 am – 4:00 pm** (lunch 1:00–2:00) — *NotebookLM and Gemini: The Potential of Artificial Intelligence in Data & Documentation Automation* (~3.5 hours)

**Audience:** Administrative Officers (Medical Records) & Assistants — mostly first-time users of Power BI / AI tools. Background in medical records management, medical reports, medical boards.

**Delivery format:** *Hands-on* workshop with a brief introductory lecture (~20 min) for each slot. Participants bring their own laptops.

## 2. Design Decisions (locked)

| # | Decision |
|---|---|
| Format | Hands-on workshop + brief introductory lecture |
| Power BI environment | **Power BI Desktop, local only** (Windows). Installation done **before** the course via a setup guide. No Power BI Service. |
| Language | **Bahasa Melayu primary**, technical terms kept in English (Power Query, measure, DAX, etc.) |
| Power BI dataset | **Synthetic** (fake but realistic medical data) — no privacy risk |
| AI scope (Module 2) | **Document-centric**, 3 core workflows + an explore section |
| NotebookLM sample documents | **Links to genuine public KKM/JPA documents** (not stored in the repo) |
| Phase 1 scope | **Markdown content backbone only** + synthetic dataset + list of public links. Slides, screenshots, finished `.pbix`, audio files = Phase 2 |
| Repo structure | Topic-first, two self-contained modules |

## 3. Repository Architecture

```
README.md                      ← course overview, 2 slots, agenda, "how to use this repo"
LICENSE                        ← permissive license (public/reusable repo)
00-setup/
  README.md                    ← pre-course setup: install Power BI Desktop, set up Google account
module-1-power-bi/
  README.md                    ← intro lecture notes + lab roadmap
  lab/                         ← focused lab step files (one task per file, numbered)
  data/                        ← synthetic medical dataset (CSV) + generator script
module-2-notebooklm-gemini/
  README.md                    ← intro + 3 workflows
  lab/                         ← workflow guides
  public-references.md              ← list of public KKM/JPA document links
docs/superpowers/specs/        ← this design document
```

**Conventions:**
- Each lab step file is short and focused — one task, numbered in sequence.
- Narrative in Bahasa Melayu; English terms/UI in `code` or quotes (e.g. "Transform Data", measure, DAX).
- Each step is written so participants can replay it **after** the course unaided.
- Screenshots are referenced as placeholders for now (`![...](../img/...)`) — actual images = Phase 2.

**Time budget:**
- **Slot 1 (Power BI):** 8:00–10:00 (2h) + 10:30–11:30 (1h) = 3h. ~20 min intro + ~2.5h hands-on + buffer.
- **Slot 2 (AI):** 11:30–1:00 (1.5h) + 2:00–4:00 (2h) = 3.5h. ~20 min intro + ~2.5–3h hands-on + buffer.

## 4. Module 1 — Power BI (3 hours)

**Principle:** first-time users → one new concept at a time, always tied to medical statistics output they already recognize.

**`module-1-power-bi/README.md` — intro lecture notes (~20 min):**
- What Power BI is & why it's relevant for medical statistics (from manual Excel → automated dashboard)
- Power BI workflow: Get Data → Transform → Model → Visualize → Share
- Brief interface tour (Report / Data / Model views)
- Preview of the final dashboard to be built

**`lab/` — step files (hands-on, ~2.5h + buffer):**

| File | Content |
|---|---|
| `01-import-data.md` | Get Data → import the medical dataset (CSV) |
| `02-power-query-bersih.md` | Power Query: check data types, remove spaces/errors, format dates |
| `03-model-hubungan.md` | Modeling basics: relationships between the admissions fact table ↔ reference tables (ward, discipline, date) — lightweight |
| `04-ukuran-dax.md` | Basic measures: Total Admissions, Total Discharges, **BOR %**, **ALOS**, **Patient Count by Ward** |
| `05-visual-asas.md` | Card (KPI), bar chart (admissions by discipline), bar chart (patient count by ward), line chart (monthly trend) |
| `06-dashboard-interaktif.md` | Assemble a one-page dashboard + slicers (discipline, ward, date) |
| `07-eksport-simpan.md` | Save `.pbix`, export PDF (local only; brief note about publishing as optional/Phase 2) |

**Scope discipline (YAGNI):** no advanced DAX, no dataflows, no publishing to the Service, no custom visuals. Just enough to produce a genuine interactive medical-statistics dashboard that can be rebuilt at the workplace.

## 5. Module 2 — NotebookLM + Gemini (3.5 hours)

**`module-2-notebooklm-gemini/README.md` — intro lecture notes (~20 min):**
- What NotebookLM is (AI *grounded* on your documents + citations) vs Gemini (general generative AI)
- Why it's relevant: stop "flipping through papers" — query the reference corpus directly
- Key concepts: *grounding*, *citation*, and a **sensitive-data warning** (do not upload real patient data to personal accounts)

**`lab/` — 3 core workflows + explore (~2.5–3h):**

| File | Workflow |
|---|---|
| `01-set-up-notebook.md` | Open NotebookLM, create a notebook, upload sample documents (from public links in `public-references.md`) |
| `02-query-the-corpus.md` | **Workflow 1:** ask procedure/guideline questions, read the answer + citations, verify sources |
| `03-project-paper-to-slides.md` | **Workflow 2:** from a project paper → use Studio (briefing doc, slide structure) + Gemini prompts to turn it into slides |
| `04-meeting-audio-to-minutes.md` | **Workflow 3:** meeting recording transcript → draft meeting minutes (using a sample/example transcript) |
| `05-explore-further.md` | Audio Overview, FAQ, Study Guide, Mind Map; Gemini for drafting official memos/reports |

**Cross-module note:** a clear **data-safety guideline** box — participants will be tempted to upload real PUU/patient documents; the module repeatedly flags what's safe (public, de-identified documents) versus not.

**`public-references.md`:** a list of genuine public KKM/JPA documents (record-management guidelines, circulars, etc.) that participants download and upload to NotebookLM for the lab. Note: links may change/expire; will be written with an access date.

**Note:** Workflow 2 depends on current NotebookLM Studio features — written based on what's available now, with a note that the UI keeps evolving.

## 6. Synthetic Medical Dataset (Module 1)

Designed as a small **star schema** so the modeling step is meaningful and every measure can be computed from real columns.

**Fact table — `kemasukan.csv`** (~12 months, a few thousand rows):
`ID_Kemasukan`, `Tarikh_Masuk`, `Tarikh_Discaj`, `Kod_Wad`, `Kod_Disiplin`, `Diagnosis_DRG`, `Umur`, `Jantina`
→ Length-of-stay derived from the two dates (feeds **ALOS**); row counts feed **Total Admissions / Discharges / Patient Count by Ward**.

**Dimension table — `wad.csv`:**
`Kod_Wad`, `Nama_Wad`, `Kapasiti_Katil`, `Jenis_Wad`
→ `Kapasiti_Katil` enables **BOR %** (patient-days ÷ available bed-days).

**Dimension table — `disiplin.csv`:**
`Kod_Disiplin`, `Nama_Disiplin` (Medical, Surgical, O&G, Pediatrics, Orthopedics, …)

**Dimension table — `tarikh.csv`:** date table for monthly trends — *or* built in Power Query during the lab; CSV provided as a fallback so no participant gets stuck.

**Generation:** a small Python script (`module-1-power-bi/data/jana_data.py`) using stdlib only — data is reproducible (`random.seed`), volume is adjustable. Generated CSVs are committed alongside it. Fully synthetic, realistic distributions (seasonality, reasonable LOS, BOR within a credible range).

**Format:** CSV only.

## 7. Phase 1 Scope (deliverable)

Includes:
- `README.md` (root), `LICENSE`
- `00-setup/README.md`
- `module-1-power-bi/` — README + all lab files + dataset CSV + generator script
- `module-2-notebooklm-gemini/` — README + all lab files + `public-references.md`

**Not included (Phase 2):** actual slides, screenshots/images, finished `.pbix` files, sample audio files.

## 8. Excluded Scope (YAGNI)

- Power BI Service / publishing / sharing online
- Advanced DAX, dataflows, custom visuals
- Storing real documents or patient data in the repo
- `.xlsx` version of the dataset (CSV only)
- Slides & media (Phase 2)
