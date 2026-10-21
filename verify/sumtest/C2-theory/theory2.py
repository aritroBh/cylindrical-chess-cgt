"""Theory-lens checks for claim C2 (second pass, 2026-10-16).

Run:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C2-theory/theory2.py

T1  options of G under cylcgt (textbook test) and how they reduce to *2 = {0,*|0,*}
T2  robustness of the value to the size of BIG (independent model, indep.py)
T3  robustness to variants of the "count" race rule (no double-step credit; ties to the mover)
T4  *2's outcome vector recomputed with cgt (canonical forms), not with sumsolver trees
T5  what a single real-chess root outcome can and cannot discriminate
"""
import sys
from functools import lru_cache

sys.path.insert(0, "verify/sumtest/C2-theory")
import indep  # noqa: E402  (third independent pawn model, does not import cylcgt.pawns)
from cylcgt import cgt, pawns  # noqa: E402

POS = "W: a2 c2 / B: b7 d7"
S2 = cgt.nimber(2)


def eq(a, b):
    return cgt.le(a, b) and cgt.le(b, a)


def t1():
    print("== T1: options of G under cylcgt (textbook passed test)")
    for rule in ("count", "opponent"):
        for ep in (False, True):
            pawns.RACE_RULE = rule
            pawns._value.cache_clear()
            b = pawns.Board(4, 8, False, ep)
            p = pawns.Pos.parse(POS)
            Lv = [(str(c), cgt.show(pawns._child(b, c, "W"))) for c in pawns.moves(b, p, "W")]
            Rv = [(str(c), cgt.show(pawns._child(b, c, "B"))) for c in pawns.moves(b, p, "B")]
            g = pawns.value(b, p)
            print(f"  {rule:8s} ep={'on ' if ep else 'off'} G = {cgt.show(g)}")
            for s, v in Lv:
                print(f"     L-> {s:34s} {v}")
            for s, v in Rv:
                print(f"     R-> {s:34s} {v}")


def canon(m, root):
    @lru_cache(maxsize=None)
    def val(st, mover):
        d = m.resolve(st, mover)
        if d is not None:
            return cgt.integer(d)
        L = [val(c, "W") for c in m.moves(m.strip_ep_for(st, "W"), "W")]
        R = [val(c, "B") for c in m.moves(m.strip_ep_for(st, "B"), "B")]
        return cgt.make(L, R)
    return val(root, None)


ROOT = (indep.sqs("a2 c2"), indep.sqs("b7 d7"), None)
SETTINGS = ((False, False, "ep off"), (True, False, "ep on, textbook"), (True, True, "ep on, ep-aware"))


def t2():
    print("== T2: value as a function of BIG (independent model)")
    saved = indep.BIG
    for big in (4, 8, 16, 32, 64, 256, 1024, 4096):
        indep.BIG = big
        row = []
        for race in ("count", "mover", "opponent"):
            for ep, aware, lab in SETTINGS:
                row.append(f"{race}/{lab}: {cgt.show(canon(indep.Model(ep, aware, race), ROOT))}")
        print(f"  BIG={big:5d} | " + " | ".join(row))
    indep.BIG = saved


class TieToMover(indep.Model):
    """count rule, but a tie in moves-to-promote goes to the side that just moved."""

    def resolve(self, st, mover):
        if self.race == "count" and self.passed(st, "W") and self.passed(st, "B"):
            opp = "B" if mover == "W" else "W"
            win = opp if self.dist(st, opp) < self.dist(st, mover) else mover
            return indep.BIG if win == "W" else -indep.BIG
        return super().resolve(st, mover)


def t3():
    print("== T3: variants of the count race rule (independent model)")
    for ep, aware, lab in SETTINGS:
        a = canon(indep.Model(ep, aware, "count", credit=False), ROOT)
        b = canon(TieToMover(ep, aware, "count"), ROOT)
        c = canon(TieToMover(ep, aware, "count", credit=False), ROOT)
        print(f"  {lab:16s} no double-step credit: {cgt.show(a):22s} ties->mover: {cgt.show(b):22s} both: {cgt.show(c)}")


def t4():
    print("== T4: outcome vector of *2 + X from cgt canonical forms")
    z, s = cgt.integer(0), cgt.nimber(1)
    up = cgt.make([z], [s])
    down = cgt.neg(up)
    upstar = cgt.add(up, s)
    dupstar = cgt.add(cgt.add(up, up), s)
    half = cgt.make([z], [cgt.integer(1)])
    one, m1 = cgt.integer(1), cgt.integer(-1)
    sw10 = cgt.make([one], [z])
    pm1 = cgt.make([one], [m1])
    tiny1 = cgt.make([z], [cgt.make([z], [m1])])
    ref = [("0", z), ("*", s), ("*2", S2), ("*3", cgt.nimber(3)), ("up", up), ("down", down),
           ("up*", upstar), ("dup*", dupstar), ("1/2", half), ("-1/2", cgt.neg(half)), ("1", one),
           ("-1", m1), ("{1|0}", sw10), ("+-1", pm1), ("tiny1", tiny1)]
    vec = "".join(cgt.outcome(cgt.add(S2, x)) for _, x in ref)
    print("  reference:", " ".join(n for n, _ in ref))
    print("  *2 + X   :", vec, "(worker: NNPNLRLLLRLRLNN)", "MATCH" if vec == "NNPNLRLLLRLRLNN" else "MISMATCH")
    return ref


def t5(ref):
    print("== T5: which hypotheses a root outcome (no sum partner) can separate")
    z = cgt.integer(0)
    two_pm1 = cgt.make([cgt.integer(3)], [cgt.integer(1)])
    aware_val = cgt.make([two_pm1], [cgt.neg(two_pm1)])  # {2+-1 | -2+-1}
    cands = [("*2", S2), ("*", cgt.nimber(1)), ("*3", cgt.nimber(3)), ("0", z),
             ("{2±1|-2±1}", aware_val), ("±1", cgt.make([cgt.integer(1)], [cgt.integer(-1)]))]
    print("  check {2±1|-2±1} built here:", cgt.show(aware_val), "mean", cgt.mean(aware_val),
          "temp", cgt.temperature(aware_val))
    for n, g in cands:
        print(f"  {n:12s} outcome alone: {cgt.outcome(g)}   outcome +*: {cgt.outcome(cgt.add(g, cgt.nimber(1)))}"
              f"   outcome +*2: {cgt.outcome(cgt.add(g, S2))}")


if __name__ == "__main__":
    t1()
    t2()
    t3()
    ref = t4()
    t5(ref)
