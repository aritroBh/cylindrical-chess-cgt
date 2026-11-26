# L15: corrections to the Lean project after the second outside read

Repository root is the working directory. The Lean project is `lean/` (Lean 4.36.0, no Mathlib; `lake` is on the PATH). The referee reports are `delegate/out/L14_codex/REPORT.md` (the main one: read its sections "E", "B" and "Trust, strengthened tests and scope of the verdict"; its probe files `Audit.lean`, `Extra.lean`, `FlagCount.lean` show the counterexamples), `delegate/out/L14_kilo/REPORT.md`, `delegate/out/L14_opencode/REPORT.md`. No referee found a wrong theorem. They found tests that are weaker than described, one fast function that is wrong outside the boards used, one missing statement and several wrong comments. Fix exactly the items below; change nothing else.

## Code

1. `lean/CylChess/SearchWide.lean`, `Ext.ofPawns` / `passedF`: the empty-file value of `mn` is the constant 1000, so `passedF` disagrees with `hasPassed` on boards with about 1000 ranks or more (Codex: one-file flat board with 1003 ranks and a lone black pawn on rank 1001; and a wrong winner for `wide` on a flat 5-file, 1005-rank board, W a1001 e1001 / B b1002 d1002, heap 0, Black to move, fuel 10: `WH` gives `some true`, `wide` gave `some false`). Replace the constant by a value taken from the board (`b.ranks + 1` is larger than every rank) and check by hand that every comparison in `blockedF` stays false for an empty file, also across the Möbius seam. Update the doc comments.
2. `lean/CylChess/SearchWideAgrees.lean`: (a) add both Codex counterexamples as theorems that now pass (`passedF = hasPassed` on the 1003-rank board; `wideRun = WH = some true` on the 1005-rank position); (b) `agreeSpec` accepts `none == none`: require the specification's answer to be definite (`isSome`) as well as equal; (c) the header says "every position reachable"; the code stops at depth two: say that.
3. `lean/CylChess/HeapsAgrees.lean`, `agreeWith`: it compares `wl.mem j` with `win ... == some true`, so an unknown answer passes as a loss. Compare with `some (wl.mem j)` and `some (wr.mem j)`, so that the reference must be definite. Codex reports that the strict form passes on all four test sets.
4. `lean/CylChess/SearchAgrees.lean`: check whether its comparison also lets `none == none` pass; if so require a definite answer in the same way, if that passes. Codex reports that 2,658 of the 3,378 open test positions fail `Position.valid` (Black pawns on rank 5 of a five-rank board), which leaves 720 valid ones. Confirm the two numbers with a Lean evaluation, add a small theorem that states them, and say in the header that the family is a set of test inputs for the code, most of them not legal placements. Do not change the family itself. Carry the same sentence to `SearchWideAgrees.lean` and `HeapsAgrees.lean` where they quote the 3,378 or 5,010.
5. `lean/CylChess/Claims/L7a_S6Rings.lean`: the paper (`dist/tog/sections/08_star2.tex`, "with n+1 pawns on C_11") states a whole-board star-3 for the twelve-pawn ring `W c4 d6 e3 h3 i2 k2 / B a4 b7 d7 f7 g6 j6`; the theorem `c11_twelve_pawn_ring_sum` checks the sum model only although its comment names both. Add `c11_twelve_pawn_ring_whole` (`Wide.WideStar (defEnv (cylinder 11)) wideFuel <pos> 3 6`) and correct the comment.
6. Controls: `L7b_Controls.lean` and `Mobius_controls` use `sigString`, which has no test that the root is open. Add one theorem per file stating that each control root (six cylinder controls, three Möbius controls) has no passed pawn for either side in the default setting.
7. Add `#print axioms` lines for every new theorem to `lean/CylChess/Claims/Axioms_L7_L10.lean` (or `Axioms.lean` for `SearchAgrees`).

## Comments and notes (wording only)

8. `lean/CylChess/Heaps.lean` lines 18-20: the tests are in `HeapsAgrees.lean`; heaps 0 to 3 against the specification and 0 to 7 against the fast search.
9. `lean/CylChess/Census.lean`, the `Tally` comment: the last class (`noNimber`) is every record whose set of lost heaps has no `j ≥ 2` and is neither `{0}` nor `{1}`; that includes the empty set. Also say in the header of `Census.lean` that every record has no en passant right (a diagram, not a position reached by a double step).
10. `lean/CylChess/Claims/RootsOpen.lean` lines 14-16: do not say more than is proved; the census screens its records in `Census.records`, the family claims test the root in `starTest`, the controls get item 6.
11. `lean/CylChess/Claims/L7b_Star3.lean` line 11: the bases are 22 for `Q`, 19 for `Qo`, 20 for `T`, 23 for `S`.
12. `lean/notes/L7_L10.md`: line 55 says the six-pawn ring on `C_3` with e.p. off is not 0 under the mover rule; that is wrong (it is 0 under count and mover, not 0 under opponent, as the note's own later paragraph and Codex's computation say). Lines 3-5: `CylChess.lean` now imports everything. Where the note says the "finite part" of each paper proof is redone: say that the base outcomes are redone, not the reduced-graph hypotheses the insertion uses. Add the new theorems to its tables.
13. `lean/notes/L8_L9.md`: winning ring widths beyond 20 come from the recurrence, not from pawn play; `ring_grundy` compares the position after a push on every file for n ≤ 12 and on files 0 and 1 for n = 13 to 16; the macro-move Grundy value tests only that each macro-move hands the turn over, which is enough at the full starting position (by `ring_structure`) and is not a proof that every quiet position is impartial. Mention `Claims/L8_Period.lean` (period 34 from n = 52 to 300, exception at n = 51).

## Build and report

- While editing, build one module at a time: `cd lean && LEAN_NUM_THREADS=2 nice -n 15 lake build CylChess.<Module>`.
- When every item is done, run one clean build and keep its log: `cd lean && nice -n 15 lake clean && LEAN_NUM_THREADS=2 /usr/bin/time -l nice -n 15 lake build > ../delegate/out/L15_build.log 2>&1` (about 45 minutes; run it in the background and wait for it). It must end with "Build completed successfully". If a strengthened test fails, do not weaken it back: stop and report the failing case exactly.
- Final message: for each item 1 to 13, what you changed (file and theorem names) and what the build said; the wall time and peak memory of the clean build; anything a referee claimed that you could not confirm.

## Rules

- NEVER use `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Kill only a process whose PID you started and recorded. Other projects' jobs run on this machine (another project's Lean job among them).
- At most two heavy processes, under 4 GB each. No `sorry`, `axiom`, `unsafe`, `partial`, `implemented_by`, `@[extern]`.
- Edit only files under `lean/` (and write `delegate/out/L15_build.log`). No git commands. No network. No absolute paths in any file you write.
