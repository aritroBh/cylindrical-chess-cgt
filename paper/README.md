# Paper

- `Bhattacharjee_Cylinder_Chess_IEEE.pdf`: the paper (IEEE format, 15 pages).
- `Bhattacharjee_Cylinder_Chess_IEEE_review_anonymous.pdf`: the anonymous version for double-blind review (14 pages).
- `ieee/`: the LaTeX source (`main.tex`, `main_review.tex`, `sections/`, `refs.bib`, `figures/`).
- `SUBMISSION.md`, `VENUES.md`: where and how to submit.
- `part1_2025.tex` and `../prior_work/`: the June 2025 study this paper extends.

Build both PDFs from `ieee/`:

```bash
tectonic -X compile main.tex
```

```bash
tectonic -X compile main_review.tex
```

Build and check the arXiv package from the repository root (writes `dist/arxiv/cylinder-chess-arxiv.zip`):

```bash
sh dist/arxiv/build.sh
```

All 19 references were checked against Crossref, OpenAlex, arXiv and the publishers' pages on 2026-10-27
(`../delegate/out/citation_check/REPORT.md`).
