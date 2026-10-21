# Paper

**Overleaf:**
1. Zip this folder (`main.tex`, `refs.bib`, `sections/`).
2. Upload it with New Project → Upload Project.
3. Set the compiler to pdfLaTeX.

On Overleaf the diagrams come from the `xskak` / `chessboard` packages. Elsewhere, if those packages are missing,
a placeholder box is drawn instead.

**Local build:**
```
tectonic -X compile main.tex
```

**Before submission:**
- Check every `refs.bib` entry marked VERIFY.
- Fill in the acknowledgements.
- Update §6.1 once the eight decisive end positions of the 1/8 position are resolved
  (`realchess/targets18/`).
