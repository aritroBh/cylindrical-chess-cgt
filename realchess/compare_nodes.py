"""Real-chess results of the 8-man model nodes against cylcgt predictions,
under both passed-pawn conventions (textbook / e.p.-aware), every RACE_RULE.

Input: results/<tag>_nodes_<mode><label>.json (from `solve_candidate nodes`).
For every node FEN whose real result is known, the model predicts "the side
to move wins" iff the component's value (with the e.p. right of the side to
move, if any) is a first-player win for it. Nodes that are terminal under a
convention are scored by the model's terminal verdict. Per configuration
(component, both sides to move) the real outcome class (L/R/N/P/draw) is
compared with the model's outcome class.

    PYTHONPATH=. .venv/bin/python -m realchess.compare_nodes --label _offline

(runs itself once per convention, in a subprocess; see model_values.py)
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RULES = ("count", "mover", "opponent")


def _inner(path):
    from cylcgt import cgt, pawns
    from cylcgt.pawns import Pos
    from . import component as C
    from . import movegen as mg
    from .solve_candidate import Model
    d = json.load(open(path))
    model = Model()
    out = {"cylcgt_file": pawns.__file__,
           "convention": "e.p.-aware" if getattr(pawns, "PASSED_RESPECTS_EP", False) else "textbook",
           "pred": {}}
    for r in d["nodes"]:
        for side in "WB":
            fen = r.get(side + "_fen")
            if not fen:
                continue
            pos = mg.parse_fen(fen)
            p = model.comp(pos)
            row = {"component": str(p), "terminal": C.is_terminal(model.board, p)}
            for rule in RULES:
                row[rule] = model.stm_wins(pos, rule)
                if not row["terminal"]:
                    row["value_" + rule] = cgt.show(model.value(Pos(p.white, p.black, p.ep), rule))
            out["pred"][fen] = row
    print(json.dumps(out))


def _cls(w_first_white, b_first_white):
    if w_first_white is None or b_first_white is None:
        return None
    m = {(1, 1): "L", (-1, -1): "R", (1, -1): "N", (-1, 1): "P"}
    return m.get((w_first_white, b_first_white), "D")


def run(path, epaware_path=None):
    from .model_values import EPAWARE_DEFAULT
    ep_path = epaware_path or os.environ.get("REALCHESS_EPAWARE_PATH", EPAWARE_DEFAULT)
    py = sys.executable

    def sub(cylcgt_root):
        env = dict(os.environ, PYTHONPATH=cylcgt_root + os.pathsep + ROOT)
        r = subprocess.run([py, "-m", "realchess.compare_nodes", "--inner", path], env=env,
                           cwd=cylcgt_root, capture_output=True, text=True, check=True)
        o = json.loads(r.stdout.strip().splitlines()[-1])
        if not os.path.realpath(o["cylcgt_file"]).startswith(os.path.realpath(cylcgt_root)):
            raise RuntimeError("wrong cylcgt imported: " + o["cylcgt_file"])
        return o

    convs = {"textbook": sub(ROOT)}
    if os.path.isdir(os.path.join(ep_path, "cylcgt")):
        convs["e.p.-aware"] = sub(ep_path)
    d = json.load(open(path))
    real = {}
    for r in d["nodes"]:
        for side in "WB":
            fen, iv = r.get(side + "_fen"), r.get(side)
            if fen and iv and iv[0] == iv[1]:
                real[fen] = iv[0]
    out = {"input": os.path.relpath(path, ROOT), "positions_with_real_result": len(real),
           "real_results": dict(Counter({1: "win", 0: "draw", -1: "loss"}[v] for v in real.values()))}
    for conv, o in convs.items():
        res = {}
        for rule in RULES:
            t = Counter()
            bad = []
            for fen, v in real.items():
                pred = o["pred"][fen][rule]
                if pred is None:
                    t["outside model"] += 1
                elif v == 0:
                    t["real draw (model says " + ("win" if pred else "loss") + ")"] += 1
                elif (v == 1) == pred:
                    t["agree"] += 1
                else:
                    t["DISAGREE"] += 1
                    bad.append({"fen": fen, "real_for_stm": v, "model_stm_wins": pred,
                                "component": o["pred"][fen]["component"],
                                "model_value": o["pred"][fen].get("value_" + rule, "terminal")})
            res[rule] = {"tally": dict(t), "disagreements": bad}
        # outcome classes per configuration (both sides to move resolved)
        cfg = {}
        for r in d["nodes"]:
            w, b = r.get("W_fen"), r.get("B_fen")
            if not (w and b and w in real and b in real):
                continue
            rc = _cls(real[w], -real[b])
            mc = {}
            for rule in RULES:
                pw, pb = o["pred"][w][rule], o["pred"][b][rule]
                mc[rule] = None if pw is None or pb is None else \
                    _cls(1 if pw else -1, -1 if pb else 1)
            cfg[r["component"]] = {"real": rc, "model": mc, "fen_W": w, "fen_B": b}
        res["configurations"] = {
            "n": len(cfg),
            "real_classes": dict(Counter(v["real"] for v in cfg.values())),
            "agree": {rule: sum(1 for v in cfg.values() if v["model"][rule] == v["real"]) for rule in RULES},
            "rows": cfg}
        out[conv] = res
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inner", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--component", default="W: a2 c2 / B: b7 d7")
    ap.add_argument("--mode", default="pure")
    ap.add_argument("--label", default="_offline")
    a = ap.parse_args()
    if a.inner:
        _inner(a.inner)
        return
    from cylcgt.pawns import Pos
    from .solve_candidate import RESULTS, tag_of, write_json
    tag = tag_of(Pos.parse(a.component))
    path = os.path.join(RESULTS, f"{tag}_nodes_{a.mode}{a.label}.json")
    out = run(path)
    write_json(os.path.join(RESULTS, f"{tag}_nodes_vs_model{a.label}.json"), out)
    brief = {k: v for k, v in out.items() if k not in ("textbook", "e.p.-aware")}
    for conv in ("textbook", "e.p.-aware"):
        if conv in out:
            brief[conv] = {rule: out[conv][rule]["tally"] for rule in RULES}
            brief[conv]["configurations"] = {k: v for k, v in out[conv]["configurations"].items() if k != "rows"}
    print(json.dumps(brief, indent=1))


if __name__ == "__main__":
    main()
