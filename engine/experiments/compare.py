#!/usr/bin/env python3
"""Side-by-side: Stockfish 19 static eval vs Lc0 at one node, on the 275 probed positions.

Needs engine/experiments/results/static_eval.json and lc0_value_n1.json (see README.md there).
Run from the project root:
    .venv/bin/python engine/experiments/compare.py
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from run_suite import parse_epd, solutions  # noqa: E402


def group_of(r):
    v = r["value_count"]
    if r["o"] == "N":
        if v.startswith("*"):
            return "N: nimber"
        if "W" in v:
            return "N: hot, a passed pawn at stake (+-BIG)"
        return "N: other (small switches, ...)"
    return f"{r['o']}"


def main():
    se = {r["id"]: r for r in json.loads((HERE / "results" / "static_eval.json").read_text())["rows"]}
    lc = {r["id"]: r for r in json.loads((HERE / "results" / "lc0_value_n1.json").read_text())["rows"]}
    by = defaultdict(lambda: [0, 0, 0])
    flip = defaultdict(lambda: [0, 0, 0])
    for i, r in se.items():
        l = lc[i]
        sgn = 1 if r["stm"] == "W" else -1
        if r["tb_root"] in ("win", "loss"):
            g = group_of(r)
            want = r["tb_root"] == "win"
            for key in (g, "all"):
                by[key][0] += 1
                by[key][1] += (sgn * r["final"] > 0) == want
                by[key][2] += (sgn * l["lc0_orig_white_cp"] > 0) == want
        # flip test, judged against the CGT model: N -> delta > 0, P -> delta < 0
        if r["o"] in "NP":
            d_sf = (r["final"] - r["twin_final"]) * sgn
            d_lc = (l["lc0_orig_white_cp"] - l["lc0_twin_white_cp"]) * sgn
            want_pos = r["o"] == "N"
            flip[r["o"]][0] += 1
            flip[r["o"]][1] += (d_sf > 0) == want_pos
            flip[r["o"]][2] += (d_lc > 0) == want_pos
    print("## Sign of the evaluation for the side to move vs the tablebase root (win/loss roots only)")
    print("| group (CGT outcome of the component) | n | Stockfish 19 static eval | Lc0 one node (value head) |")
    print("|---|---|---|---|")
    for g in sorted(by, key=lambda k: (k != "all", k)):
        n, a, b = by[g]
        print(f"| {g} | {n} | {a} ({100*a/n:.0f}%) | {b} ({100*b/n:.0f}%) |")
    print("\n## Flip test: does the White-POV evaluation move the way CGT says when the side to move flips?")
    print("(N: White should look better with White to move; P: worse.) Judged against the CGT model.")
    print("| CGT outcome | n | Stockfish 19 static eval right | Lc0 one node right |")
    print("|---|---|---|---|")
    for o in "NP":
        n, a, b = flip[o]
        print(f"| {o} | {n} | {a} ({100*a/n:.0f}%) | {b} ({100*b/n:.0f}%) |")


def policy_on_suite():
    """Lc0's one-node move on the 233 EPD positions (solved = in the EPD solution set)."""
    lc = {r["id"]: r for r in json.loads((HERE / "results" / "lc0_value_n1.json").read_text())["rows"]}
    sol, slow = {}, {}
    for name in ("cgt_verified.epd", "cgt_disagree.epd"):
        for line in open(HERE.parent / "suite" / name, encoding="utf-8"):
            e = parse_epd(line)
            if e:
                fen4, ops = e
                i = ops["id"][0]
                sol[i] = (solutions(fen4, ops), name)
                slow[i] = "only-slow-winning-move true" in line
    print("\n## Lc0 one-node policy on the suite")
    ok = [i for i in sol if lc[i]["lc0_orig_best"] in sol[i][0]]
    print(f"solved {len(ok)} of {len(sol)}")
    for flag in (True, False):
        ids = [i for i in sol if slow[i] == flag]
        print(f"  only a slow single push wins = {flag}: {sum(i in ok for i in ids)}/{len(ids)}")
    for i in sol:
        if i not in ok:
            print(f"  miss {i}: played {lc[i]['lc0_orig_best']}, solutions {sorted(sol[i][0])} ({sol[i][1]})")
    kings = [r for r in lc.values() if r["lc0_orig_best"] in r["king_moves"]]
    print(f"king moves chosen (all 275 probed positions): {len(kings)}; in tablebase-lost roots "
          f"{sum(r['tb_root'] == 'loss' for r in kings)}, drawn {sum(r['tb_root'] == 'draw' for r in kings)}, "
          f"king move itself wins {sum(r['tb_moves'].get(r['lc0_orig_best']) == 'win' for r in kings)}")


if __name__ == "__main__":
    main()
    policy_on_suite()
