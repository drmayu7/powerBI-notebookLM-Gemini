# Modul 1: Transformasi Statistik Perubatan menggunakan Power BI

**Slot 1 — 25 Jun 2026 (Khamis), 8:00 pg – 11:30 tgh**
Penceramah: Dr. Muhammad Naufal bin Nordin

Modul ini membimbing anda membina satu **dashboard statistik perubatan interaktif**
dari awal menggunakan **Power BI Desktop**, walaupun anda tidak pernah menggunakannya.

> **Belum pasang Power BI Desktop?** Sila ikut [panduan persediaan](../00-persediaan/)
> terlebih dahulu sebelum kursus.

---

## Pengenalan (Ceramah ~20 min)

### Apa itu Power BI?
Power BI ialah alat *business intelligence* daripada Microsoft yang menukar data
mentah (Excel, CSV, pangkalan data) kepada **dashboard** dan **laporan** yang
interaktif. Untuk Jabatan Rekod Perubatan, ini bermakna beralih daripada
mengira statistik secara manual di Excel kepada dashboard automatik yang
sentiasa dikemas kini.

### Kenapa relevan untuk statistik perubatan?
- Kira **BOR**, **ALOS**, bilangan kemasukan/discaj secara automatik.
- Tapis mengikut wad, disiplin, atau bulan dengan satu klik.
- Kongsi gambaran statistik yang konsisten kepada pengurusan.

### Aliran kerja Power BI
```
Get Data  →  Transform (Power Query)  →  Model  →  Visualize  →  Share
```

### Lawatan ringkas antara muka
Power BI Desktop ada tiga *view* di tepi kiri:
- **Report view** — kanvas untuk bina visual & dashboard.
- **Data view** — lihat jadual data (rows & columns).
- **Model view** — lihat & urus hubungan (*relationship*) antara jadual.

### Pratonton hasil akhir
Pada penghujung modul, anda akan ada satu halaman dashboard dengan:
- Kad KPI (Jumlah Kemasukan, ALOS, BOR %)
- Carta bilangan kemasukan ikut disiplin
- Carta bilangan pesakit ikut wad
- Carta trend kemasukan bulanan
- Slicer (penapis) untuk disiplin, wad, dan bulan

---

## Peta Lab

Ikut langkah secara berurutan. Setiap fail boleh diulang sendiri selepas kursus.

| Langkah | Fail | Anggaran masa |
| --- | --- | --- |
| 1 | [Import data](lab/01-import-data.md) | 15 min |
| 2 | [Bersihkan data (Power Query)](lab/02-power-query-bersih.md) | 25 min |
| 3 | [Model & hubungan](lab/03-model-hubungan.md) | 20 min |
| 4 | [Ukuran (measure) DAX](lab/04-ukuran-dax.md) | 30 min |
| 5 | [Visual asas](lab/05-visual-asas.md) | 30 min |
| 6 | [Dashboard interaktif](lab/06-dashboard-interaktif.md) | 25 min |
| 7 | [Eksport & simpan](lab/07-eksport-simpan.md) | 10 min |

Jumlah ~2.5 jam (termasuk buffer untuk soal jawab).

---

## Dataset

Dataset latihan berada dalam folder [`data/`](data/). Ia **sepenuhnya sintetik**
(rekaan) — tiada kaitan dengan pesakit sebenar. Ia disusun sebagai *star schema*:

| Fail | Jenis | Kandungan |
| --- | --- | --- |
| `kemasukan.csv` | Jadual fakta | Satu baris setiap episod kemasukan (tarikh masuk/discaj, wad, disiplin, diagnosis, umur, jantina) |
| `wad.csv` | Dimensi | Senarai wad + kapasiti katil |
| `disiplin.csv` | Dimensi | Senarai disiplin perubatan |
| `tarikh.csv` | Dimensi | Kalendar harian (untuk analisis trend) |

Untuk menjana semula data (pilihan): `python data/jana_data.py`
