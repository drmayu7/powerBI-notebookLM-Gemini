# Modul 2: NotebookLM dan Gemini

**Slot 2 — 25 Jun 2026 (Khamis), 11:30 tgh – 4:00 ptg**
Penceramah: Dr. Muhammad Naufal bin Nordin

*Potensi Kecerdasan Buatan (AI) dalam Automasi Data & Dokumentasi.*

Modul ini menunjukkan bagaimana AI boleh membantu kerja harian pengurusan rekod:
menjawab soalan daripada timbunan dokumen rujukan, menukar kertas projek kepada
slaid, dan menyediakan minit mesyuarat daripada rakaman audio.

---

## Pengenalan (Ceramah ~20 min)

### NotebookLM vs Gemini — apa bezanya?

| | **NotebookLM** | **Gemini** |
| --- | --- | --- |
| Sifat | AI *grounded* — jawapan berdasarkan **dokumen yang anda upload** | AI generatif umum |
| Kekuatan | Jawapan disertai **petikan (citation)** ke sumber asal | Menjana & mengolah teks bebas |
| Guna untuk | Tanya korpus rujukan, ringkasan dokumen | Draf memo, olah slaid, idea umum |

### Kenapa relevan untuk pengurusan rekod?
Anda menyimpan banyak surat PUU, surat edaran, garis panduan, dan prosedur.
Untuk menjawab satu soalan, selalunya perlu *flip* banyak muka surat. Dengan
NotebookLM, anda upload semua dokumen sekali, kemudian **tanya sahaja** — dan
jawapan datang dengan rujukan ke sumbernya.

### Konsep penting
- **Grounding** — NotebookLM hanya menjawab berdasarkan dokumen yang anda beri,
  bukan dari "pengetahuan umum" yang mungkin tidak tepat.
- **Citation (petikan)** — setiap jawapan menunjukkan dari bahagian mana sumber
  ia diambil, supaya anda boleh sahkan sebelum guna.

### ⚠️ Amaran Data Sensitif

> **JANGAN** muat naik data pesakit sebenar, surat PUU sulit, atau dokumen
> terhad ke akaun Google peribadi. Untuk latihan, gunakan **dokumen awam**
> (lihat [`rujukan-awam.md`](rujukan-awam.md)) atau dokumen yang telah
> di-*deidentify* (nyahkenal). Sentiasa patuhi dasar keselamatan maklumat
> jabatan anda.

---

## 3 Aliran Kerja Utama

1. **Tanya korpus rujukan** — upload garis panduan/prosedur, tanya soalan,
   dapat jawapan + citation.
2. **Kertas projek → slaid** — tukar kertas projek kepada rangka slaid.
3. **Audio mesyuarat → minit** — transkrip rakaman, draf minit mesyuarat.

---

## Peta Lab

| Langkah | Fail | Anggaran masa |
| --- | --- | --- |
| 1 | [Sediakan notebook](lab/01-sediakan-notebook.md) | 20 min |
| 2 | [Aliran 1: Tanya korpus](lab/02-tanya-korpus.md) | 30 min |
| 3 | [Aliran 2: Kertas projek → slaid](lab/03-kertas-projek-ke-slaid.md) | 35 min |
| 4 | [Aliran 3: Audio → minit mesyuarat](lab/04-audio-mesyuarat-ke-minit.md) | 35 min |
| 5 | [Explore lanjut](lab/05-explore-lanjut.md) | 20 min |

Jumlah ~2.5–3 jam (termasuk buffer untuk soal jawab).
