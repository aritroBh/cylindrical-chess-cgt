"""Resolve the open sides of the terminals listed in pinneed/need/iterate
outputs (fields 'needed_terminals' or tests.*.terminals), up to --max-men,
cheapest first; results are appended to realdb.jsonl.

    PYTHONPATH=. .venv/bin/python -m realchess.certify.resolve_list <json> [<json> ...] --max-men 8 \
        --cap 1200 --max-new 60 --per-side 12 --ext 6 [--use-l8]
"""
from __future__ import annotations

import argparse
import json
import sys
import time

from realchess import movegen as mg
from realchess.probe import CapReached

from . import infra, termdb
from .search9 import DeepSearcher


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--max-men", type=int, default=8)
    ap.add_argument("--cap", type=int, default=1200)
    ap.add_argument("--max-new", type=int, default=60)
    ap.add_argument("--per-side", type=int, default=12)
    ap.add_argument("--ext", type=int, default=6)
    ap.add_argument("--use-l8", action="store_true")
    a = ap.parse_args()
    sys.setrecursionlimit(1000000)
    from realchess.solve_candidate import Model, RealOracle, deepen, is_model_internal, make_order
    todo = {}
    for p in a.inputs:
        d = json.load(open(p))
        lst = d.get("needed_terminals") or []
        for test in ("lower", "upper"):
            if isinstance(d.get(test), dict):
                lst += d[test].get("terminals", [])
        for e in lst:
            for s in "WB":
                fen = e["fen_" + s]
                todo.setdefault(fen, (e["terminal"], s, e["men"]))
    db = termdb.load()
    todo = {f: v for f, v in todo.items() if f not in db and v[2] <= a.max_men}
    print(f"[resolve_list] {len(todo)} open sides <= {a.max_men} men", flush=True)
    pr = infra.CertProber(a.cap, tag="certify-resolve-list")
    oracle = RealOracle(pr, a.max_new)
    model = Model()
    region = lambda pos: "model" if is_model_internal(pos, model) else "off"
    s = DeepSearcher(oracle, order_hint=make_order(model, pr.cached), region=region, cached=pr.cached,
                     kb=infra.kb(), max_nodes=4 * 10**6)
    if a.use_l8:
        s.l8, s.kb_max_men = True, 8
    glob = oracle.max_new
    out = []
    try:
        for fen, (term, side, men) in sorted(todo.items(), key=lambda kv: (kv[1][2], kv[0])):
            pos = mg.parse_fen(fen)
            oracle.max_new = min(glob, oracle.new_requests + a.per_side)
            try:
                if pos.men() <= 7:
                    iv, how = s.search(pos, 0), "tablebase (<=7 men)"
                else:
                    iv, how = deepen(s, pos, a.ext), f"search ({pos.men()} men, ext<={a.ext})"
            except CapReached:
                if oracle.new_requests >= glob:
                    raise
                iv, how = (-1, 1), "per-side budget"
            except RuntimeError as e:
                iv, how = (-1, 1), repr(e)
            finally:
                oracle.max_new = glob
            if iv[0] == iv[1]:
                r = termdb.make_row(pos, iv, how + (" [may use Lichess 8-man categories]" if a.use_l8 else ""),
                                    a.ext)
                r.update(terminal=term, side=side, source="resolve_list", l8=bool(a.use_l8))
                termdb.append([r])
                out.append((term, side, men, r["white"]))
            else:
                out.append((term, side, men, None))
            print(json.dumps(out[-1]), flush=True)
    except CapReached:
        print("[resolve_list] --max-new reached", flush=True)
    print(json.dumps({"resolved": sum(1 for x in out if x[3] is not None), "attempted": len(out),
                      "new_requests": oracle.new_requests, "ledger": pr.ledger_count()}))


if __name__ == "__main__":
    main()
