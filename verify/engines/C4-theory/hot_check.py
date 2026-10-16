"""Recompute values of verified 'hot-BIG' / 'decided' rows and test hotness with cgt.temperature.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C4-theory/hot_check.py
"""
import collections, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "engine", "suite"))
import build_suite as BS  # noqa
import cgtpos as C  # noqa
from cylcgt import cgt, pawns  # noqa

C.set_rule("count")
rows = json.load(open(BS.RESULTS))
cands = {(r["pos"], r["stm"]): r for r in json.load(open(BS.CANDS))}
ver = [r for r in rows if r["tb_root"] in BS.WINS and r["rules"]["count"]["win_set_agree"]]
BIG = pawns.BIG
seen = {}
tally = collections.Counter()
for r in ver:
    cls = r["features"]["class"]
    rec = cands[(r["component"], r["stm"])]
    pos = BS.rec_pos(rec)
    g = pawns.value(C.B4, pos)
    assert cgt.show(g) == r["value"]["count"], (cgt.show(g), r["value"]["count"])
    key = cgt.show(g)
    if key in seen:
        tally[(cls, seen[key][0])] += 1
        continue
    try:
        t = cgt.temperature(g)
    except Exception as e:  # noqa
        t = f"ERR {e}"
    try:
        m = cgt.mean(g)
    except Exception as e:  # noqa
        m = f"ERR {e}"
    o = cgt.outcome(g)
    # is it BIG + (something infinitesimal/number)?  test g - BIG and g + BIG
    shifted = None
    for s in (BIG, -BIG):
        h = cgt.add(g, cgt.integer(-s))
        if not any(abs(x.num) >= BIG // 2 for x in [h] if x.num is not None):
            pass
    hot = (t is not None) and (not isinstance(t, str)) and t > 0
    ls, rs = cgt.stops(g)
    o = f"{o} stops=({ls},{rs})"
    label = "hot" if hot else "not-hot"
    seen[key] = (label, t, m, o)
    tally[(cls, label)] += 1
    print(f"{cls:14s} {key:60s} temp={t} mean={m} outcome={o} -> {label}")
print()
for k, n in sorted(tally.items()):
    print(k, n)
