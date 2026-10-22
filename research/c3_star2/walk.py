"""T33 walk-through: move tables, reversibility/domination and setting checks.

Run from the project root:
    PYTHONPATH=. .venv/bin/python research/c3_star2/walk.py
Prints every value used in REPORT.md (appendix).
"""
from cylcgt import pawns, cgt

RACE_OPTS = ("count", "mover", "opponent")


def setup(race="count", passed_ep=True):
    pawns.RACE_RULE = race
    pawns.PASSED_RESPECTS_EP = passed_ep
    pawns._value.cache_clear()


def val(B, pos, mover):
    """Value of the option reached by `mover` (engine's own accounting)."""
    return pawns._child(B, pos, mover)


def root_value(B, P):
    return pawns.value(B, P)


def fmt_pos(p):
    s = str(p)
    return s


def fmt_val(g):
    return cgt.show(g)


def walk(B, P, label):
    G = root_value(B, P)
    print(f"=== {label}: root {P} on {B.files}x{B.ranks} wrap={B.wrap} ep={B.ep}")
    print(f"root value = {fmt_val(G)}  outcome={cgt.outcome(G)}  canonical L={[fmt_val(x) for x in G.L]} R={[fmt_val(x) for x in G.R]}")
    print(f"ZERO={cgt.ZERO is G}  STAR={cgt.STAR is G}")
    for side in ("W", "B"):
        print(f"--- {side} to move at root: {len(pawns.moves(B, P, side))} moves")
        opts = pawns.moves(B, P, side)
        vals = []
        for i, c in enumerate(opts, 1):
            v = val(B, c, side)
            vals.append(v)
            dbl = c.ep is not None
            # reversibility: a reply of the other side whose value reverses
            other = "B" if side == "W" else "W"
            rev = []
            for j, d in enumerate(pawns.moves(B, c, other), 1):
                # other side's reply d: reversing if it is <= G (for Left move) or >= G (for Right move)
                w = val(B, d, other)
                if side == "W" and cgt.le(w, G):
                    rev.append((d, w))
                if side == "B" and cgt.le(G, w):
                    rev.append((d, w))
            print(f"  {side}{i:02d} {c}  -> {fmt_val(v)} [{cgt.outcome(v)}]"
                  + (" [double step, ep right]" if dbl else "")
                  + (f"  reverses via {[str(d) for d, _ in rev]}" if rev else ""))
        # domination among the options of this side (compare option values)
        uniq = {}
        for i, v in enumerate(vals):
            uniq.setdefault(v.id, []).append(i + 1)
        for vid, idxs in uniq.items():
            pass
        for i, vi in enumerate(vals):
            for j, vj in enumerate(vals):
                if i == j or vi is vj:
                    continue
                if side == "W" and cgt.le(vi, vj) and i < j + 1:
                    if not cgt.le(vj, vi) or i < j:
                        print(f"    dominated: W{i+1:02d} ({fmt_val(vi)}) <= W{j+1:02d} ({fmt_val(vj)}) for Left")
                if side == "B" and cgt.le(vj, vi):
                    if not cgt.le(vi, vj) or i < j:
                        print(f"    dominated: B{i+1:02d} ({fmt_val(vi)}) >= B{j+1:02d} ({fmt_val(vj)}) for Right")
    print()
    return G


if __name__ == "__main__":
    import sys
    P3 = pawns.Pos.parse("W: a2 a3 b2 / B: b7 c6 c7")
    P4 = pawns.Pos.parse("W: a4 b2 c2 / B: b6 c5 d6 d7")
    B3 = pawns.Board(3, 8, True, True)
    B4 = pawns.Board(4, 8, True, True)
    setup("count", True)
    walk(B3, P3, "C3 default (count, e.p. on, aware test)")
    walk(B4, P4, "C4 default (count, e.p. on, aware test)")
