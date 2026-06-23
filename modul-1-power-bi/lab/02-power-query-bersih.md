# Lab 2: Bersihkan Data dengan Power Query

**Matlamat:** Pastikan jenis data (*data type*) betul dan tambah lajur tempoh
tinggal (*length of stay*) yang akan kita guna untuk ALOS.

> **Power Query** ialah editor untuk membersih dan mengubah data sebelum ia
> dimuatkan ke model. Ia merekod setiap langkah supaya boleh diulang automatik.

---

## Langkah

1. Pada tab **Home**, klik **Transform Data**. Tetingkap **Power Query Editor**
   terbuka.

2. Di panel **Queries** (kiri), klik jadual **`kemasukan`**.

3. Semak jenis data setiap lajur (ikon di sebelah nama lajur). Tetapkan seperti
   berikut — klik ikon jenis pada tajuk lajur untuk menukar:
   - `Tarikh_Masuk` → **Date**
   - `Tarikh_Discaj` → **Date**
   - `Umur` → **Whole Number**
   - `Kod_Wad`, `Kod_Disiplin`, `Diagnosis_DRG`, `ID_Kemasukan`, `Jantina` → **Text**

   ![Tetapkan jenis data lajur](img/02-data-type.png)

4. Buang ruang berlebihan pada lajur teks: pilih `Kod_Wad`, `Kod_Disiplin`
   (tahan **Ctrl** untuk pilih banyak) → tab **Transform** → **Format** → **Trim**.

5. Buang baris ralat (jika ada): tab **Home** → **Remove Rows** →
   **Remove Errors**.

6. **Tambah lajur tempoh tinggal (LOS):**
   - Tab **Add Column** → **Custom Column**.
   - **New column name:** `Tempoh_Tinggal`
   - **Formula:**
     ```
     Duration.Days([Tarikh_Discaj] - [Tarikh_Masuk])
     ```
   - Klik **OK**.
   - Klik ikon jenis pada lajur `Tempoh_Tinggal` dan tukar kepada
     **Whole Number**.

   ![Custom Column untuk Tempoh_Tinggal](img/02-custom-column-los.png)

7. Ulang semakan jenis data untuk jadual lain (ringkas):
   - `wad`: `Kapasiti_Katil` → **Whole Number**.
   - `tarikh`: `Tarikh` → **Date**, `Tahun`/`Bulan` → **Whole Number**.

8. Klik **Home** → **Close & Apply**. Power BI akan memuatkan semula data.

---

## Hasil yang dijangka

- Semua lajur tarikh berjenis **Date**, lajur nombor berjenis **Whole Number**.
- Jadual `kemasukan` mempunyai lajur baharu **`Tempoh_Tinggal`** (nilai ≥ 1).
- Tiada ralat pada mana-mana jadual.

➡️ Seterusnya: [Lab 3 — Model & hubungan](03-model-hubungan.md)
