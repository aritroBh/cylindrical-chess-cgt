"""K75: one position per failing context for ref3pv lines (the first differing position in the order A b, A w, B b,
B w, qA b, qA w, qB b, qB w).  Adapted from kings/delegate/out/K72/src/pick_lines.py: every pair of the summary, a
blank line between pairs (ref3pv clears its memo there); at most CAP contexts per pair.
Usage (repository root):
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K75/src/pick_lines.py NN [OUT]  -> in/lines_NN.pos
then, through heavy.sh and watch.sh:  bin/ref3pv --board pln:8x8 --pv 160 < in/lines_NN.pos
"""
import sys
V = "kings/delegate/out/K75"
LAB = ["A b", "A w", "B b", "B w", "qA b", "qA w", "qB b", "qB w"]
nn = sys.argv[1]
CAP = 3     # at most 3 failing contexts per pair (spread over the list), to keep the line run short
# only groups of at most 7 men (ref3pv's tables for 8 men may pass 2 GB) and pairs K72 did not already explain
MEN = {l.split("|")[0]: int(l.split("|")[1]) for l in open(f"{V}/in/groups48.txt") if not l.startswith("#")}
K72 = {"C125_05_f", "C125_05_g", "C125_05_h", "C125_08_h", "C125_10_h", "C145_07_a", "C145_07_b", "C145_07_c",
       "C145_09_a", "C145_09_b", "C145_09_h"}
outf = sys.argv[2] if len(sys.argv) > 2 else f"{V}/in/lines_{nn}.pos"
tags = []
for l in open(f"{V}/logs/summary_{nn}.txt"):
    if l.startswith("SUM ") and " fail 0 " not in l:
        t = l.split()[1]
        if t not in tags and MEN[t[:7]] <= 7 and t[:9] not in K72: tags.append(t)
blocks = []
for t in tags:
    pos = [l.strip() for l in open(f"{V}/in/{t}.pos") if l.strip()]
    rows = [l for l in open(f"{V}/logs/{t}_table.txt") if not l.startswith("#")]
    out = []
    fails = [i for i, row in enumerate(rows) if "DIFFER" in row]
    if len(fails) > CAP: fails = [fails[round(j * (len(fails) - 1) / (CAP - 1))] for j in range(CAP)]   # spread
    for i, row in enumerate(rows):
        if i not in fails: continue
        c = row.split(" P ")[0].strip()
        lab = row.split("DIFFER at ")[1].strip().split(", ")[0].replace(" (below)", "").replace(" (ABOVE)", "")
        out.append(f"# {t} | {c} | {lab}\n{pos[8 * i + LAB.index(lab)]}\n")
    blocks.append("".join(out))
open(outf, "w").write("\n".join(blocks))
print(sum(b.count("# ") for b in blocks), "positions in", len(blocks), "pairs", file=sys.stderr)
