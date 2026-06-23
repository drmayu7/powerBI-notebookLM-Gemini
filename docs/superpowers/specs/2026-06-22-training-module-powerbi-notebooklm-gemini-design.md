# Reka Bentuk: Modul Latihan Power BI + NotebookLM & Gemini

**Tarikh:** 2026-06-22
**Penceramah:** Dr. Muhammad Naufal bin Nordin (Ketua Penolong Pengarah Kanan, Bahagian Perancangan, KKM)
**Kursus:** Kursus Lanjutan (Advanced) — Pegawai Tadbir (Rekod Perubatan) & Penolong Pegawai Tadbir, Peringkat Kebangsaan KKM 2026
**Slot:** 25 Jun 2026 (Khamis)

## 1. Konteks & Matlamat

Repositori awam GitHub yang mengandungi modul latihan untuk dirujuk oleh peserta kursus. Dua slot latihan oleh penceramah pada 25 Jun 2026:

1. **8:00 pg – 11:30 tgh** (rehat 10:00–10:30) — *Transformasi Statistik Perubatan menggunakan Power BI* (~3 jam)
2. **11:30 tgh – 4:00 ptg** (makan tengah hari 1:00–2:00) — *NotebookLM dan Gemini: Potensi Kecerdasan Buatan dalam Automasi Data & Dokumentasi* (~3.5 jam)

**Audiens:** Pegawai Tadbir (Rekod Perubatan) & Penolong — kebanyakannya pengguna kali pertama Power BI / AI tools. Latar belakang pengurusan rekod perubatan, laporan perubatan, lembaga perubatan.

**Format penyampaian:** Bengkel *hands-on* dengan ceramah pengenalan ringkas (~20 min) setiap slot. Peserta membawa laptop sendiri.

## 2. Keputusan Reka Bentuk (terkunci)

| # | Keputusan |
|---|---|
| Format | Hands-on workshop + ceramah pengenalan ringkas |
| Persekitaran Power BI | **Power BI Desktop tempatan sahaja** (Windows). Pemasangan dibuat **sebelum** kursus melalui panduan persediaan. Tiada Power BI Service. |
| Bahasa | **Bahasa Melayu primary**, istilah teknikal kekal English (Power Query, measure, DAX, dll.) |
| Dataset Power BI | **Sintetik** (data perubatan palsu tetapi realistik) — tiada risiko privasi |
| Skop AI (Modul 2) | **Document-centric**, 3 aliran kerja teras + seksyen explore |
| Dokumen sampel NotebookLM | **Pautan dokumen awam KKM/JPA sebenar** (tidak disimpan dalam repo) |
| Skop Fasa 1 | **Tulang belakang kandungan markdown sahaja** + dataset sintetik + senarai pautan awam. Slaid, screenshot, `.pbix` siap, fail audio = Fasa 2 |
| Struktur repo | Topic-first, dua modul berdiri sendiri |

## 3. Seni Bina Repositori

```
README.md                      ← gambaran kursus, 2 slot, agenda, "cara guna repo ini"
LICENSE                        ← lesen permisif (repo awam/boleh guna semula)
00-setup/
  README.md                    ← persediaan sebelum kursus: pasang Power BI Desktop, sedia akaun Google
module-1-power-bi/
  README.md                    ← nota ceramah pengenalan + peta lab
  lab/                         ← fail langkah fokus (satu tugas setiap fail, bernombor)
  data/                        ← dataset perubatan sintetik (CSV) + skrip penjana
module-2-notebooklm-gemini/
  README.md                    ← pengenalan + 3 aliran kerja
  lab/                         ← panduan aliran kerja
  public-references.md              ← senarai pautan dokumen awam KKM/JPA
docs/superpowers/specs/        ← dokumen reka bentuk ini
```

**Konvensyen:**
- Setiap fail langkah lab pendek dan fokus — satu tugas, bernombor mengikut urutan.
- Naratif BM; istilah/UI English dalam `code` atau petikan (cth. "Transform Data", measure, DAX).
- Setiap langkah ditulis supaya peserta boleh ulang **selepas** kursus tanpa bantuan.
- Screenshot dirujuk sebagai placeholder buat masa ini (`![...](../img/...)`) — imej sebenar = Fasa 2.

**Belanjawan masa:**
- **Slot 1 (Power BI):** 8:00–10:00 (2j) + 10:30–11:30 (1j) = 3j. ~20 min pengenalan + ~2.5j hands-on + buffer.
- **Slot 2 (AI):** 11:30–1:00 (1.5j) + 2:00–4:00 (2j) = 3.5j. ~20 min pengenalan + ~2.5–3j hands-on + buffer.

## 4. Modul 1 — Power BI (3 jam)

**Prinsip:** pengguna kali pertama → satu konsep baharu pada satu masa, sentiasa berkait dengan output statistik perubatan yang mereka kenali.

**`module-1-power-bi/README.md` — nota ceramah pengenalan (~20 min):**
- Apa itu Power BI & kenapa relevan untuk statistik perubatan (dari Excel manual → dashboard automatik)
- Aliran kerja Power BI: Get Data → Transform → Model → Visualize → Share
- Lawatan ringkas antara muka (Report / Data / Model views)
- Pratonton dashboard akhir yang akan dibina

**`lab/` — fail langkah (hands-on, ~2.5j + buffer):**

| Fail | Isi |
|---|---|
| `01-import-data.md` | Get Data → import dataset perubatan (CSV) |
| `02-power-query-bersih.md` | Power Query: semak jenis data, buang ruang/error, format tarikh |
| `03-model-hubungan.md` | Asas modeling: hubungan antara jadual fakta kemasukan ↔ jadual rujukan (wad, disiplin, tarikh) — ringan |
| `04-ukuran-dax.md` | Measure asas: Jumlah Kemasukan, Jumlah Discaj, **BOR %**, **ALOS**, **Bilangan Pesakit ikut Wad** |
| `05-visual-asas.md` | Card (KPI), bar chart (kemasukan ikut disiplin), bar chart (Bilangan Pesakit ikut Wad), line chart (trend bulanan) |
| `06-dashboard-interaktif.md` | Susun satu halaman dashboard + slicer (disiplin, wad, tarikh) |
| `07-eksport-simpan.md` | Simpan `.pbix`, eksport PDF (tempatan sahaja; nota ringkas pasal publish sebagai optional/Fasa 2) |

**Disiplin skop (YAGNI):** tiada advanced DAX, tiada dataflows, tiada publish ke Service, tiada custom visuals. Cukup untuk hasilkan satu dashboard statistik perubatan interaktif sebenar yang boleh dibina semula di tempat kerja.

## 5. Modul 2 — NotebookLM + Gemini (3.5 jam)

**`module-2-notebooklm-gemini/README.md` — nota ceramah pengenalan (~20 min):**
- Apa itu NotebookLM (AI *grounded* pada dokumen anda + petikan/citation) vs Gemini (AI generatif umum)
- Kenapa relevan: berhenti "flip2 paper" — tanya terus korpus rujukan
- Konsep penting: *grounding*, *citation*, dan **amaran data sensitif** (jangan upload data pesakit sebenar ke akaun peribadi)

**`lab/` — 3 aliran kerja teras + explore (~2.5–3j):**

| Fail | Aliran kerja |
|---|---|
| `01-set-up-notebook.md` | Buka NotebookLM, cipta notebook, muat naik dokumen contoh (dari pautan awam di `public-references.md`) |
| `02-query-the-corpus.md` | **Aliran 1:** tanya soalan prosedur/garis panduan, baca jawapan + citation, sahkan sumber |
| `03-project-paper-to-slides.md` | **Aliran 2:** dari kertas projek → guna Studio (briefing doc, struktur slaid) + prompt Gemini untuk olah jadi slaid |
| `04-meeting-audio-to-minutes.md` | **Aliran 3:** transkrip rakaman mesyuarat → draf minit mesyuarat (guna sampel/transkrip contoh) |
| `05-explore-further.md` | Audio Overview, FAQ, Study Guide, Mind Map; Gemini untuk draf memo/laporan rasmi |

**Nota merentas modul:** kotak **garis panduan keselamatan data** yang jelas — peserta akan tergoda untuk upload PUU/dokumen pesakit sebenar; modul berulang kali tandakan apa yang selamat (dokumen awam, de-identified) vs tidak.

**`public-references.md`:** senarai dokumen awam KKM/JPA sebenar (garis panduan pengurusan rekod, pekeliling, dll.) yang peserta muat turun dan upload ke NotebookLM untuk lab. Nota: pautan boleh berubah/luput; akan ditulis dengan tarikh akses.

**Catatan:** Aliran 2 bergantung pada ciri NotebookLM Studio semasa — ditulis mengikut apa yang ada sekarang, dengan nota bahawa UI sentiasa berkembang.

## 6. Dataset Sintetik Perubatan (Modul 1)

Direka sebagai **star schema** kecil supaya langkah modeling bermakna dan setiap measure boleh dikira daripada kolum sebenar.

**Jadual fakta — `kemasukan.csv`** (~12 bulan, beberapa ribu baris):
`ID_Kemasukan`, `Tarikh_Masuk`, `Tarikh_Discaj`, `Kod_Wad`, `Kod_Disiplin`, `Diagnosis_DRG`, `Umur`, `Jantina`
→ Length-of-stay diterbitkan daripada dua tarikh (feed **ALOS**); kiraan baris feed **Jumlah Kemasukan / Discaj / Bilangan Pesakit ikut Wad**.

**Jadual dimensi — `wad.csv`:**
`Kod_Wad`, `Nama_Wad`, `Kapasiti_Katil`, `Jenis_Wad`
→ `Kapasiti_Katil` membolehkan **BOR %** (patient-days ÷ available bed-days).

**Jadual dimensi — `disiplin.csv`:**
`Kod_Disiplin`, `Nama_Disiplin` (Perubatan, Pembedahan, O&G, Pediatrik, Ortopedik, …)

**Jadual dimensi — `tarikh.csv`:** date table untuk trend bulanan — *atau* dibina dalam Power Query semasa lab; CSV disediakan sebagai fallback supaya tiada peserta tersekat.

**Penjanaan:** skrip Python kecil (`module-1-power-bi/data/jana_data.py`) menggunakan stdlib sahaja — data boleh dihasilkan semula (`random.seed`), boleh ubah volum. CSV yang dijana di-commit bersama. Sepenuhnya sintetik, taburan realistik (seasonality, LOS munasabah, BOR dalam julat dipercayai).

**Format:** CSV sahaja.

## 7. Skop Fasa 1 (deliverable)

Termasuk:
- `README.md` (akar), `LICENSE`
- `00-setup/README.md`
- `module-1-power-bi/` — README + semua fail lab + dataset CSV + skrip penjana
- `module-2-notebooklm-gemini/` — README + semua fail lab + `public-references.md`

**Tidak termasuk (Fasa 2):** slaid sebenar, screenshot/imej, fail `.pbix` siap, fail audio contoh.

## 8. Skop yang Dikecualikan (YAGNI)

- Power BI Service / publishing / sharing online
- Advanced DAX, dataflows, custom visuals
- Penyimpanan dokumen sebenar atau data pesakit dalam repo
- Versi `.xlsx` dataset (CSV sahaja)
- Slaid & media (Fasa 2)
