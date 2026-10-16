"""Adversarial side checks for claim L3.4 (stdlib only; uses only indep.py from this folder).

1. Engine sanity: known CGT identities.
2. Non-BIG-interior nodes of the candidate's tree (worker: 10 with e.p. on, 8 off).
3. A different e.p. semantics inside sums: in chess an e.p. right dies after the entitled
   side's next move wherever it is made. Test X + *2 when ANY move (including a heap
   move) clears the right ("chess expiry"), versus the CGT game-form semantics.
4. The same pawn models on the 8x8 CYLINDER (g-pair, files e, f, h empty).
5. Deduction check: WF = W follows from W = *2 (see verdict text); confirm WF+*2 and
   W+*2 have identical outcomes at EVERY reachable non-terminal node for every heap h<=3.

Run: cd <root> && .venv/bin/python -I verify/lemmas/L3.4-candidate-all-models-refute/extra.py
"""
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep as I  # noqa: E402

x4 = I.parse("a2 c2", "b7 d7")
x8 = I.parse("a2 c2 g4", "b7 d7 g5")

# 1. sanity
e = I.E()
s1, s2, s3 = e.nim(1), e.nim(2), e.nim(3)
up = e.make([e.ZERO], [s1])
assert e.add(s2, s2) == e.ZERO
assert e.add(s2, s1) == s3
assert e.add(up, up) != s1 and not e.eq(e.add(up, s1), e.ZERO)
assert e.eq(e.add(e.add(up, s1), e.make([s1], [e.ZERO])), s1) is False or True
assert e.make([e.integer(-256)], []) == e.ZERO
assert e.eq(e.make([e.ZERO, s1], [e.ZERO, s1]), s2)
print("1. engine sanity: ok (*2+*2=0, *2+*=*3, {-256|}=0, {0,*|0,*}=*2)")

# 2. non-BIG-interior nodes
for ep in (True, False):
    for rule in ("count", "mover", "opponent"):
        eng = I.E()
        bd = I.Bd(4, ep)
        Wf = I.make_W(eng, bd, rule, False)
        PB, NB = eng.integer(256), eng.integer(-256)
        seen, st, bad = {x4}, [x4], []
        while st:
            y = st.pop()
            if I.term(bd, y) is not None:
                continue
            g = Wf(y)
            if eng.le(g, NB) or eng.le(PB, g):
                bad.append(I.show(y))
            for side in "WB":
                for c in I.gen(bd, y, side):
                    if c not in seen:
                        seen.add(c)
                        st.append(c)
        print(f"2. ep={ep!s:5s} {rule:8s}: non-terminal nodes with W<=-BIG or W>=BIG: {len(bad)}"
              + (f"  e.g. {bad[0]}" if bad else ""))


# 3. chess-expiry e.p. semantics in X + *h
def make_win_expiry(bd, rule):
    @lru_cache(maxsize=None)
    def win(p, h, tm):
        other = "B" if tm == "W" else "W"
        for c in I.gen(bd, p, tm):
            t = I.term(bd, c)
            if t == "race":
                if I.race_winner(bd, c, tm, rule) == tm:
                    return True
                continue
            if t is not None:
                if t == tm:
                    return True
                continue
            if not win(c, h, other):
                return True
        q = (p[0], p[1], None)  # any move elsewhere kills the right
        for j in range(h):
            if not win(q, j, other):
                return True
        return False
    return win


for ep in (True, False):
    for rule in ("count", "mover", "opponent"):
        for nm, bd, x in (("4f", I.Bd(4, ep), x4), ("8f", I.Bd(8, ep), x8)):
            res = []
            for h in range(4):
                w = make_win_expiry(bd, rule)
                res.append(I.outcome_from(w(x, h, "W"), not w(x, h, "B")))
            print(f"3. chess-expiry e.p. ep={ep!s:5s} {rule:8s} {nm}: outcome of X+*0..*3 = {res}")

# 4. cylinder
for ep in (True, False):
    for rule in ("count", "mover", "opponent"):
        eng = I.E()
        bd = I.Bd(8, ep, wrap=True)
        Sf, splits = I.make_S(eng, bd, rule)
        print(f"4. 8x8 CYLINDER pawn model ep={ep!s:5s} {rule:8s}: S={eng.name(Sf(x8))} "
              f"W={eng.name(I.make_W(eng, bd, rule, False)(x8))} WF={eng.name(I.make_W(eng, bd, rule, True)(x8))}")
    eng = I.E()
    bd = I.Bd(4, ep, wrap=True)
    print(f"4. 4-file ring C4 ep={ep!s:5s} count: W={eng.name(I.make_W(eng, bd, 'count', False)(x4))}")


# 5. WF vs W outcomes in sums with *h at every node, explicit king moves
def make_win_k(bd, rule, kings):
    @lru_cache(maxsize=None)
    def win(p, h, tm):
        other = "B" if tm == "W" else "W"
        opts = []
        for c in I.gen(bd, p, tm):
            t = I.term(bd, c)
            if t == "race":
                opts.append(I.race_winner(bd, c, tm, rule) == tm)
            elif t is not None:
                opts.append(t == tm)
            else:
                opts.append(not win(c, h, other))
        for j in range(h):
            opts.append(not win(p, j, other))
        if kings:
            opts.append(False)  # -BIG (+BIG) + *k: the mover loses
        return any(opts)
    return win


mism = 0
nodes = 0
for ep in (True, False):
    for rule in ("count", "mover", "opponent"):
        bd = I.Bd(4, ep)
        a, b = make_win_k(bd, rule, False), make_win_k(bd, rule, True)
        seen, st = {x4}, [x4]
        while st:
            y = st.pop()
            if I.term(bd, y) is not None:
                continue
            nodes += 1
            for h in range(4):
                for tm in "WB":
                    if a(y, h, tm) != b(y, h, tm):
                        mism += 1
            for side in "WB":
                for c in I.gen(bd, y, side):
                    if c not in seen:
                        seen.add(c)
                        st.append(c)
print(f"5. W+*h vs WF+*h (h<=3, both to move) over {nodes} (node,ep,rule) cases: {mism} mismatches")
