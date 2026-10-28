# Chess Endgames on a Cylindrical Chessboard

Aritro Bhattacharjee

**Paper:** [paper/Bhattacharjee_Cylinder_Chess_IEEE.pdf](paper/Bhattacharjee_Cylinder_Chess_IEEE.pdf) (IEEE
format, 15 pages). Source: [paper/ieee/](paper/ieee/). An arXiv-ready package is built by `sh dist/arxiv/build.sh`.

Cylinder chess joins the a-file to the h-file, so the board has no side edges or corners. This repository studies
its king-and-pawn endgames with combinatorial game theory (CGT), following Elkies: a passed pawn wins, and the kings
are frozen in a mutual zugzwang worth zero. It holds the code, data, proofs and cross-checks behind every number in
the paper.

## Main results

The labels are the paper's:
- **P:** proved in the paper.
- **S:** proof sketched in the paper and given in full here, independent check pending.
- **C2:** two independently written programs agree.
- **C1:** one program.

- **A passed-pawn test that respects en passant**, and conditions under which the frozen kings give the exact result
  (S). With the new test, the textbook \*2 candidate is not \*2.
- **The least \*2.** No position with six pawns or fewer is \*2 on an ordinary board of any width, but \*2 appears with
  seven pawns (C2). A \*3 appears as a single component with nine pawns (C2).
- **Rings on the n-file cylinder** (a pawn on every file):
  - The least number of pawns in a ring \*2 is n+3 for 3 ≤ n ≤ 7 and ten for 7 ≤ n ≤ 10 (C2).
  - It is n, one pawn per file, for 10 ≤ n ≤ 60 (C1). On C10 and C11 that ring is unique up to symmetry and colour
    reversal (C1).
  - Rings \*3 with n+1 pawns exist on every C_n with 11 ≤ n ≤ 59 (C1), and on C11 n+1 is the least.
  - No \*4 has turned up among about 24 million rings.
- **Real chess.** With queen promotions only and frozen kings, the 1/8 position is exactly 1/8 (C1).
- **Tablebases.** King and rook win only 2.80% of cylinder positions. On the torus only two major pieces force mate.
  On the Möbius strip KRK is always won (C2).
- **Dawson's chess on the 3×n cylinder** is a first-player win exactly when the 3×(n−3) strip has Grundy value 0 (P).
- **Engines.** Stockfish is weakest on infinitesimals at low depth. On sums of components, engines often miss the
  model's winning moves (C1).

## Repository map

| Path | Contents |
|---|---|
| [`paper/`](paper/) | The paper (PDF, LaTeX source in `paper/ieee/`), submission notes |
| [`cylcgt/`](cylcgt/) | Exact CGT engine and the cylinder/flat pawn solver used throughout |
| [`crosscheck/`](crosscheck/) | Independent whole-board minimax that validates `cylcgt` |
| [`research/`](research/) | One folder per result: scans, families, proofs (`ring_family_proof/`, `ring_n_proof/`, `star3_proof/`) and referee reports |
| [`research/c9_rings/`](research/c9_rings/) | The ring minimum on C9 to C11, the n-pawn and n+1-pawn families ([REPORT](research/c9_rings/REPORT.md)) |
| [`kings/`](kings/) | When the frozen-king convention is exact; king-and-pawn solver (`kpsolve`) |
| [`realchess/`](realchess/) | Real-chess checks against the Lichess Syzygy tablebases |
| [`tablebase/`](tablebase/), [`research/mobius/`](research/mobius/) | Retrograde tablebases for the cylinder and torus; the Möbius strip and Klein bottle |
| [`dawson/`](dawson/) | Dawson's chess on strips and cylinders |
| [`engine/`](engine/) | Stockfish and Lc0 experiments on cylinder positions and CGT sums |
| [`atlas/`](atlas/), [`sumtest/`](sumtest/), [`lemmas/`](lemmas/) | The value atlas, sum-model tests, lemma checks |
| [`verify/`](verify/), [`delegate/`](delegate/) | Independent re-implementations, cross-checks and their reports |
| [`prior_work/`](prior_work/) | The June 2025 study this work extends |
| [`RESULTS.md`](RESULTS.md) | Every result with its status and the file that holds it |

## How results are checked

Every computational claim is run by at least two programs where the paper says C2. The second program is written
from the rules alone, without reading the first. Exhaustive scans have their ring counts confirmed by an independent
counter, a transfer matrix with Burnside's lemma (`research/c9_rings/validate/`). Hand proofs of the wall families
rest on three lemmas (`research/ring_family_proof/proof.tex`), and their finite base cases are checked by computer.
[`RESULTS.md`](RESULTS.md) records the status of each claim.

## Reproduce

Run these from the repository root, one command per block.

Run the tests:

```bash
.venv/bin/python -m pytest -q tests
```

Recompute the 2025 paper's claims:

```bash
.venv/bin/python -m cylcgt.verify_paper
```

Compare the value spectra of the cylinder and the flat board:

```bash
.venv/bin/python -m cylcgt.explore --files 4 --white 2 --black 2
```

Run the independent cross-check (a few minutes):

```bash
.venv/bin/python -m crosscheck.compare
```

Build the tablebase prototype, then run it for one endgame (board type, then the white pieces besides the king):

```bash
cc -O2 -o egt tablebase/egt_prototype.c
```

```bash
./egt cyl BN
```

Build the paper:

```bash
cd paper/ieee && tectonic -X compile main.tex
```

## Environments

- `.venv`: the solver, tests and workflows. Standard library and pytest only.
- `.venv-ml`: the learning experiments (PyTorch with the MPS backend, MLX on Metal). It is separate so that the
  solver environment stays minimal. Pinned versions are in `ml/requirements-lock.txt`.

Recreate the learning environment:

```bash
uv venv .venv-ml --python 3.12
```

Then install the pinned packages:

```bash
uv pip install --python .venv-ml/bin/python -r ml/requirements-lock.txt
```

## Citing

```bibtex
@misc{Bhattacharjee2026cylinder,
  author = {Aritro Bhattacharjee},
  title  = {Chess Endgames on a Cylindrical Chessboard},
  year   = {2026},
  url    = {https://github.com/aritroBh/cylindrical-chess-cgt}
}
```
