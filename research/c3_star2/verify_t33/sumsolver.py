"""Verifier's sum solver: disjunctive sum of several independent pawn boards plus explicit H nodes.
A board that becomes decided (one-sided passed pawn, or race winner) freezes as a number +-BIG (bank)."""
import sys
from mysolve import Solver, parse, name
sys.setrecursionlimit(100000)

def neg_marker(m, R=8):
    (tf,tr),(vf,vr),cap = m
    return ((tf,R+1-tr),(vf,R+1-vr),"B" if cap=="W" else "W")

def neg(W,B,EP,R=8):
    nW = tuple(sorted((f,R+1-r) for f,r in B))
    nB = tuple(sorted((f,R+1-r) for f,r in W))
    return nW,nB,tuple(sorted(neg_marker(m) for m in EP))

class SumSolver:
    def __init__(self, F, race="count", ep_on=True, aware=True):
        self.S = Solver(F, race, ep_on, aware)
        self.memo = {}
    def wins(self, comps, bank, side):
        if bank != 0:
            return (bank > 0) == (side == "W")
        key = (comps, side)
        v = self.memo.get(key)
        if v is not None: return v
        opp = "B" if side == "W" else "W"
        S = self.S
        res = False
        for i, c in enumerate(comps):
            if c[0] == "G":
                _, W, B, EP = c
                for (nW, nB, nEP) in S.pawn_moves(W, B, EP, side):
                    vd = S.verdict(nW, nB, nEP, side)
                    if vd is not None:
                        nbank = bank + (1 if vd == "W" else -1)
                        newc = comps[:i] + comps[i+1:]
                    else:
                        nbank = bank
                        newc = comps[:i] + (("G", nW, nB, nEP),) + comps[i+1:]
                    if not self.wins(newc, nbank, opp):
                        res = True; break
            else:
                h = c[1]
                Lo, Ro = S.H[h]
                for h2 in (Lo if side == "W" else Ro):
                    newc = comps[:i] + (("H", h2),) + comps[i+1:]
                    if not self.wins(newc, bank, opp):
                        res = True; break
            if res: break
        self.memo[key] = res
        return res
    def G(self, text, ep=()):
        W, B = parse(text)
        return ("G", W, B, tuple(ep))
    def negG(self, text, ep=()):
        W, B = parse(text)
        nW, nB, nEP = neg(W, B, tuple(ep))
        return ("G", nW, nB, nEP)
    def le(self, a_text, b_text, a_ep=(), b_ep=()):
        """a <= b  iff  b - a >= 0 iff Left wins (b + (-a)) moving second."""
        comps = (self.G(b_text, b_ep), self.negG(a_text, a_ep))
        return not self.wins(comps, 0, "B")
    def ge(self, a, b, **kw): return self.le(b, a, **kw)
    def le_H(self, a_text, h, a_ep=()):
        """a <= H (node)"""
        return not self.wins((("H", h), self.negG(a_text, a_ep)), 0, "B")
    def ge_H(self, a_text, h, a_ep=()):
        """a >= H: Right moving second loses in a + (-H): equivalently a - H >= 0.  Use H' = -H via explicit DAG instead."""
        raise NotImplementedError
    def outcome(self, text, ep=(), h=None):
        S = self.S
        if h is None: h = S.zero()
        return S.outcome_with(*(lambda W,B: (W,B,tuple(ep),h))(*parse(text)))
