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
