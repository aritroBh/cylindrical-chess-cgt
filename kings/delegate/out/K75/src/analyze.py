"""K75: the table of question 1 and the rule tests of question 3.

Usage (repository root):  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K75/src/analyze.py NN
Reads in/groups48.txt, logs/summary_NN.txt (SUM lines of cmp.py; the last line of each pair counts),
logs/G_F_NN_table.txt and, if present, logs/mech_NN.txt (one ref3pv line label per failing context);
writes logs/table_NN.txt.
Distances: |file of the context - file of the king| for the White king and for each shuttle square of the Black king.
"""
import re, sys, os
V = "kings/delegate/out/K75"
nn = sys.argv[1]
G = {}
for l in open(f"{V}/in/groups48.txt"):
    if l.startswith("#"): continue
    r = l.rstrip("\n").split("|"); G[r[0]] = r
S = {}
for l in open(f"{V}/logs/summary_{nn}.txt"):
    if l.startswith("SUM "):
        t = l.split(); S[t[1]] = l.strip()
mech = {}
if os.path.exists(f"{V}/logs/mech_{nn}.txt"):
    for l in open(f"{V}/logs/mech_{nn}.txt"):
        m = re.match(r"(\S+) \| (.*?) \| (.*?)\s+P=(\S)\s+ctx-capture: (.*?)\s+promotes: (.*?)\s+plies", l)
        if m: mech[(m.group(1), m.group(2))] = (m.group(3), m.group(4), m.group(5), m.group(6))
fd = lambda a, b: abs(ord(a[0]) - ord(b[0]))
rows = []
for nm, r in G.items():
    for f in r[13]:
        tag = f"{nm}_{f}_{nn}"
        if tag not in S: continue
        s = S[tag]
        ag = int(re.search(r" agree (\d+)", s).group(1)); fl = int(re.search(r" fail (\d+)", s).group(1))
        mis = re.search(r"pk/ref3m-mismatch (\d+)", s).group(1)
        kinds = re.search(r"kinds \[(.*)\]", s).group(1)
        both = 0; tot = 0; kc = {}
        for line in open(f"{V}/logs/{tag}_table.txt"):
            if line.startswith("#") or "DIFFER" not in line: continue
            c = line.split(" P ")[0].strip()
            tot += 1; both += {t[0] for t in c.split()} == {"P", "p"}
            k = mech.get((tag, c))
            if k:
                who = "Wk-takes" if k[1].startswith("White king") else ("bk-takes" if k[1].startswith("Black king") else "no-ctx-capture")
                kc[who] = kc.get(who, 0) + 1
        rows.append((nm, r[1], r[2], f, fd(f, r[3]), fd(f, r[4]), fd(f, r[5]), ag, fl, both, tot, mis, kinds,
                     ", ".join(f"{k} {v}" for k, v in sorted(kc.items()))))
with open(f"{V}/logs/table_{nn}.txt", "w") as fh:
    fh.write(f"# group men class file dW dA dB agree fail fails-with-both-colours pk/ref3m-mismatch | position kinds |"
             f" line kinds (one ref3pv line per failing context)\n")
    for x in rows:
        fh.write(f"{x[0]} {x[1]} {x[2]:6s} {x[3]} {x[4]} {x[5]} {x[6]} {x[7]:3d} {x[8]:3d} {x[9]}/{x[10]} {x[11]} | {x[12]} | {x[13]}\n")
print(len(rows), "pairs;", sum(1 for x in rows if x[8] == 0), "with no failure")
