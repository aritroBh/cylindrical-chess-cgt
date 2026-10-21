#!/usr/bin/env python3
"""Experiments E5/E6 for Lc0: what do the policy and value heads say before any search?

Uses the 275 tablebase-probed positions and their side-to-move twins from
engine/experiments/results/static_eval.json (run static_eval.py first). For every FEN, Lc0 is asked
`go nodes N` (default N = 1, i.e. one network evaluation of the root: the move is the policy head's
choice and the score is the value head's). Scores are converted to White's point of view.

Run from the project root (Homebrew lc0 0.32.1, bundled net, default options):
    PYTHONPATH=. .venv/bin/python engine/experiments/lc0_value.py --engine /opt/homebrew/bin/lc0 --nodes 1
Writes engine/experiments/results/lc0_value_n<N>.json and prints tables like static_eval.py, plus the
policy check (is the chosen move a tablebase win; is it a king move).
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from run_suite import Engine  # noqa: E402

SUITE = HERE.parent / "suite" / "results.json"


def cp_of(score):
    if score is None:
        return None
    kind, v = score.split()
    v = int(v)
    if kind == "mate":
        return 100000 if v > 0 else -100000
    return v


def query(eng, fen, nodes, timeout):
    eng.send("ucinewgame")
    eng.ready()
    eng.send(f"position fen {fen}")
    eng.send(f"go nodes {nodes}")
    score, best = None, None
    for line in eng.until("bestmove", timeout=timeout):
        t = line.split()
        if t and t[0] == "info" and "score" in t:
            i = t.index("score")
            score = f"{t[i+1]} {t[i+2]}"
        if line.startswith("bestmove"):
            best = t[1]
    return best, score


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine")
    ap.add_argument("--nodes", type=int, default=1)
    ap.add_argument("--timeout", type=float, default=120)
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()
    out = HERE / "results" / f"lc0_value_n{a.nodes}.json"
    if not a.summary:
        rows = json.loads((HERE / "results" / "static_eval.json").read_text())["rows"]
        tb = {r["id"]: r for r in json.loads(SUITE.read_text())}
        eng = Engine(a.engine, {}, timeout=a.timeout)
        for r in rows:
            for key, fen in (("orig", r["fen"]), ("twin", r["twin"])):
                best, score = query(eng, fen, a.nodes, a.timeout)
                stm_white = fen.split()[1] == "w"
                cp = cp_of(score)
                r[f"lc0_{key}_best"] = best
                r[f"lc0_{key}_white_cp"] = None if cp is None else (cp if stm_white else -cp)
            r["tb_moves"] = tb[r["id"]]["tb_moves"]
            r["king_moves"] = tb[r["id"]]["king_moves"]
        engine_name = eng.name
        eng.quit()
        out.write_text(json.dumps({"engine": engine_name, "nodes": a.nodes, "rows": rows}, indent=0))
    d = json.loads(out.read_text())
    summarize(d["rows"], d["engine"], d["nodes"])


def summarize(rows, name, nodes):
    print(f"engine {name}; go nodes {nodes}; {len(rows)} positions + twins")
    print("\n## Value head sign vs tablebase root (originals; draws excluded)")
    print("| group | n | TB root = win | value sign right |")
    print("|---|---|---|---|")
    groups = defaultdict(list)
    for r in rows:
        if r["tb_root"] in ("win", "loss"):
            groups["all"].append(r)
            groups["tempo-sensitive (N/P)" if r["o"] in "NP" else "tempo-insensitive (L/R)"].append(r)
            groups[f"CGT outcome {r['o']}"].append(r)
            if not r["race_sensitive"] and r["class"] not in ("hot-BIG", "decided"):
                groups[f"tame, race-insensitive: {r['class']}"].append(r)
    for g in sorted(groups, key=lambda k: (k != "all", not k.startswith("tempo"), k)):
        rs = groups[g]
        wins = sum(r["tb_root"] == "win" for r in rs)
        ok = 0
        for r in rs:
            v = r["lc0_orig_white_cp"]
            stm_v = v if r["stm"] == "W" else -v
            ok += (stm_v > 0) == (r["tb_root"] == "win")
        print(f"| {g} | {len(rs)} | {wins} | {ok} ({100*ok/len(rs):.0f}%) |")
    print("\n## Side-to-move flip, White POV centipawns: delta = v(White to move) - v(Black to move)")
    print("| CGT outcome class | n | median delta | share delta > 0 |")
    print("|---|---|---|---|")
    by = defaultdict(list)
    for r in rows:
        a, b = r["lc0_orig_white_cp"], r["lc0_twin_white_cp"]
        if a is None or b is None:
            continue
        by[r["o"]].append(a - b if r["stm"] == "W" else b - a)
    for o in "NPLR":
        if by[o]:
            print(f"| {o} | {len(by[o])} | {statistics.median(by[o]):+.0f} | "
                  f"{sum(x > 0 for x in by[o])}/{len(by[o])} |")
    print("\n## Policy (move chosen at the root) on the originals")
    n = win = king = kingwin = 0
    for r in rows:
        mv = r["lc0_orig_best"]
        n += 1
        win += r["tb_moves"].get(mv) == "win"
        if mv in r["king_moves"]:
            king += 1
            kingwin += r["tb_moves"].get(mv) == "win"
    has_win = sum(any(v == "win" for v in r["tb_moves"].values()) for r in rows)
    print(f"positions {n}; with a TB-winning move {has_win}; chosen move is a TB win {win}; "
          f"chosen move is a king move {king} (of which TB wins {kingwin})")


if __name__ == "__main__":
    main()
