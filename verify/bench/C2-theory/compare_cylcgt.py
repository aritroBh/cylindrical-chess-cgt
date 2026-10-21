"""Cross-check indep.py against cylcgt on the 418 library components (and the KEY-FACT position).

For each component: root and child values with indep.py (textbook test; count rule; e.p. on), and the
cylcgt (main checkout, textbook) game mapped structurally into indep.py's engine. Identical objects mean
the two engines agree on the canonical form. Also checks every child against the library's stored child
list length and the stored outcome.

Run from the project root:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python verify/bench/C2-theory/compare_cylcgt.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import indep as I  # noqa: E402
from cylcgt import pawns  # noqa: E402

LIB = HERE.parents[2] / "bench" / "data" / "components.jsonl"
_map = {}


def conv(g):
    r = _map.get(g.id)
    if r is None:
        r = I.make([conv(x) for x in g.L], [conv(x) for x in g.R])
        _map[g.id] = r
    return r


def to_cyl(p):
    return pawns.Pos(p[0], p[1], None if p[2] is None else None)


def main():
    assert not getattr(pawns, "PASSED_RESPECTS_EP", False), "use the textbook (main) cylcgt"
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()
    bad, n, nk = [], 0, 0
    for line in LIB.read_text().splitlines():
        c = json.loads(line)
        w, p = c["width"], I.parse(c["position"])
        m, root, kids = I.root_and_children(w, p, True, False, "count")
        b = pawns.Board(w, 8, False, True)
        cp = pawns.Pos.parse(c["position"])
        croot = conv(pawns.value(b, cp))
        ok = croot is root and I.outcome(root) == c["outcome"] and len(kids) == len(c["moves"])
        # children: match by resulting pawn sets (e.p. square equivalence checked via moves of cylcgt)
        cyl_kids = {}
        for side in "WB":
            for q in pawns.moves(b, cp, side):
                cyl_kids[(side, q.white, q.black)] = conv(pawns._child(b, q, side))
        for side, q, g in kids:
            nk += 1
            if cyl_kids.get((side, q[0], q[1])) is not g:
                ok = False
        n += 1
        if not ok:
            bad.append(c["comp_id"])
    kf = I.parse("W: a2 c2 / B: b7 d7")
    _, kroot, _ = I.root_and_children(4, kf, True, False, "count")
    kc = conv(pawns.value(pawns.Board(4, 8, False, True), pawns.Pos.parse("W: a2 c2 / B: b7 d7")))
    print(f"components {n}, children {nk}, disagreements {len(bad)} {bad[:10]}")
    print("KEY-FACT indep == cylcgt (textbook, count, e.p. on):", kc is kroot, I.show(kroot))


if __name__ == "__main__":
    main()
