"""T20 step 2/4: resolve the decisive terminal sides of a component with the
Lichess tablebase (through realchess.certify.infra.CertProber) and the
realchess searcher (realchess.search.Searcher) -- an implementation that is
independent of kings/kpsolve.

The terminal sides of these components have 8..11 men, so none of them is
directly in the <= 7-man tablebase: an 8-man position is resolved by the
search, with the tablebase at every capture into <= 7 men.

    PYTHONPATH=. .venv/bin/python research/star2_oracle/resolve_tb.py \
        research/star2_oracle/min_support_A.json --max-new 60 --ext 6 \
        --out research/star2_oracle/tb_A.json
"""
import argparse
import json
import os
import time

from cylcgt.pawns import Pos

from realchess import movegen as mg
from realchess.certify.infra import CertProber
from realchess.certify.oracle10 import side_fens
from realchess.oracle_value import Terminals
from realchess.search import Searcher
from realchess.solve_candidate import deepen

HERE = os.path.dirname(os.path.abspath(__file__))

ap = argparse.ArgumentParser()
ap.add_argument("min_support")
ap.add_argument("--max-new", type=int, default=60)
ap.add_argument("--ext", type=int, default=6)
ap.add_argument("--cap", type=int, default=200)
ap.add_argument("--mode", default="pure")
ap.add_argument("--only-men", type=int, default=99, help="only resolve sides of terminals with this many men")
ap.add_argument("--ledger", default=os.path.join(HERE, "ledger.jsonl"))
ap.add_argument("--out", required=True)
a = ap.parse_args()

d = json.load(open(a.min_support))
T = Terminals(Pos.parse(d["component"]))
byname = {str(t): t for t in T.terms}
needed = [byname[x["terminal"]] for x in d["needed_terminals"]]

pr = CertProber(cap=a.cap, ledger=a.ledger, tag="star2_oracle")
import realchess.certify.infra as _infra
s = Searcher(lambda fen: pr.probe(fen), mode=a.mode, kb=_infra.kb())

out = {"component": d["component"], "mode": a.mode, "ext": a.ext, "sides": []}
t0 = time.time()
for t in needed:
    men = T.men(t)
    if men > a.only_men:
        continue
    f = side_fens(T, t)
    for sside in "WB":
        pos = mg.parse_fen(f[sside])
        try:
            iv = deepen(s, pos, a.ext)
        except Exception as e:  # noqa: BLE001
            out["sides"].append({"terminal": str(t), "men": men, "side": sside,
                                 "fen": mg.normal_fen(pos), "error": repr(e)})
            print("ERR", t, sside, repr(e), flush=True)
            continue
        out["sides"].append({"terminal": str(t), "men": men, "side": sside,
                             "fen": mg.normal_fen(pos), "interval": list(iv),
                             "exact": iv[0] == iv[1]})
        print(men, sside, str(t), iv, "new:", pr.requests_this_process, flush=True)
out["new_requests"] = pr.requests_this_process
out["seconds"] = round(time.time() - t0, 1)
out["categories_seen"] = dict(s.cats_seen)
out["special_categories"] = s.special
with open(a.out, "w") as fh:
    json.dump(out, fh, indent=1)
print("wrote", a.out, "new requests", out["new_requests"])
