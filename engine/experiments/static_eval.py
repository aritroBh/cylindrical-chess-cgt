#!/usr/bin/env python3
"""Experiments E3/E5: does Stockfish's static (NNUE) evaluation know the CGT value?

For each of the 275 tablebase-probed suite positions (engine/suite/results.json) and for its
side-to-move twin (same men, other side to move), ask Stockfish's `eval` command for
  * the raw NNUE output ("NNUE evaluation ... (white side)") and
  * the final static evaluation ("Final evaluation ... (white side)"),
both in pawns from White's point of view. No search is done.

Ground truth:
  * originals: the Lichess tablebase root result (results.json, `tb_root`, for the side to move);
  * the CGT outcome class o(G) of the queenside component under RACE_RULE "count"
    (cylcgt, 4-file flat 8-rank board, e.p. on, textbook passed test): L, R, N or P.
    With the trebuchet frozen, o(G) says who wins with each side to move:
    L = White either way, R = Black either way, N = the mover, P = the non-mover.
    This is the model, not the tablebase: twins are judged against it only.

Run from the project root:
    PYTHONPATH=. .venv/bin/python engine/experiments/static_eval.py \
        --engine engine/vendor/Stockfish/src/stockfish
Writes engine/experiments/results/static_eval.json and prints the summary tables.
"""
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from cylcgt import cgt, pawns
from realchess import movegen

HERE = Path(__file__).resolve().parent
SUITE = HERE.parent / "suite" / "results.json"
BOARD = pawns.Board(4, 8, False, True)


def flip_stm(fen: str) -> str:
    f = fen.split()
    f[1] = "b" if f[1] == "w" else "w"
    f[3] = "-"
    return " ".join(f[:4]) + " 0 1"


def legal(fen: str) -> bool:
    pos = movegen.parse_fen(fen)
    return not movegen.validity_errors(pos) and len(movegen.legal_moves(pos)) > 0


def run_evals(engine: str, fens: list[str]) -> list[tuple[float | None, float | None]]:
    cmds = ["uci", "setoption name Threads value 1", "isready"]
    for fen in fens:
        cmds += [f"position fen {fen}", "eval", "isready"]
    cmds.append("quit")
    out = subprocess.run([engine], input="\n".join(cmds) + "\n", capture_output=True, text=True,
                         timeout=600).stdout
    vals, nnue, final = [], None, None
    blocks = out.split("readyok")[1:]  # one block per position, after the first isready
    for blk in blocks[: len(fens)]:
        nnue = final = None
        for line in blk.splitlines():
            if line.startswith("NNUE evaluation") and "(white side)" in line:
                nnue = float(line.split()[2])
            if line.startswith("Final evaluation"):
                tok = line.split()[2]
                final = None if tok == "none" else float(tok)
        vals.append((nnue, final))
    assert len(vals) == len(fens), (len(vals), len(fens))
    return vals


def outcome_class(component: str) -> str:
    pawns.RACE_RULE = "count"
    return cgt.outcome(pawns.value(BOARD, pawns.Pos.parse(component)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine")
    ap.add_argument("--summary", action="store_true", help="only re-print the tables from the JSON")
    a = ap.parse_args()
    if a.summary:
        summarize(json.loads((HERE / "results" / "static_eval.json").read_text())["rows"])
        return
    recs = json.loads(SUITE.read_text())
    rows, fens = [], []
    for r in recs:
        twin = flip_stm(r["fen"])
        rows.append({"id": r["id"], "fen": r["fen"], "twin": twin, "twin_legal": legal(twin),
                     "stm": r["stm"], "treb": r["treb"], "component": r["component"],
                     "value_count": r["value"]["count"], "class": r["features"]["class"],
                     "race_sensitive": r["features"]["race_sensitive"], "tb_root": r["tb_root"],
                     "o": outcome_class(r["component"])})
        fens += [r["fen"], twin]
    vals = run_evals(a.engine, fens)
    for i, row in enumerate(rows):
        (row["nnue"], row["final"]), (row["twin_nnue"], row["twin_final"]) = vals[2 * i], vals[2 * i + 1]
    outdir = HERE / "results"
    outdir.mkdir(exist_ok=True)
    (outdir / "static_eval.json").write_text(json.dumps({"engine": a.engine, "rows": rows}, indent=0))
    summarize(rows)


def stm_pov(row, key="final"):
    v = row[key]
    return v if row["stm"] == "W" else -v


def summarize(rows):
    print(f"positions: {len(rows)}; twins legal: {sum(r['twin_legal'] for r in rows)}")
    # 1. originals: sign of the static eval (side-to-move POV) vs tablebase root
    print("\n## 1. Static eval sign vs tablebase root (originals; draws excluded)")
    groups = defaultdict(list)
    for r in rows:
        if r["tb_root"] in ("win", "loss"):
            tempo = "tempo-sensitive (N/P)" if r["o"] in "NP" else "tempo-insensitive (L/R)"
            groups["all"].append(r)
            groups[tempo].append(r)
            groups[f"CGT outcome {r['o']}"].append(r)
            if not r["race_sensitive"] and r["class"] not in ("hot-BIG", "decided"):
                groups[f"tame, race-insensitive: {r['class']}"].append(r)
    print("| group | n (win/loss roots) | TB root = win | final eval sign right | raw NNUE sign right |")
    print("|---|---|---|---|---|")
    for g in sorted(groups, key=lambda k: (k != "all", not k.startswith("tempo"), k)):
        rs = groups[g]
        wins = sum(r["tb_root"] == "win" for r in rs)
        ok = sum((stm_pov(r) > 0) == (r["tb_root"] == "win") for r in rs)
        okn = sum((stm_pov(r, "nnue") > 0) == (r["tb_root"] == "win") for r in rs)
        print(f"| {g} | {len(rs)} | {wins} | {ok} ({100*ok/len(rs):.0f}%) | {okn} ({100*okn/len(rs):.0f}%) |")
    # 2. twins: does the White-POV eval move the right way when the side to move flips?
    print("\n## 2. Side-to-move flip: delta = eval(White to move) - eval(Black to move), White POV, pawns")
    print("CGT says: N -> White wins only when White moves (delta should be large +);")
    print("P -> the mover loses (delta should be large -); L/R -> same winner (delta ~ 0).")
    print("| CGT outcome class | n | median delta (final) | share delta > 0 | median delta (raw NNUE) |")
    print("|---|---|---|---|---|")
    by = defaultdict(list)
    for r in rows:
        if not r["twin_legal"] or r["final"] is None or r["twin_final"] is None:
            continue
        w_first = r if r["stm"] == "W" else None
        if w_first is None:
            d = r["twin_final"] - r["final"]
            dn = r["twin_nnue"] - r["nnue"]
        else:
            d = r["final"] - r["twin_final"]
            dn = r["nnue"] - r["twin_nnue"]
        by[r["o"]].append((d, dn))
    for o in "NPLR":
        if by[o]:
            ds = [x for x, _ in by[o]]
            dns = [y for _, y in by[o]]
            pos = sum(x > 0 for x in ds)
            print(f"| {o} | {len(ds)} | {statistics.median(ds):+.2f} | {pos}/{len(ds)} | "
                  f"{statistics.median(dns):+.2f} |")


if __name__ == "__main__":
    sys.exit(main())
