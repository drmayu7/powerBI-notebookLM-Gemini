# Lab 4 (Aliran 3): Audio Mesyuarat → Minit Mesyuarat

**Matlamat:** Tukar rakaman audio mesyuarat kepada **draf minit mesyuarat**
berstruktur.

> **⚠️ Amaran:** Dapatkan **kebenaran** sebelum merakam mesyuarat. Elak
> memuat naik perbincangan yang mengandungi maklumat sulit ke akaun peribadi.

---

## Langkah

1. **Sediakan sumber audio/transkrip:**
   - Rakam mesyuarat (cth. guna perakam suara telefon), **atau**
   - Jika anda sudah ada transkrip teks, gunakan terus sebagai sumber.

2. Dalam NotebookLM, **Add source** dan upload fail audio (atau tampal transkrip).
   NotebookLM akan memproses kandungannya.

3. Dalam chat, minta ringkasan berstruktur. Contoh *prompt*:
   ```
   Ringkaskan mesyuarat ini. Senaraikan:
   1. Perkara yang dibincangkan
   2. Keputusan yang dibuat
   3. Tindakan susulan (siapa & bila)
   ```

4. Minta format minit mesyuarat. Contoh *prompt*:
   ```
   Susun semula sebagai minit mesyuarat dengan jadual berlajur:
   Bil | Perkara | Keputusan/Tindakan | Pegawai Bertanggungjawab | Tarikh
   ```

   ![Draf minit mesyuarat berlajur](img/04-minit-jadual.png)

5. (Pilihan) Halusi di **Gemini** — tampal draf dan minta:
   ```
   Kemaskan minit mesyuarat ini dalam nada rasmi dan format kemas untuk
   diedarkan. Pastikan setiap tindakan ada pegawai bertanggungjawab.
   ```

6. Semak dan betulkan draf secara manual sebelum diedarkan — AI membantu draf,
   bukan menggantikan semakan anda.

---

## Hasil yang dijangka

Satu **draf minit mesyuarat** berstruktur (Bil, Perkara, Tindakan, Pegawai,
Tarikh) yang dijana daripada rakaman/transkrip, sedia untuk disemak dan
dimuktamadkan.

➡️ Seterusnya: [Lab 5 — Explore lanjut](05-explore-lanjut.md)
