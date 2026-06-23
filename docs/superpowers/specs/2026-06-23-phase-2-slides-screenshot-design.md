# Design: Phase 2 — Intro Slides + Lab Screenshots

**Date:** 2026-06-23
**Presenter:** Dr. Muhammad Naufal bin Nordin
**Course:** Advanced Course — Administrative Officer (Medical Records) & Assistants, KKM 2026
**Slot:** 25 June 2026 (Thursday)
**Reference:** Follow-up to [Phase 1 design](2026-06-22-training-module-powerbi-notebooklm-gemini-design.md)

## 1. Context & Goals

Phase 1 (markdown content backbone + synthetic dataset + public links) is complete and committed. Phase 2 originally bundled four items: slides, screenshots, finished `.pbix` files, and audio files. This session focuses on the **two** most needed before the course:

1. **Intro slides** for the ~20-minute lecture in each slot (2 decks).
2. **In-lab screenshots** — replace placeholders with a consistent structure + a capture manifest.

Finished `.pbix` files and audio files are **excluded** from this session (remain a later Phase 2 item).

## 2. Design Decisions (locked)

| # | Decision |
|---|---|
| Slide tooling | **Marp** (Markdown → PPTX/PDF/HTML) |
| Slide rendering | **Marp CLI via `npx @marp-team/marp-cli`** (Approach A). `.md` is the canonical source; PDF is rendered & committed |
| Slide scope | **Two intro decks only** (one per slot, ~20 min / ~12–15 slides) |
| Slide content source | Existing intro notes in each module's `README.md` (slides & lab stay aligned) |
| Theme | **Clean built-in Marp theme** (e.g. `default`/`gaia`) + course footer; no official logo committed |
| Language | Bahasa Melayu primary, technical terms in English in `code`/quotes (consistent with the repo) |
| Screenshots | **Manifest + placeholder + folder** — audit all labs, standardize references, provide a capture checklist |
| Actual image capture | Done by the user (cannot be AI-generated); the repo provides the structure only |

## 3. Repository Architecture (new files)

```
slides/
  README.md                     ← how to render (npx Marp CLI commands), theme notes
  module-1-power-bi.md           ← Marp deck: Slot 1 intro (~20 min)
  module-2-notebooklm-gemini.md  ← Marp deck: Slot 2 intro (~20 min)
  build/
    module-1-power-bi.pdf        ← rendered PDF (committed; presentable with no setup)
    module-2-notebooklm-gemini.pdf
module-1-power-bi/lab/img/       ← screenshot folder (.gitkeep)
module-2-notebooklm-gemini/lab/img/
docs/SCREENSHOTS.md             ← capture manifest/checklist (every shot, by lab/step)
```

**Note on committing PDFs:** PDFs are rendered using `npx @marp-team/marp-cli` and committed so there's a presentable file on course day with no setup required. If the network blocks the Marp package download, the fallback is to commit the `.md` source + the build recipe only.

## 4. Slides — Content

Both decks are sourced from the existing intro notes in each module's `README.md`. Title level only (titles + a few bullets) — step-by-step detail stays in the lab, not the slides. ~12–15 slides per deck.

**Deck 1 — `slides/module-1-power-bi.md` (Slot 1 intro):**

1. Title (course, slot, presenter, date)
2. What Power BI is & why it's relevant for medical statistics (manual Excel → automated dashboard)
3. Workflow: Get Data → Transform → Model → Visualize → Share
4. Interface tour: Report / Data / Model views
5. Preview of the final dashboard (KPI cards, bar, line, slicer)
6. What we're building today (7-lab roadmap)
7. Data-safety note (synthetic dataset) + hands-on expectations
8. Let's begin → Lab 1

**Deck 2 — `slides/module-2-notebooklm-gemini.md` (Slot 2 intro):**

1. Title
2. NotebookLM (grounded + citation) vs Gemini (general generative)
3. Why it's relevant: stop "flipping through papers" → query the corpus
4. Concepts: *grounding*, *citation*
5. ⚠️ Sensitive-data warning (do not upload real patient data)
6. 3 core workflows (query the corpus / paper→slides / audio→minutes) + explore
7. 5-lab roadmap + public references
8. Let's begin → Lab 1

**Marp front-matter for each deck:** `marp: true`, a chosen built-in theme, `paginate: true`, course + presenter footer.

## 5. Screenshots — Manifest, Placeholder, Folder

**Folder:** create `module-1-power-bi/lab/img/` and `module-2-notebooklm-gemini/lab/img/` (with `.gitkeep` so the empty folders can be committed).

**Placeholder convention:** every screenshot reference is standardized as `![Brief description](img/NN-name.png)`, placed right after the step it illustrates. Naming = lab number + short slug (e.g. `02-power-query.png`). Existing inconsistent references (module-1 labs 01/03/05/06) are corrected; missing ones are added across all labs.

**Coverage:** one screenshot per important visual step (not every step) — typically 1–3 per lab, at the moment a learner most needs to confirm "am I on the right screen". NotebookLM/Gemini labs also get placeholders, with a note that their UI changes over time.

**`docs/SCREENSHOTS.md` manifest:** a checklist table — `[ ]` | filename | lab/step | what to capture | notes — grouped by module, so the user can capture and drop in each PNG without rereading the lab.

**Caveat:** placeholders won't render until the image is captured — a broken-image icon will appear in the markdown preview meanwhile. This is expected; the manifest tracks what's still pending.

## 6. Excluded Scope (YAGNI)

- Finished `.pbix` files (remain a later Phase 2 item)
- Sample audio files / transcripts (remain a later Phase 2 item)
- Official KKM theme/branding + logo (can be added later; clean theme for now)
- Per-lab divider slides or a full teaching deck (intro only)
- Actual image capture (done by the user on their own machine)

## 7. Verification

- `npx @marp-team/marp-cli slides/module-1-power-bi.md --pdf` produces a PDF with no error; same for deck 2.
- Each deck opens & all slides render correctly (BM text + English terms correct).
- All labs: placeholder references follow the `![...](img/NN-name.png)` convention; the `img/` folder exists.
- `docs/SCREENSHOTS.md` lists every screenshot file referenced in any lab (no reference left out).
