import sys, time
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames')
import cylcgt.pawns as pawns
from cylcgt.pawns import Board, Pos, value, describe
from cylcgt import cgt

def make_pos(n, phase):
    # core
    W={(0,5),(2,4),(3,4),(5,3)}
    B={(1,7),(3,7),(4,6),(5,6)}
    wr,br = (2,4) if phase=='W2/B4' else (3,5)
    m=(n-6)//2
    for k in range(m):
        f=6+2*k
        W.add((f,wr))
        B.add((f+1,br))
    w=frozenset(W); b=frozenset(B)
    return Pos(w,b)

# monkeypatch components to single component
pawns.components = lambda b, p: [p]

for phase in ['W2/B4','W3/B5']:
    for n in [8,10,12]:
        pos=make_pos(n,phase)
        board=Board(files=n, ranks=8, wrap=True, ep=True)
        t=time.time()
        try:
            g=value(board,pos)
            dt=time.time()-t
            print(f"phase={phase} n={n} value={cgt.show(g)} outcome={cgt.outcome(g)} time={dt:.1f}s")
        except Exception as e:
            dt=time.time()-t
            print(f"phase={phase} n={n} ERROR {e} time={dt:.1f}s")
