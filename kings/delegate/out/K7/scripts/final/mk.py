import re,sys
t=open('final_edits.txt').read()
def ded(x):
    ls=x.split("\n")
    return "\n".join([ls[0]]+[l[2:] if l.startswith("  ") else l for l in ls[1:]])
def rep(old,new,cnt=1):
    global t
    n=t.count(old)
    if n!=cnt:
        old,new=ded(old),ded(new)
        n=t.count(old)
    assert n==cnt,(n,old[:80])
    t=t.replace(old,new)

# ---------- EDIT 1
rep("""was found false. Theorem 2.7 and P12 were repaired afterwards (task K7, 2026-10-22): they are PROVED after
repair in P, and K3's objection to Theorem 2.7 conflated the model P with the D-model (revised after K7,
2026-10-22).
>>>>>>> NEW""","""was found false. Theorem 2.7 and P12 were repaired afterwards (task K7, 2026-10-22): they are PROVED after
repair in P (revised after K7, 2026-10-22). K3's objection to Theorem 2.7 read it as a statement about the
D-model; it is a statement about P (Remark after Theorem 2.7). **Caveat for the K7 repair:** it is one
AI-written proof. Three AI reviewers read its first draft and found one real error, in the window form (b),
which was false when Q carried an en passant right with its target off F_Z; the text now accounts for that
right (revised after K7, 2026-10-22). K3 did not see the repair, and no second model and no human has
re-derived it.
>>>>>>> NEW""")

# ---------- EDIT 2
rep("""K3's objection (a context passer within the window ends the game in s's favour) is right in the D-model and wrong in P: in P only a promotion is terminal, and (L2) bounds it. The theorem gives a P-win only. A C-win needs (A_Q), and the D-model use in Theorem 1.14 needs (V2) |""",
"""K3's objection (a context passer within the window ends the game in s's favour) assumes that a passer is terminal. That holds in the D-model and not in P: in P only a promotion is terminal, and (L2) bounds it. Whether a passer is decisive in D is (V2), a hypothesis of Theorem 1.14, which Theorem 2.7 does not claim. The window form (b) of the first K7 draft was FALSE when Q carried an e.p. right with its target off F_Z (counterexample in the text); (L2) now counts that right. The theorem gives a P-win only. A C-win needs (A_Q) |""")

# ---------- EDIT 8: Data bullet on e.p.
rep("""The e.p. right and the place of
    s's king were not said.)
""","""The e.p. right and the place of
    s's king were not said.)
  - In (a), r is a Z-move, so an e.p. right carried by Q has its target on F_Z. In the window form (b) the
    target may be anywhere, and (L2) accounts for it (revised after K7, 2026-10-22).
""")
# unsafe promotion
rep("""An unsafe promotion is
       not counted as a win.""","""An unsafe
       promotion ends the game as a failure for s̄.""")
# L2 definition
rep("""an s̄ context pawn stays
    where it is unless s captures it, and no e.p. right exists. Then **μ_s ≥ T + 1**.""",
"""an s̄ context pawn stays
    where it is unless s captures it, and no e.p. right exists except the one described next. If Q carries an
    e.p. right whose target square is **off F_Z**, Q° keeps it: s may use it at its first move, and only then
    (the capture lands on the target and removes the s̄ pawn that has just double-stepped). A right whose target
    is on F_Z concerns Z-pawns only, which Q° has deleted, so it is dropped. In (a) Q carries no right of the first
    kind. Then **μ_s ≥ T + 1**.""")
rep("""A king move that captures an s̄ context
      blocker is one of the moves, so the king's help is counted.""","""A king move that captures an s̄ context
      blocker is one of the moves, so the king's help is counted, and so is the e.p. capture just described.""")
# Theorem statement (b)
rep("""Theorem 2.7 (sufficiency of the certificate). PROVED after repair (in P). (revised after K7, 2026-10-22)**""",
"""Theorem 2.7 (sufficiency of the certificate). PROVED after repair (in P). (revised after K7, 2026-10-22)**
(The first K7 draft of (b) had no e.p. clause in (L2) and was FALSE; see the example in the list "The conditions
cannot be dropped" below.)""")
rep("""s̄'s king stands on F_Z, and no s̄ context pawn attacks s's king (automatic if s's king is on F_Z). If (L1),""",
"""s̄'s king stands on F_Z, and no s̄ context pawn attacks s's king (automatic if s's king is on F_Z). Q may
    carry an e.p. right with its target anywhere: (L2) counts a right whose target is off F_Z, and π keeps a
    right whose target is on F_Z. If (L1),""")
# Step 0: I5
rep("""iff an s̄
      Z-pawn attacks its king, iff s is in check in π(R).""","""iff an s̄
      Z-pawn attacks its king, iff s is in check in π(R).
    - (I5) *E.p. rights.* A right created by s̄ comes from a Z-pawn double step, since s̄ plays Z-moves only, so its
      target is on F_Z, and only Z-pawns of s can use it (a context pawn is not adjacent to F_Z). A right created by
      s is of no use to s̄'s prescribed moves. So the only e.p. capture that an s context pawn can ever make is the
      one of the right carried by Q, if its target is off F_Z, and it can be made at s's first turn only.""")
rep("""an
      e.p. right it creates has a target off F_Z and is dropped by π, as a pass does.""","""an
      e.p. right it creates has a target off F_Z and is dropped by π, as a pass does. The e.p. capture of the right
      of Q (target off F_Z, I5) is such a move too: it moves an s context pawn and removes an s̄ context pawn.""")
# Claim M
rep("""(I4); and no e.p. right is used, because s̄'s context pawns never double-step. So μ_s ≤ j ≤ T, which
      contradicts (L2).""","""(I4); and the only e.p. right that can be used is the one of Q (I5), at s's first turn. If it is used, it is
      the first move of the sequence, and Q° keeps exactly that right for its first move. So μ_s ≤ j ≤ T, which
      contradicts (L2).""")
rep("""*Part (b)* is the same proof with Q as the starting point: only (I1)–(I4) at Q were used, and they are the
  hypotheses of (b) together with Lemma 2.2.""","""*Part (b)* is the same proof with Q as the starting point: only (I1)–(I5) at Q were used, and they are the
  hypotheses of (b) together with Lemma 2.2. *Part (a)* is part (b) applied to Q: m and r are Z-moves, so
  every pawn is still a Z-pawn on F_Z or a context pawn on a context file and the buffer is empty (Lemma 2.2);
  s̄'s king is on F_Z by the Data; no s̄ context pawn attacks s's king, because m was legal and r moves no context
  pawn; and the only e.p. right Q can carry is one created by r, with its target on F_Z.""")
# Remark
i=t.index("**Remark (K3's objection, answered).**")
j=t.index("**What Theorem 2.7 does not give.**")
t=t[:i]+"""**Remark (K3's objection, answered).** K3 wrote that (L2) counts promotions only and that a context passer within
T ends the game in s's favour. In the D-model a passer is a terminal. Whether it is decisive is (V2), a hypothesis
of Theorem 1.14 (Remark 2.11, P11), and Theorem 2.7 does not claim it. Theorem 2.7 is a statement about P. In P a
context passer of s is not terminal. Only a promotion ends the game, and (L2) bounds the first promotion of every
context pawn of s, passer or not, by T + 1 moves of s. A passer that stands at the end of the window has not
promoted, and s̄ has. So the objection does not apply to Theorem 2.7: it reads a P-statement as a D-statement.

"""+t[j:]
# conditions cannot be dropped: e.p. example
rep("""- *The conditions cannot be dropped.* All three examples are in cyl:7×6 and checked with the P solver.""",
"""- *The conditions cannot be dropped.* All examples are in cyl:7×6 and checked with the P solver.""")
rep("""  - (L1) is the substance: with no local win there is nothing to transfer.
""","""  - (L2), the e.p. clause: `Kd6 kc4 Pe3 pa4 pe4 pf3`, White to move, e.p. right on f4 (Black has just played
    f5–f3). Black (s̄) has a local win with T = 3 (a3, a2, a1=Q), (L3) holds, and without the clause μ_s = 6, so
    (L1), (L2) and (L3) would all hold. Yet White wins in P: exf4 e.p., f5, f6=Q, and its third move promotes
    before Black's third. With the clause μ_s = 3 < T + 1 = 4, as it should. The same position without the right
    is a Black win in P. This is why the first K7 draft of (b) was false. Part (a) cannot meet this case.
  - (L1) is the substance: with no local win there is nothing to transfer.
""")
# Cor 2.7'
rep("""P-loss, and for that m, every legal reply r and every T, (L1), (L2) or (L3) fails.
- *Proof.*""","""P-loss, and for that m, every admissible reply r (Definition 2.6: a non-promoting Z-move of σ̄ that leaves its
king on F_Z) and every T ≥ 1, (L1), (L2) or (L3) fails. A promoting reply by σ̄ would make m a P-loss for σ, so
it does not occur for a move that is not a P-loss; replies that are not admissible are outside LC_T.
- *Proof.*""")
# EDIT 13
rep("""for every reply r and every T, every king move that does not lose in P
  violates (L1), (L2) or (L3)""","""for every admissible reply r (Definition 2.6) and every T ≥ 1, every king
  move that does not lose in P violates (L1), (L2) or (L3)""")
# EDIT 14
rep("""For that move, and for every reply r and every T, (L1), (L2) or (L3) fails.""","""For that move, and for every admissible reply r (Definition 2.6) and every T ≥ 1, (L1), (L2) or (L3) fails.""")
# EDIT 10 add e.p. bullet
rep("""    the s Z-pawn is captured by r. In §5.3 and P8 it survives; it is far from promotion, and (L1) covers it.
>>>>>>> NEW""","""    the s Z-pawn is captured by r. In §5.3 and P8 it survives; it is far from promotion, and (L1) covers it.
  - *The e.p. clause of (L2)* (revised after K7, 2026-10-22). In the window form (b), Q may carry an e.p. right with
    its target off F_Z, and Q° then lets s use it at its first move. It does not change the T = 1 argument: the
    capture lands on the target square, the third rank of s's side, so it is never a promotion on a board with
    at least 4 ranks, and a pawn that promotes at once still has to stand on its penultimate rank.
>>>>>>> NEW""")
# EDIT 12 mention e.p.
rep("""its Z-pawn g7 has the moves g6 and g5 in every context (revised after K7, 2026-10-22);""",
"""its Z-pawn g7 has the moves g6 and g5 in every context; if Y carries an e.p. right, (L2) counts it, and it cannot promote at once (revised after K7, 2026-10-22);""")
open('final_edits2.txt','w').write(t)
print("ok")
