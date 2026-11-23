"""K52 integration: re-check the named positions of the K51/K52 Codex reports.

Run from the repository root:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python kings/delegate/out/K52/integrate/verify.py

Imports cylcgt and lemmas read-only. Own code here: the any-order reach, (E), the
stopped tempo counts, the two threat sets (passer-colour and scored), and a
second whole-board minimax (`wb`) written only on pawns.moves / pawns.passed.
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas import common

assert pawns.BIG == 256 and pawns.PASSED_RESPECTS_EP


def other(s):
    return "B" if s == "W" else "W"


def src(pos, side):
    """Position from which `side` generates moves: a right of the other side lapses."""
    if pos.ep and pos.ep[2] != side:
        return Pos(pos.white, pos.black, None)
    return pos


def passers(board, pos):
    return {s for s in "WB" if pawns.passed(board, pos, s)}


def kids(board, pos):
    for side in "WB":
        for c in pawns.moves(board, src(pos, side), side):
            yield side, c


def race(board, pos, mover, rule):
    if rule == "mover":
        return mover
    if rule == "opponent":
        return other(mover)
    o = other(mover)
    return o if pawns.promote_distance(board, pos, o) <= pawns.promote_distance(board, pos, mover) else mover


def credit(board, pos, mover, rule="count"):
    p = passers(board, pos)
    if not p:
        return None
    if len(p) == 2:
        return race(board, pos, mover, rule)
    return p.pop()


def reach(board, root):
    """Any-order reach, not expanding past a passer (the root is included)."""
    seen, stack = {root}, [root]
    while stack:
        x = stack.pop()
        if passers(board, x):
            continue
        for _, c in kids(board, x):
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def usable(board, pos):
    if not pos.ep:
        return False
    target, victim, capturer = pos.ep
    return any(target in (c.white if capturer == "W" else c.black)
               and victim not in (c.black if capturer == "W" else c.white)
               for c in pawns.moves(board, pos, capturer))


def E_holds(board, root):
    return all(not (usable(board, y) and len(pawns.components(board, y)) > 1)
               for y in reach(board, root) if not passers(board, y))


@lru_cache(maxsize=None)
def tempo(board, pos, side):
    """Stopped tempo count: most `side` moves in an any-order sequence, a final move into a terminal counted."""
    if passers(board, pos):
        return 0
    return max(((m == side) + tempo(board, c, side) for m, c in kids(board, pos)), default=0)


@lru_cache(maxsize=None)
def tau_passer(board, pos):
    p = passers(board, pos)
    if p:
        return frozenset(p)
    out = set()
    for _, c in kids(board, pos):
        out |= tau_passer(board, c)
    return frozenset(out)


@lru_cache(maxsize=None)
def tau_scored(board, pos, rule="count"):
    out = set()
    for m, c in kids(board, pos):
        cr = credit(board, c, m, rule)
        out |= {cr} if cr else tau_scored(board, c, rule)
    return frozenset(out)


def hss(board, root, tau):
    for y in reach(board, root):
        if passers(board, y):
            continue
        ts = [tau(board, c) for c in pawns.components(board, y)]
        if any(i != j and "W" in a and "B" in b for i, a in enumerate(ts) for j, b in enumerate(ts)):
            return False
    return True


def max_tempo(board, root):
    return max(sum(tempo(board, c, s) for c in pawns.components(board, y))
               for y in reach(board, root) if not passers(board, y) for s in "WB")


@lru_cache(maxsize=None)
def wb(board, pos, tm, rule="count"):
    """Whole-board D-game winner with `tm` to move, global flag (second implementation)."""
    for c in pawns.moves(board, src(pos, tm), tm):
        cr = credit(board, c, tm, rule)
        if (cr if cr else wb(board, c, other(tm), rule)) == tm:
            return tm
    return other(tm)


def oc(w_first, b_first):
    return {("W", "W"): "L", ("B", "B"): "R", ("W", "B"): "N", ("B", "W"): "P"}[(w_first, b_first)]


def report(tag, board, x, ep_should_fail=None):
    S = cgt.outcome(pawns.value(board, x))
    W1 = common.alt_outcome(board, x)
    W2 = oc(wb(board, x, "W"), wb(board, x, "B"))
    pf = not passers(board, x)
    h_code = common.hereditarily_safe(board, x)
    h_p, h_s = hss(board, x, tau_passer), hss(board, x, tau_scored)
    e = E_holds(board, x)
    mt = max_tempo(board, x)
    print(f"{tag}: {board} {x}\n   o(S)={S} o(W) alt={W1} own={W2} passer-free={pf} "
          f"HSS code={h_code} passer-tau={h_p} scored-tau={h_s} (E)={e} max tempo={mt} (<256: {mt < 256})")
    for z in pawns.components(board, x):
        print("   component", z, cgt.show(pawns.value(board, z)), "tau_P", sorted(tau_passer(board, z)),
              "tau_scored", sorted(tau_scored(board, z)))
    return S, W1, W2, pf, h_code, h_p, h_s, e, mt


print("== 1. no-(E) witnesses (flat 5x7, after a2-a4, flag for Black on a3)")
b57 = Board(5, 7, False, True)
for text, tm in (("W: a4 b3 e2 / B: a5 b4 e4", None), ("W: a4 b2 b3 e2 e4 / B: a5 b4 b6 e6", "B")):
    p = Pos.parse(text)
    x = Pos(p.white, p.black, ((0, 3), (0, 4), "B"))
    parent = Pos((x.white - {(0, 4)}) | {(0, 2)}, x.black)
    assert x in pawns.moves(b57, parent, "W") and not passers(b57, parent)
    r = report("witness", b57, x)
    assert r[0] != r[1] and r[1] == r[2] and r[3] and r[4] and r[5] and r[6] and not r[7] and r[8] < 256
    print("   Black options in W:", [(str(c), credit(b57, c, "B") or wb(b57, c, "W")) for c in pawns.moves(b57, x, "B")])
    print("   White options in W:", [(str(c), credit(b57, c, "W") or wb(b57, c, "B")) for c in pawns.moves(b57, x, "W")])

print("== 2. M-monotonicity (flat 5x6, e.p. off)")
b56 = Board(5, 6, False, False)
x = Pos.parse("W: a2 a3 c2 d2 d3 e3 / B: a4 b3 d4")
y = Pos.parse("W: a2 a3 b3 d2 d3 e3 / B: a4 d4")
assert y in pawns.moves(b56, x, "W") and not passers(b56, y)
mx = sum(tempo(b56, c, "B") for c in pawns.components(b56, x))
my = [tempo(b56, c, "B") for c in pawns.components(b56, y)]
print(f"   M_B(X)={mx} (components {len(pawns.components(b56, x))}); after c2xb3 components M_B={my}, "
      f"sum {sum(my)}; HSS code={common.hereditarily_safe(b56, x)}")
assert mx == 1 and my == [1, 1]
for c in pawns.components(b56, y):
    print("   daughter", c, "Black moves ->", [(str(d), sorted(passers(b56, d))) for d in pawns.moves(b56, c, "B")])

print("== 3. (HSS) necessity (flat 5x6, e.p. off)")
r = report("no-HSS", b56, Pos.parse("W: a4 d4 / B: b5 e5"))
assert r[0] == "P" and r[1] == "N" and not r[4] and r[7] and r[3]

print("== 4. (B) necessity, B = 1 by hand-built CGT sum; and B = 256 on flat 4x263")
B = 1
ab = cgt.make([cgt.integer(B)], [cgt.integer(-B)])
for n in (0, 1, 2, 3):
    print(f"   B=1, n={n}: o({{1|-1}} - {n}) =", cgt.outcome(cgt.total([ab, cgt.integer(-n)])))
H = 263
bt = Board(4, H, False, False)
x = Pos.parse(f"W: a4 d2 / B: b5 d3 d{B + 260}")
S = cgt.outcome(pawns.value(bt, x))
d = pawns.components(bt, x)
print(f"   flat 4x{H} {x}: components {[cgt.show(pawns.value(bt, c)) for c in d]}, o(S)={S}, "
      f"o(W)={oc(wb(bt, x, 'W'), wb(bt, x, 'B'))}, HSS code={common.hereditarily_safe(bt, x)}, "
      f"M_B(d-comp)={tempo(bt, d[1], 'B')}")

print("== 5. root with both passers (flat 8x8)")
x = Pos.parse("W: a2 / B: h7")
print("   W a2 / B h7: passers", sorted(passers(pawns.FLAT8, x)), "value", cgt.show(pawns.value(pawns.FLAT8, x)))
try:
    pawns._value(pawns.FLAT8, Pos.parse("W: b2 / B: d6"))
    print("   one-component race root: no error")
except pawns.RaceError as e:
    print("   one-component race root W b2 / B d6: RaceError", e)

print("== 6. tau: passer-colour vs scored (flat 8x8, W b2 d6 / B c7)")
x = Pos.parse("W: b2 d6 / B: c7")
print("   tau_P =", sorted(tau_passer(pawns.FLAT8, x)), " tau_scored(count) =", sorted(tau_scored(pawns.FLAT8, x)),
      " common.threats =", sorted(common.threats(pawns.FLAT8, x)))

print("== 7. short boards")
for h, text in ((4, "W: a2 / B: b3"), (5, "W: a2 b2 / B: b4")):
    bb = Board(3, h, False)
    x = Pos.parse(text)
    for c in pawns.moves(bb, x, "W"):
        if (0, 4) in c.white:
            print(f"   H={h} {x} a2-a4 -> {c}: passers {sorted(passers(bb, c))}, credit {credit(bb, c, 'W')}")
            if h == 5:
                for e in pawns.moves(bb, c, "W"):
                    if (0, 5) in e.white:
                        print(f"      then a4-a5 -> {e}: passers {sorted(passers(bb, e))}")
print("done")
