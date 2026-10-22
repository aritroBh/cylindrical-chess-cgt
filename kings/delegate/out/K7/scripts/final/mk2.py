t=open('final_edits2.txt').read()
def rep(old,new):
    global t
    assert t.count(old)==1,(t.count(old),old[:70])
    t=t.replace(old,new)
rep("""Q may
    carry an e.p. right with its target anywhere: (L2) counts a right whose target is off F_Z, and π keeps a
    right whose target is on F_Z. If (L1),""","""Q may
  carry an e.p. right with its target anywhere: (L2) counts a right whose target is off F_Z, and π keeps a
  right whose target is on F_Z. If (L1),""")
rep("""    e.p. right it creates has a target off F_Z and is dropped by π, as a pass does. The e.p. capture of the right
    of Q (target off F_Z, I5) is such a move too: it moves an s context pawn and removes an s̄ context pawn. It is legal only if s is not
""","""    e.p. right it creates has a target off F_Z and is dropped by π, as a pass does. The e.p. capture of the right
    of Q (target off F_Z, I5) is such a move too: it moves an s context pawn and removes an s̄ context pawn. A
    context move is legal only if s is not
""")
rep("""capture lands on the target square, the third rank of s's side, so it is never a promotion on a board with
    at least 4 ranks, and a pawn that promotes at once still has to stand on its penultimate rank.""",
"""capture lands on the target square, which is on the third rank of s̄'s side and so is never s's last rank, and a
    pawn that promotes at once still has to stand on its penultimate rank.""")
# new edits
t=t.rstrip("\n")+"""

### EDIT 16: Corollary 2.8: finite budgets are a side remark
<<<<<<< OLD
- for every finite k, provided s's king always has a legal move in Q_Z. This is the stalemate proviso: a
  king boxed in at a rank edge, with no pass left, would be stalemated.
=======
- for every finite k, provided s's king always has a legal move in Q_Z. This is the stalemate proviso: a
  king boxed in at a rank edge, with no pass left, would be stalemated.

The finite-k clause is a side remark (revised after K7, 2026-10-22). The local game of Definition 2.6 has k = ∞
only, and Theorem 2.7 uses nothing else. The first clause gives (L1) of Definition 2.6 for this Q_Z: p promotes
by pushes with s̄'s king never moving, s has no pawn to promote, and s cannot be stalemated because it may pass.
>>>>>>> NEW

### EDIT 17: 5.1: the (L1) evidence, old game and K7 re-run
<<<<<<< OLD
    not checked; they differ from ∞ when T ≥ 6. This is scratch evidence (Appendix A) (revised after review:
    R1 item 10, R4 item 9).
=======
    not checked; they differ from ∞ when T ≥ 6. This is scratch evidence (Appendix A) (revised after review:
    R1 item 10, R4 item 9).
    - These runs used the local game as it was before K7 (finite budgets, optional confinement). K7 re-ran the local
      game of Definition 2.6 (k = ∞, king confined to {h, a, b}, a mate of s a win) on the five sorties, after the
      reply Kxa4, with a second scratch implementation. (L1) holds with T = 6, 6, 5, 6, 6 for Kg4, Kg5, Kg6, Kh6,
      Ka6, and with T = 6, 6, 6, 7, 7 if the new queen must also be safe. This is still scratch evidence: the label
      stays CONJECTURE (revised after K7, 2026-10-22).
>>>>>>> NEW

### EDIT 18: Appendix A: the old local game
<<<<<<< OLD
- **Local promotion game.** Retrograde least fixed point over (position, side to move, pass budget k ≤ 4 or
  ∞), with only Z's pieces on the board.
=======
- **Local promotion game.** Retrograde least fixed point over (position, side to move, pass budget k ≤ 4 or
  ∞), with only Z's pieces on the board. (This is the game as it was before K7. Definition 2.6 now has k = ∞
  only, counts a mate of s as a win for s̄, and always confines s̄'s king to F_Z. The K7 checks below use the new
  game; revised after K7, 2026-10-22.)
>>>>>>> NEW
"""
open('final_edits3.txt','w').write(t+"\n")
