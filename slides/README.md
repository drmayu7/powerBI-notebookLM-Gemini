# Slaid Pengenalan (Marp)

Slaid ceramah pengenalan untuk dua slot kursus, ditulis sebagai Markdown
[Marp](https://marp.app/). Fail `.md` ialah sumber utama; PDF dalam `build/`
di-commit supaya boleh terus dibentangkan tanpa sebarang pemasangan.

| Fail | Slot |
|------|------|
| `modul-1-power-bi.md` | Slot 1 — Power BI (~30 min, English) |
| `modul-2-notebooklm-gemini.md` | Slot 2 — NotebookLM & Gemini (~20 min) |

## Render semula

Memerlukan Node.js. Tiada pemasangan global perlu — `npx` muat turun Marp
secara automatik kali pertama.

```bash
# PDF (untuk bentang/cetak)
npx -y @marp-team/marp-cli slides/modul-1-power-bi.md --pdf -o slides/build/modul-1-power-bi.pdf

# PowerPoint (untuk edit dalam PowerPoint)
npx -y @marp-team/marp-cli slides/modul-1-power-bi.md --pptx -o slides/build/modul-1-power-bi.pptx

# HTML (untuk bentang dari pelayar)
npx -y @marp-team/marp-cli slides/modul-1-power-bi.md --html -o slides/build/modul-1-power-bi.html
```

Tema: `gaia` (terbina-dalam Marp). Untuk tukar tema, edit `theme:` dalam
front-matter setiap fail.
