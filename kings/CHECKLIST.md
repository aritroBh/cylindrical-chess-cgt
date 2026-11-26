# Kings checklist

Updated 2026-11-24. `[x]` done and committed, `[~]` running, `[ ]` open. Each item has an investigator and an
independent referee; details are in `kings/delegate/out/K*/REVIEW.md` and `kings/theory/LOOPY.md`.

## Open questions of LOOPY §8

1. Tempo matching
   - [x] As worded: false (K18)
   - [x] Promotion-free form: false; Proposition 8.1′ proved (K42)
   - [ ] Is there a form that uses no king of the sortie side? Every K42 failure uses that king
2. Dud and over groups
   - [x] Dud groups exist in P on the cylinder: Z_B, Z_C, G8a, G8b (K15b, K26)
   - [x] In chess Z_B and Z_C are not exactly two-shuttle (K28, K39)
   - [x] No over group on four adjacent files, up to 3 + 3 pawns (K43)
   - [x] Exact over and under groups exist in P on cyl:8×6 and wider, files a, b, e (K45)
   - [x] The K45 group is not equal to over in sums (38 of 1,100 results differ); its d4 freeze is a mutual zugzwang,
         proved by hand (K47)
   - [x] The other exact groups in sums: the 2 + 3 group of cyl:10×6 has the results of over on all 752 tests; the
         3 + 3 group does not on any width (K55)
   - [ ] The value of the 3 + 3 group: no candidate of 3,000 survives; it is not a stopper (K55)
   - [ ] The 2 + 3 group beside P contexts and in chess; groups on cyl:11×6 and wider in sums
   - [x] Lemma 4.13: tempo-exact groups have the results of over beside every finite test game (proved by hand,
         refereed); none of the nine known groups is tempo-exact (K56)
   - [x] The 2 + 3 group has the results of over beside every finite test game: Proposition 4.14, Lemma 4.15 (proved,
         refereed, proved again blind by Codex K58), Corollary 4.16 (proved given two twice-checked computations) (K57)
   - [x] The four cyl:8×7 groups have the results of over (Black-side condition by two programs); five groups with
         the results of over on flat 8×7, the smallest with 2 + 2 pawns, four of them also on flat 8×8:
         Corollary 4.17 (proved given twice-checked computations, refereed) (K59)
   - [x] The 2 + 2 group on the ordinary 8×8 board: in chess, and beside P contexts (K63, refereed): not an exact over group in chess (tablebase), one freeze survives as a mutual zugzwang; beside file-h pawns in P the prediction fails in 12 of 283 contexts
   - [x] Census of exact over groups on flat 8×8, classes {b,c,f} and {b,e,f}, with (B1), condition (C) and ladder length for every group (K65 refereed, K66 independent check): 38 groups; 27 with (B1); 7 with the results of over without (B1); 4 fail (C); 5 seven-man groups exact in chess (tablebase). Both search programs agree on both classes
   - [x] The other two classes of the known shape on flat 8×8, {a,b,e} and {a,d,e}: 10 and 3 groups, 48 distinct in the four classes, 27 up to symmetry; two more exact in chess (K67, refereed by K77; census paragraph of Corollary 4.17)
   - [ ] Other file classes of flat 8×7; flat 9×7
   - [x] The exact condition in place of the Black-side condition: Theorem 4.18, decided by one game on the group's
         own graph or by one short test game, Corollary 4.19 (proved, refereed) (K60)
   - [x] Blind proof of Theorem 4.18 by Codex: all four statements proved; part (c) without the determinacy theorem;
         the proofs need the e.p. right to add moves only, as in chess (K61)
   - [x] A test family for the results of over that does not depend on the group: none that is finite, for abstract
         groups (Theorem 4.22); a ladder as long as the number of boards decides, so one ladder per board size
         (Theorem 4.20, Corollary 4.23) (proved, refereed) (K62)
   - [x] Blind proof of Theorems 4.20 and 4.22 by Codex: both proved, no repair (K64)
   - [x] Does a real group need a ladder longer than 2? Yes: one group of the 8×8 census needs 3 (Proposition 4.24; K65 referee, K66)
   - [x] A hand proof for one real group: `Kd4 kb4/kb5 Pb6 Pc2 Pc5 pb7 pc6` (K68, refereed; Proposition 4.25): Definition 4.8's White half and (B1) by hand; the Black half reduced by hand to one computed lemma on two pawns against one (three programs)
   - [x] That lemma: a case table of 486 rows (K70, Codex, blind), accepted by two separately written checkers; referee K73 checked 42 rows by hand, no error; label stays CHECKED-2 (Proposition 4.25 updated). K71 (change the reduction): not achieved, 14 positions left, unrefereed
   - [ ] That lemma by a short hand proof, or the full table checked by hand (30 to 50 hours by the referee's estimate): open
   - [x] The five chess-exact groups beside real pawns on a separated file of the same board, in P (K72, refereed by K74 with a third solver: only C125_10 agrees in all 283 contexts of at most 2 + 2 pawns, and it fails in 3 of all 729 placements on h; the other four fail with 1 + 1 pawns already; paragraph after Proposition 4.25)
   - [~] Which of the 48 groups keep the results of ω beside real pawns, and a rule in terms of the kings' distance to the context file (K75 done, unrefereed: 58 group and file pairs, 11 clean with one pawn a side, no rule in distances alone; referee K76 running)
   - [ ] The seven two-file classes of flat 8×8 outside the four classes: {a,c}, {a,f}, {a,g}, {a,h}, {b,d}, {b,g}, {c,e}
   - [x] Does a real group need a ladder longer than 3? Not among the 48 groups of the four classes (K67, K77); open for other shapes and boards
   - [ ] Hand proof of (O1) and of the d5 root of the K45 group
   - [x] The K45 group in chess at cap 1: d4 freeze and its zero exact, the rest undecided; exact groups also on flat
         8×6 to 10×6 and on cyl:8×7 (K48)
   - [ ] The K45 group in chess at cap 2 (kpsolve is at the 3 GB limit there); other file classes on flat 9×6, 10×6 and
         cyl:8×7; cyl:8×8
3. King-against-king fights
   - [x] Values up to width 10, three blocked pairs: over, under, ±1 occur (K20, K44)
   - [ ] The parity classes and the 885,715 unclassified roots
4. Loopy sums (stopper analogue)
   - [x] Theorems 3.7, 3.8, 3.11 proved and re-derived outside the Claude family (K21, K33)
5. Gafni's K+P v K without edges
   - [x] Answered on cyl:3–8 × 6–8 (K40)
   - [x] ON class reduced by hand to Lemma P; proved outright for the pawn on rank H−1 (K49)
   - [ ] Lemma P below rank H−1 by hand; the two types of ON (Conjecture 7); the odd-width fortresses
   - [ ] The parity classes under the chess stalemate rule
6. Universal zeros
   - [x] Four classes act as 0 beside all contexts of at most 2 pawns a side on cyl:7×6 (K29)
   - [ ] Beyond 2 pawns a side; the T of Definition 2.6 for these groups
7. Hand proofs
   - [x] Position 7.2 (K30) and P5 (K38)

## Foundations (found while the paper's proofs appendix was refereed)

- [x] Theorem 1.11(c): (E) added as a hypothesis, frontier step proved (435ccdc7)
- [x] Promotion convention, order of operations in S, threats in any order, passer-free root for 1.11(c),
      Theorem 1.14 per side to move (16 refereed edits after Codex T81)

- [x] Theorem 2.7 timing clause corrected after Codex T83 (39e19a98)
- [x] Codex blind proofs: Theorem 3.4 (K51), Proposition 2.10(a) (K53); Codex read of 1.11(c) and 1.14 (K52)
- [x] 1.11(c) proof replaced (quiet-move argument), (E) shown necessary, τ_P, 1.14(i) pre-event root (29 refereed edits)
- [x] Codex read of the new 1.11(c) proof text and the repaired 2.7: every step sound; wording fixes applied (K54)
- [ ] Can (E) be dropped at a root with no e.p. right? No counterexample in 12,600 later-failure roots (K54)
- [ ] Lemma 2.6a (the checker's `--ctx` argument): parked; refereed once, not in the note. 0 of the 23 separated
      engine-test positions are certified even with it, so it is written only if a purpose-built test set is wanted

## Paper support (the main session owns `paper/` and `dist/`)

- [x] King claims of Sections IV, V, the conclusion and S12 audited: 14 fixes sent and applied
- [x] General referee report sent; applied where it checked out
- [x] Engine-on-sums test: only separated placements count (answered)
- [x] K47 result sent to the paper side (the K45 group is not over in sums)
- [x] Over-group wording sent (K57 result); neither paper has an over-group sentence, the author has not asked for one
- [ ] Self-contained S12 (referee point M4), if the paper side asks

## Housekeeping

- [x] Post-commit checks K41 and K46 applied
- [x] Pushed by the paper side on the author's word, up to 9fe01bb5 (2026-11-24); later commits wait for the next push
- [x] No raw CLI transcripts in commits (rule since 2026-11-22): `kings/.gitignore` ignores them since 2026-11-24;
      15 older ones are still tracked and wait for the author's decision on the history
- [x] Loose files of the second referee rounds of K20 to K24 packed into local archives, compared byte for byte
      (2026-11-24)
