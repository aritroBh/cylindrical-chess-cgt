# K76: edit for kings/theory/LOOPY.md (replaces kings/delegate/out/K75/EDITS.md)

One edit: a paragraph after Proposition 4.25, after the K72 paragraph and immediately before the K43 paragraph (OLD is
anchored on the line `*Computable test (K43).*` only). Tested on a scratch copy with
`.venv/bin/python kings/delegate/apply_edits.py kings/theory/LOOPY.md <scratch> kings/delegate/out/K75/verify/EDITS.md`
(1 applied, 0 rejected).

### EDIT after Proposition 4.25: K75 (all 48 groups beside real pawns on one file in P; refereed, K76)
<<<<<<< OLD
*Computable test (K43).* `kings/delegate/out/K43/plocalp3.cpp` (table solver of P for all king placements
=======
*K75 (2026-11-26; `kings/delegate/out/K75/findings.txt`; refereed (K76), `kings/delegate/out/K75/verify/VERIFY.md`).* K72's test, in P on flat 8×8, run on all 48 exact over groups of the K65 census and K67 (K67's search CHECKED-2, p45a and r48; its referee pending) and every file Definition 2.1 allows (58 pairs; seven groups have none): beside every context of at most 1 + 1 pawns on that file (43 contexts; both roots against r(ω ⊞ X), both q's against r(X), either side to move) the P result is the predicted one for 11 pairs (10 groups) and differs in 427 contexts of the other 47, every one with pawns of both colours (CHECKED-2: pk, ref3m and the referee's p74 agree at all 19,952 positions; four predictors agree). For the three groups that fail (C) (C125_14, C145_19, C014_08) only q = 0_D and root ≤ ω are proved (Theorem 4.18 (a)); against that, 18 of the 427 contexts are no failure and C145_19 on h has none. The clean pairs stay clean in larger contexts (CHECKED-2 up to 2 + 2 for C125_10 and C145_13 and up to 3 + 3 for C014_01 on h; the rest COMPUTED-1, p74): C014_01, C145_13, C145_17, C145_20 on h and C125_20 on a, C125_21 on h beside all 729 placements of pawns on the file; C125_17, C125_18 on h and C014_06 on g and h beside every context of at most 2 + 2; C125_10 on h beside every context of at most 3 + 3 (not 4 + 1, K72 paragraph). Every clean pair has d_W ≥ 4 and d_W + d_B ≥ 8 (d_W, d_B the file distances from the context file to the White king and to the nearer shuttle square), but the distances do not decide: of the 12 pairs with d_W = 7, d_B = 5 four are clean and eight fail, among them C145_13 and C145_12, one shape a rank apart. In the eight the smallest failing context is Ph2, ph3, a dead D-game; in the three played through (C125_03, C125_04, C145_12) the released Black king takes a group pawn while the White king must also guard h2 (after …K×h2 the h3-pawn is passed) and the counter-raid on Black's b-pawn, which wins beside nothing, now loses (explanation, not a proof). This is a description of the 58 pairs, not a conjecture.

*Computable test (K43).* `kings/delegate/out/K43/plocalp3.cpp` (table solver of P for all king placements
>>>>>>> NEW
