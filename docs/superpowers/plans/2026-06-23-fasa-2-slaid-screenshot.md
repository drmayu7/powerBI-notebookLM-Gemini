# Fasa 2 — Slaid Pengenalan + Screenshot Lab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers-extended-cc:subagent-driven-development (recommended) or superpowers-extended-cc:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce two Marp intro slide decks (rendered to committed PDFs) and standardize screenshot placeholders + a capture manifest across all 12 lab files.

**Architecture:** Marp Markdown decks under `slides/` rendered to PDF via `npx @marp-cli/marp`; `.md` is canonical, PDFs committed for zero-setup presenting. Screenshot work creates `lab/img/` folders, normalizes/inserts `![...](img/NN-nama.png)` references at key visual steps, and lists every shot in `docs/SCREENSHOTS.md`.

**Tech Stack:** Marp (`@marp-cli/marp` via npx, Node 20 available), Markdown.

**User decisions (already made):**
- Phase 2 focus = slides + screenshots only (`.pbix`/audio excluded).
- Slides via Marp, rendered with `npx @marp-cli/marp` (Approach A); `.md` canonical, PDF committed.
- Two intro decks only (one per slot), sourced from each module's existing `README.md` intro notes.
- Clean built-in Marp theme (`gaia`); no official KKM logo committed.
- Screenshots = manifest + placeholders + folders; real image capture done by the user.
- BM primary, English technical terms in `code`/quotes.

---

### Task 1: Marp scaffolding + Power BI intro deck (Deck 1)

**Goal:** Create the `slides/` directory, the render guide, and the rendered Power BI intro deck.

**Files:**
- Create: `slides/modul-1-power-bi.md`
- Create: `slides/README.md`
- Create: `slides/build/modul-1-power-bi.pdf` (rendered output, committed)

**Acceptance Criteria:**
- [ ] `slides/modul-1-power-bi.md` has Marp front-matter (`marp: true`, `theme: gaia`, `paginate: true`, footer) and ~8–9 slides matching the spec breakdown.
- [ ] `npx @marp-cli/marp slides/modul-1-power-bi.md --pdf -o slides/build/modul-1-power-bi.pdf` produces a PDF with no error.
- [ ] `slides/README.md` documents the render commands (PDF/PPTX/HTML) and the theme choice.

**Verify:** `npx -y @marp-cli/marp slides/modul-1-power-bi.md --pdf -o slides/build/modul-1-power-bi.pdf && test -f slides/build/modul-1-power-bi.pdf && echo OK` → prints `OK`

**Steps:**

- [ ] **Step 1: Write `slides/modul-1-power-bi.md`**

```markdown
---
marp: true
theme: gaia
paginate: true
footer: 'Kursus Lanjutan KKM 2026 · Dr. Muhammad Naufal bin Nordin'
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Transformasi Statistik Perubatan menggunakan Power BI

**Slot 1 — 25 Jun 2026 (Khamis)**
Kursus Lanjutan (Advanced) — Pegawai Tadbir (Rekod Perubatan) & Penolong
KKM 2026

Dr. Muhammad Naufal bin Nordin

---

## Apa itu Power BI?

- Alat *business intelligence* daripada Microsoft.
- Menukar data mentah (Excel, CSV, pangkalan data) → **dashboard** & **laporan** interaktif.
- Untuk Rekod Perubatan: beralih daripada kira statistik **manual di Excel** → **dashboard automatik** yang sentiasa dikemas kini.

---

## Kenapa relevan untuk statistik perubatan?

- Kira **BOR**, **ALOS**, kemasukan/discaj secara **automatik**.
- Tapis ikut **wad**, **disiplin**, atau **bulan** dengan satu klik.
- Kongsi gambaran statistik yang **konsisten** kepada pengurusan.

---

## Aliran kerja Power BI

```
Get Data → Transform → Model → Visualize → Share
```

1. **Get Data** — import CSV/Excel.
2. **Transform** — bersihkan (Power Query).
3. **Model** — hubungan antara jadual.
4. **Visualize** — carta & dashboard.
5. **Share** — eksport/kongsi.

---

## Lawatan ringkas antara muka

Tiga *view* di tepi kiri Power BI Desktop:

- **Report view** — kanvas untuk bina visual & dashboard.
- **Data view** — lihat jadual data (rows & columns).
- **Model view** — urus hubungan (*relationship*) antara jadual.

---

## Pratonton hasil akhir

Satu halaman dashboard dengan:

- Kad **KPI** (Jumlah Kemasukan, ALOS, BOR %)
- Carta kemasukan **ikut disiplin**
- Carta pesakit **ikut wad**
- Carta **trend kemasukan bulanan**
- **Slicer** (disiplin, wad, bulan)

---

## Apa yang kita bina hari ini

| # | Lab | Masa |
|---|-----|------|
| 1 | Import data | 15 min |
| 2 | Bersihkan data (Power Query) | 25 min |
| 3 | Model & hubungan | 20 min |
| 4 | Ukuran (measure) DAX | 30 min |
| 5 | Visual asas | 30 min |
| 6 | Dashboard interaktif | 25 min |
| 7 | Eksport & simpan | 10 min |

---

## Sebelum mula

- Dataset **sepenuhnya sintetik** — tiada data pesakit sebenar.
- Format: **hands-on** — ikut langkah, tanya bila tersekat.
- Setiap lab boleh **diulang sendiri** selepas kursus.

---

<!-- _class: lead -->

# Mari mula → Lab 1
```

- [ ] **Step 2: Render the deck to PDF**

Run: `npx -y @marp-cli/marp slides/modul-1-power-bi.md --pdf -o slides/build/modul-1-power-bi.pdf`
Expected: command exits 0; `slides/build/modul-1-power-bi.pdf` created. (First run downloads Marp + a headless Chromium; allow time. If the network blocks the download, skip PDF generation, note it, and commit the `.md` source only — the PDF can be rendered later with the same command.)

- [ ] **Step 3: Write `slides/README.md`**

```markdown
# Slaid Pengenalan (Marp)

Slaid ceramah pengenalan untuk dua slot kursus, ditulis sebagai Markdown
[Marp](https://marp.app/). Fail `.md` ialah sumber utama; PDF dalam `build/`
di-commit supaya boleh terus dibentangkan tanpa sebarang pemasangan.

| Fail | Slot |
|------|------|
| `modul-1-power-bi.md` | Slot 1 — Power BI (~20 min) |
| `modul-2-notebooklm-gemini.md` | Slot 2 — NotebookLM & Gemini (~20 min) |

## Render semula

Memerlukan Node.js. Tiada pemasangan global perlu — `npx` muat turun Marp
secara automatik kali pertama.

```bash
# PDF (untuk bentang/cetak)
npx -y @marp-cli/marp slides/modul-1-power-bi.md --pdf -o slides/build/modul-1-power-bi.pdf

# PowerPoint (untuk edit dalam PowerPoint)
npx -y @marp-cli/marp slides/modul-1-power-bi.md --pptx -o slides/build/modul-1-power-bi.pptx

# HTML (untuk bentang dari pelayar)
npx -y @marp-cli/marp slides/modul-1-power-bi.md --html -o slides/build/modul-1-power-bi.html
```

Tema: `gaia` (terbina-dalam Marp). Untuk tukar tema, edit `theme:` dalam
front-matter setiap fail.
```

- [ ] **Step 4: Commit**

```bash
git add slides/modul-1-power-bi.md slides/README.md slides/build/modul-1-power-bi.pdf
git commit -m "feat: slaid pengenalan Modul 1 (Power BI) + panduan render Marp"
```

---

### Task 2: NotebookLM & Gemini intro deck (Deck 2)

**Goal:** Create and render the Slot 2 intro deck using the same Marp setup.

**Files:**
- Create: `slides/modul-2-notebooklm-gemini.md`
- Create: `slides/build/modul-2-notebooklm-gemini.pdf` (rendered output, committed)

**Acceptance Criteria:**
- [ ] `slides/modul-2-notebooklm-gemini.md` has matching Marp front-matter and ~8 slides per the spec breakdown, including the data-sensitivity warning slide.
- [ ] PDF renders without error.

**Verify:** `npx -y @marp-cli/marp slides/modul-2-notebooklm-gemini.md --pdf -o slides/build/modul-2-notebooklm-gemini.pdf && test -f slides/build/modul-2-notebooklm-gemini.pdf && echo OK` → prints `OK`

**Steps:**

- [ ] **Step 1: Write `slides/modul-2-notebooklm-gemini.md`**

```markdown
---
marp: true
theme: gaia
paginate: true
footer: 'Kursus Lanjutan KKM 2026 · Dr. Muhammad Naufal bin Nordin'
---

<!-- _class: lead -->
<!-- _paginate: false -->

# NotebookLM dan Gemini

**Slot 2 — 25 Jun 2026 (Khamis)**
Potensi Kecerdasan Buatan (AI) dalam Automasi Data & Dokumentasi

Dr. Muhammad Naufal bin Nordin

---

## NotebookLM vs Gemini — apa bezanya?

| | **NotebookLM** | **Gemini** |
|---|---|---|
| Sifat | AI *grounded* pada dokumen anda | AI generatif umum |
| Kekuatan | Jawapan + **petikan (citation)** | Menjana & mengolah teks bebas |
| Guna untuk | Tanya korpus, ringkas dokumen | Draf memo, olah slaid, idea |

---

## Kenapa relevan untuk pengurusan rekod?

- Anda simpan banyak **surat PUU, edaran, garis panduan, prosedur**.
- Untuk jawab satu soalan → selalunya perlu *flip* banyak muka surat.
- Dengan NotebookLM: upload sekali, **tanya sahaja** — jawapan datang dengan **rujukan ke sumber**.

---

## Konsep penting

- **Grounding** — NotebookLM jawab **hanya** berdasarkan dokumen yang anda beri, bukan "pengetahuan umum" yang mungkin tidak tepat.
- **Citation (petikan)** — setiap jawapan tunjuk dari bahagian mana sumber ia diambil, supaya boleh **disahkan** sebelum guna.

---

<!-- _class: lead -->

# ⚠️ Amaran Data Sensitif

**JANGAN** upload data pesakit sebenar, surat PUU sulit, atau dokumen terhad ke akaun Google peribadi.

Gunakan **dokumen awam** atau dokumen yang telah **di-deidentify**.
Sentiasa patuhi dasar keselamatan maklumat jabatan.

---

## 3 aliran kerja utama

1. **Tanya korpus rujukan** — upload garis panduan, tanya, dapat jawapan + citation.
2. **Kertas projek → slaid** — tukar kertas projek kepada rangka slaid.
3. **Audio mesyuarat → minit** — transkrip rakaman, draf minit mesyuarat.

➕ **Explore lanjut** — Audio Overview, FAQ, Study Guide, Mind Map, draf memo Gemini.

---

## Apa yang kita buat hari ini

| # | Lab | Masa |
|---|-----|------|
| 1 | Sediakan notebook | 20 min |
| 2 | Aliran 1: Tanya korpus | 30 min |
| 3 | Aliran 2: Kertas projek → slaid | 35 min |
| 4 | Aliran 3: Audio → minit | 35 min |
| 5 | Explore lanjut | 20 min |

Dokumen latihan: lihat `rujukan-awam.md` (pautan awam KKM/JPA).

---

<!-- _class: lead -->

# Mari mula → Lab 1
```

- [ ] **Step 2: Render the deck to PDF**

Run: `npx -y @marp-cli/marp slides/modul-2-notebooklm-gemini.md --pdf -o slides/build/modul-2-notebooklm-gemini.pdf`
Expected: command exits 0; PDF created. (Same network caveat as Task 1 Step 2.)

- [ ] **Step 3: Commit**

```bash
git add slides/modul-2-notebooklm-gemini.md slides/build/modul-2-notebooklm-gemini.pdf
git commit -m "feat: slaid pengenalan Modul 2 (NotebookLM & Gemini)"
```

---

### Task 3: Screenshot scaffolding — Modul 1 (Power BI) labs

**Goal:** Create the modul-1 image folder and standardize/insert screenshot placeholders across all 7 Power BI labs using the `![...](img/NN-nama.png)` convention.

**Files:**
- Create: `modul-1-power-bi/lab/img/.gitkeep`
- Modify: `modul-1-power-bi/lab/01-import-data.md` (normalize `../img/` → `img/`; add result shot)
- Modify: `modul-1-power-bi/lab/02-power-query-bersih.md` (add 2 placeholders)
- Modify: `modul-1-power-bi/lab/03-model-hubungan.md` (normalize `../img/` → `img/`; add cardinality shot)
- Modify: `modul-1-power-bi/lab/04-ukuran-dax.md` (add 1 placeholder)
- Modify: `modul-1-power-bi/lab/05-visual-asas.md` (normalize `../img/` → `img/`; add card shot)
- Modify: `modul-1-power-bi/lab/06-dashboard-interaktif.md` (normalize `../img/` → `img/`; add slicer shot)
- Modify: `modul-1-power-bi/lab/07-eksport-simpan.md` (add 1 placeholder)

**Acceptance Criteria:**
- [ ] `modul-1-power-bi/lab/img/` exists (via `.gitkeep`).
- [ ] No lab references `../img/` anymore; every screenshot ref matches `![...](img/NN-...png)`.
- [ ] Each of the 7 labs has 1–2 placeholders at the key visual step(s) listed below.

**Verify:** `! grep -rn "\.\./img/" modul-1-power-bi/lab/ && grep -rEc "\!\[.*\]\(img/" modul-1-power-bi/lab/*.md` → no `../img/` matches; each lab reports its placeholder count.

**Steps:**

- [ ] **Step 1: Create the image folder**

```bash
mkdir -p modul-1-power-bi/lab/img
printf '' > modul-1-power-bi/lab/img/.gitkeep
```

- [ ] **Step 2: Lab 01 — normalize existing ref + add result shot**

In `modul-1-power-bi/lab/01-import-data.md`, change the existing line `   ![Get Data Text/CSV](../img/01-get-data.png)` to `   ![Get Data Text/CSV](img/01-get-data.png)`.

Then, after the "Hasil yang dijangka" paragraph ending `…**4 jadual**: \`kemasukan\`, \`wad\`, \`disiplin\`, dan \`tarikh\`.`, insert on a new line:

```markdown

![Empat jadual di panel Data](img/01-jadual-dimuat.png)
```

- [ ] **Step 3: Lab 02 — add 2 placeholders**

In `modul-1-power-bi/lab/02-power-query-bersih.md`, after step 3 (the data-type list ending `… → **Text**`), insert:

```markdown

   ![Tetapkan jenis data lajur](img/02-data-type.png)
```

After step 6 (the Custom Column block ending `… tukar kepada\n     **Whole Number**.`), insert:

```markdown

   ![Custom Column untuk Tempoh_Tinggal](img/02-custom-column-los.png)
```

- [ ] **Step 4: Lab 03 — normalize existing ref + add cardinality shot**

In `modul-1-power-bi/lab/03-model-hubungan.md`, change `   ![Model view star schema](../img/03-model.png)` to `   ![Model view star schema](img/03-model.png)`.

In step 4, after the "Cross filter direction" line and before the model screenshot line, insert:

```markdown

   ![Dialog Edit relationship — cardinality & cross filter](img/03-edit-relationship.png)
```

- [ ] **Step 5: Lab 04 — add measure shot**

In `modul-1-power-bi/lab/04-ukuran-dax.md`, after the "Cara cipta measure" paragraph ending `… tekan **Enter**.`, insert:

```markdown

![Cipta measure baharu (formula bar)](img/04-new-measure.png)
```

- [ ] **Step 6: Lab 05 — normalize existing ref + add card shot**

In `modul-1-power-bi/lab/05-visual-asas.md`, change `![Visual asas](../img/05-visual.png)` to `![Visual asas](img/05-visual.png)`.

After section A (the line `> Letakkan tiga kad berbaris di bahagian atas kanvas.`), insert:

```markdown

![Kad KPI](img/05-card-kpi.png)
```

- [ ] **Step 7: Lab 06 — normalize existing ref + add slicer shot**

In `modul-1-power-bi/lab/06-dashboard-interaktif.md`, change `   ![Dashboard interaktif](../img/06-dashboard.png)` to `   ![Dashboard interaktif](img/06-dashboard.png)`.

In step 3, after the line `   - Letakkan ketiga-tiga slicer di tepi (cth. lajur kiri).`, insert:

```markdown

   ![Tiga slicer ditambah](img/06-slicer.png)
```

- [ ] **Step 8: Lab 07 — add export shot**

In `modul-1-power-bi/lab/07-eksport-simpan.md`, in step 2, after the line `   - Power BI menjana PDF setiap halaman laporan untuk dikongsi atau dicetak.`, insert:

```markdown

   ![Export to PDF](img/07-export-pdf.png)
```

- [ ] **Step 9: Verify and commit**

```bash
grep -rn "\.\./img/" modul-1-power-bi/lab/   # expect: no output
git add modul-1-power-bi/lab/
git commit -m "docs: seragamkan placeholder screenshot Modul 1 (lab/img/)"
```

---

### Task 4: Screenshot scaffolding — Modul 2 (NotebookLM & Gemini) labs

**Goal:** Create the modul-2 image folder and insert screenshot placeholders across all 5 AI labs using the same convention.

**Files:**
- Create: `modul-2-notebooklm-gemini/lab/img/.gitkeep`
- Modify: `modul-2-notebooklm-gemini/lab/01-sediakan-notebook.md` (2 placeholders)
- Modify: `modul-2-notebooklm-gemini/lab/02-tanya-korpus.md` (1 placeholder)
- Modify: `modul-2-notebooklm-gemini/lab/03-kertas-projek-ke-slaid.md` (2 placeholders)
- Modify: `modul-2-notebooklm-gemini/lab/04-audio-mesyuarat-ke-minit.md` (1 placeholder)
- Modify: `modul-2-notebooklm-gemini/lab/05-explore-lanjut.md` (1 placeholder)

**Acceptance Criteria:**
- [ ] `modul-2-notebooklm-gemini/lab/img/` exists (via `.gitkeep`).
- [ ] Each of the 5 labs has 1–2 placeholders matching `![...](img/NN-...png)` at the steps below.
- [ ] No `../img/` references introduced.

**Verify:** `grep -rEc "\!\[.*\]\(img/" modul-2-notebooklm-gemini/lab/*.md && ! grep -rn "\.\./img/" modul-2-notebooklm-gemini/lab/` → each lab reports ≥1 placeholder; no `../img/` matches.

**Steps:**

- [ ] **Step 1: Create the image folder**

```bash
mkdir -p modul-2-notebooklm-gemini/lab/img
printf '' > modul-2-notebooklm-gemini/lab/img/.gitkeep
```

- [ ] **Step 2: Lab 01 — 2 placeholders**

In `modul-2-notebooklm-gemini/lab/01-sediakan-notebook.md`, after step 3 (`3. Klik **Add sources** (Tambah sumber).`), insert:

```markdown

   ![Add sources di NotebookLM](img/01-add-sources.png)
```

After the "Hasil yang dijangka" paragraph (ending `… NotebookLM bersedia untuk menjawab soalan.`), insert:

```markdown

![Sumber diproses & tersenarai](img/01-sumber-diproses.png)
```

- [ ] **Step 3: Lab 02 — citation shot**

In `modul-2-notebooklm-gemini/lab/02-tanya-korpus.md`, after step 4 (ending `… sahkan jawapan itu benar-benar daripada dokumen.`), insert:

```markdown

   ![Jawapan dengan citation yang diklik](img/02-citation.png)
```

- [ ] **Step 4: Lab 03 — 2 placeholders**

In `modul-2-notebooklm-gemini/lab/03-kertas-projek-ke-slaid.md`, after Bahagian A step 3 (the briefing/study-guide list ending `… pecahan topik utama dan soalan.`), insert:

```markdown

   ![Output berstruktur dari Studio](img/03-studio-output.png)
```

After Bahagian B step 2 (the Gemini prompt code block), insert:

```markdown

   ![Rangka slaid dijana oleh Gemini](img/03-gemini-slaid.png)
```

- [ ] **Step 5: Lab 04 — minutes shot**

In `modul-2-notebooklm-gemini/lab/04-audio-mesyuarat-ke-minit.md`, after step 4 (the meeting-minutes table prompt code block), insert:

```markdown

   ![Draf minit mesyuarat berlajur](img/04-minit-jadual.png)
```

- [ ] **Step 6: Lab 05 — audio overview shot**

In `modul-2-notebooklm-gemini/lab/05-explore-lanjut.md`, after the blockquote `> Cuba jana **Audio Overview** … secara perbualan.`, insert:

```markdown

![Audio Overview di panel Studio](img/05-audio-overview.png)
```

- [ ] **Step 7: Verify and commit**

```bash
grep -rn "\.\./img/" modul-2-notebooklm-gemini/lab/   # expect: no output
git add modul-2-notebooklm-gemini/lab/
git commit -m "docs: tambah placeholder screenshot Modul 2 (lab/img/)"
```

---

### Task 5: Screenshot capture manifest

**Goal:** Write `docs/SCREENSHOTS.md` — a checklist covering every screenshot referenced in any lab, so the user can capture and drop in each PNG without rereading the labs.

**Files:**
- Create: `docs/SCREENSHOTS.md`

**Acceptance Criteria:**
- [ ] Every `img/NN-*.png` filename referenced in any lab (Modul 1 + Modul 2) appears as a row in the manifest.
- [ ] Each row has: checkbox, filename, lab/step, what to capture, notes.
- [ ] Rows grouped by module; a note explains placeholders show broken-image icons until captured, and that NotebookLM/Gemini UI changes over time.

**Verify:** `for f in $(grep -rhoE "img/[0-9]+-[a-z-]+\.png" modul-1-power-bi/lab modul-2-notebooklm-gemini/lab | sort -u); do grep -q "$(basename $f)" docs/SCREENSHOTS.md || echo "MISSING: $f"; done` → no `MISSING:` lines.

**Steps:**

- [ ] **Step 1: Write `docs/SCREENSHOTS.md`**

```markdown
# Manifest Screenshot

Senarai semua screenshot yang dirujuk oleh fail lab. Tangkap setiap imej,
namakan **tepat** seperti dalam jadual, dan simpan ke folder `lab/img/` modul
berkenaan. Sehingga ditangkap, pratonton markdown akan menunjukkan **ikon imej
rosak** — ini normal.

> **Nota:** UI NotebookLM/Gemini kerap berubah; tangkap apa yang paling hampir
> dengan langkah jika butang dinamakan berbeza.

## Modul 1 — Power BI (`modul-1-power-bi/lab/img/`)

| Siap | Fail | Lab / langkah | Apa yang ditangkap |
|------|------|---------------|--------------------|
| [ ] | `01-get-data.png` | Lab 1, langkah 2 | Menu Home → Get Data → Text/CSV |
| [ ] | `01-jadual-dimuat.png` | Lab 1, hasil | Panel Data menunjukkan 4 jadual |
| [ ] | `02-data-type.png` | Lab 2, langkah 3 | Menukar jenis data lajur di Power Query |
| [ ] | `02-custom-column-los.png` | Lab 2, langkah 6 | Dialog Custom Column dengan formula Tempoh_Tinggal |
| [ ] | `03-edit-relationship.png` | Lab 3, langkah 4 | Dialog Edit relationship (cardinality & cross filter) |
| [ ] | `03-model.png` | Lab 3, langkah 4 | Model view star schema (3 hubungan) |
| [ ] | `04-new-measure.png` | Lab 4, pengenalan | Cipta measure baharu pada formula bar |
| [ ] | `05-card-kpi.png` | Lab 5, bahagian A | Tiga kad KPI di atas kanvas |
| [ ] | `05-visual.png` | Lab 5, hasil | Semua visual (3 kad, 2 bar, 1 garis) |
| [ ] | `06-slicer.png` | Lab 6, langkah 3 | Tiga slicer ditambah di tepi |
| [ ] | `06-dashboard.png` | Lab 6, langkah 4 | Dashboard lengkap selepas tapis |
| [ ] | `07-export-pdf.png` | Lab 7, langkah 2 | File → Export → Export to PDF |

## Modul 2 — NotebookLM & Gemini (`modul-2-notebooklm-gemini/lab/img/`)

| Siap | Fail | Lab / langkah | Apa yang ditangkap |
|------|------|---------------|--------------------|
| [ ] | `01-add-sources.png` | Lab 1, langkah 3 | Butang Add sources di NotebookLM |
| [ ] | `01-sumber-diproses.png` | Lab 1, hasil | Senarai sumber diproses di panel kiri |
| [ ] | `02-citation.png` | Lab 2, langkah 4 | Jawapan dengan nombor citation diklik |
| [ ] | `03-studio-output.png` | Lab 3, Bahagian A | Output berstruktur (briefing/study guide) di Studio |
| [ ] | `03-gemini-slaid.png` | Lab 3, Bahagian B | Rangka slaid dijana oleh Gemini |
| [ ] | `04-minit-jadual.png` | Lab 4, langkah 4 | Draf minit mesyuarat berlajur |
| [ ] | `05-audio-overview.png` | Lab 5 | Audio Overview di panel Studio |
```

- [ ] **Step 2: Verify all referenced files are listed**

Run: `for f in $(grep -rhoE "img/[0-9]+-[a-z-]+\.png" modul-1-power-bi/lab modul-2-notebooklm-gemini/lab | sort -u); do grep -q "$(basename $f)" docs/SCREENSHOTS.md || echo "MISSING: $f"; done`
Expected: no output (every referenced screenshot is in the manifest).

- [ ] **Step 3: Commit**

```bash
git add docs/SCREENSHOTS.md
git commit -m "docs: manifest tangkapan screenshot (checklist semua lab)"
```

---

## Notes

- All `npx -y @marp-cli/marp` and `grep`/`mkdir` commands are written for the Bash tool (POSIX). On this Windows host, run them via the Bash tool, not PowerShell.
- If Marp's first-run download is blocked, commit the `.md` slide source without the PDF and note it; the render command stays valid for later.
