## 7. Proof of Theorem A

*Part 1* is Lemma S. *Part 2*: the legal moves at each root are those of section 4, and every non-shuttle one is one of the
26 deviations C01-C26 of section 6; for each, the certificate shows that the opponent (the winner of the entry) promotes first
in at most 11 plies after the move.
*Part 3.* Let r be a root, Y either colour. Y's strategy: "if it is Y's turn and the opponent has never left the shuttle,
play the shuttle step (legal by Lemma S; the position is again a root); if the opponent leaves the shuttle, he plays one
of the 26 deviation moves (the list of section 4 is complete), and Y wins by the certificate of that case". Against this strategy
either both sides shuttle for ever (every position is a root, nobody promotes, nobody is mated or stalemated: a draw), or the opponent
deviates at some root and Y wins. So each colour can guarantee at least a draw from every root and the value is D for the
side to move, i.e. (D, D). QED

## 8. The mirror group (Theorem B)

tau(f, r) = (f, 7 - r), colours swapped, side to move swapped. It maps the pawn rules to themselves (White pawns forward = up,
promotion on rank 6 <-> Black pawns forward = down, promotion on rank 1; the double-step rank 2 <-> 5; e.p. squares to
e.p. squares), kings and king-adjacency to themselves, so it maps legal moves to legal moves, checkmate/stalemate to the same,
and first-promotion-wins to the same rule. tau(Z_B) = `Ka3/Kb2 (White shuttle), kb5/kc4 (Black shuttle), Pb4 Pc3 pa4 pb3`:
the White king b2/c3 becomes the Black king b5/c4, the Black king a4/b5 becomes the White king a3/b2, Pa3 -> pa4, Pb4 -> pb3,
pb3 -> Pb4, pc4 -> Pc3. A root `(wk, bk, side)` of Z_B goes to the root `(tau(bk), tau(wk), other side)` of the mirror. So
Theorem A for the mirror follows. Machine check (`scripts/tau_check.py`): tau of the 8 roots is the set of the 8 roots of
the mirror group, and the legal-move sets are equivariant on all 22,818 positions reachable from the roots within 8 plies;
the certificates of the 52 children (26 of Z_B, 26 of the mirror) are verified independently, section 9.

## 9. Machine checks (what was run, and what each check covers)

1. `scripts/pm.py` is a third implementation of the P model (written from SPEC.md; independent of kpsolve.c, kp_p.c, ref3.cpp).
   Its move lists at the 16 roots equal those of kpp (`--pmodel --moves`) and ref3m (`--moves`), and its depth-bounded search
   finds no win for either side from any root within 21 plies, and the win of every one of the 52 deviation children
   within at most 11 plies (`scripts/t1.py`).
2. `scripts/verify_certs.py` re-checks every position cited in the certificates (409 opponent-to-move positions, 626 leaf
   positions, 52 deviations of Z_B and its mirror) against **kpp and ref3m**: the set of legal replies of each cited position
   equals the certificate's list, each reply leads to a position valued as a win for the winner, each leaf has a promotion move
   valued as a win. 2,642 reply values, 0 discrepancies.
3. `scripts/tau_check.py`: the symmetry tau (above).
4. Root values: kpp and ref3 both give D at all 16 roots.
