"""Re-check, two ways, every terminal side in the support of a certificate
(certify_check.py output):
  (a) realchess.search.Searcher WITHOUT Lichess 8-man categories (exact
      tablebase only at <= 7 men; probes allowed within --max-new);
  (b) realchess.verify_proof.Prover: an independent AND/OR prover that reads
      cached records only (<= 7-man leaves) and writes an explicit proof tree.

    PYTHONPATH=. .venv/bin/python -m realchess.certify.verify_sides <cert.json> --test lower --max-new 40
"""
from __future__ import annotations

import argparse
import json
import sys

from realchess import movegen as mg
from realchess.verify_proof import Prover, stats

from . import infra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("--test", default="lower")
    ap.add_argument("--cap", type=int, default=1200)
    ap.add_argument("--max-new", type=int, default=40)
    ap.add_argument("--ext", type=int, default=6)
    ap.add_argument("--depth", type=int, default=30)
    ap.add_argument("--out", default=None)
    ap.add_argument("--store", action="store_true", help="append the l8-free search results to realdb.jsonl")
    a = ap.parse_args()
    sys.setrecursionlimit(1000000)
    from realchess.solve_candidate import Model, RealOracle, deepen, is_model_internal, make_order
    from realchess.search import Searcher
    d = json.load(open(a.cert))
    sup = d["tests"][a.test]["support"]
    pr = infra.CertProber(a.cap, tag="certify-verify")
    oracle = RealOracle(pr, a.max_new)
    model = Model()
    region = lambda pos: "model" if is_model_internal(pos, model) else "off"
    s = Searcher(oracle, order_hint=make_order(model, pr.cached), region=region, cached=pr.cached, kb=infra.kb())
    s.kb_max_men = 7
    P = Prover(kb=infra.kb())
    P.pr = infra.CertProber(0, offline=True)
    rows = []
    for e in sup:
        want_white = 1 if e["class"] == "L" else -1
        for side in "WB":
            fen = e["fen_" + side]
            pos = mg.parse_fen(fen)
            want_stm = want_white if pos.stm == mg.WHITE else -want_white
            try:
                iv = s.search(pos, 0) if pos.men() <= 7 else deepen(s, pos, a.ext)
            except Exception as ex:  # budget
                iv = (-1, 1)
                print("search stopped:", repr(ex), flush=True)
            claim = "win" if want_stm == 1 else "loss"
            cert = P.prove(pos, claim, a.depth)
            row = {"terminal": e["terminal"], "side": side, "fen": fen, "men": pos.men(), "claim_stm": claim,
                   "search_no_l8": list(iv), "search_agrees": iv[0] == iv[1] == want_stm,
                   "prover_proved": cert is not None, "prover_stats": stats(cert) if cert else None}
            rows.append(row)
            if row["search_agrees"] and a.store:
                from . import termdb
                r = termdb.make_row(pos, iv, ("tablebase (<=7 men)" if pos.men() <= 7 else
                                              f"search ({pos.men()} men, ext<={a.ext})") + ", no Lichess 8-man categories",
                                    a.ext)
                r.update(terminal=e["terminal"], side=side, source="verify_sides", l8=False)
                termdb.append([r])
            print(json.dumps(row), flush=True)
    out = {"cert": a.cert, "test": a.test, "rows": rows,
           "all_search_agree": all(r["search_agrees"] for r in rows),
           "all_prover_proved": all(r["prover_proved"] for r in rows),
           "new_requests": oracle.new_requests, "ledger": pr.ledger_count()}
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(out, fh, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}))


if __name__ == "__main__":
    main()
