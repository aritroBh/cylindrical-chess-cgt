"""Collect the headline numbers of the A2-realchess workstream into
results/final_summary.json (offline; reads the other results files).

    PYTHONPATH=. .venv/bin/python -m realchess.final_summary [--component "W: a2 c2 / B: b7 d7"]

Every input file must exist (run the stages listed in the report first).
"""
from __future__ import annotations

import glob
import json
import os
from collections import Counter

from .kb import default_kb
from .solve_candidate import RESULTS, write_json

TAG = "comp_Wa2c2_Bb7d7"


def J(name):
    return json.load(open(os.path.join(RESULTS, name)))


def main():
    import argparse
    from cylcgt.pawns import Pos
    from .solve_candidate import tag_of
    global TAG
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", default="W: a2 c2 / B: b7 d7")
    a = ap.parse_args()
    TAG = tag_of(Pos.parse(a.component))
    out = {"component": a.component}
    led = [json.loads(l) for l in open(os.path.join(os.path.dirname(RESULTS), "logs", "ledger.jsonl"))]
    out["requests"] = {"ledger_total": len(led), "cap": 1200, "by_tag": dict(Counter(r["tag"] for r in led)),
                       "by_status": dict(Counter(str(r["status"]) for r in led))}
    kb = default_kb()
    out["knowledge_base"] = kb.stats()
    mv = J("movegen_validation.json")["summary"]
    out["movegen_validation"] = {k: mv[k] for k in ("positions", "http_200", "exact_match")}
    mvals = J(f"{TAG}_model_values.json")
    out["model_values"] = {conv: {k: v["value"] for k, v in mvals[conv]["values"].items()}
                           for conv in ("textbook", "ep_aware")}
    out["model_values"]["control_matches_textbook"] = mvals["control_matches_textbook"]
    out["model_values"]["benchmark_eligible"] = mvals["benchmark_eligible"]
    roots = J(f"{TAG}_roots_pure.json")
    out["roots"] = {"W_to_move": roots["roots"]["W"]["result"], "B_to_move": roots["roots"]["B"]["result"],
                    "real_outcome_class": roots["real_outcome_class"],
                    "certificates": {s: J(f"cert_root_{s}.json")["summary"] for s in "wb"}}
    for conv in ("textbook", "epaware"):
        rt = J(f"{TAG}_root_table_{conv}.json")
        out["roots"]["move_table_" + conv] = {
            stm: [(m["move"], m["real_result_for_mover"], m.get("model_child_value", {}).get("count", m.get("model")))
                  for m in r["moves"]] for stm, r in rt["roots"].items()}
    kr = J(f"{TAG}_kings_pure_root.json")
    out["roots"]["king_moves"] = [(r["fen"].split()[1], r["king_move"], r["verdict"], r["refutation"]) for r in kr["rows"]]
    nodes = J(f"{TAG}_nodes_pure_offline.json")
    out["nodes"] = {k: nodes[k] for k in ("targets", "targets_done", "ext", "class_counts")}
    cmp_ = J(f"{TAG}_nodes_vs_model_offline.json")
    out["nodes"]["positions_with_real_result"] = cmp_["positions_with_real_result"]
    out["nodes"]["real_results"] = cmp_["real_results"]
    for conv in ("textbook", "e.p.-aware"):
        out["nodes"]["vs_model_" + conv] = {
            "per_position": {r: cmp_[conv][r]["tally"] for r in ("count", "mover", "opponent")},
            "per_configuration": {k: v for k, v in cmp_[conv]["configurations"].items() if k != "rows"}}
    ver = J(f"{TAG}_nodes_verified_offline.json")
    out["nodes"]["independent_prover"] = ver["tally"]
    out["nodes"]["vs_lichess_8man_category"] = ver["vs_lichess_8man_category"]
    kg = J(f"{TAG}_kings_pure_offline.json")
    out["king_audit"] = {"nodes": kg["nodes"], "king_moves": kg["king_moves"], "tally": kg["tally"],
                         "non_losing": [(r["fen"], r["king_move"], r["verdict"]) for r in kg["non_losing"]]}
    out["oracle"] = {}
    for lab in ("_textbook_offline", "_epaware_offline", "_epaware_offline_l8"):
        d = J(f"{TAG}_oracleall_pure{lab}.json")
        o = {k: d[k] for k in ("passed_test", "uses_lichess_8man_categories", "internal_nodes", "terminals_total",
                               "sides_resolved", "terminals_resolved_both_sides", "terminals_partial",
                               "terminals_unresolved", "class_counts", "model_values")}
        o["non_LR_terminals"] = [(r["terminal"], r["real_class"]) for r in d["non_LR_terminals"]]
        o["LR_terminals_disagreeing_with_model"] = d["LR_terminals_disagreeing_with_model"]
        o["sandwich"] = {name: {k: v for k, v in b.items() if k.startswith("excludes") and "(how)" not in k
                                and "enumerating" not in k} | {"pinned": b["pinned"]}
                         for name, b in d["bounds"].items()}
        pins = {}
        for f in sorted(glob.glob(os.path.join(RESULTS, f"{TAG}_pin{lab}__*.json"))):
            p = json.load(open(f))
            c = p["certificate"]
            key = p["treatment"]
            if isinstance(c, dict):
                if key in pins and "values" not in pins[key]:
                    del pins[key]  # a superseded "not attempted" run
                agg = pins.setdefault(key, {"cases": 0, "pinned_cases": 0, "values": set(), "lo": set(), "hi": set(),
                                            "essential_open_sides": p["greedy"]["essential_open_sides"]})
                agg["cases"] += c["cases"]
                agg["pinned_cases"] += c["pinned_cases"]
                agg["values"] |= set(c["values_of_pinned_cases"])
                agg["lo"] |= set(c["overall_lower_bound_candidates"])
                agg["hi"] |= set(c["overall_upper_bound_candidates"])
            elif key not in pins:
                pins[key] = {"not_attempted": c, "essential_open_sides": len(p["greedy"]["essential_open_sides"])}
        for key, agg in pins.items():
            if "values" in agg:
                agg["value_certified"] = (next(iter(agg["values"])) if agg["cases"] == agg["pinned_cases"]
                                          and len(agg["values"]) == 1 else None)
                agg["values"], agg["lo"], agg["hi"] = sorted(agg["values"]), sorted(agg["lo"]), sorted(agg["hi"])
        o["pin_certificates"] = pins
        tv = os.path.join(RESULTS, f"{TAG}_terminals8_verified_{lab.lstrip('_')}.json".replace("__", "_"))
        cand = glob.glob(os.path.join(RESULTS, f"{TAG}_terminals8_verified_pure{lab}.json"))
        if cand:
            v = json.load(open(cand[0]))
            o["terminals8_independent_prover"] = v["tally"]
            o["terminals8_vs_lichess_8man_category"] = v["vs_lichess_8man_category"]
        out["oracle"][lab.strip("_")] = o
    enum_log = os.path.join(RESULTS, f"{TAG}_exclude_star2_textbook_offline.jsonl")
    if os.path.exists(enum_log):
        out["oracle"]["textbook_offline"]["ep_partial_enumeration_certificates"] = [
            json.loads(l) for l in open(enum_log) if l.strip().startswith("{")]
    name = "final_summary.json" if TAG == "comp_Wa2c2_Bb7d7" else f"{TAG}_final_summary.json"
    write_json(os.path.join(RESULTS, name), out)
    print(json.dumps(out, indent=1, default=str)[:20000])


if __name__ == "__main__":
    main()
