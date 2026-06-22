# Lab 3: Model & Hubungan (Relationship)

**Matlamat:** Sambungkan jadual fakta `kemasukan` kepada jadual dimensi supaya
penapis (slicer) berfungsi merentas semua visual.

> **Hubungan (relationship)** memberitahu Power BI bagaimana jadual berkaitan.
> Susunan ini dipanggil **star schema** — satu jadual fakta di tengah, dikelilingi
> jadual dimensi.

---

## Langkah

1. Klik ikon **Model view** di tepi kiri (ikon tiga kotak bersambung).

2. Anda akan nampak empat kotak jadual. Susun supaya `kemasukan` di tengah.

3. Cipta hubungan dengan **menarik (drag)** medan dari fakta ke dimensi:
   - Tarik `kemasukan[Kod_Wad]` → lepas pada `wad[Kod_Wad]`.
   - Tarik `kemasukan[Kod_Disiplin]` → lepas pada `disiplin[Kod_Disiplin]`.
   - Tarik `kemasukan[Tarikh_Masuk]` → lepas pada `tarikh[Tarikh]`.

4. Bagi setiap hubungan, klik dua kali garis penyambung dan sahkan:
   - **Cardinality:** `Many to one (*:1)` — banyak di `kemasukan`, satu di dimensi.
   - **Cross filter direction:** `Single`.

   ![Model view star schema](../img/03-model.png)

---

## Hasil yang dijangka

Tiga garis hubungan terbentuk:
`kemasukan` → `wad`, `kemasukan` → `disiplin`, `kemasukan` → `tarikh`.
Simbol `*` berada di hujung `kemasukan` dan `1` di hujung jadual dimensi.

➡️ Seterusnya: [Lab 4 — Ukuran (measure) DAX](04-ukuran-dax.md)
