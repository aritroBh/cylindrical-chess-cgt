import re
R='/Users/aritro/Downloads/Research/Chessendgames/kings/'
L=open(R+'theory/LOOPY.md').read()
E=open(R+'delegate/out/K19/EDITS.md').read()
blocks=re.findall(r'### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW',E,re.S)
fix={}
for lab,old,new in blocks:
    fix[lab]=(old,new)
# 1: black moves
old,new=fix['5.1-black-moves']
new=new[:new.index('  (Corrected after K19')]+"""  (Corrected after K19, 2026-10-27: the earlier list had Kb5 in place of Kb3, and a zugzwang argument for a move
  that is not legal. This was a transcription slip in this section: `notes/diagram_audit.md` §C.3 and the scratch
  list of Appendix A both give the correct list a3, b3, c3, c4, c5. The conclusion stands. K19's move generator,
  checked against `kpsolve --moves`, gives the list above, and so does the referee's.)"""
fix['5.1-black-moves']=(old,new)
# 2: status-5.5
old,new=fix['status-5.5']
new=new.replace("(T = 6 + k) and not against unlimited passes","(T = 6 + k with the queen clause, T = 5 + k for k ≥ 1 without it) and not against unlimited passes")
assert 'without it' in new
fix['status-5.5']=(old,new)
# 3: 5.5-escape
old,new=fix['5.5-escape']
a="which are nevertheless punished in P and in C, because the real supply is finite."
assert a in new
new=new.replace(a,"which are nevertheless punished in P and in C in the bare group, where Black has no spare move\n  (k = 0, T = 6). A context with k spare moves costs k tempi (T = 6 + k), and (L2) then asks for μ ≥ 7 + k.")
fix['5.5-escape']=(old,new)
# 4: L1 bullet
old,new=fix['5.1-L1-bullet']
a="""(revised after K19, 2026-10-27: the scratch run and K19's code agree. The budgets k = 5, 6, 7, 8 equal k = ∞,
    and every k ≥ 7 equals k = ∞, because the window contains at most T ≤ 7 moves of s, so no budget is used up.)"""
assert a in new
new=new.replace(a,"""(revised after K19, 2026-10-27: for k ≤ 4 and k = ∞ the scratch run and K19's code agree. The budgets k = 5, 6, 8 were
    never run before: K19's code and the referee's own code (K19/VERIFY.md) agree that they equal k = ∞. Every
    k ≥ 7 equals k = ∞ for a reason: the window contains at most T ≤ 7 moves of s, so no budget is used up.)""")
a2="(L3) holds in the bare group for the five sorties: **COMPUTED-1** (K19 only; Appendix A)."
assert a2 in new
new=new.replace(a2,"(L3) holds in the bare group for the five sorties: **CHECKED-2** (K19's code and the referee's own code; Appendix A).")
fix['5.1-L1-bullet']=(old,new)
# 5: status 5.1 L3 label
old,new=fix['status-5.1-L1']
a="(L3): COMPUTED-1 (K19 only): in the bare group"
assert a in new
new=new.replace(a,"(L3): CHECKED-2 (K19 and the referee's own code, each written from the definition): in the bare group")
a="The budgets k = 5, 6 (not checked before) equal k = ∞,"
assert a in new
new=new.replace(a,"The budgets k = 5, 6 (not checked before; K19 and the referee agree) equal k = ∞,")
fix['status-5.1-L1']=(old,new)
# extra edit: labels paragraph
fix['labels-kpsolve']=("""kpsolve results (§6) are data, not proofs: a claim that only a kpsolve run supports keeps the label
CONJECTURE, with "kpsolve agrees" (revised after review: R1 item 6).""","""kpsolve results (§6) are data, not proofs: a claim that only a kpsolve run supports keeps the label
CONJECTURE (for a statement over all contexts) or COMPUTED-1 (for the finite computation itself), with
"kpsolve agrees" (revised after review: R1 item 6; after K19, 2026-10-27: CHECKED-2 needs a second, independently
written implementation, and a second run of the same code or of a build derived from it does not count).""")
out=["# Corrected EDIT blocks (K19 referee, VERIFY.md). Use these in place of the K19 blocks with the same label; all other K19 blocks stand. OLD occurs exactly once in the current LOOPY.md.\n"]
for lab in ['5.1-black-moves','status-5.5','5.5-escape','5.1-L1-bullet','status-5.1-L1','labels-kpsolve']:
    o,n=fix[lab]
    assert L.count(o)==1,lab
    out.append(f"### EDIT {lab}\n<<<<<<< OLD\n{o}\n=======\n{n}\n>>>>>>> NEW\n")
open('EDITS_FIXED.md','w').write('\n'.join(out))
print('ok')
# validate that all (K19 blocks minus replaced + fixed) apply sequentially
cur=L
final=dict((l,(o,n)) for l,o,n in blocks); final.update(fix)
for lab,(o,n) in final.items():
    assert cur.count(o)==1,(lab,cur.count(o)); cur=cur.replace(o,n)
print('all',len(final),'apply in sequence')
