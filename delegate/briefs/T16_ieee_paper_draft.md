# T16 (codex): write the IEEE paper, one continuous document

**Output directory:** `paper/ieee/`. The spec there, `paper/ieee/SPEC.md`, is the contract: read all of it first.

**Task.** Write the complete paper as an IEEE journal article (`\documentclass[journal]{IEEEtran}`). Follow the
spec's section plan, voice, figure rules and verified fact sheet exactly.
- **The base.** Aritro's own 2025 paper (`paper/part1_2025.tex`). Keep his explanations and voice, trim them
  for length, and fix his errors in place, using the audit list in the spec.
- **Carrying on.** Continue straight on to the new results, in the same voice.
- **One paper.** No "part 1 / part 2" and no "2025 / 2026" seams.

**Sources to draw on:**
- `paper/sections/09_looking_back.tex`, `10_fine_print.tex` and `11_every_small_position.tex`: a recent draft
  of the continuation in Aritro's voice;
- `paper/archive/formal_v1/sections/*.tex`: an older formal draft with all the results, but too dry and too
  long;
- `paper/archive/formal_v1/refs.bib`;
- `RESULTS.md` and `delegate/REVIEW.md`.

**Figures.**
- Copy `paper/figures/make_figures.py` to `paper/ieee/make_figures.py` and extend it. Point `HERE` at
  `paper/ieee/figures/`.
- Add a board for every position the paper shows. The basic positions of the 2025 paper (0, ±1, ±2, \*, ↑, Tiny
  1, Trebuchet, Puzzles 7.1–7.3) are read from `prior_work/Pictures/*.png` and from `prior_work/main.tex`, and
  Position 4.2 is corrected to pawns e2/e5.
- Group small boards with the `subcaption` package.
- Run it with `.venv/bin/python paper/ieee/make_figures.py`. It uses tectonic and the macOS font Apple Symbols.
- `Pictures/CoverPic.png` may be Fig. 1. Copy it into `paper/ieee/figures/`.

**Build.** `cd paper/ieee && tectonic -X compile main.tex`. Fix every error, every undefined reference, and every
overfull box over 5pt. Target 12–14 pages.

**Hard rules.**
- Use only numbers from the spec's fact sheet, or from RESULTS.md / REVIEW.md with their evidence label.
- No placeholders and no code listings. The code appears only in the Code Availability paragraph.
- Leave out unverified references: Muller's claim; Mäser and Siegel's "Coping with cycles" unless you can
  verify them offline from `notes/lit_*.md`.

**REPORT.md.**
1. A 5-line summary.
2. The section list with page counts.
3. A table of every number in the paper, with its source file.
4. Any deviation from the spec, and why.
