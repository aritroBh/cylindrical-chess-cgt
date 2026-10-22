import sys,random
sys.path.insert(0,'..'); sys.path.insert(0,'.')
sys.path.insert(0,'/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k7')
from kpgen import Board
from lc import Cert
W,H=7,6
B=Board(W,H,True); C=Cert(B,[0,1,2])
random.seed(5)
FZ=[0,1,2]
fzk=[r*W+f for r in range(H) for f in FZ]
found=0
for it in range(400000):
    s=0
    wk=random.choice(fzk); bk=random.choice(fzk)
    # white z pawn on rank index 4 (one move from promotion on rank 5)
    wp=frozenset([4*W+random.choice(FZ)])
    bp=frozenset(random.sample([r*W+f for r in range(1,H-1) for f in FZ],random.choice([1,2])))
    pos=(wk,bk,wp,bp,0,-1)
    occ=[wk,bk]+list(wp)+list(bp)
    if len(set(occ))!=len(occ): continue
    if not B.legal_pos(pos): continue
    if not B.in_check(pos,0): continue
    T=C.L1(pos,False,3)
    if T is not None:
        print(B.to_text(pos),T); found+=1
        if found>=3: break
print('found',found)
