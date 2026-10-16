"""Temperature of every 'hot-BIG' / 'decided' value in cgt_verified.epd (uses cylcgt read-only).
    cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/engines/C4-reproduce/hot_check.py
"""
import collections, json, os
from cylcgt import cgt, pawns
ROOT = os.getcwd()
res = json.load(open(os.path.join(ROOT, "engine/suite/results.json")))
ver = {" ".join(l.split()[:4]) for l in open(os.path.join(ROOT, "engine/suite/cgt_verified.epd")) if l.strip()}
B4 = pawns.Board(4, 8, False, True)
pawns.RACE_RULE = "count"; pawns._value.cache_clear()
out = collections.Counter()
for r in res:
    if " ".join(r["fen"].split()[:4]) not in ver or r["features"]["class"] not in ("hot-BIG", "decided"):
        continue
    w, b = r["component"].split("/")
    pos = pawns.Pos.parse(r["component"].split(" (ep")[0])
    if "(ep" in r["component"]:
        print("ep component", r["component"])
    g = pawns.value(B4, pos)
    assert cgt.show(g) == r["value"]["count"], (cgt.show(g), r["value"]["count"])
    t = cgt.temperature(g)
    out[(r["features"]["class"], r["value"]["count"], "number" if t is None else str(t))] += 1
for k, v in sorted(out.items()):
    print(v, k)
