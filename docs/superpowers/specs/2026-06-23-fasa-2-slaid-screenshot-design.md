# Reka Bentuk: Fasa 2 — Slaid Pengenalan + Screenshot Lab

**Tarikh:** 2026-06-23
**Penceramah:** Dr. Muhammad Naufal bin Nordin
**Kursus:** Kursus Lanjutan (Advanced) — Pegawai Tadbir (Rekod Perubatan) & Penolong, KKM 2026
**Slot:** 25 Jun 2026 (Khamis)
**Rujukan:** Sambungan kepada [reka bentuk Fasa 1](2026-06-22-modul-latihan-powerbi-notebooklm-gemini-design.md)

## 1. Konteks & Matlamat

Fasa 1 (tulang belakang kandungan markdown + dataset sintetik + pautan awam) telah siap dan di-commit. Fasa 2 asalnya membungkus empat perkara: slaid, screenshot, fail `.pbix` siap, dan fail audio. Sesi ini memberi tumpuan kepada **dua sahaja** yang paling perlu sebelum kursus:

1. **Slaid pengenalan** untuk ceramah ~20 minit setiap slot (2 deck).
2. **Screenshot dalam lab** — gantikan placeholder dengan struktur konsisten + manifest tangkapan.

`.pbix` siap dan fail audio **dikecualikan** daripada sesi ini (kekal Fasa 2 lanjutan).

## 2. Keputusan Reka Bentuk (terkunci)

| # | Keputusan |
|---|---|
| Tooling slaid | **Marp** (Markdown → PPTX/PDF/HTML) |
| Render slaid | **Marp CLI via `npx @marp-team/marp-cli`** (Approach A). `.md` ialah sumber kanonik; PDF dirender & di-commit |
| Skop slaid | **Dua deck pengenalan sahaja** (satu setiap slot, ~20 min / ~12–15 slaid) |
| Sumber kandungan slaid | Nota pengenalan sedia ada dalam `README.md` setiap modul (slaid & lab kekal selaras) |
| Tema | **Tema terbina-dalam Marp yang bersih** (cth. `default`/`gaia`) + footer kursus; tiada logo rasmi di-commit |
| Bahasa | BM primary, istilah teknikal English dalam `code`/petikan (sama dengan repo) |
| Screenshot | **Manifest + placeholder + folder** — audit semua lab, seragamkan rujukan, sediakan checklist tangkapan |
| Tangkapan imej sebenar | Dilakukan oleh pengguna (tidak boleh dijana AI); repo sediakan struktur sahaja |

## 3. Seni Bina Repositori (fail baharu)

```
slides/
  README.md                     ← cara render (arahan npx Marp CLI), nota tema
  modul-1-power-bi.md           ← Marp deck: pengenalan Slot 1 (~20 min)
  modul-2-notebooklm-gemini.md  ← Marp deck: pengenalan Slot 2 (~20 min)
  build/
    modul-1-power-bi.pdf        ← PDF dirender (di-commit; presentable tanpa setup)
    modul-2-notebooklm-gemini.pdf
modul-1-power-bi/lab/img/       ← folder screenshot (.gitkeep)
modul-2-notebooklm-gemini/lab/img/
docs/SCREENSHOTS.md             ← manifest/checklist tangkapan (semua shot, ikut lab/langkah)
```

**Nota commit PDF:** PDF dirender guna `npx @marp-team/marp-cli` dan di-commit supaya ada fail presentable pada hari kursus tanpa sebarang setup. Jika rangkaian menghalang muat turun pakej Marp, fallback = commit sumber `.md` + resipi build sahaja.

## 4. Slaid — Kandungan

Kedua-dua deck bersumberkan nota pengenalan sedia ada dalam `README.md` setiap modul. Tahap tajuk (titles + beberapa bullet) sahaja — detail langkah-demi-langkah kekal dalam lab, bukan slaid. ~12–15 slaid setiap deck.

**Deck 1 — `slides/modul-1-power-bi.md` (pengenalan Slot 1):**

1. Tajuk (kursus, slot, penceramah, tarikh)
2. Apa itu Power BI & kenapa relevan untuk statistik perubatan (Excel manual → dashboard automatik)
3. Aliran kerja: Get Data → Transform → Model → Visualize → Share
4. Lawatan antara muka: Report / Data / Model views
5. Pratonton dashboard akhir (KPI cards, bar, line, slicer)
6. Apa yang kita bina hari ini (peta 7 lab)
7. Nota keselamatan data (dataset sintetik) + jangkaan hands-on
8. Mari mula → Lab 1

**Deck 2 — `slides/modul-2-notebooklm-gemini.md` (pengenalan Slot 2):**

1. Tajuk
2. NotebookLM (grounded + citation) vs Gemini (generatif umum)
3. Kenapa relevan: berhenti "flip-flip paper" → tanya korpus
4. Konsep: *grounding*, *citation*
5. ⚠️ Amaran data sensitif (jangan upload data pesakit sebenar)
6. 3 aliran kerja teras (tanya korpus / kertas→slaid / audio→minit) + explore
7. Peta 5 lab + rujukan awam
8. Mari mula → Lab 1

**Marp front-matter setiap deck:** `marp: true`, tema terbina-dalam terpilih, `paginate: true`, footer kursus + penceramah.

## 5. Screenshot — Manifest, Placeholder, Folder

**Folder:** cipta `modul-1-power-bi/lab/img/` dan `modul-2-notebooklm-gemini/lab/img/` (dengan `.gitkeep` supaya folder kosong boleh commit).

**Konvensyen placeholder:** setiap rujukan screenshot diseragamkan sebagai `![Keterangan ringkas](img/NN-nama.png)`, diletak betul-betul selepas langkah yang diilustrasikan. Penamaan = nombor lab + slug pendek (cth. `02-power-query.png`). Rujukan sedia ada yang tidak konsisten (lab 01/03/05/06 modul-1) diperbetulkan; yang tiada ditambah merentas semua lab.

**Liputan:** satu screenshot bagi setiap langkah visual penting (bukan setiap langkah) — biasanya 1–3 setiap lab, pada saat pelajar paling perlu sahkan "adakah saya di skrin yang betul". Lab NotebookLM/Gemini turut dapat placeholder, dengan nota bahawa UI mereka berubah dari masa ke masa.

**`docs/SCREENSHOTS.md` manifest:** jadual checklist — `[ ]` | nama fail | lab/langkah | apa yang ditangkap | nota — dikumpul ikut modul, supaya pengguna boleh tangkap & letak setiap PNG tanpa baca semula lab.

**Caveat:** placeholder tidak akan render sehingga imej ditangkap — ikon imej rosak akan muncul dalam pratonton markdown sementara itu. Ini dijangka; manifest menjejak apa yang belum siap.

## 6. Skop yang Dikecualikan (YAGNI)

- Fail `.pbix` siap (kekal Fasa 2 lanjutan)
- Fail audio contoh / transkrip (kekal Fasa 2 lanjutan)
- Tema/branding KKM rasmi + logo (boleh ditambah kemudian; tema bersih sekarang)
- Slaid divider per-lab atau deck pengajaran penuh (pengenalan sahaja)
- Tangkapan imej sebenar (dilakukan oleh pengguna di mesin sendiri)

## 7. Pengesahan (verification)

- `npx @marp-team/marp-cli slides/modul-1-power-bi.md --pdf` menghasilkan PDF tanpa error; sama untuk deck 2.
- Setiap deck dibuka & semua slaid render (teks BM + istilah English betul).
- Semua lab: rujukan placeholder mengikut konvensyen `![...](img/NN-nama.png)`; folder `img/` wujud.
- `docs/SCREENSHOTS.md` menyenaraikan setiap fail screenshot yang dirujuk dalam mana-mana lab (tiada rujukan tertinggal).
