# T84 — Re-read of two FINAL ring-proof texts after their fixes (one pawn per file; *3 with n+1 pawns)

Output directory: `delegate/out/T84/` (create it). Write `REPORT.md` there and any programs. Do not edit
anything else. Never run git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs
you started and recorded yourself. At most 1 process at a time, under 3 GB, `nice -n 15` if your sandbox allows
it; total compute budget about 30 minutes. Other people's jobs run on this machine: leave them alone.
Do not copy raw terminal transcripts into your report, and do not write anything from your own memory of other
projects or any personal identifier (names, email addresses, home paths outside this repository) into it.

## Why
Both notes were written by an AI model, refereed by two models of other vendors (one of them you, in an earlier
run: reports `research/ring_n_check/` and `research/star3_proof_check/` if present, or search `RESULTS.md` for
T66 and T70), and then EDITED by a third model to apply the fixes and to prepare them for typesetting. No record
shows that anyone read the final wording. Referee the texts exactly as they now stand, as a hostile reader; an
edit may have introduced an error or dropped a hypothesis. Form your own verdict before comparing with any
earlier report.

## Texts
1. `dist/tog/supp_src/s14_ringn.md` (supplement Section S14): rings of value *2 with one pawn per file on every
   cylinder C_n with n >= 10, as whole-board games.
2. `dist/tog/supp_src/s15_note4.md` (supplement Section S15, Note 4): rings of value *3 with n+1 pawns on every
   C_n with n >= 12.
They build on `dist/tog/supp/s13.tex` (setting, move classes T, L, P, K, the reduced game, Lemmas 1 to 3) and on
`dist/tog/supp_src/s15_note1.md` section 2b (the written-out proof of Lemma 3). Rules of the game:
`dist/tog/sections/02_rules.tex`.

## For each text
1. Is the family defined unambiguously, and does the stated range of n match the paper's claim
   (`dist/tog/sections/08_star2.tex`: "the two families with n pawns ... for every n >= 10"; "with n+1 pawns on
   C_11 [two programs] and on every C_n with n >= 12")? Is any width skipped between the direct computations and
   the base of the induction (check even and odd n separately)?
2. Are all hypotheses of Lemmas 1 to 3 verified at every node the induction uses (no e.p. flag, the ten-file arc
   around the cut made of pattern files of one wall and clear of the files that change)? Is the step an
   isomorphism of reduced games including the T-flags? Is the passage from the signature for heaps 0..3 to the
   value against every nim-heap justified?
3. List every computed fact the proof depends on, with the note's label and the number of independently written
   programs it claims. Is each label honest? With your own code (do not import or run the repository's solvers)
   recompute the signature of the two smallest members of each family by plain whole-board search with heaps
   0..3 (heaps 0..4 for *3), and, if your budget allows, one reduced-graph node count. Report agreement.
4. Any sentence that states more than is proved, any reference to a program, table or section that is not in the
   supplement, any undefined symbol.

## Report
`delegate/out/T84/REPORT.md`: first line a verdict per text (FINAL TEXT SOUND / SOUND WITH FIXES / GAP). Then the
findings as `file:line` with severity (BLOCKER, MAJOR, MINOR) and exact replacement text, the list of computed
facts with labels, and the commands to rerun your programs. Say plainly what you did not check.
