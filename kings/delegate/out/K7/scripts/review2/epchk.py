import sys
sys.path.insert(0,'/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k7')
from kpgen import Board
from lc import Cert
B=Board(7,6,True); C=Cert(B,[0,1,2])
# parse
import re
def parse(txt):
    toks=txt.split()
    wk=bk=None; wp=set(); bp=set()
    for t in toks[:-2]:
        sq=B.sq(t[1:])
        if t[0]=='K': wk=sq
        elif t[0]=='k': bk=sq
        elif t[0]=='P': wp.add(sq)
        elif t[0]=='p': bp.add(sq)
    stm=0 if toks[-2]=='w' else 1
    ep=-1 if toks[-1]=='-' else B.sq(toks[-1])
    return (wk,bk,frozenset(wp),frozenset(bp),stm,ep)
Q=parse('Kd6 kc4 Pe3 pa4 pe4 pf3 w f4')
print(B.to_text(Q))
print('L1 T (P-only):',C.L1(Q,False,6),' with safe queen:',C.L1(Q,True,6))
print('mu base (no ep):',C.mu(Q,False))
Qn=parse('Kd6 kc4 Pe3 pa4 pe4 pf3 w -')
print('mu base no right:',C.mu(Qn,False), 'L1 no right', C.L1(Qn,False,6))
for T in range(1,6):
    print('T',T,'L3',C.L3(Q,T,False))
import inspect, textwrap, lc
_src=inspect.getsource(Cert.L3)
print(_src)
_src=_src.replace("e = False; a = False\n                    bad.append(('spromo', pos))\n                    continue","continue")
assert "spromo" not in _src
_src=textwrap.dedent(_src).replace("def L3(","def L3s(")
_ns={}
exec(_src,{**lc.__dict__},_ns)
Cert.L3s=_ns['L3s']
for T in range(1,6):
    print('T',T,'L3s',C.L3s(Q,T,False))
