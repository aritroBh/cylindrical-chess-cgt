"""Non-decisive cross-check: are my (indep.py) values the same games as cylcgt's?

For the 418 library components, root and every child, in every setting that
the given cylcgt supports (main: textbook only; ep-wt: both tests).
cylcgt games are converted to indep.G by rebuilding them with indep.make.

  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<cylcgt root> .venv/bin/python verify/bench/C2-refute/xcheck_cylcgt.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import indep as I  # noqa: E402
from cylcgt import pawns  # noqa: E402
from cylcgt.pawns import Board, Pos  # noqa: E402

ROOT = HERE.parents[2]
_conv = {}


def conv(g):
    r = _conv.get(g.id)
    if r is None:
        r = I.number(g.num) if g.num is not None else I.make([conv(x) for x in g.L], [conv(x) for x in g.R])
        _conv[g.id] = r
    return r


rows = [json.loads(x) for x in (ROOT / "bench/data/components.jsonl").read_text().splitlines()]
has_flag = hasattr(pawns, "PASSED_RESPECTS_EP")
tests = (False, True) if has_flag else (False,)
out = {"cylcgt": pawns.__file__}
for aware in tests:
    if has_flag:
        pawns.PASSED_RESPECTS_EP = aware
    for rule in ("count", "mover", "opponent"):
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        for ep in (True, False):
            bad = 0
            n = 0
            for r in rows:
                w = r["width"]
                p = Pos.parse(r["position"])
                b = Board(w, 8, False, ep)
                mine_root, mine_kids = I.Solver(w, aware, rule, ep).root_and_children(I.parse(r["position"]))
                g = conv(pawns.value(b, p))
                n += 1
                if g is not mine_root:
                    bad += 1
                for side in "WB":
                    for c in pawns.moves(b, p, side):
                        n += 1
                        if conv(pawns._child(b, c, side)) is not mine_kids[(side, c.white, c.black)]:
                            bad += 1
            out[f"{'aware' if aware else 'textbook'}/{rule}/ep-{'on' if ep else 'off'}"] = f"{n - bad}/{n} agree"
print(json.dumps(out, indent=1))
