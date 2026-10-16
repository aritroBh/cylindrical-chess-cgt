# Results so far (2026-10-16, 00:05)

Plan: [RESEARCH_PLAN.md](RESEARCH_PLAN.md). This page lists what the 2026-10-15 run established and how
strongly. "Verified" means two independent implementations agree **and** adversarial checkers could not
break the claim. The workflow run that produces the rest is still going; items marked *pending* are
filled in when it finishes.

## 1. The \*2 question (Elkies' open problem): the candidate does not survive real chess

The candidate was `W a2 c2 / B b7 d7` on files a–d, plus a trébuchet (W g4 / B g5, WK f5, BK h4).

| Check | Result | Status |
|---|---|---|
| Value under the paper's convention (cylcgt) | \*2 under race rules "count" and "mover"; **0** under "opponent" | verified with **e.p. off**: three implementations agree (cylcgt, `sumtest/`, and a verifier's own). All three were written by Claude models. With e.p. on, the \*2 needs the convention below |
| Same, but a pawn that can still be taken en passant is **not** yet "passed" | **{2±1 \| −2±1}** (mean 0, temperature 2), not \*2 | one implementation (`sumtest/`); the mechanism is proved by hand (a2–a4 is met by b4×a3 e.p.) |
| Real chess, both sides to move (Lichess 7-man tablebase + exact search) | the side to move wins (outcome N), as \*2 predicts | proved by certificate (`realchess/results/cert_root_*.json`) |
| Real-chess value: the pawn tree with real tablebase results at its end positions | **excluded from being \*2.** Among the 65 end positions resolved so far, 3 are first-player wins and 2 are draws; the model scores all 5 as won for one side. One end position flips from a Black win to a White win | computed once (`realchess/results/comp_Wa2c2_Bb7d7_oracle_pure.json`); *pending verification* |

**Why it fails.** The convention "first passed pawn wins" breaks down in two ways:
- **En passant.** A pawn that double-steps past an enemy pawn counts as passed before the opponent's legal
  en passant capture. This is a **modelling defect in `cylcgt.pawns.passed()`**: it ignores `pos.ep`. It is
  not a coding bug: on the e.p.-off board the independent solver agrees on all 2,483,775 outcome predictions.
- **Frozen kings.** In real chess the trébuchet kings are not always frozen. Across 94 tablebase-checked
  positions, 41 of 449 king moves draw and 7 win (`engine/suite/`).

**What this means.** A \*2 made only of kings and pawns on 8×8 is still open. The negative result is
publishable as is: it shows exactly where the convention breaks. The search for other candidates and their
certification are *pending*. They start from `atlas/flat8/` and run through `realchess/certify/`.

## 2. Mating without corners: 4-man tablebases on the cylinder and torus (verified)

Two independent solvers agree on every position of all 24 tables, about 607 million values, for both sides
to move ([tablebase/replica/REPORT.md](tablebase/replica/REPORT.md)).

| Material (cylinder 8×8) | White to move: share won | Longest mate (moves) |
|---|---|---|
| KQK | 100% | 10 |
| KRK | 2.80%: **no forced mate** | 3 |
| KBBK, opposite-coloured bishops | **100%** | **14** |
| KBNK | 0.0245%: **draw** | 2 |
| KNNK | 0.0077% | 1 |
| KRBK | 99.74% | 13 |
| KRRK | 100% | 8 |
| KQRK | 100% | 5 |

On the torus, KQ, KR, KBB, KBN and KNN against a lone king are all 0% won, and KRB vs K is 0.022%. The bishop
pair forcing mate on the cylinder contradicts H.G. Muller's published claim. We found no earlier tablebase
for these boards.

## 3. The 2025 paper, re-audited (verified)

A blind re-transcription of every diagram matches the solver's input on every pawn square. A pixel scan confirmed it independently. The kings, and diagrams 2.3 and 5.1, were checked against the images only
([notes/diagram_audit.md](notes/diagram_audit.md)). Three verifiers checked each audit claim. Corrected
verdicts are in [notes/audit.md](notes/audit.md):
- **Correct:** 2.1, 2.2, 2.3, 3.2, 4.1, 4.3, 5.1, the 7.1 c- and f-files, and the 7.2 king zugzwang.
- **Correct only with en passant:** 3.1.
- **Wrong:**
  - 4.2 is one rank off.
  - 7.1 a/h is {+W \| \*}, not 1.
  - 7.2's pawn part is not ±1.
  - 7.3 is decided at move 0.
  - 7.3's {c,d} part is tiny(1), not 1.
  - §1's knight squares are wrong.
  - §8 misstates Dawson's chess.

## 4. The solver itself (verified)

- `cylcgt` agrees with a from-scratch brute-force solver on **4,967,550** outcome predictions. These cover
  55,195 positions (≤2 pawns a side, 3–5 files) × 3 race rules × e.p. on/off × 15 reference games (`sumtest/`).
  With e.p. on, this holds under the textbook passed-pawn test. OpenCode was to write a fourth,
  non-Claude implementation, but every model route failed, so all the checkers are Claude-written.
- It also agrees with Codex's whole-board minimax on 1,070/1,070 single-component positions (`crosscheck/`).
- The `sum_safe` flag was exact on a 3,600-position family that tests when +BIG and −BIG cancel.
- **The one defect found** is the en passant convention in §1, above.

## 5. Engines

- [engine/ENGINES.md](engine/ENGINES.md) makes 16 predictions about how Stockfish and Lc0 search fails on
  zugzwang, tempo battles and nimbers, and designs 8 experiments.
  - Stockfish's null-move pruning never fires in king-and-pawn endings, because it requires pieces.
  - Reverse futility pruning is the predicted zugzwang-blind cut.
- **Test suite:** `engine/suite/cgt_verified.epd` holds **181 legal 8×8 positions** whose winning moves
  follow from CGT and are confirmed by the Lichess tablebase. `engine/suite/cgt_disagree.epd` holds the 52
  where CGT and the tablebase disagree.
- **Stockfish 19 on the suite.** Official release `sf_19`, built locally in `engine/vendor/` (git-ignored);
  1 thread, 64 MB hash, no tablebases. Runs and analysis are in `engine/runs/`.
  - **It solves all 233 positions at 100k nodes, and 232/233 already at 1k nodes.** At ≤7 men these
    positions are easy for a modern engine. The CGT-versus-engine contrast has to come from larger sums,
    beyond the tablebase, where only CGT gives ground truth. That is the ChessSums benchmark.
  - **At shallow depth, accuracy depends on the CGT value class.** The table gives the share of Stockfish
    evaluations that match the tablebase result:

| CGT class | n | depth 1 | depth 2 | depth 4 | depth 6 | depth 8 | depth 12 |
|---|---|---|---|---|---|---|---|
| hot (±BIG switch) | 68 | 81% | 78% | 91% | 97% | 99% | 100% |
| number | 57 | 79% | 81% | 84% | 93% | 95% | 98% |
| switch | 37 | 73% | 78% | 89% | 100% | 100% | 100% |
| **infinitesimal** | 27 | **30%** | **26%** | **59%** | 85% | 100% | 100% |
| other tame | 20 | 60% | 50% | 75% | 95% | 100% | 100% |
| **nimber** | 17 | **53%** | 65% | 88% | 100% | 100% | 100% |

  Infinitesimals and nimbers, which are tempo and parity fights, are the ones the static evaluation
  misreads at low depth. CGT predicts exactly that. Hot positions and numbers are read correctly early.
  This is one engine on a small sample, so it is a pilot result.
- **Cylinder engine:** the only public cylinder fork of Fairy-Stockfish (mtaktikos/CylindricalChess)
  appears, from reading its code, to miss checks, pins and en passant across the seam.
  [engine/FAIRY_CYLINDER.md](engine/FAIRY_CYLINDER.md) gives a corrected design.

## 6. Pending (the workflow is still running)

- Dawson's chess:
  - **Ring values are computed for n ≤ 300:** period 34, last exception at n = 51.
  - **Misère** (Dawson's original open question): in progress (`dawson/`).
- Proofs of the structural lemmas: `notes/lemmas.md`.
- The cylinder value atlas (`atlas/cylinder/`) and the flat-board nimber search (`atlas/flat8/`).
- The ChessSums benchmark and the RL reward (`bench/`).
- Adversarial verification of every remaining headline claim, and a final completeness review.

## 7. Decisions still needed from you

- **Installs.** Stockfish and Lc0 are needed to run the engine suite. PyTorch and MLX are needed for the ML
  track. Each is a download, so each needs your OK.
- **Conventions.** Should the "passed" test respect en passant? (This run says it should.) Should we model
  kings explicitly (loopy CGT) instead of assuming they are frozen?
- **Mentor.** Should the corrected audit go to Prof. Morley?
