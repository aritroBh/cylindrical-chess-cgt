# K72: edit for kings/theory/LOOPY.md (not yet refereed)

One edit: a paragraph after Proposition 4.25, before the K43 paragraph. Tested on a scratch copy with
`.venv/bin/python kings/delegate/apply_edits.py kings/theory/LOOPY.md <scratch> kings/delegate/out/K72/EDITS.md`
(1 applied, 0 rejected).

### EDIT after Proposition 4.25: K72 (the five chess-exact over groups beside real pawns in P; not yet refereed)
<<<<<<< OLD
*Computable test (K43).* `kings/delegate/out/K43/plocalp3.cpp` (table solver of P for all king placements
=======
*K72 (2026-11-25; `kings/delegate/out/K72/findings.txt`; not yet refereed).* The five seven-man groups of K65 that are exact over groups in chess were tested in P beside real pawns on one file of the same board at distance ≥ 2 from the group (Definition 2.1), with every context of at most 2 + 2 pawns on ranks 2–7 (283 per file), against the prediction r(ω ⊞ X) at the roots and r(X) at the q's. Only C125_10 (White Kc5, Pb6, Pf2, Pf6; Black Ke5/Ke6, pb7, pf7) has the predicted result everywhere: 283 of 283 contexts on file h, its only separated file, 2,264 positions. The others fail on every separated file: C125_05 on f, g, h 208, 233, 252 of 283; C125_08 on h 248; C145_07 on a, b, c 271, 261, 232; C145_09 on a, b, h 233, 209, 224 (F2: 271, K63). Every failing context has pawns of both colours on the context file, and the smallest are 1 + 1: e.g. C125_08's q after b2–b3 (White Ke5, Pb3, Pb6, Pf6; Black Kc5, pb7, pf7) beside Ph2, ph3, White to move, is predicted lost and is a White win in P (1.b4 Kc6 2.Kf4 …, Kg3×h3 and the h-pawn queens). So exactness in chess does not protect a group: besides F2's failure (the Black king leaves the shuttle and wins a White context pawn; C145_07, C145_09 on h) there is a new one in White's favour, where the non-shuttling White king leaves the group, wins a Black context pawn and breaks the q's mutual zugzwang (C125_05, C125_08, C145_09 on a, b). CHECKED-2 (the K63 referee's pk and the K63 investigator's ref3m agree on all 24,904 P values; two predictors agree); the mechanisms are read from one ref3pv line per failing context (COMPUTED-1).

*Computable test (K43).* `kings/delegate/out/K43/plocalp3.cpp` (table solver of P for all king placements
>>>>>>> NEW
