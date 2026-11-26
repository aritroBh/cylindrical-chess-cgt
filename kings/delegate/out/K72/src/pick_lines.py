"""K72: pick one disagreement position per failing context for ref3pv lines (the first differing position in the
order A b, A w, B b, B w, qA b, qA w, qB b, qB w).  Usage (repository root):
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K72/src/pick_lines.py 11   -> in/lines_11.pos
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K72/src/pick_lines.py 22   -> in/lines_22.pos
For 22 the contexts of at most 1 + 1 pawns are left out (they are in lines_11).  Then, through heavy.sh:
  zsh kings/delegate/out/K72/src/watch.sh lines_NN in/lines_NN.pos logs/lines_NN.out bin/ref3pv --board pln:8x8 --pv 160
"""
import sys
V = "kings/delegate/out/K72"
LAB = ["A b", "A w", "B b", "B w", "qA b", "qA w", "qB b", "qB w"]
nn = sys.argv[1]
tags = [f"{t}_{nn}" for t in ["C125_08_h", "C125_05_f", "C125_05_g", "C125_05_h", "C145_07_a", "C145_07_b",
                              "C145_07_c", "C145_09_a", "C145_09_b", "C145_09_h"]]
out = []
for t in tags:
    pos = [l.strip() for l in open(f"{V}/in/{t}.pos") if l.strip()]
    rows = [l for l in open(f"{V}/logs/{t}_table.txt") if not l.startswith("#")]
    for i, row in enumerate(rows):
        if "DIFFER" not in row: continue
        c = row.split(" P ")[0].strip()
        if nn == "22" and len(c.split()) <= 2: continue
        lab = row.split("DIFFER at ")[1].strip().split(", ")[0]
        out.append(f"# {t} | {c} | {lab}\n{pos[8 * i + LAB.index(lab)]}\n")
open(f"{V}/in/lines_{nn}.pos", "w").write("\n".join(out))
print(len(out), "positions", file=sys.stderr)
