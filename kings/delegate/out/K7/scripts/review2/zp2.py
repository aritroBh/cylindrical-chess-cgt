import sys
sys.path.insert(0,'/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k7')
from kpgen import Board
from lc import Cert
exec(open('epchk.py').read().split("Q=parse")[0].split("B=Board")[0])  # imports only
B=Board(7,6,True); C=Cert(B,[0,1,2])
def parse(txt):
    toks=txt.split(); wk=bk=None; wp=set(); bp=set()
    for t in toks[:-2]:
        sq=B.sq(t[1:])
        if t[0]=='K': wk=sq
        elif t[0]=='k': bk=sq
        elif t[0]=='P': wp.add(sq)
        elif t[0]=='p': bp.add(sq)
    return (wk,bk,frozenset(wp),frozenset(bp),0 if toks[-2]=='w' else 1,-1)
Q=parse('Kc1 ka2 Pa5 pb2 w -')
print('in check:',B.in_check(Q,0),'L1 P-only',C.L1(Q,False,4),'L1 safe-queen',C.L1(Q,True,4),'mu ctx',C.mu(Q,False))
print([ (B.fname(m['frm']),B.fname(m['to']),m['kind'],m['promo']) for m in B.moves(Q)])
print('L3s-ish', C.L3(Q,1,False))
