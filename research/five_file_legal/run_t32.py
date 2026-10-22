"""T32 driver: the 21 five-file *2 positions (research/star2_width5/hits.tsv, C/aware rows).

For each position:
  * counts: n_W, n_B pawns; the exact pawn-only capture counts (White makes 8 - n_B captures,
    Black 8 - n_W); the file-shift lower bound LB (min_captures) and the covering test LB <= count;
  * S0: is the position reachable by a pawn-only history from the start (en passant included)?
    The history is validated by replay_check.replay;
  * S1: the same with the trebuchet pawns W g4 and B g5 added (reachable beside T);
  * legality beside the trebuchet T (W Kf5 g4, B Kh4 g5) on files f-h, and the mirror check
    (files reversed: the block on files d-h, T on files a-c).

Reproduce (project root):
  PYTHONPATH=. .venv/bin/python -I research/five_file_legal/run_t32.py \
      > research/five_file_legal/run_t32.out
Output: one TSV-like line per position on stdout, plus research/five_file_legal/results.json.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pawnhist as ph            # noqa: E402
import replay_check as rc       # noqa: E402
from positions import load_positions, fmt_pos  # noqa: E402

NODE_CAP = int(os.environ.get("T32_NODE_CAP", 3_000_000))
MAX_SEC = float(os.environ.get("T32_MAX_SEC", 900))
WHICH = os.environ.get("T32_WHICH", "S0,S1")       # subset of the two reachability settings
ONLY = os.environ.get("T32_ONLY", "")              # comma-separated 1-based indices, optional


def search(W, B):
    m, info = ph.find_history(W, B, prune=True, node_cap=NODE_CAP, max_seconds=MAX_SEC)
    row = {"status": info["status"], "nodes": info["nodes"]}
    if m is not None:
        ok, msg = rc.replay(m, W, B)
        row["history"] = ph.format_history(m)
        row["n_moves"] = len(m)
        row["replay"] = ok
        row["replay_msg"] = msg
    return row


def sorted_sq(s):
    return sorted(s, key=lambda q: (q[1], q[0]))


def main():
    pos = load_positions()
    only = {int(x) for x in ONLY.split(",") if x.strip()} if ONLY else None
    results = []
    tre = ph.TREB
    tre_mir = ph.TREB_MIRROR
    print("# T32 run", time.strftime("%Y-%m-%d %H:%M:%S"), "node_cap", NODE_CAP, "max_sec", MAX_SEC,
          "which", WHICH, flush=True)
    for i, p in enumerate(pos, start=1):
        if only and i not in only:
            continue
        W = frozenset(p["white"])
        B = frozenset(p["black"])
        nw, nb = len(W), len(B)
        t0 = time.time()
        row = {"idx": i, "position": p["position"], "k": p["k"], "settings": p["settings"],
               "n_W": nw, "n_B": nb,
               "captures_W_exact": 8 - nb, "captures_B_exact": 8 - nw}
        lbw, fw = ph.min_captures(W, True)
        lbb, fb = ph.min_captures(B, False)
        row["LB_W_fileshift"] = lbw
        row["LB_B_fileshift"] = lbb
        row["covering_W"] = bool(fw and lbw <= 8 - nb)
        row["covering_B"] = bool(fb and lbb <= 8 - nw)
        if "S0" in WHICH:
            row["S0"] = search(W, B)
        if "S1" in WHICH:
            WT = W | {tre["W_pawn"]}
            BT = B | {tre["B_pawn"]}
            row["S1"] = search(WT, BT)
        # legality beside T (files f-h); mirror check on files d-h with T on a-c
        leg = ph.legality(W, B, tre)
        row["legal_beside_T"] = not leg["checks"] and not leg["king_capture_conflicts"]
        row["checks"] = leg["checks"]
        row["king_capture_conflicts"] = leg["king_capture_conflicts"]
        row["efile_touching"] = leg["efile_touching"]
        row["adjacent_enemy_pawns"] = leg["adjacent_enemy_pawns"]
        Wm, Bm = ph.mirror(W), ph.mirror(B)
        legm = ph.legality(Wm, Bm, tre_mir)
        row["mirror_legal_beside_T"] = not legm["checks"] and not legm["king_capture_conflicts"]
        row["mirror_consistent"] = (row["legal_beside_T"] == row["mirror_legal_beside_T"]
                                    and len(legm["efile_touching"]) == len(leg["efile_touching"]))
        row["seconds"] = round(time.time() - t0, 2)
        results.append(row)

        s0 = row.get("S0", {})
        s1 = row.get("S1", {})
        print(f"{i}\t{p['position']}\tnW={nw} nB={nb}\tcapW={8-nb} capB={8-nw}"
              f"\tLB_W={lbw} LB_B={lbb} cover={row['covering_W'] and row['covering_B']}"
              f"\tS0={s0.get('status')} nodes={s0.get('nodes')} "
              f"hist={' '.join(s0.get('history', [])) if s0.get('history') else '-'}"
              f" replay={s0.get('replay')}"
              f"\tS1={s1.get('status')} nodes={s1.get('nodes')} "
              f"hist={' '.join(s1.get('history', [])) if s1.get('history') else '-'}"
              f" replay={s1.get('replay')}"
              f"\tlegalT={row['legal_beside_T']} mirror={row['mirror_legal_beside_T']} "
              f"consistent={row['mirror_consistent']}"
              f"\tsec={row['seconds']}", flush=True)
        if leg["checks"]:
            print("   checks:", "; ".join(leg["checks"]), flush=True)
        if leg["king_capture_conflicts"]:
            print("   king conflicts:", "; ".join(leg["king_capture_conflicts"]), flush=True)
        if leg["efile_touching"]:
            print("   e-file touching:", leg["efile_touching"], flush=True)

    out = os.path.join(HERE, "results.json")
    if only is None:
        with open(out, "w") as fh:
            json.dump(results, fh, indent=1, default=list)
        print("wrote", out, flush=True)


if __name__ == "__main__":
    main()
