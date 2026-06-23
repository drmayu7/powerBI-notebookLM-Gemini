# Lab 5: Visual Asas

**Matlamat:** Bina visual pertama menggunakan measure dari Lab 4.

> Pastikan anda berada di **Report view** (ikon carta di tepi kiri). Untuk
> menambah visual, klik ikon visual yang dikehendaki di panel **Visualizations**,
> kemudian seret medan ke dalam *well* (Axis / Values / dsb).

---

## Langkah

### A. Kad KPI (3 kad)
1. Klik visual **Card**.
2. Seret measure **`Jumlah Kemasukan`** ke dalam **Fields**.
3. Ulang untuk dua kad lagi: satu untuk **`ALOS`**, satu untuk **`BOR %`**.

> Letakkan tiga kad berbaris di bahagian atas kanvas.

![Kad KPI](img/05-card-kpi.png)

### B. Carta bar — Kemasukan ikut Disiplin
1. Klik visual **Clustered bar chart** (atau **Clustered column chart**).
2. **Y-axis / Axis:** `disiplin[Nama_Disiplin]`
3. **X-axis / Values:** `[Jumlah Kemasukan]`

### C. Carta bar — Bilangan Pesakit ikut Wad
1. Klik visual **Clustered bar chart** baharu.
2. **Axis:** `wad[Nama_Wad]`
3. **Values:** `[Bilangan Pesakit ikut Wad]`

### D. Carta garis — Trend kemasukan bulanan
1. Klik visual **Line chart**.
2. **X-axis:** `tarikh[Bulan]` (guna `Bulan` untuk urutan betul 1–12; anda boleh
   tukar paparan kepada `Nama_Bulan` kemudian).
3. **Y-axis / Values:** `[Jumlah Kemasukan]`

![Visual asas](img/05-visual.png)

---

## Hasil yang dijangka

Pada kanvas: **3 kad KPI**, **2 carta bar** (ikut disiplin & ikut wad), dan
**1 carta garis** trend bulanan — semua menunjukkan nilai dari dataset.

➡️ Seterusnya: [Lab 6 — Dashboard interaktif](06-dashboard-interaktif.md)
