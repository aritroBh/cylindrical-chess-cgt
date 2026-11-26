# K75: edit for kings/theory/LOOPY.md (not yet refereed)

One edit: a paragraph after Proposition 4.25, immediately before the K43 paragraph (anchored on the line
`*Computable test (K43).*` only, so a K72 paragraph installed before it does not matter). Tested on a scratch copy with
`.venv/bin/python kings/delegate/apply_edits.py kings/theory/LOOPY.md <scratch> kings/delegate/out/K75/EDITS.md`.

### EDIT after Proposition 4.25: K75 (all 48 groups beside real pawns on one file in P; not yet refereed)
<<<<<<< OLD
*Computable test (K43).* `kings/delegate/out/K43/plocalp3.cpp` (table solver of P for all king placements
=======
*K75 (2026-11-26; `kings/delegate/out/K75/findings.txt`; not yet refereed).* K72's test, in P on flat 8×8, run on all 48 exact over groups of the K65 census and K67 (K67's ten from a search confirmed by one program) and every file Definition 2.1 allows (58 pairs; seven groups have none): beside every context of at most 1 + 1 pawns on that file (43 contexts; both roots with r(ω ⊞ X), both q's with r(X), either side to move) the P result is the predicted one for 11 pairs (10 groups) and fails in 427 contexts of the other 47 pairs (CHECKED-2: pk and ref3m agree at all 19,952 positions; two predictors agree). Every failing context has pawns of both colours. Beside every context of at most 2 + 2 pawns on h the groups `Ka5 kc5/kc6 Pb2 Pe5 Pe6 pb7 pe7` and C125_10 agree everywhere (283 contexts), and `Ka5 kc4/kc5 Pa4 Pa6 Pb2 pa7` (K67) beside every context of at most 3 + 3 pawns on h (583 contexts; CHECKED-2). CONJECTURE (empirical, these 58 pairs): with d_W, d_B the file distances from the context file to the White king and to the nearer shuttle square, White-favour failures occur in every pair with d_W ≤ 3 and Black-favour failures in every pair with d_B ≤ 4 except C125_10 on h (clean) and C014_04 on h (it fails for White only), so a clean pair needs d_W ≥ 4 and d_B ≥ 5 (exception C125_10); beyond that the two distances do not decide (6 of the 18 pairs with d_W, d_B ≥ 5 are clean; 10 fail for Black, most first at Ph2 ph3, Ph2 ph4 as F2 does).

*Computable test (K43).* `kings/delegate/out/K43/plocalp3.cpp` (table solver of P for all king placements
>>>>>>> NEW
