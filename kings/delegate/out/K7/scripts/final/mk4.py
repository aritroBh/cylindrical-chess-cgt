t=open('final_edits3.txt').read()
i=t.index("### EDIT 15:")
j=t.index("### EDIT 16:")
new15='''### EDIT 15: Appendix A: K7 checks
<<<<<<< OLD
- **Full P-model check.** The local promotion game run on the full positions of §6, with no budget (k = 0).
=======
- **Full P-model check.** The local promotion game run on the full positions of §6, with no budget (k = 0).
- **K7 checks of Theorem 2.7 (2026-10-22; scripts in the K7 scratchpads, not saved in the project).** They test the
  statement, not the proof, on random positions with at most 3 pawns a side (revised after K7, 2026-10-22):
  - a Python move generator, which agrees with `kpsolve --moves` on 1200 random positions (cyl:7×6, cyl:6×5,
    flat:5×4) and on 600 positions with an e.p. right (cyl:7×6, flat:6×6);
  - a solver of the local game of (L1) (passes, confined king, mate of s a win, promotion by s a failure, T ≤ 5),
    a search for μ_s (context pawns only, and the old count with Z-pawns), and a search of the real window game
    for (L3) (s̄ restricted to winning local moves, s free);
  - the exact P value from a private copy of `kings/kpsolve.c` with one added switch (a promotion wins at once
    for the promoter, kings move normally). The project file is unchanged.
  - **Run 1 (first draft; no e.p. right at Q).** Window positions (Theorem 2.7(b); Z-group on files a–c): 9300
    positions on cyl:7×6, 7×5, 7×7, 8×6 and flat:6×6; (L1) holds in 2221, and LC_T (with (L2) on context pawns and
    (L3)) in 1379. In all 1379 s̄ wins P. Random Y, Z-move m, reply r (any non-promoting Z-move reply keeping s̄'s king
    on F_Z), cyl:7×6: 3787 triples, LC_T in 508, again all P-wins. The generator set no e.p. right at Q, so this run
    could not meet the case that broke the first draft of (b). Its (L3) routine also rejected any real promotion
    by s, which cannot happen under (L1) and (L2), so it tested a subset of the stated hypotheses.
  - **Run 2 (after the review of the first draft; e.p. right at Q).** Each position has an e.p. right: an s̄ pawn has
    just double-stepped, and an s pawn stands beside it in 85% of the cases. The target is on a context file in
    most positions and on F_Z in 522 of the positions with LC_T. 34000 random positions on cyl:7×6 (twice), 8×6,
    7×5, 7×7 and flat:6×6, T ≤ 4 (T ≤ 3 on 7×5), with (L3) as stated (stalemate of s only). (L1) holds in 7559.
    LC_T with the e.p. clause of (L2) holds in 4998, and **in all 4998 s̄ wins P: no counterexample**. LC_T read
    without the e.p. clause (the first draft) holds in 5128, and in 70 of them s̄ does not win P, which are
    counterexamples to the first draft of (b).
  - Where hypotheses fail (run 1): (L1) holds and (L2) fails in 709 non-wins; (L3) fails in 3 of the window positions
    and in 3 of the triples (all draws by stalemate of s); the old Z-pawn count would have rejected 105 window
    positions that are P-wins; in 221 the queen clause of (L1) fails while (L1_P) holds and s̄ wins P.
  - Examples: `Kb5 kd5 Pb4 Pc5 Pe3 Pf3 Pf4 Pf5` (b), `Kd6 kc2 pa3 Pe4 pe5 pf5` (w), `Ke6 ka1 Pc4 pb3 pc5` (w),
    `Kd6 kc4 Pe3 pa4 pe4 pf3` with e.p. right f4 (w) (cyl:7×6). The last one, found by the reviewers, is a White
    win in P and a Black win in P without the right (`kpsolve`-style P solver, private copy).
>>>>>>> NEW

'''
t=t[:i]+new15+t[j:]
open('final_edits4.txt','w').write(t)
