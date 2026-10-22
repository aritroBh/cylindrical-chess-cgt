# T28: Overleaf / arXiv package of the paper (light compute)

**Output directory:** `dist/arxiv/`. Create it; do not edit `paper/`.

**Build the package.**
1. Copy `paper/ieee` into `dist/arxiv/src/`. Resolve every symlink into a real file. Keep only what
   `main.tex` needs:
   - `main.tex`, `macros.tex`, `refs.bib`, `main.bbl`, `sections/*.tex`;
   - the figures it includes (find them with `grep includegraphics`).

   Do not include `main_review.tex`, the review logs, the plans, `make_figures.py` or `figures/src`.
2. Prove it builds from a fresh folder: in a new temp dir, run `tectonic -X compile main.tex`. It must give 13
   pages, no errors and no undefined references.
3. Check the arXiv rules from `paper/ieee/GUIDELINES.md`:
   - no `\write18`;
   - relative paths only;
   - file names: letters, digits, `-`, `_` and `.` only;
   - `main.bbl` present and current;
   - total size under 10 MB.
4. Make `dist/arxiv/cylinder-chess-arxiv.zip`, and an Overleaf-ready `dist/arxiv/cylinder-chess-overleaf.zip`
   (the same contents plus a `latexmkrc` that selects XeLaTeX).
5. List every font and package the build needs, and anything that might fail on arXiv's TeX Live. The paper
   uses `fontspec`-free IEEEtran with T1 fontenc under XeTeX.
   - Try a pdflatex build too, if `pdflatex` exists.
   - Report whether arXiv, which uses pdflatex by default, will compile it. If not, say what to change.

**REPORT.md:** file list, sizes, build logs (summary), the pdflatex verdict, upload steps.
