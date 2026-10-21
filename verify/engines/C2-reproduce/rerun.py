#!/usr/bin/env python3
"""Independent re-run of claim C2 (flip test). Writes only into this directory.

* Recomputes the CGT outcome class of every component in a fresh process (cache cleared, all 3 race rules).
* Builds twins itself (flip side to move, e.p. '-').
* Re-runs Stockfish 19 `eval` (own parser) and Lc0 `go nodes 1` (own UCI loop) on all 550 FENs.
* Compares every number with the worker's JSON files.

Run from the project root:
    PYTHONPATH=. .venv/bin/python verify/engines/C2-reproduce/rerun.py
"""
import json
import statistics
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

from cylcgt import cgt, pawns

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SF = ROOT / "engine/vendor/Stockfish/src/stockfish"
LC0 = "/opt/homebrew/bin/lc0"
BOARD = pawns.Board(4, 8, False, True)

recs = json.loads((ROOT / "engine/suite/results.json").read_text())
se_w = {r["id"]: r for r in json.loads((ROOT / "engine/experiments/results/static_eval.json").read_text())["rows"]}
lc_w = {r["id"]: r for r in json.loads((ROOT / "engine/experiments/results/lc0_value_n1.json").read_text())["rows"]}


def twin_of(fen):
    f = fen.split()
    return f"{f[0]} {'b' if f[1] == 'w' else 'w'} {f[2]} - 0 1"


# 1. CGT classes, fresh, each rule with a cleared cache
cls = defaultdict(dict)
for rule in ("count", "mover", "opponent"):
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    for r in recs:
        cls[r["id"]][rule] = cgt.outcome(pawns.value(BOARD, pawns.Pos.parse(r["component"])))
pawns.RACE_RULE = "count"
pawns._value.cache_clear()
mism_o = [i for i in cls if cls[i]["count"] != se_w[i]["o"]]
print("CGT class (count) mismatches vs worker:", mism_o)
print("count-rule classes:", Counter(c["count"] for c in cls.values()))
print("rule-sensitive N/P classes:", sum(1 for c in cls.values() if c["count"] in "NP" and len(set(c.values())) > 1))

# 2. Stockfish eval
fens = []
for r in recs:
    tw = twin_of(r["fen"])
    assert tw == se_w[r["id"]]["twin"], (r["id"], tw, se_w[r["id"]]["twin"])
    fens += [r["fen"], tw]
cmds = ["uci", "isready"]
for f in fens:
    cmds += [f"position fen {f}", "eval", "isready"]
cmds.append("quit")
out = subprocess.run([str(SF)], input="\n".join(cmds) + "\n", capture_output=True, text=True, timeout=900).stdout
blocks = out.split("readyok\n")[1:1 + len(fens)]
sf = []
for b in blocks:
    fin = [l for l in b.splitlines() if l.startswith("Final evaluation")]
    nn = [l for l in b.splitlines() if l.startswith("NNUE evaluation") and "(white side)" in l]
    assert len(fin) == 1 and len(nn) == 1, b[-300:]
    sf.append((float(nn[0].split()[2]), float(fin[0].split()[2])))
assert len(sf) == len(fens)

# 3. Lc0 nodes 1
p = subprocess.Popen([LC0], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
                     bufsize=1)


def send(s):
    p.stdin.write(s + "\n")
    p.stdin.flush()


def read_until(prefix):
    lines = []
    while True:
        l = p.stdout.readline()
        if not l:
            raise RuntimeError("lc0 exited")
        l = l.rstrip("\n")
        lines.append(l)
        if l.startswith(prefix):
            return lines


send("uci")
read_until("uciok")
send("isready")
read_until("readyok")
lc = []
for f in fens:
    send("ucinewgame")
    send("isready")
    read_until("readyok")
    send(f"position fen {f}")
    send("go nodes 1")
    lines = read_until("bestmove")
    infos = [l.split() for l in lines if l.startswith("info") and " score " in l]
    t = infos[-1]
    kind, v = t[t.index("score") + 1], int(t[t.index("score") + 2])
    cp = (100000 if v > 0 else -100000) if kind == "mate" else v
    nodes = int(t[t.index("nodes") + 1])
    white = cp if f.split()[1] == "w" else -cp
    lc.append((white, nodes, lines[-1].split()[1]))
send("quit")
print("lc0 node counts at the reported info line:", Counter(x[1] for x in lc))

# 4. Compare with worker data and recompute the claim's numbers
rows = []
diff_sf = diff_lc = 0
for k, r in enumerate(recs):
    i = r["id"]
    (nn_o, fin_o), (nn_t, fin_t) = sf[2 * k], sf[2 * k + 1]
    lo, lt = lc[2 * k][0], lc[2 * k + 1][0]
    w = se_w[i]
    diff_sf += (abs(fin_o - w["final"]) > 1e-9) + (abs(fin_t - w["twin_final"]) > 1e-9) \
        + (abs(nn_o - w["nnue"]) > 1e-9) + (abs(nn_t - w["twin_nnue"]) > 1e-9)
    diff_lc += (lo != lc_w[i]["lc0_orig_white_cp"]) + (lt != lc_w[i]["lc0_twin_white_cp"])
    sgn = 1 if r["stm"] == "W" else -1
    rows.append({"id": i, "stm": r["stm"], "o": cls[i]["count"], "o_all": cls[i], "tb_root": r["tb_root"],
                 "sf_delta": round((fin_o - fin_t) * sgn, 4), "sf_nnue_delta": round((nn_o - nn_t) * sgn, 4),
                 "lc_delta": (lo - lt) * sgn, "sf_orig": fin_o, "sf_twin": fin_t, "lc_orig": lo, "lc_twin": lt,
                 "lc_best_orig": lc[2 * k][2]})
print("Stockfish values differing from worker JSON:", diff_sf, "of", 4 * len(recs))
print("Lc0 values differing from worker JSON:", diff_lc, "of", 2 * len(recs))
(OUT / "rerun_rows.json").write_text(json.dumps(rows, indent=0))

print("\nFlip test (fresh engine output, fresh CGT classes):")
for o in "NPLR":
    rs = [x for x in rows if x["o"] == o]
    want = {"N": lambda d: d > 0, "P": lambda d: d < 0, "L": None, "R": None}[o]
    sd = [x["sf_delta"] for x in rs]
    ld = [x["lc_delta"] for x in rs]
    line = f"{o}: n={len(rs)} SF median {statistics.median(sd):+.2f} (pos {sum(d > 0 for d in sd)}, zero " \
           f"{sum(d == 0 for d in sd)}, neg {sum(d < 0 for d in sd)}); Lc0 median {statistics.median(ld):+.0f} " \
           f"(pos {sum(d > 0 for d in ld)}, zero {sum(d == 0 for d in ld)}, neg {sum(d < 0 for d in ld)})"
    if want:
        line += f"; right SF {sum(want(d) for d in sd)}/{len(rs)}, Lc0 {sum(want(d) for d in ld)}/{len(rs)}"
    print(line)
