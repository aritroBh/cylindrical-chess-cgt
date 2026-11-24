# W9: second program for o(S(X)), X = W b2 d4 g3 h5 / B a7 c7 f7 g4 (cyl 8x8, e.p. off, count, BIG=256)

Verdict: my program AGREES. S(X) has outcome R (Black wins whoever starts); W(X) has outcome N.

Files: sx2.py (solver, imports nothing from cylcgt), validate.py (compares against cylcgt as a black box), reach.py (item 4); logs main_run.log, validate.log, reach.log.

## Rules as implemented (from 02_rules.tex, 05_sums.tex, s12a_core.tex A.I-A.II)
1. Files a..h wrap (distance on the 8-cycle); ranks 1..8 are edges. White moves up, Black down. Step to an empty square; double step from rank 2 (W) / rank 7 (B) over an empty square to an empty one; capture diagonally forward on a file at distance 1 (seam included). No e.p. A pawn on its last rank has no move.
2. A pawn is passed iff no enemy pawn is ahead of it on its file or on a neighbouring file (textbook test; e.p. off). A pawn on its last rank is passed.
3. Race (both sides have a passed pawn after a move): distance = steps to the last rank as on an empty board, a double step counted as one move (W: 8 - r - [r = 2]; B: r - 1 - [r = 7]); each side uses its best passed pawn; fewer moves wins; a tie goes to the side that did not move.
4. W(X): after a move, if some side has a passed pawn the game ends (one side: it wins; both: race rule); a player with no move loses.
5. S(X): position = multiset of live components plus one integer t. After a move in a component, the WHOLE moved component is tested first: a passed pawn gives +-BIG (race rule if both), added to t; otherwise it is re-split along empty files (one ring if no file is empty, arcs merged across the seam). Components are maximal runs of adjacent occupied files.
6. Integers: t > 0: Left may move to t-1; t < 0: Right may move to t+1; 0: no move. Normal play, player with no move loses.
Ambiguity: the count rule says "needs fewer moves"; I use min over passed pawns, which equals the front-pawn choice in cylcgt (a rear pawn on a file is never closer). Nothing else needed cylcgt.

Why one integer total is valid: the integer components are numbers (a +BIG is the game BIG = {BIG-1|}, a -BIG is {|-BIG+1}); numbers add, so their sum equals the single integer t, and replacing a summand by an equal game never changes the outcome of the whole sum. No bound or other shortcut is used; the state is (sorted tuple of components, t, player), solved by exact memoised minimax with no pruning of t. (The state space turned out tiny: 273 nodes.)

## Validation (rule reading)
- Integer checks: empty sum is P; t = 3 is L; t = -2 is R (assertions in validate.py).
- 400 random pawn positions on cyl8 (e.p. off, 4-8 pawns, ranks 2-7, no initial passed pawn; seed 7): my S-outcome equals cylcgt.value + cgt.outcome in 400/400. Outcome mix N 153, R 115, L 108, P 24; 217 had two or more components at the root; in 27 of them S and W differ in outcome (so the sum-model rule, freeze-then-split, and the cancellation of +BIG against -BIG are really exercised), and cylcgt agrees with me on all 27. No disagreement to report.
- {BIG|0}+{0|-BIG} = 0 is a statement about abstract games; my solver takes pawn components, so it is covered only through the sum-with-cancellation cases above (not tested as an abstract game).

## Result for X
- X is one component at the root (files f,g,h,a,b,c,d; e empty). Confirmed: split() returns 1 component.
- S(X): White to move: Black wins (White does not win); Black to move: Black wins. Overall outcome R. 273 memo nodes, 15 splitting moves seen, at most 2 live components at once, 0.02 s, 14 MB.
- W(X): White to move wins, Black to move wins: outcome N. 176 nodes, instant. This matches the proposition and the two earlier programs.

## Item 4 (reach.py)
Positions reachable from X by moves of either side in any order, before any passed pawn: 660. Of these 312 have two or more live components, and in all 312 one component carries a White threat (a passed pawn for White can be forced within its files, no earlier passed pawn) and a different one a Black threat. Example: W b6 d5 g3 / B c7 f5 g4 h4 (components b,c,d and f,g,h). So X is not HSS, and the sentence "X is one component at the root, yet components with opposite threats appear later" is confirmed. (My threat test: reachable by moves of either side in any order inside the component; a passed pawn of either side counts for that side, both in a race.)

## Conclusion
A separately written program (own rules code, own solver, own whole-board code, no import of cylcgt) agrees: o(S(X)) = R for both starting sides, o(W(X)) = N. The label "two separately written programs agree" is supported for (ii), with the caveat that the author of this second program read the rules from the paper but could consult pawns.py for the min-over-passed-pawns detail (above); no other consultation. Compute: under 3 minutes in total, one process, nice 15, under 20 MB for the main run.
