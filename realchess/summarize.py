"""Offline summary of every realchess result (no network).

    PYTHONPATH=. .venv/bin/python -m realchess.summarize [--component "W: a2 c2 / B: b7 d7"]

Writes results/<tag>_summary.json with: request ledger by stage, every
category seen in the records this workstream fetched (50-move-rule cases),
race terminals vs each RACE_RULE, and the per-node comparison table.
"""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter

from cylcgt import pawns
from cylcgt.pawns import Pos

from . import component as C
from .probe import Prober, DEFAULT_LEDGER
from .solve_candidate import RESULTS, tag_of, write_json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", default="W: a2 c2 / B: b7 d7")
    ap.add_argument("--ledger", default=DEFAULT_LEDGER)
    a = ap.parse_args()
    comp = Pos.parse(a.component)
    tag = tag_of(comp)
    out = {"component": str(comp)}
    # ledger
    rows = [json.loads(l) for l in open(a.ledger) if l.strip()]
    out["ledger_total"] = len(rows)
    out["ledger_by_tag"] = dict(Counter(r["tag"] for r in rows))
    out["ledger_by_status"] = dict(Counter(str(r["status"]) for r in rows))
    # categories in every record fetched by this ledger
    pr = Prober(0, a.ledger, offline=True)
    cats, special = Counter(), []
    for f in sorted({r["fen"] for r in rows}):
        rec = pr.cached(f)
        if not rec or not rec.get("data"):
            continue
        d = rec["data"]
        cats["root:" + str(d.get("category"))] += 1
        for m in d.get("moves", []):
            c = m.get("category")
            cats["move:" + str(c)] += 1
            if c in ("cursed-win", "blessed-loss", "maybe-win", "maybe-loss"):
                special.append((f, m["uci"], c))
        if d.get("category") in ("cursed-win", "blessed-loss", "maybe-win", "maybe-loss"):
            special.append((f, "root", d.get("category")))
    out["categories_in_fetched_records"] = dict(cats)
    out["fifty_move_rule_categories"] = special
    # races
    p = os.path.join(RESULTS, f"{tag}_oracle_pure.json")
    if os.path.exists(p):
        o = json.load(open(p))
        races = [r for r in o["terminals"] if r["race"] and r["real_class"]]
        agree = Counter()
        for r in races:
            for rule, cl in r["model_by_rule"].items():
                if cl == [r["real_class"]]:
                    agree[rule] += 1
        out["race_terminals_resolved"] = len(races)
        out["race_terminals_agreeing_with_rule"] = dict(agree)
        out["race_terminals"] = [{k: r[k] for k in ("terminal", "men", "entered_by", "real_W_first",
                                                    "real_B_first", "real_class", "model_by_rule")}
                                 for r in races]
        allr = [r for r in o["terminals"] if r["real_class"]]
        out["terminals_resolved"] = len(allr)
        out["terminals_agreeing_with_rule"] = {
            rule: sum(1 for r in allr if r["model_by_rule"][rule] == [r["real_class"]])
            for rule in ("count", "mover", "opponent")}
    p = os.path.join(RESULTS, f"{tag}_nodes_pure.json")
    if os.path.exists(p):
        n = json.load(open(p))
        out["nodes_class_counts"] = n.get("class_counts")
        out["nodes_agreement_with_rule"] = n.get("agreement_with_rule")
        resolved = [r for r in n["nodes"] if len(r["real_class"]) == 1]
        out["nodes_fully_resolved"] = len(resolved)
        out["nodes_configs"] = len(n["nodes"])
        dis = []
        for r in resolved:
            if r["model_outcome"]["count"] != r["real_class"]:
                dis.append({"component": r["component"], "real": r["real_class"], "model": r["model_outcome"]})
        out["nodes_disagreeing_with_count"] = dis
        half = Counter()
        for r in n["nodes"]:
            for side, key in (("W", "real_W_first_for_White"), ("B", "real_B_first_for_White")):
                if r[key] != "unresolved":
                    half[side] += 1
        out["nodes_side_results"] = dict(half)
    write_json(os.path.join(RESULTS, f"{tag}_summary.json"), out)
    print(json.dumps({k: v for k, v in out.items() if k not in ("race_terminals", "nodes_disagreeing_with_count")},
                     indent=1))
    print("nodes disagreeing with count model:", len(out.get("nodes_disagreeing_with_count", [])))


if __name__ == "__main__":
    main()
