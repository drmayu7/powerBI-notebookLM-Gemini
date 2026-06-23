# Lab 1: Import Data ke Power BI

**Matlamat:** Memuatkan keempat-empat fail CSV ke dalam Power BI Desktop.

---

## Langkah

1. Buka **Power BI Desktop**. Jika skrin permulaan (*start screen*) muncul, klik
   **Blank report** atau tutup tetingkap itu.

2. Pada tab **Home**, klik **Get Data** → **Text/CSV**.

   ![Get Data Text/CSV](img/01-get-data.png)

3. Pergi ke folder `modul-1-power-bi/data/` dan pilih **`kemasukan.csv`**.
   Klik **Open**.

4. Tetingkap pratonton muncul. Pastikan data kelihatan betul (lajur
   `ID_Kemasukan`, `Tarikh_Masuk`, dan lain-lain). Klik **Load**.

5. Ulang langkah 2–4 untuk tiga fail lagi, satu demi satu:
   - `wad.csv`
   - `disiplin.csv`
   - `tarikh.csv`

> **Tip:** Jika *encoding* huruf kelihatan pelik (cth. simbol ganti), pada
> pratonton tukar **File Origin** kepada `65001: Unicode (UTF-8)`.

---

## Hasil yang dijangka

Pada panel **Data** (atau **Fields**) di sebelah kanan, anda sepatutnya nampak
**4 jadual**: `kemasukan`, `wad`, `disiplin`, dan `tarikh`.

![Empat jadual di panel Data](img/01-jadual-dimuat.png)

➡️ Seterusnya: [Lab 2 — Bersihkan data (Power Query)](02-power-query-bersih.md)
