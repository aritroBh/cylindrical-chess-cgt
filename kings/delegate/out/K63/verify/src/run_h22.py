"""K63 referee: P values of F2 + X for every context X of at most 2 + 2 pawns on file h, by the referee's own
solver pk (src/pk.cpp), compared with (a) the referee's own D-sum prediction (src/dpred_h.py, logs/dpred_h.txt)
and (b) the investigator's table (kings/delegate/out/K63/logs/ctx_h22_table.txt: P column and prediction column).
Usage (repository root):
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K63/verify/src/run_h22.py gen   (writes logs/h22_pk.in)
  zsh kings/delegate/out/K63/verify/src/hrun.sh h22_pk <in> <out> <pk binary>                (logs/h22_pk.out)
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K63/verify/src/run_h22.py cmp
"""
import re, sys
V = "kings/delegate/out/K63/verify"
BASE = ["Ka4 kc4 Pb2 Pf5 pb6 pf6 {} b -", "Ka4 kc4 Pb2 Pf5 pb6 pf6 {} w -",
        "Ka4 kc5 Pb2 Pf5 pb6 pf6 {} b -", "Ka4 kc5 Pb2 Pf5 pb6 pf6 {} w -",
        "Ka4 kc4 Pb4 Pf5 pb6 pf6 {} b b3", "Ka4 kc4 Pb4 Pf5 pb6 pf6 {} w -",
        "Ka4 kc5 Pb3 Pf5 pb6 pf6 {} b -", "Ka4 kc5 Pb3 Pf5 pb6 pf6 {} w -"]
LAB = ["A b", "A w", "B b", "B w", "qA b", "qA w", "qB b", "qB w"]
pred = {}
for line in open(f"{V}/logs/dpred_h.txt"):
    parts = line.split()
    pred[" ".join(parts[:-8])] = parts[-8:]
ctxs = list(pred)
if sys.argv[1] == "gen":
    inp = []
    for c in ctxs:
        x = "" if c == "empty" else c
        for b in BASE: inp.append(re.sub(r"\s+", " ", b.format(x)))
        inp.append("")
    open(f"{V}/logs/h22_pk.in", "w").write("\n".join(inp) + "\n")
    sys.exit(0)
inv = {}
for line in open("kings/delegate/out/K63/logs/ctx_h22_table.txt"):
    m = re.match(r"^ctx\d+\s+(.*?)\s+P ([WLD ]+?)\s+kp_p ([WLD ]+?)\s+pred ([WLD ]+?)(\s+DIFFER.*)?$", line.rstrip())
    if m: inv[m.group(1)] = (m.group(2).split(), m.group(3).split(), m.group(4).split())
assert len(inv) == len(ctxs) == 283, (len(inv), len(ctxs))
vals = [l.split()[-3] for l in open(f"{V}/logs/h22_pk.out") if l.strip()]
assert len(vals) == 8 * len(ctxs), len(vals)
nag = 0; diffs = []; npi = 0; npp = 0
O = {"L": 0, "D": 1, "W": 2}
with open(f"{V}/logs/h22_referee_table.txt", "w") as fh:
    fh.write("# context | P by pk (A b, A w, B b, B w, qA b, qA w, qB b, qB w; White's view) | referee's D-sum prediction | verdict\n")
    for i, c in enumerate(ctxs):
        P = vals[8 * i: 8 * i + 8]; pr = pred[c]
        iP, ikp, ipred = inv[c]
        if iP != P or ikp != P: npi += 1; print("P MISMATCH with investigator", c, P, iP, ikp)
        if ipred != pr: npp += 1; print("PRED MISMATCH with investigator", c, pr, ipred)
        d = [k for k in range(8) if P[k] != pr[k]]
        verdict = "agree" if not d else "DIFFER at " + ", ".join(LAB[k] for k in d)
        if not d: nag += 1
        else: diffs.append((c, [(LAB[k], pr[k], P[k]) for k in d]))
        fh.write(f"{c:22s} P {' '.join(P)}  pred {' '.join(pr)}  {verdict}\n")
npos = sum(len(x[1]) for x in diffs)
fav = {"Black": 0, "White": 0}
kinds = {}
for c, lst in diffs:
    for lab, p, q in lst:
        fav["Black" if O[q] < O[p] else "White"] += 1
        kinds[(p, q)] = kinds.get((p, q), 0) + 1
        kinds[lab] = kinds.get(lab, 0) + 1
blocked = [c for c in ctxs if "Ph2" in c.split() and ("ph3" in c.split() or "ph4" in c.split())]
dc = [c for c, _ in diffs]
print(f"contexts {len(ctxs)}; agree {nag}; differ {len(diffs)}; positions differing {npos}; in favour of {fav}")
print(f"(prediction, P) pairs and positions: {kinds}")
print(f"contexts where pk's P differs from the investigator's P or kp_p column: {npi}")
print(f"contexts where the referee's prediction differs from the investigator's prediction column: {npp}")
print(f"contexts with Ph2 and ph3 or ph4: {len(blocked)}; of them differ {len([c for c in blocked if c in dc])}, agree {len([c for c in blocked if c not in dc])}")
print(f"differing contexts without that pair: {[c for c in dc if c not in blocked]}")
for c, lst in diffs: print("  DIFF", c, lst)
print("agreeing contexts with the pair:", [c for c in blocked if c not in dc])
