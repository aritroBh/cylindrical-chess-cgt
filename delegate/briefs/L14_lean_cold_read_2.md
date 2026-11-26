# L14: second cold read of the Lean 4 check (rings, ring rule, cut lemma, census, corrections)

You are an outside referee. Your output directory is `delegate/out/L14_$TOOL/` (the launcher tells you `$TOOL`); write only there.

## What is being checked

`lean/` is a Lean 4.36 project (no Mathlib). Round 1 (L12) covered `Rules.lean`, `Game.lean`, `Search.lean` and the claims L4 to L6. This round covers what was added since. Paper text is in `dist/tog/sections/`, supplement text in `dist/tog/supp/` and `dist/tog/supp_src/`.

| Part | Paper or supplement source | Lean files |
|---|---|---|
| A. Corrections after round 1: 1/8 for every race function; the starting positions are open; X is not hereditarily sum-safe | `07_targets.tex` Theorem `thm:eighth`; `05_sums.tex` Definition `def:hss` and Proposition `prop:sumcounter` | `lean/CylChess/Claims/L5_EmptyTable.lean`, `RootsOpen.lean`, `L6_NotHSS.lean` |
| B. Ring base cases: named rings, wall rings, one pawn per file, star-3 rings, Möbius strip, controls, smallest rings | `08_star2.tex` (section "Rings and Higher Nimbers"); supplement `supp/s06.tex`, `supp/s13.tex`, `supp/s14.tex`, `supp_src/s15_note1.md` to `s15_note6.md` | `lean/CylChess/SearchWide.lean`, `WideLemmas.lean`, `SearchWideAgrees.lean`, `Families.lean`, `RingScan.lean`, `Claims/WideCommon.lean`, `Claims/L7a_*.lean`, `Claims/L7b_*.lean`, `Claims/L11_RingMin.lean` |
| C. Dawson's chess on a ring | `11_dawson.tex`, Theorem `thm:ring` | `lean/CylChess/Dawson.lean` |
| D. Cut lemma, one step | `02_rules.tex`, Theorem `thm:cut` | `lean/CylChess/Claims/L9_Cut.lean` |
| E. Census: 231,071 records, 459,443 positions, 6,724 zeros, 4,042 stars, no star-k with k at least 2 | `06_atlas.tex`; `08_star2.tex` Theorem `thm:census` | `lean/CylChess/Census.lean`, `CensusData.lean`, `Heaps.lean`, `HeapsAgrees.lean`, `Claims/L10_*.lean` |

The authors' own notes on what is and is not proved are `lean/notes/L7_L10.md` and `lean/notes/L8_L9.md`. Read them last, after you have formed your own view.

## Your job: try to show that the check is wrong or says less than it claims

Your starting part depends on your tool; do it first and most carefully, then the others in the order A, B, C, D, E as time allows.
`codex`: E. `cursor`: B. `kilo`: C then D. `opencode`: A then the Möbius part of B. Any other tool: B.

1. Statements. For each theorem: does it assert what the paper or supplement asserts (board, topology, every pawn's square, setting, pawn counts, range of n, which heaps, side to move, quantifiers)? Is the range in Lean smaller than the range the paper says was computed? Is a family in `Families.lean` the same list of files as in the supplement? Is the game of `SearchWide.lean` (`WH`) the whole-board game with a heap that `supp/s13.tex` defines?
2. Definitions. Look for errors in: `Wide.WH`, `Wide.wide`, `passedF`, `scan`, the memo key; `Heaps.solve` and `Heaps.sets` (is "the set of heaps j such that the mover wins X + *j" computed correctly for every j, and is the finite-or-cofinite claim right?); `Census.records` (does it list each position once up to translation and mirror image, with the right multiplicity?); the pawn rules and the mex computation in `Dawson.lean`; `cut` in `L9_Cut.lean` (is it the map of Theorem `thm:cut`, and are the hypotheses the theorem's?); `withRace` and the monotonicity proof in `L5_EmptyTable.lean`; `lineOK` in `L6_NotHSS.lean` (does the witness really show the definition of hereditary sum-safety fails?).
3. Trust. Search for `sorry`, `axiom`, `unsafe`, `partial`, `implemented_by`, `@[extern]`, a false hypothesis, a statement that is true for a trivial reason (an empty list under `all`, a family function that returns `[]`, a check that cannot fail). Say which theorems are `native_decide` (compiled code) and which `decide` (kernel). Say which statements rest on a fast search that is only tested against its specification.
4. Recompute with a program YOU write from the paper's and the supplement's text (Python with `.venv/bin/python`, or C), in your output directory. Do NOT read, import or copy `cylcgt/`, `crosscheck/`, `atlas/`, `lemmas/`, `research/`, `lean/tools/` or any other solver or data file in the repository for this step: independence is the point. Choose from this list, your starting part first:
   - A: the value 1/8 of `W a2 b2 b3 / B a5 a6 b6` when every race is left undecided (an undecided race must not be needed); the two witness lines of `L6_NotHSS.lean` played on a board.
   - B: the wall rings of `supp/s13.tex` on the cylinder with 5 to 10 files: `G + *h` is lost by the mover exactly for h = 2 (h = 0..4), whole-board game, default setting; the rings `M_10` and the eleven-file ring of `08_star2.tex`; one Möbius family member and the three Möbius controls of `Claims/L7b_Mobius.lean`; the six-pawn ring on three files is star-2 and is 0 with en passant off.
   - C: Grundy values of Dawson's chess on a ring for n = 3..20 and the list of n at most 60 where the first player wins.
   - D: one of the eleven one-step instances of `L9_Cut.lean`, by brute force.
   - E: the number of census records and positions for widths 1 to 3 (all pawn counts) and for width 4 with at most 4 pawns, and how many have value 0 and value star, in the default setting. Compare with `expected` in `CensusData.lean` group by group.
5. You may evaluate Lean expressions with `cd lean && nice -n 15 lake env lean <your file>` on a file in your output directory. Do NOT run `lake build` or `lake clean` and do not edit anything under `lean/`.

## Report

`delegate/out/L14_$TOOL/REPORT.md`: a verdict per theorem or group of theorems (says what the paper says / says less, state what / wrong), every error or doubt with file and line, your own program's results next to Lean's and the paper's, and what you did not check. Be specific; "looks fine" is not a finding. Use paths relative to the repository root; no absolute paths in anything you write.

## Extra rules for this task

- NEVER use `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Kill only a process whose PID you started and recorded. Other projects' jobs run on this machine.
- `nice -n 15` for anything heavy; at most one heavy process; under 4 GB of memory; total time under 60 minutes.
- No network. Install nothing. No git commands. Do not create a virtual environment. Do not edit `paper/`, `dist/`, `kings/`, `lean/`, `cylcgt/`.
