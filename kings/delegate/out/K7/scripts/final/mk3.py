t=open('final_edits3.txt').read()
def rep(old,new):
    global t
    assert t.count(old)==1,(t.count(old),old[:70])
    t=t.replace(old,new)
rep("""P-loss, and for that m, every admissible reply r (Definition 2.6: a non-promoting Z-move of σ̄ that leaves its
king on F_Z) and every T ≥ 1, (L1), (L2) or (L3) fails. A promoting reply by σ̄ would make m a P-loss for σ, so
it does not occur for a move that is not a P-loss; replies that are not admissible are outside LC_T.""",
"""P-loss, and for that m, every admissible reply r (Definition 2.6, with s = σ̄ and s̄ = σ: a non-promoting Z-move
of σ that leaves σ's king on F_Z) and every T ≥ 1, (L1), (L2) or (L3) fails. A promoting reply by σ would make m a
P-loss for σ̄, so it does not occur for a move that is not a P-loss; replies that are not admissible are outside
LC_T.""")
t=t.rstrip("\n")+"""

### EDIT 19: status table: 5.1 (L1) row
<<<<<<< OLD
| §5.1, (L1) | CONJECTURE (scratch, k ≤ 4 and k = ∞ only; (L3) not checked) | R1 items 3 and 10, R4 item 9 |
=======
| §5.1, (L1) | CONJECTURE (scratch, k ≤ 4 and k = ∞ only; (L3) not checked). The k = ∞ case was re-run in K7 against the local game of Definition 2.6 (T = 5 to 7), same label (revised after K7, 2026-10-22) | R1 items 3 and 10, R4 item 9; K7 |
>>>>>>> NEW
"""
open('final_edits3.txt','w').write(t+"\n")
