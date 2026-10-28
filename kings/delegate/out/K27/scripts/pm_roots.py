"""pm_roots.py: pm.py's own verdicts: no forced win for the mover (within 25 plies) at any of the 16 roots; every non-shuttle child is a
win for the opponent (minimal plies listed); also no mate/stalemate entry in any certificate."""
import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm, greedy, importlib
roots=[pm.parse(l) for l in open(sys.argv[1]) if l.strip()]
for r in roots:
    w=pm.win(r,25)
    # also: can the side NOT to move win against best play? (pass the move: opponent to move after the shuttle)
    print(pm.show(r),'mover forced win within 25 plies:',w)
SHUT={'Kb2-c3','Kc3-b2','Ka4-b5','Kb5-a4','Kb2-a3','Ka3-b2','Kb5-c4','Kc4-b5'}
mx=0; n=0
for r in roots:
    for lab,q in pm.moves(r):
        if lab in SHUT: continue
        n+=1
        d=pm.dtw(q,31); mx=max(mx,d)
        importlib.reload(greedy); greedy.add(q)
        for x,(l,qq,reps) in greedy.S.items():
            if qq!='PROMO' and not reps: print('MATE/EMPTY ENTRY',pm.show(x))
print('deviations',n,'max plies for the winner (from the child)',mx)
