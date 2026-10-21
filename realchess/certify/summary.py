"""Collect the certify workstream's key numbers into results/certify_summary.json
(offline; reads only files under realchess/certify).

    PYTHONPATH=. .venv/bin/python -m realchess.certify.summary
"""
from __future__ import annotations

import json
import os
from collections import Counter

from . import infra

R = infra.RESULTS
CANDS = [("Wa3b3c2_Bb5b7c6", "W: a3 b3 c2 / B: b5 b7 c6"), ("Wa3b2b4_Ba7b6c6", "W: a3 b2 b4 / B: a7 b6 c6"),
         ("Wa3b2c2_Ba4b6c5", "W: a3 b2 c2 / B: a4 b6 c5"), ("Wa5b3c4_Ba6b7c7", "W: a5 b3 c4 / B: a6 b7 c7"),
         ("Wa3b2d3_Ba6c7d6", "W: a3 b2 d3 / B: a6 c7 d6"), ("Wa2c2_Bb7d7", "W: a2 c2 / B: b7 d7")]


def j(name):
    p = os.path.join(R, name)
    return json.load(open(p)) if os.path.exists(p) else None


def main():
    led = [json.loads(l) for l in open(infra.LEDGER)]
    out = {"requests": {"ledger": os.path.relpath(infra.LEDGER, infra.REALCHESS), "total": len(led),
                        "by_tag": dict(Counter(r["tag"] for r in led)),
                        "by_status": dict(Counter(str(r["status"]) for r in led))},
           "realdb_rows": sum(1 for _ in open(os.path.join(R, "realdb.jsonl"))), "candidates": {}}
    sf = j("sf_roots10_movetime60s.json")
    sfmap = {r["fen"]: r for r in sf["results"]} if sf else {}
    for tag, comp in CANDS:
        c = {"component": comp}
        mv = j(f"comp_{tag}_model_values.json")
        if mv:
            c["model_values"] = {conv: {k: v["value"] for k, v in mv[conv]["values"].items()}
                                 for conv in ("textbook", "ep_aware")}
            c["benchmark_eligible"] = mv["benchmark_eligible"]
        tr = j(f"comp_{tag}_tree.json")
        if tr:
            c["tree"] = {conv: {k: o[k] for k in ("internal_nodes", "terminals", "terminals_by_men",
                                                  "race_terminals", "race_terminals_by_men",
                                                  "all_races_free_excludes_star2")}
                         for conv, o in tr.items()}
        rr = j(f"comp_{tag}_races_real.json")
        if rr:
            c["critical_races"] = [{k: e[k] for k in ("terminal", "side_to_move", "men", "ref_winner",
                                                      "count_winner", "real", "fen")} for e in rr["entries"]]
        for conv in ("textbook", "epaware"):
            ce = j(f"comp_{tag}_cert_{conv}_nol8.json") or j(f"comp_{tag}_cert_{conv}.json")
            if ce:
                c[f"certificate_{conv}"] = {t: {k: v for k, v in res.items() if k != "support"}
                                            for t, res in ce["tests"].items()}
                c[f"certificate_{conv}_support"] = ce["tests"]["lower"].get("support")
        for conv in ("tb", "ea"):
            b = j(f"comp_{tag}_bounds_{conv}_v3.json") or j(f"comp_{tag}_bounds_{conv}_v2.json")
            if b:
                c[f"bounds_{conv}"] = {p: {t: {"G_lo": x["G_lo"], "G_hi": x["G_hi"], "excludes *2": x["excludes *2"]}
                                           for t, x in res.items() if t != "fill_stats"}
                                       for p, res in b["policies"].items()}
                c[f"one_sided_real_vs_model_{conv}"] = b["one_sided_real_vs_model"]
        c["engine_roots"] = {f: {"best": r["bestmove"], "score": r["lines"][0]["score"], "depth": r["lines"][0]["depth"]}
                             for f, r in sfmap.items() if f in open(os.path.join(R, "roots10_fens.txt")).read()
                             and any(f == x.strip() for x in open(os.path.join(R, "roots10_fens.txt")))
                             and _match(f, comp)}
        out["candidates"][tag] = c
    rp = j("comp_Wa3b3c2_Bb5b7c6_realproof_Bfirst.json")
    if rp:
        out["candidates"]["Wa3b3c2_Bb5b7c6"]["real_root_proof_attempt"] = {k: v for k, v in rp.items()
                                                                           if k != "leaf_list"}
    sk = j("sf_c2_strategy_kingmoves_5s.json")
    if sk:
        sc = [r["lines"][0]["score"] for r in sk["results"]]
        out["candidates"]["Wa3b3c2_Bb5b7c6"]["engine_king_moves"] = {
            "positions": len(sc), "mate_scores_for_white": sum(1 for s in sc if s.startswith("mate") and int(s.split()[1]) > 0),
            "min_cp_for_white": min(int(s.split()[1]) for s in sc if s.startswith("cp"))}
    with open(os.path.join(R, "certify_summary.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out["requests"], indent=1))


def _match(fen, comp):
    from cylcgt.pawns import Pos
    from realchess import component as C
    from realchess import movegen as mg
    p = Pos.parse(comp)
    return fen in (mg.normal_fen(C.embed(p, "W")), mg.normal_fen(C.embed(p, "B")))


if __name__ == "__main__":
    main()
