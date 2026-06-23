# Introduction Slides (Marp)

Introductory talk slides for the two course slots, written as Markdown
[Marp](https://marp.app/). The `.md` file is the primary source; the PDF and
PowerPoint (`.pptx`) files in `build/` are committed so they can be presented
immediately without any installation.

> **Note on `.pptx`:** Marp's default PowerPoint export embeds each slide as a
> full-slide image (great for presenting, but the text is not editable). For
> editable text boxes, use the experimental `--pptx-editable` flag (requires
> LibreOffice/SOffice installed).

| File | Slot |
|------|------|
| `module-1-power-bi.md` | Slot 1 — Power BI (~30 min, English) |
| `module-2-notebooklm-gemini.md` | Slot 2 — NotebookLM & Gemini (~20 min) |

## Re-render

Requires Node.js. No global installation needed — `npx` downloads Marp
automatically the first time.

```bash
# PDF (for presenting/printing)
npx -y @marp-team/marp-cli slides/module-1-power-bi.md --pdf -o slides/build/module-1-power-bi.pdf

# PowerPoint (for editing in PowerPoint)
npx -y @marp-team/marp-cli slides/module-1-power-bi.md --pptx -o slides/build/module-1-power-bi.pptx

# Speaker notes: Marp does NOT copy <!-- notes --> into the .pptx, so run this
# afterwards to inject them into the PowerPoint Notes pane (needs python-pptx):
python slides/apply_pptx_notes.py slides/module-1-power-bi.md slides/build/module-1-power-bi.pptx

# HTML (for presenting from a browser)
npx -y @marp-team/marp-cli slides/module-1-power-bi.md --html -o slides/build/module-1-power-bi.html
```

Theme: `gaia` (built into Marp). To change the theme, edit the `theme:` in
each file's front-matter.
