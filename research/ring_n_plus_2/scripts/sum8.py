import sys, time
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames')
from cylcgt.pawns import Board, Pos, value, describe
from cylcgt import cgt
def make_pos(n, phase):
    W={(0,5),(2,4),(3,4),(5,3)}
    B={(1,7),(3,7),(4,6),(5,6)}
    wr,br = (2,4) if phase=='W2/B4' else (3,5)
    m=(n-6)//2
    for k in range(m):
        f=6+2*k
        W.add((f,wr)); B.add((f+1,br))
    return Pos(frozenset(W),frozenset(B))
phase='W2/B4'; n=8
pos=make_pos(n,phase)
board=Board(files=n, ranks=8, wrap=True, ep=True)
t=time.time()
g=value(board,pos)  # default components
print(f"sum-model phase={phase} n={n} value={cgt.show(g)} outcome={cgt.outcome(g)} time={time.time()-t:.1f}s", flush=True)
