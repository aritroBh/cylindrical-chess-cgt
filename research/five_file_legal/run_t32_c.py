"""T32 main runner: reachability of the 21 five-file *2 positions by the C search, plus legality.

For each position (research/star2_width5/hits.tsv, C/aware rows):
  * covering counts (exact pawn-only captures; file-shift lower bound);
  * S0: reachable from the standard start by a pawn-only history (en passant included)?
  * S1: the same with the trebuchet pawns W g4 and B g5 (reachable beside T)?
    Each C result FOUND is replayed by replay_check.replay (independent code);
  * legal beside T (files f-h), and the mirror check (files d-h with T on a-c).

Reproduce (project root, after building the C search):
  cc -O2 -o /tmp/t32_search research/five_file_legal/t32_search.c      # any scratch path
  PYTHONPATH=. .venv/bin/python -I research/five_file_legal/run_t32_c.py /tmp/t32_search \
      > research/five_file_legal/run_t32_c.out
Writes research/five_file_legal/results.json.
Environment: T32_LOG2 (visited-table log2, default 26), T32_NODE_CAP (default 200000000),
T32_TIMEOUT (seconds per search, default 1500), T32_ONLY (comma-separated 1-based indices),
T32_TAGS (default "S0,S1"), T32_ORDERED ("1" = witness-first ordering), T32_OUT (results file).
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pawnhist as ph            # noqa: E402
import replay_check as rc       # noqa: E402
from positions import load_positions  # noqa: E402

LOG2 = int(os.environ.get("T32_LOG2", 26))
NODE_CAP = int(os.environ.get("T32_NODE_CAP", 200_000_000))
TIMEOUT = float(os.environ.get("T32_TIMEOUT", 1500))
ONLY = {int(x) for x in os.environ.get("T32_ONLY", "").split(",") if x.strip()}
TAGS = [t for t in os.environ.get("T32_TAGS", "S0,S1").split(",") if t]
ORDERED = os.environ.get("T32_ORDERED", "0") == "1"
OUT = os.environ.get("T32_OUT", os.path.join(HERE, "results.json"))


def mask_of(pawns):
    m = 0
    for f, r in pawns:
        m |= 1 << ((r - 1) * 8 + f)
    return m


def run_c(binary, W, B):
    """One target through the C search.  Returns (status, nodes, moves) or ('timeout', None, None)."""
    start_w = format(mask_of(ph.START_W), "x")
    start_b = format(mask_of(ph.START_B), "x")
    inp = f"{mask_of(W)} {mask_of(B)}\n"
    args = [binary, str(LOG2), str(NODE_CAP), start_w, start_b] + (["ordered"] if ORDERED else [])
    try:
        p = subprocess.run(args, input=inp, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return "timeout", None, None
    if p.returncode != 0:
        raise RuntimeError(f"C search failed: {p.stderr}")
    lines = p.stdout.splitlines()
    head = lines[0].split()
    status = head[1].lower()          # found / exhausted / cap
    nodes = int(head[3])
    moves = []
    if status == "found":
        nm = int(head[5])
        for line in lines[1:1 + nm]:
            _, kind, side, f, r, tf, tr = line.split()
            moves.append((kind, side, (int(f), int(r)), (int(tf), int(tr))))
    return status, nodes, moves


def main():
    binary = sys.argv[1]
    pos = load_positions()
    tre = ph.TREB
    rows = []
    print(f"# T32 C-search run {time.strftime('%Y-%m-%d %H:%M:%S')} log2={LOG2} node_cap={NODE_CAP} "
          f"timeout={TIMEOUT}", flush=True)
    for i, p in enumerate(pos, start=1):
        if ONLY and i not in ONLY:
            continue
        W = frozenset(p["white"])
        B = frozenset(p["black"])
        nw, nb = len(W), len(B)
        row = {"idx": i, "position": p["position"], "n_W": nw, "n_B": nb,
               "captures_W_exact": 8 - nb, "captures_B_exact": 8 - nw}
        lbw, fw = ph.min_captures(W, True)
        lbb, fb = ph.min_captures(B, False)
        row["LB_W_fileshift"] = lbw
        row["LB_B_fileshift"] = lbb
        row["covering"] = bool(fw and fb and lbw <= 8 - nb and lbb <= 8 - nw)
        t0 = time.time()
        for tag, (TW, TB) in (("S0", (W, B)),
                              ("S1", (W | {tre["W_pawn"]}, B | {tre["B_pawn"]}))):
            if tag not in TAGS:
                continue
            status, nodes, moves = run_c(binary, TW, TB)
            entry = {"status": status, "nodes": nodes}
            if status == "found":
                ok, msg = rc.replay(moves, TW, TB)
                entry["replay"] = ok
                entry["replay_msg"] = msg
                entry["n_moves"] = len(moves)
                entry["history"] = ph.format_history(moves)
            row[tag] = entry
        leg = ph.legality(W, B, tre)
        row["legal_beside_T"] = (not leg["checks"]) and (not leg["king_capture_conflicts"])
        row["checks"] = leg["checks"]
        row["king_capture_conflicts"] = leg["king_capture_conflicts"]
        row["efile_touching"] = leg["efile_touching"]
        legm = ph.legality(ph.mirror(W), ph.mirror(B), ph.TREB_MIRROR)
        row["mirror_legal_beside_T"] = (not legm["checks"]) and (not legm["king_capture_conflicts"])
        row["mirror_consistent"] = (row["legal_beside_T"] == row["mirror_legal_beside_T"]
                                    and len(legm["efile_touching"]) == len(leg["efile_touching"]))
        row["seconds"] = round(time.time() - t0, 1)
        rows.append(row)
        s0 = row.get("S0", {"status": "not run", "nodes": None})
        s1 = row.get("S1", {"status": "not run", "nodes": None})
        hist0 = " ".join(s0.get("history", [])) or "-"
        hist1 = " ".join(s1.get("history", [])) or "-"
        print(f"{i}\t{p['position']}\tcapW={8-nb} capB={8-nw} LB_W={lbw} LB_B={lbb} "
              f"cover={row['covering']}\tS0={s0['status']} n={s0['nodes']} replay={s0.get('replay')} "
              f"[{hist0}]\tS1={s1['status']} n={s1['nodes']} replay={s1.get('replay')} [{hist1}]\t"
              f"legalT={row['legal_beside_T']} mirror={row['mirror_legal_beside_T']} "
              f"consistent={row['mirror_consistent']} sec={row['seconds']}", flush=True)
        for c in leg["checks"]:
            print("   check:", c, flush=True)
        for c in leg["king_capture_conflicts"]:
            print("   king conflict:", c, flush=True)
        if leg["efile_touching"]:
            print("   e-file touching:", leg["efile_touching"], flush=True)

    with open(OUT, "w") as fh:
        json.dump(rows, fh, indent=1)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()
