# Introduction Slides (Marp)

Introductory talk slides for the two course slots, written as Markdown
[Marp](https://marp.app/). The `.md` file is the primary source; the PDF in
`build/` is committed so it can be presented immediately without any
installation.

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

# HTML (for presenting from a browser)
npx -y @marp-team/marp-cli slides/module-1-power-bi.md --html -o slides/build/module-1-power-bi.html
```

Theme: `gaia` (built into Marp). To change the theme, edit the `theme:` in
each file's front-matter.
