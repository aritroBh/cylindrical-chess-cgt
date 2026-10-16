"""Offline re-check of every EPD bm against the raw cached Lichess responses (no network).

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C4-theory/tb_recheck.py
"""
import collections, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.join(ROOT, "engine", "suite"))
import run_suite as RS  # noqa
import tb  # noqa

for name in ("cgt_verified.epd", "cgt_disagree.epd"):
    bad = 0; n = 0; cats = collections.Counter(); roots = collections.Counter(); nmoves = 0
    for line in open(os.path.join(ROOT, "engine", "suite", name)):
        e = RS.parse_epd(line)
        if not e:
            continue
        fen4, ops = e
        rec = tb.lookup(fen4 + " 0 1", allow_network=False)
        assert rec and rec.get("status") == 200, fen4
        d = rec["data"]
        roots[d["category"]] += 1
        win = {m["uci"] for m in d["moves"] if m["category"] in ("loss",)}
        draw = {m["uci"] for m in d["moves"] if m["category"] == "draw"}
        for m in d["moves"]:
            cats[m["category"]] += 1
        nmoves += len(d["moves"])
        bm = set(" ".join(ops["c2"]).split())
        want = win if win else draw
        n += 1
        if bm != want:
            bad += 1
            print("MISMATCH", name, fen4, bm, want)
    print(name, "positions", n, "bm != raw-TB set:", bad, "root categories", dict(roots), "move categories", dict(cats))
