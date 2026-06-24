# Design Spec: Module 2 Labs — Working Healthcare Examples

**Date:** 2026-06-24
**Author:** Dr. Muhammad Naufal bin Nordin (with Claude Code)
**Status:** Approved (design); pending implementation plan

---

## Problem

Module 2 labs 1, 2, 3, 4, and 6 are structurally sound but **abstract**. They tell
participants to "upload a public document," "paste your project paper," or "record a
meeting," using `[paste here]` placeholders. `public-references.md` lists only
`[verify]` placeholder links with nothing concrete.

The audience — Administrative Officers (Medical Records) under the KKM 2026 National
Advanced Course — benefits most from a lab they can **run end-to-end out of the box**
with a concrete, healthcare/medical-records example. Lab 5 (Gemini Canvas dashboard)
is already satisfactory and is **out of scope**.

## Goal

Make Labs 1, 2, 3, 4, and 6 runnable with concrete, healthcare-relevant examples,
tied together by a single coherent scenario, while preserving a "use your own
document" path so participants can later apply the workflows to their real work.

## Approach (chosen)

**Concrete example pack + inline integration**, scenario-threaded:

- Ship synthetic scenario artifacts in a new `examples/` folder.
- Use a real, verified public MOH document as the corpus for Labs 1–2.
- Edit each target lab to walk through the specific example inline, keeping a short
  "use your own document" note.

Rejected alternatives: dual-track "Worked Example" callouts (feels bolted-on);
full scenario-first rewrite (over-rewrites labs that already work, weakens
"apply to your own documents" framing).

## The scenario (narrative spine)

The **Unit Rekod Perubatan of a fictional "Hospital Daerah Seri Aman"** is launching a
project to **digitize its paper medical records** and tighten records-management
practice. Every lab advances one arc: **reference → ask → propose → decide → communicate.**

| Lab | Story beat | Source used |
|---|---|---|
| 1 — Set up | The unit gathers its governing reference | Real public MOH guideline (linked) |
| 2 — Query corpus | Officers ask the guideline procedural questions | Same MOH guideline |
| 3 — Paper → slides | Unit head presents the digitization proposal to management | Synthetic project paper |
| 4 — Audio → minutes | Records Committee reviews the rollout; minutes needed | Synthetic transcript + audio |
| 6 — Explore further | Officer drafts a memo to the Pengarah + summarizes the proposal | Reuses Lab 3 paper |

Lab 5 is unchanged and slots in naturally as "visualize the COVID figures."

**Naming/language defaults (approved):**
- Fictional hospital: **"Hospital Daerah Seri Aman"** (clearly fictional, neutral).
- All shipped artifacts written in **Bahasa Melayu** (matches audience + existing prompts).

## Anchor reference document

**"Garis Panduan Pengendalian dan Pengurusan Rekod Perubatan Pesakit di Fasiliti KKM"**
— official MOH general guideline (Medical Development Division, ~2023, last updated
Oct 2025). Directly about handling/managing patient medical records at MOH facilities,
in Bahasa Melayu.

- Primary URL: `https://www.moh.gov.my/images/04-penerbitan/pekeliling/Garis%20Panduan%20Pengendalian%20dan%20Pengurusan%20Rekod%20Perubatan%20Pesakit%20di%20Fasiliti%20KKM.pdf`
- Fallback (official portal listing): `https://kkm.synchronet.my/en/publications-and-reports/dasar-akta-polisi-garis-panduan/garis-panduan-umum-kkm/senarai-garis-panduan-umum-awam/garis-panduan-pengendalian-dan-pengurusan-rekod-perubatan-pesakit-di-fasiliti-kkm`
- Note: the direct `moh.gov.my` PDF hits a TLS-certificate error in some clients;
  treat as `[verify]` until confirmed at the venue, and keep a USB backup.
- Optional second source: older **Garis Panduan Rekod Perubatan KKM 3/2005** or a JPA
  records-management circular, if a live public link verifies.

## Components

### 1. `examples/` folder (new)

```
module-2-notebooklm-gemini/
  examples/
    README.md                                # scenario overview + artifact→lab map + disclaimer
    01-project-paper-pendigitalan-rekod.md   # Lab 3 source
    02-mesyuarat-jk-rekod-transcript.md      # Lab 4 source (transcript)
    02-mesyuarat-jk-rekod-audio.m4a          # Lab 4 source (generated audio)
    generate_audio.py                        # builds the .m4a from the transcript
```

- **`01-project-paper-pendigitalan-rekod.md`** — realistic ~2-page *Kertas Cadangan*
  in Malay: latar belakang (paper-records pain points), objektif, skop, cadangan
  penyelesaian (scan + EMR), implikasi kos/latihan, cadangan jadual pelaksanaan.
  Substantive enough to yield a meaningful 8-slide outline.
- **`02-mesyuarat-jk-rekod-transcript.md`** — ~3–4 named speakers (Pengerusi, Ketua
  Unit Rekod, Pegawai IT, etc.) discussing the rollout: items raised, decisions, and
  follow-up actions with responsible officers + dates — so the minutes table comes
  out genuinely populated.
- **`02-mesyuarat-jk-rekod-audio.m4a`** — generated from the transcript by
  `generate_audio.py` using macOS `say` with **different voices per speaker**,
  converted to `.m4a` (e.g. via `afconvert`). Committed so participants need only the
  file. Malay text read with built-in (English-ish) voices — intelligible and clearly
  synthetic; acceptable for a "how audio→minutes works" demo.
- **`generate_audio.py`** — committed for reproducibility; reads the transcript,
  assigns a voice per speaker, emits the `.m4a`.
- **`README.md`** — states the scenario, lists artifacts, maps each to its lab,
  repeats the synthetic-data disclaimer.

### 2. Lab edits (surgical; keep structure + screenshots)

- **Lab 1 (Set up):** Step 4 → download *this specific* MOH guideline (link from
  `public-references.md`) as Hospital Seri Aman's governing reference. Notebook name
  suggestion → *"Rujukan Rekod Perubatan — Hospital Seri Aman"*. Keep offline-backup tip.
- **Lab 2 (Query corpus):** Replace generic questions with ones answerable from the
  actual MOH guideline, e.g. retention period, who approves a medical-report request,
  Jawatankuasa Rekod Perubatan terms. Citation-verify step points at a known section.
  Exact wording finalized against the live PDF during implementation.
- **Lab 3 (Paper → slides):** Step 1 → upload `examples/01-project-paper-pendigitalan-rekod.md`.
  Gemini prompts stay; outline now about the digitization proposal; refine prompts
  reference real slides (e.g. "make the kos/implikasi slide more concise").
- **Lab 4 (Audio → minutes):** Step 1 → upload `examples/02-mesyuarat-jk-rekod-audio.m4a`
  (or the transcript `.md`). Summary + minutes-table prompts stay; outputs populate
  from the committee meeting.
- **Lab 6 (Explore further):** Anchor Gemini drafting prompts to the scenario — memo to
  the Pengarah announcing the project; summarize the Lab 3 paper to 5 points. "Audio
  Overview" suggestion points at the MOH guideline from Lab 1.

### 3. `public-references.md` update

- Promote the MOH guideline to a named primary entry with real URL, marked `[verify]`
  until confirmed live at the venue.
- Add the KKM portal listing URL as a stable fallback path.
- Keep the presenter pre-course verification checklist; add "download a backup copy of
  the guideline PDF to USB."

## Data safety

- All shipped artifacts are clearly fabricated; "Hospital Daerah Seri Aman" and all
  names are fictional. Each artifact carries a one-line synthetic-data disclaimer header.
- Labs keep existing "do not upload real patient data / confidential PUU" warnings.

## Verification

- `generate_audio.py` runs on macOS and produces a playable `.m4a`; committed file
  opens in a player.
- Each edited lab references a file/link that actually exists in the repo (no dangling
  paths) — checked by listing `examples/` against lab references.
- Project paper and transcript are substantive enough to yield a real 8-slide outline
  and a fully-populated minutes table (sanity-read, not automated).
- All internal markdown links (lab→examples, README→labs) resolve.
- `README.md` lab map / time estimates still accurate (content swap, not added labs;
  no time change expected).

## Out of scope (YAGNI)

- No rewrite of Lab 5.
- No rendering the project paper to PDF (markdown upload works in NotebookLM).
- No automated link-checker tooling.
- No English translations of the artifacts.
