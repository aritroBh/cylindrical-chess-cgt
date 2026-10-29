"""inv1.py -- K30: greatest closed subset of a candidate family of Black-to-move KPK positions (P model)."""
import sys, collections
sys.path.insert(0,'.')
from kpm import *
spec=sys.argv[1]
B=Board(spec)
E=4
def sqn(f,r):  # file index, rank (1-based) -> square, None if off
    if r<1 or r>B.H: return None
    if B.cyl: f%=B.W
    elif f<0 or f>=B.W: return None
    return (r-1)*B.W+f
def family(r):
    out=set()
    for (df,dr) in [(0,-1),(0,-2),(-1,-2),(1,-2)]:
        s=sqn(E+df,r+dr)
        if s is not None: out.add(s)
    return out
cand=set()
for r in range(2,8):
    ps=sqn(E,r)
    for wk in family(r):
        for bk in range(B.N):
            pos=norm(B,(1,wk,bk,(),(ps,),-1))
            if legal(B,pos): cand.add(pos)
print(len(cand),'candidate positions')
S=set(cand)
def ok(pos):
    ms=gen(B,pos)
    if not ms: return not in_check(B,pos,1)   # Black stalemated: draw; Black mated impossible
    for lab,k,t in ms:
        if k=='p': return False       # Black promotes
        # White replies
        wms=gen(B,t)
        if not wms:
            if in_check(B,t,0): return False  # White mated
            continue                  # White stalemated: draw
        good=False
        for l2,k2,t2 in wms:
            if k2=='p': continue
            if not t2[4]: good=True;break      # pawn captured
            if t2 in S: good=True;break
        if not good: return False
    return True
changed=True
while changed:
    changed=False
    for pos in list(S):
        if not ok(pos):
            S.discard(pos); changed=True
print(len(S),'in greatest closed subset')
import pickle
pickle.dump(S,open('inv1_%s.pkl'%spec.replace(':','_'),'wb'))
byr=collections.defaultdict(lambda: collections.defaultdict(set))
for pos in S:
    r=B.r(pos[4][0])+1
    byr[r][B.name(pos[1])].add(B.name(pos[2]))
for r in sorted(byr,reverse=True):
    print('pawn rank',r)
    for wk in sorted(byr[r]): print('   WK',wk,'#BK',len(byr[r][wk]), (' '.join(sorted(byr[r][wk])) if len(byr[r][wk])<14 else ''))
