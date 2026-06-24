# Module 2 Labs — Working Healthcare Examples Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers-extended-cc:subagent-driven-development (recommended) or superpowers-extended-cc:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Module 2 Labs 1, 2, 3, 4, and 6 runnable out-of-the-box with concrete, healthcare/medical-records examples tied together by one coherent scenario.

**Architecture:** Add a new `module-2-notebooklm-gemini/examples/` folder holding synthetic scenario artifacts (a digitization project paper, a records-committee meeting transcript, and a TTS-generated audio of that transcript), use a real verified public MOH guideline as the corpus for Labs 1–2, and make surgical inline edits to each target lab so it walks through the specific example while keeping a short "use your own document" note. Lab 5 is untouched.

**Tech Stack:** Markdown (labs + artifacts), Python via `uv` (audio generation), macOS `say` + `afconvert` for TTS.

**User decisions (already made):**
- "Approach A" — concrete example pack + inline integration, scenario-threaded.
- Real public links + shipped synthetic artifacts (mix per lab).
- Corpus source: "Malaysian MOH/government only" — anchor on the official MOH medical-records guideline.
- "One coherent scenario across labs" — fictional Hospital Daerah Seri Aman digitizing paper records.
- Lab 4: "Transcript + generated audio file."
- Artifacts written in Bahasa Melayu; fictional hospital named "Hospital Daerah Seri Aman".

---

## Scenario facts (use these verbatim across all artifacts for consistency)

- **Setting:** Unit Rekod Perubatan, **Hospital Daerah Seri Aman**.
- **Project:** *Projek Pendigitalan Rekod Perubatan* — scan + index ~120,000 paper case files into an EMR over 18 months; storage room at capacity.
- **Fictional people:**
  - **Dr. Aisyah binti Rahman** — Timbalan Pengarah (Pengerusi Jawatankuasa Rekod Perubatan)
  - **Encik Faizal bin Osman** — Ketua Unit Rekod Perubatan
  - **Puan Lim Mei Ling** — Pegawai Teknologi Maklumat
  - **Cik Nurul Huda binti Ismail** — Penolong Pegawai Tadbir (Rekod)
- **Meeting:** *Mesyuarat Jawatankuasa Rekod Perubatan Bil. 2/2026*, 15 Jun 2026.
- **Indicative figures for the project paper:** anggaran kos RM450,000; latihan 25 kakitangan; sasaran imbasan 18 bulan; pengurangan masa carian fail dari ~30 minit ke <2 minit.

---

## File structure

| File | Responsibility |
|---|---|
| `module-2-notebooklm-gemini/examples/01-project-paper-pendigitalan-rekod.md` | Lab 3 source — the digitization proposal (project paper) |
| `module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-transcript.md` | Lab 4 source — committee meeting transcript |
| `module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-audio.m4a` | Lab 4 source — generated audio of the transcript |
| `module-2-notebooklm-gemini/examples/generate_audio.py` | Builds the `.m4a` from the transcript (reproducible) |
| `module-2-notebooklm-gemini/examples/README.md` | Scenario overview + artifact→lab map + synthetic-data disclaimer |
| `module-2-notebooklm-gemini/public-references.md` | Promote MOH guideline to a named primary corpus entry |
| `module-2-notebooklm-gemini/lab/01-set-up-notebook.md` | Point setup at the specific MOH guideline |
| `module-2-notebooklm-gemini/lab/02-query-the-corpus.md` | Scenario questions answerable from the MOH guideline |
| `module-2-notebooklm-gemini/lab/03-project-paper-to-slides.md` | Upload the project paper artifact |
| `module-2-notebooklm-gemini/lab/04-meeting-audio-to-minutes.md` | Upload the audio/transcript artifact |
| `module-2-notebooklm-gemini/lab/06-explore-further.md` | Scenario-anchored Gemini drafting prompts |

---

### Task 1: Create the digitization project paper artifact

**Goal:** A realistic ~2-page Malay *Kertas Cadangan* for the digitization project, rich enough to yield a meaningful 8-slide outline in Lab 3.

**Files:**
- Create: `module-2-notebooklm-gemini/examples/01-project-paper-pendigitalan-rekod.md`

**Acceptance Criteria:**
- [ ] First line is a synthetic-data disclaimer: `> **Nota:** Dokumen ini adalah contoh rekaan (synthetic) untuk tujuan latihan sahaja. Semua nama, fasiliti dan angka adalah fiktif.`
- [ ] Uses the scenario facts verbatim (Hospital Daerah Seri Aman, Encik Faizal bin Osman as pencadang, RM450,000, 18 bulan, ~120,000 fail).
- [ ] Contains these sections as Markdown headings: `Latar Belakang`, `Pernyataan Masalah`, `Objektif`, `Skop`, `Cadangan Penyelesaian`, `Implikasi Kos & Latihan`, `Cadangan Jadual Pelaksanaan`, `Kesimpulan & Cadangan`.
- [ ] `Cadangan Jadual Pelaksanaan` includes a Markdown table with at least 4 phases (Fasa | Aktiviti | Tempoh).
- [ ] Length 250–600 words of body text (substantive, not stub).

**Verify:** `test -f module-2-notebooklm-gemini/examples/01-project-paper-pendigitalan-rekod.md && grep -c '^## ' module-2-notebooklm-gemini/examples/01-project-paper-pendigitalan-rekod.md` → expect `8`

**Steps:**

- [ ] **Step 1: Write the project paper file** with the disclaimer header, a title `# Kertas Cadangan: Projek Pendigitalan Rekod Perubatan — Hospital Daerah Seri Aman`, the eight `## ` sections above, and the phases table. Populate with the scenario facts. Example opening for `## Pernyataan Masalah`: "Bilik simpanan rekod fizikal telah mencapai kapasiti maksimum dengan anggaran 120,000 fail kes. Purata masa mencari satu fail ialah lebih 30 minit, melambatkan perkhidmatan kaunter dan permohonan laporan perubatan."

- [ ] **Step 2: Verify structure**

Run: `grep -c '^## ' module-2-notebooklm-gemini/examples/01-project-paper-pendigitalan-rekod.md`
Expected: `8`

- [ ] **Step 3: Commit**

```bash
git add module-2-notebooklm-gemini/examples/01-project-paper-pendigitalan-rekod.md
git commit -m "feat(m2): add synthetic digitization project paper (Lab 3 source)"
```

---

### Task 2: Create the records-committee meeting transcript artifact

**Goal:** A realistic Malay meeting transcript of *Mesyuarat Jawatankuasa Rekod Perubatan Bil. 2/2026*, structured so Lab 4's minutes table comes out fully populated.

**Files:**
- Create: `module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-transcript.md`

**Acceptance Criteria:**
- [ ] First line is the synthetic-data disclaimer (same wording as Task 1).
- [ ] Has 4 named speakers from the scenario facts (Dr. Aisyah, Encik Faizal, Puan Lim Mei Ling, Cik Nurul Huda), each labelled as `**Nama:**` dialogue turns.
- [ ] Discussion explicitly produces at least 3 decisions and at least 3 follow-up actions, each with a named responsible officer and a target date — so a `Bil | Perkara | Keputusan/Tindakan | Pegawai Bertanggungjawab | Tarikh` table is fully derivable.
- [ ] Meeting topic ties to the digitization project (rollout progress, pilot scanning, training schedule, retention/disposal compliance).
- [ ] 250–500 words of dialogue.

**Verify:** `test -f module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-transcript.md && grep -c '^\*\*' module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-transcript.md` → expect ≥ 6 (multiple speaker turns)

**Steps:**

- [ ] **Step 1: Write the transcript file** with the disclaimer, a header block (`Mesyuarat: ... Bil. 2/2026`, `Tarikh: 15 Jun 2026`, `Pengerusi: Dr. Aisyah binti Rahman`, `Hadir: ...`), then dialogue turns. Ensure concrete actionable lines, e.g. Encik Faizal: "Saya cadangkan kita mulakan imbasan perintis untuk fail tahun 2023 dahulu." Dr. Aisyah (keputusan): "Diluluskan. Encik Faizal, sila siapkan imbasan perintis menjelang 31 Julai 2026." Include similar concrete actions for Puan Lim (sistem EMR) and Cik Nurul (jadual latihan 25 staf).

- [ ] **Step 2: Verify speaker turns**

Run: `grep -c '^\*\*' module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-transcript.md`
Expected: a number ≥ 6

- [ ] **Step 3: Commit**

```bash
git add module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-transcript.md
git commit -m "feat(m2): add synthetic records-committee meeting transcript (Lab 4 source)"
```

---

### Task 3: Generate the meeting audio from the transcript

**Goal:** A committed, playable `.m4a` of the meeting plus a reproducible script that builds it, using a distinct macOS voice per speaker.

**Files:**
- Create: `module-2-notebooklm-gemini/examples/generate_audio.py`
- Create (generated, committed): `module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-audio.m4a`

**Acceptance Criteria:**
- [ ] `generate_audio.py` has a module docstring with a `Run:` line: `uv run python module-2-notebooklm-gemini/examples/generate_audio.py` (mirrors `data/aggregate_dashboard_data.py` style).
- [ ] Script parses speaker turns from `02-mesyuarat-jk-rekod-transcript.md`, assigns a distinct `say` voice per speaker (e.g. a `SPEAKER_VOICES` dict), synthesizes each turn, concatenates, and emits the `.m4a` via `afconvert` (or `say -o ... .m4a` if supported).
- [ ] Script strips Markdown markers (`**`, `>`, headings) before speaking so they aren't read aloud.
- [ ] Running the script produces a non-empty `.m4a` that opens in a media player.
- [ ] Script fails gracefully with a clear message if not on macOS / `say` missing.

**Verify:** `uv run python module-2-notebooklm-gemini/examples/generate_audio.py && test -s module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-audio.m4a && afinfo module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-audio.m4a` → prints audio info, non-zero duration

**Steps:**

- [ ] **Step 1: Write `generate_audio.py`**

```python
"""Generate the Lab 4 meeting audio from the committee transcript.

Reads 02-mesyuarat-jk-rekod-transcript.md, speaks each turn with a distinct
macOS voice per speaker, and writes 02-mesyuarat-jk-rekod-audio.m4a.

Run:
    uv run python module-2-notebooklm-gemini/examples/generate_audio.py
"""
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).parent
TRANSCRIPT = HERE / "02-mesyuarat-jk-rekod-transcript.md"
OUT = HERE / "02-mesyuarat-jk-rekod-audio.m4a"

# Distinct built-in macOS voices per speaker (intelligible for Malay text).
SPEAKER_VOICES = {
    "Dr. Aisyah binti Rahman": "Samantha",
    "Encik Faizal bin Osman": "Daniel",
    "Puan Lim Mei Ling": "Karen",
    "Cik Nurul Huda binti Ismail": "Moira",
}
DEFAULT_VOICE = "Alex"

TURN_RE = re.compile(r"^\*\*(?P<speaker>[^:*]+):\*\*\s*(?P<text>.+)$")


def clean(text: str) -> str:
    """Strip markdown so it isn't read aloud."""
    text = re.sub(r"[*_>#`]", "", text)
    return text.strip()


def main() -> None:
    if not shutil.which("say"):
        sys.exit("ERROR: macOS 'say' command not found. Run this on macOS.")

    turns = []
    for line in TRANSCRIPT.read_text(encoding="utf-8").splitlines():
        m = TURN_RE.match(line.strip())
        if m:
            turns.append((m.group("speaker").strip(), clean(m.group("text"))))
    if not turns:
        sys.exit("ERROR: no '**Speaker:** text' turns found in transcript.")

    with tempfile.TemporaryDirectory() as tmp:
        parts = []
        for i, (speaker, text) in enumerate(turns):
            voice = SPEAKER_VOICES.get(speaker, DEFAULT_VOICE)
            aiff = Path(tmp) / f"{i:03d}.aiff"
            subprocess.run(["say", "-v", voice, "-o", str(aiff), text],
                           check=True)
            parts.append(aiff)

        combined = Path(tmp) / "combined.aiff"
        subprocess.run(["sox", *map(str, parts), str(combined)], check=False) \
            if shutil.which("sox") else None
        # Fallback concat via afconvert per-part then cat is unreliable; prefer
        # sox when available, else concatenate text into one say call.
        if not combined.exists():
            full = " ... ".join(t for _, t in turns)
            subprocess.run(["say", "-o", str(combined), full], check=True)

        subprocess.run(
            ["afconvert", str(combined), str(OUT), "-f", "m4af", "-d", "aac"],
            check=True)

    print(f"Wrote {OUT.relative_to(HERE.parent.parent)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the script**

Run: `uv run python module-2-notebooklm-gemini/examples/generate_audio.py`
Expected: prints `Wrote module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-audio.m4a`

- [ ] **Step 3: Confirm the audio is valid**

Run: `afinfo module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-audio.m4a`
Expected: non-zero duration, AAC/m4a format. (If `sox` is unavailable, the fallback single-voice path still produces valid audio — acceptable.)

- [ ] **Step 4: Commit**

```bash
git add module-2-notebooklm-gemini/examples/generate_audio.py module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-audio.m4a
git commit -m "feat(m2): generate meeting audio + reproducible TTS script (Lab 4)"
```

---

### Task 4: Write the examples README (scenario hub)

**Goal:** A README that states the scenario, maps each artifact to its lab, and repeats the synthetic-data disclaimer.

**Files:**
- Create: `module-2-notebooklm-gemini/examples/README.md`

**Acceptance Criteria:**
- [ ] Describes the Hospital Daerah Seri Aman digitization scenario in 1 short paragraph.
- [ ] Contains a table mapping each artifact file to the lab that uses it (Lab 3 → project paper; Lab 4 → transcript + audio; Lab 6 → reuses project paper).
- [ ] States all artifacts are synthetic/fictional.
- [ ] Links to each artifact file with working relative paths.

**Verify:** `test -f module-2-notebooklm-gemini/examples/README.md && grep -q "Seri Aman" module-2-notebooklm-gemini/examples/README.md` → exit 0

**Steps:**

- [ ] **Step 1: Write `examples/README.md`** with title `# Module 2 — Contoh Senario (Synthetic)`, the scenario paragraph, the artifact→lab table referencing `01-project-paper-pendigitalan-rekod.md`, `02-mesyuarat-jk-rekod-transcript.md`, `02-mesyuarat-jk-rekod-audio.m4a`, and a disclaimer line.

- [ ] **Step 2: Verify links resolve**

Run: `for f in $(grep -oE '\(0[12][^)]+\)' module-2-notebooklm-gemini/examples/README.md | tr -d '()'); do test -f "module-2-notebooklm-gemini/examples/$f" && echo "OK $f" || echo "MISSING $f"; done`
Expected: all `OK`, no `MISSING`

- [ ] **Step 3: Commit**

```bash
git add module-2-notebooklm-gemini/examples/README.md
git commit -m "docs(m2): add examples README mapping scenario artifacts to labs"
```

---

### Task 5: Promote the MOH guideline in public-references.md

**Goal:** Make the official MOH medical-records guideline the named primary corpus document, with a stable fallback link and a USB-backup note.

**Files:**
- Modify: `module-2-notebooklm-gemini/public-references.md`

**Acceptance Criteria:**
- [ ] Adds a named primary entry: "Garis Panduan Pengendalian dan Pengurusan Rekod Perubatan Pesakit di Fasiliti KKM" with the direct `moh.gov.my` PDF URL, marked `[verify]`.
- [ ] Adds the KKM portal listing URL (`kkm.synchronet.my/...`) as a fallback path to the same document.
- [ ] Adds a note about the `moh.gov.my` TLS-certificate quirk and to keep a USB backup.
- [ ] Existing presenter pre-course verification checklist is preserved; one bullet added: "download a backup copy of the guideline PDF to USB."

**Verify:** `grep -q "Pengendalian dan Pengurusan Rekod Perubatan" module-2-notebooklm-gemini/public-references.md && grep -q "kkm.synchronet.my" module-2-notebooklm-gemini/public-references.md` → exit 0

**Steps:**

- [ ] **Step 1: Edit `public-references.md`** — under "Suggested documents", replace the generic first row with the named MOH guideline (direct PDF URL + `[verify]`), add a fallback-URL line and the TLS/USB note. The two URLs:
  - Primary: `https://www.moh.gov.my/images/04-penerbitan/pekeliling/Garis%20Panduan%20Pengendalian%20dan%20Pengurusan%20Rekod%20Perubatan%20Pesakit%20di%20Fasiliti%20KKM.pdf`
  - Fallback: `https://kkm.synchronet.my/en/publications-and-reports/dasar-akta-polisi-garis-panduan/garis-panduan-umum-kkm/senarai-garis-panduan-umum-awam/garis-panduan-pengendalian-dan-pengurusan-rekod-perubatan-pesakit-di-fasiliti-kkm`
- [ ] **Step 2: Add the USB-backup bullet** to the presenter checklist section.

- [ ] **Step 3: Verify**

Run: `grep -q "Pengendalian dan Pengurusan Rekod Perubatan" module-2-notebooklm-gemini/public-references.md && grep -q "kkm.synchronet.my" module-2-notebooklm-gemini/public-references.md && echo OK`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add module-2-notebooklm-gemini/public-references.md
git commit -m "docs(m2): promote MOH records guideline as primary corpus reference"
```

---

### Task 6: Point Lab 1 setup at the specific MOH guideline

**Goal:** Lab 1 tells participants to download the one named MOH guideline as Hospital Seri Aman's governing reference, keeping the "use your own document" note.

**Files:**
- Modify: `module-2-notebooklm-gemini/lab/01-set-up-notebook.md`

**Acceptance Criteria:**
- [ ] Step 4 names the specific MOH guideline (from `public-references.md`) instead of "download 2–3 documents".
- [ ] Frames it as Hospital Daerah Seri Aman's reference; suggested notebook name "Rujukan Rekod Perubatan — Hospital Seri Aman".
- [ ] Retains a one-line "you may substitute your own authorized document" note.
- [ ] Existing screenshots and the offline-backup tip are preserved.
- [ ] "Next" link still points to Lab 2.

**Verify:** `grep -q "Seri Aman" module-2-notebooklm-gemini/lab/01-set-up-notebook.md && grep -q "public-references.md" module-2-notebooklm-gemini/lab/01-set-up-notebook.md` → exit 0

**Steps:**

- [ ] **Step 1: Edit Lab 1** Step 4 to reference the specific guideline + scenario framing + notebook-name suggestion, keeping the substitute-your-own note, screenshots, and tip.

- [ ] **Step 2: Verify**

Run: `grep -q "Seri Aman" module-2-notebooklm-gemini/lab/01-set-up-notebook.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add module-2-notebooklm-gemini/lab/01-set-up-notebook.md
git commit -m "docs(m2): point Lab 1 setup at the MOH records guideline (Seri Aman scenario)"
```

---

### Task 7: Tailor Lab 2 corpus questions to the MOH guideline

**Goal:** Lab 2's example questions are answerable from the actual MOH guideline and framed in the Seri Aman scenario.

**Files:**
- Modify: `module-2-notebooklm-gemini/lab/02-query-the-corpus.md`

**Acceptance Criteria:**
- [ ] Replaces the three generic example questions with scenario questions answerable from the guideline, e.g. retention period for medical records, who approves a medical-report request, terms of reference of the Jawatankuasa Rekod Perubatan.
- [ ] Keeps the citation-verify step (clicking `[1]`) and the screenshot.
- [ ] Follow-up question examples reference the same guideline.
- [ ] "Next" link still points to Lab 3.

**Verify:** `grep -qi "tempoh penyimpanan" module-2-notebooklm-gemini/lab/02-query-the-corpus.md` → exit 0

**Steps:**

- [ ] **Step 1: Edit Lab 2** — swap the example questions (Malay) to: "Apakah tempoh penyimpanan rekod perubatan pesakit sebelum boleh dilupuskan?", "Siapakah yang bertanggungjawab meluluskan permohonan laporan perubatan?", "Apakah terma rujukan Jawatankuasa Rekod Perubatan?"; keep the citation step + screenshot; update follow-ups.

- [ ] **Step 2: Verify**

Run: `grep -qi "tempoh penyimpanan" module-2-notebooklm-gemini/lab/02-query-the-corpus.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add module-2-notebooklm-gemini/lab/02-query-the-corpus.md
git commit -m "docs(m2): tailor Lab 2 queries to the MOH records guideline"
```

---

### Task 8: Wire Lab 3 to the project-paper artifact

**Goal:** Lab 3 uploads the shipped project paper, producing a slide outline about the digitization proposal.

**Files:**
- Modify: `module-2-notebooklm-gemini/lab/03-project-paper-to-slides.md`

**Acceptance Criteria:**
- [ ] Part A Step 1 instructs uploading `../examples/01-project-paper-pendigitalan-rekod.md` (relative link from the lab folder), with a "or use your own project paper" note.
- [ ] A refine-prompt example references a real section of the paper (e.g. "ringkaskan slaid Implikasi Kos & Latihan").
- [ ] Existing Gemini prompt block and screenshots preserved.
- [ ] "Next" link still points to Lab 4.

**Verify:** `grep -q "examples/01-project-paper-pendigitalan-rekod.md" module-2-notebooklm-gemini/lab/03-project-paper-to-slides.md && test -f module-2-notebooklm-gemini/examples/01-project-paper-pendigitalan-rekod.md` → exit 0

**Steps:**

- [ ] **Step 1: Edit Lab 3** Part A Step 1 to reference the artifact via `../examples/01-project-paper-pendigitalan-rekod.md`, keep substitute note, update one refine prompt to a real section.

- [ ] **Step 2: Verify link target exists**

Run: `grep -q "examples/01-project-paper-pendigitalan-rekod.md" module-2-notebooklm-gemini/lab/03-project-paper-to-slides.md && test -f module-2-notebooklm-gemini/examples/01-project-paper-pendigitalan-rekod.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add module-2-notebooklm-gemini/lab/03-project-paper-to-slides.md
git commit -m "docs(m2): wire Lab 3 to the digitization project-paper artifact"
```

---

### Task 9: Wire Lab 4 to the meeting audio/transcript artifacts

**Goal:** Lab 4 uploads the shipped audio (or transcript), producing populated minutes for the committee meeting.

**Files:**
- Modify: `module-2-notebooklm-gemini/lab/04-meeting-audio-to-minutes.md`

**Acceptance Criteria:**
- [ ] Step 1/2 instruct uploading `../examples/02-mesyuarat-jk-rekod-audio.m4a` (or the transcript `../examples/02-mesyuarat-jk-rekod-transcript.md`), with the existing permission/confidentiality warning kept.
- [ ] Keeps the summary prompt and the minutes-table prompt (Bil | Perkara | Keputusan/Tindakan | Pegawai | Tarikh) and the screenshot.
- [ ] References the meeting by name (Bil. 2/2026) so the output is recognizable.
- [ ] "Next" link still points to Lab 5.

**Verify:** `grep -q "examples/02-mesyuarat-jk-rekod-audio.m4a" module-2-notebooklm-gemini/lab/04-meeting-audio-to-minutes.md && test -f module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-audio.m4a` → exit 0

**Steps:**

- [ ] **Step 1: Edit Lab 4** Steps 1–2 to upload the audio artifact (transcript fallback), name the meeting, keep prompts/warning/screenshot.

- [ ] **Step 2: Verify link targets exist**

Run: `grep -q "examples/02-mesyuarat-jk-rekod-audio.m4a" module-2-notebooklm-gemini/lab/04-meeting-audio-to-minutes.md && test -f module-2-notebooklm-gemini/examples/02-mesyuarat-jk-rekod-audio.m4a && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add module-2-notebooklm-gemini/lab/04-meeting-audio-to-minutes.md
git commit -m "docs(m2): wire Lab 4 to the committee meeting audio/transcript"
```

---

### Task 10: Anchor Lab 6 prompts to the scenario

**Goal:** Lab 6's Gemini drafting prompts use the Seri Aman digitization project so they connect to the rest of the module.

**Files:**
- Modify: `module-2-notebooklm-gemini/lab/06-explore-further.md`

**Acceptance Criteria:**
- [ ] The "Draft a memo" prompt is about announcing the digitization project to the Pengarah.
- [ ] The "Summarize a report" prompt references summarizing the Lab 3 project paper to 5 points.
- [ ] The Audio Overview suggestion references the MOH guideline from Lab 1.
- [ ] Existing structure, the "Challenge: use your own documents" section, and the data warning are preserved.

**Verify:** `grep -qi "pendigitalan" module-2-notebooklm-gemini/lab/06-explore-further.md` → exit 0

**Steps:**

- [ ] **Step 1: Edit Lab 6** — update the memo prompt (announce the projek pendigitalan to the Pengarah), the summarize prompt (the Lab 3 paper), and the Audio Overview suggestion (the MOH guideline); keep the rest.

- [ ] **Step 2: Verify**

Run: `grep -qi "pendigitalan" module-2-notebooklm-gemini/lab/06-explore-further.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add module-2-notebooklm-gemini/lab/06-explore-further.md
git commit -m "docs(m2): anchor Lab 6 Gemini prompts to the digitization scenario"
```

---

### Task 11: Final consistency & link verification

**Goal:** Confirm no dangling references, all internal links resolve, and the README lab map is still accurate.

**Files:**
- Modify (only if a gap is found): any of the above.

**Acceptance Criteria:**
- [ ] Every relative markdown link in the edited labs and `examples/README.md` resolves to an existing file.
- [ ] Each lab's "Next" link points to the correct subsequent lab.
- [ ] `module-2-notebooklm-gemini/README.md` lab map rows still match the lab files (no time changes expected; content swap only).
- [ ] No remaining `[paste here]`/generic placeholder text in the five edited labs where a concrete artifact now applies.

**Verify:**
```bash
cd module-2-notebooklm-gemini && \
for md in lab/01-set-up-notebook.md lab/02-query-the-corpus.md lab/03-project-paper-to-slides.md lab/04-meeting-audio-to-minutes.md lab/06-explore-further.md examples/README.md; do \
  d=$(dirname "$md"); \
  grep -oE '\]\(([^)]+\.(md|m4a|png|py))\)' "$md" | sed -E 's/\]\(|\)//g' | while read -r l; do \
    case "$l" in http*) continue;; esac; \
    test -f "$d/$l" && echo "OK $md -> $l" || echo "BROKEN $md -> $l"; \
  done; \
done | grep BROKEN && echo "FAIL: broken links" || echo "PASS: all links resolve"
```
Expected: `PASS: all links resolve`

**Steps:**

- [ ] **Step 1: Run the link checker above.** If any `BROKEN` line appears, fix the offending reference and re-run.

- [ ] **Step 2: Spot-check Next links and the README lab map** by reading the bottom of each edited lab and the `module-2-notebooklm-gemini/README.md` lab-map table.

- [ ] **Step 3: Commit any fixes**

```bash
git add -A module-2-notebooklm-gemini
git commit -m "fix(m2): resolve dangling links / consistency after scenario integration" || echo "nothing to fix"
```

---

## Self-Review

- **Spec coverage:** examples/ folder (T1–T4), MOH corpus (T5), Lab 1/2 (T6/T7), Lab 3 (T8), Lab 4 incl. audio (T2,T3,T9), Lab 6 (T10), data-safety disclaimers (T1,T2,T4), verification/links (T11). All spec sections mapped. Lab 5 correctly untouched.
- **Placeholders:** none — artifact tasks specify concrete scenario facts, names, figures, headings; the audio script is fully written.
- **Type/name consistency:** artifact filenames identical across file-structure table, artifact tasks, and lab-edit tasks (`01-project-paper-pendigitalan-rekod.md`, `02-mesyuarat-jk-rekod-transcript.md`, `02-mesyuarat-jk-rekod-audio.m4a`); speaker names match between Task 2 and Task 3's `SPEAKER_VOICES`.
