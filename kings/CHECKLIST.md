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
   - [~] Hand proof that the K45 group is exact, and whether it equals over in sums (K47)
   - [ ] The K45 group in chess (promotion cap 1 and 2)
   - [ ] Over groups on flat boards and on taller boards
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
- [~] Codex read of the new 1.11(c) proof text and the repaired 2.7 (K54)
- [ ] Lemma 2.6a (the checker's `--ctx` argument): parked; refereed once, not in the note. 0 of the 23 separated
      engine-test positions are certified even with it, so it is written only if a purpose-built test set is wanted

## Paper support (the main session owns `paper/` and `dist/`)

- [x] King claims of Sections IV, V, the conclusion and S12 audited: 14 fixes sent and applied
- [x] General referee report sent; applied where it checked out
- [x] Engine-on-sums test: only separated placements count (answered)
- [ ] Tell the paper side when K47 lands (over group: is it worth a sentence?)
- [ ] Self-contained S12 (referee point M4), if the paper side asks

## Housekeeping

- [x] Post-commit checks K41 and K46 applied
- [ ] Nothing is pushed since 2026-10-29; pushing waits for the author
- [ ] No raw CLI transcripts in commits (rule since 2026-11-22)
