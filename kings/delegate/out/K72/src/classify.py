"""K72: one-line mechanism labels for the ref3pv lines.  Usage: classify.py LINESFILE
For each line: who first captures a pawn on the context file (White king 'K..x' / Black king 'k..x'), which pawn
promotes at the end (its file: context file or group), or draw."""
import sys, re
cur = None
for l in open(sys.argv[1]):
    l = l.rstrip()
    if l.startswith("#"): cur = l[2:]; continue
    if not l: continue
    tag = cur.split(" | ")[0]; f = tag.split("_")[2]
    parts = l.split(" | ")
    res = parts[1].strip()
    line = parts[2][len("line:"):].split() if len(parts) > 2 else []
    cap = "-"
    for mv in line:
        m = re.match(r"(\.\.\.)?([Kk])([a-h]\d)([a-h]\d)x$", mv)
        if m and m.group(4)[0] == f: cap = ("White king" if m.group(2) == "K" else "Black king") + " takes " + m.group(4); break
    prom = [mv for mv in line if "promotes" in mv]
    pr = prom[0].lstrip(".") if prom else ("draw" if res == "D" else "?")
    where = "context" if prom and prom[0].lstrip(".")[1] == f else ("group" if prom else "")
    print(f"{cur:40s} P={res}  ctx-capture: {cap:24s} promotes: {pr} {where}  plies {len(line)}")
