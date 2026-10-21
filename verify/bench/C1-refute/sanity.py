import sys, threading
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/verify/bench/C1-refute')
import indep as I
from fractions import Fraction
def sq(t): return ("abcdefgh".index(t[0]), int(t[1:]))
def P(txt):
    w,b = txt.split('/')
    return (frozenset(sq(x) for x in w.split(':')[1].split()), frozenset(sq(x) for x in b.split(':')[1].split()), None)
def run():
    # engine sanity
    assert I.simplest_between(Fraction(0),Fraction(1))==Fraction(1,2)
    assert I.simplest_between(None,Fraction(-1,2))==-1
    assert I.simplest_between(Fraction(3,4),Fraction(2))==1
    assert I.simplest_between(Fraction(-1,2),Fraction(0))==Fraction(-1,4)
    assert I.add(I.STAR,I.STAR) is I.ZERO
    assert I.add(I.UP,I.DOWN) is I.ZERO
    half=I.number(Fraction(1,2)); assert I.add(half,half) is I.number(1)
    s2 = I.make([I.ZERO,I.STAR],[I.ZERO,I.STAR]); print('*2 =', I.show(s2))
    for aware in (False, True):
        for rule in ("count","mover","opponent"):
            for ep in (True, False):
                m = I.Model(4, ep, aware, rule)
                g = m.value(P("W: a2 c2 / B: b7 d7"))
                print('keyfact', 'aware' if aware else 'textbook', rule, ep, I.show(g), 'is *2' if g is s2 else '')
    for t in ["W: a2 c2 / B: a3 b6", "W: a2 c2 / B: a3 b5", "W: a6 b3 / B: a7 c7", "W: a2 c2 / B: a4 b6"]:
        w = 1+max(f for f,_ in P(t)[0]|P(t)[1])
        for aware in (False, True):
            m = I.Model(w, True, aware, "count")
            print(t, w, 'aware' if aware else 'textbook', I.show(m.value(P(t))))
threading.stack_size(512*1024*1024)
th=threading.Thread(target=run); th.start(); th.join()
