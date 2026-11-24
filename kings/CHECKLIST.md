# Kings checklist

Updated 2026-11-23. `[x]` done and committed, `[~]` running, `[ ]` open. Each item has an investigator and an
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
   - [ ] The 2 + 3 group against loopy test games and beside P contexts; groups on cyl:11×6 and wider in sums
   - [~] A stronger exact test (losing moves still lose against free passes) and a lemma that it forces the results of
         over (K56)
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
- [ ] Final over-group sentence for the long version, after K48
- [ ] Self-contained S12 (referee point M4), if the paper side asks

## Housekeeping

- [x] Post-commit checks K41 and K46 applied
- [ ] Nothing is pushed since 2026-10-29; pushing waits for the author
- [ ] No raw CLI transcripts in commits (rule since 2026-11-22)
