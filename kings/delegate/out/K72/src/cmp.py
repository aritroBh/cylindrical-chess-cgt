"""K72: compare the P values of two solvers (pk, ref3m) with each other and with the D-sum prediction.

Usage (repository root):  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K72/src/cmp.py G F NN
Reads in/G_F_NN.names, logs/G_F_NN_pk.out, logs/G_F_NN_ref3m.out, logs/dpred.txt (and K63's investigator prediction
kings/delegate/out/K63/in/ctx_h22.pred as a second predictor); writes logs/G_F_NN_table.txt and prints a summary.
Values are White's view (W, L, D).  Positions per context: A b, A w, B b, B w, qA b, qA w, qB b, qB w.
"""
import re, sys

V = "kings/delegate/out/K72"
LAB = ["A b", "A w", "B b", "B w", "qA b", "qA w", "qB b", "qB w"]
O = {"L": 0, "D": 1, "W": 2}
g, f, nn = sys.argv[1:4]
tag = f"{g}_{f}_{nn}"
names = [l.strip() for l in open(f"{V}/in/{tag}.names") if l.strip()]
tohkey = lambda c: c if c == "empty" else " ".join(t[0] + "h" + t[2:] for t in c.split())

pred = {}
for line in open(f"{V}/logs/dpred.txt"):
    p = line.split(); pred[" ".join(p[:-8])] = p[-8:]
# K63 investigator's predictor: omega w/b, zero w/b -> 8 columns
pred2 = {}
for line in open("kings/delegate/out/K63/in/ctx_h22.pred"):
    m = re.match(r"ctx\d+ \[(.*?)\] omega w (\S) b (\S) zero w (\S) b (\S)", line)
    if m:
        c = m.group(1) or "empty"
        ow, ob, zw, zb = m.group(2, 3, 4, 5)
        pred2[c] = [ob, ow, ob, ow, zb, zw, zb, zw]

pk = [l.split()[-3] for l in open(f"{V}/logs/{tag}_pk.out") if l.strip()]
rf = [l.rstrip().split("|")[-1].strip() for l in open(f"{V}/logs/{tag}_ref3m.out") if l.strip()]
assert len(pk) == len(rf) == 8 * len(names), (len(pk), len(rf), len(names))
nag = 0; ndis = 0; npd = 0; diffs = []
with open(f"{V}/logs/{tag}_table.txt", "w") as fh:
    fh.write(f"# {tag}: context | P (pk) | P (ref3m) | D-sum prediction (A b, A w, B b, B w, qA b, qA w, qB b, qB w) | verdict\n")
    for i, c in enumerate(names):
        P, R = pk[8 * i: 8 * i + 8], rf[8 * i: 8 * i + 8]
        pr = pred[tohkey(c)]
        if pred2[tohkey(c)] != pr: npd += 1; print("PREDICTOR MISMATCH", c, pr, pred2[tohkey(c)])
        if P != R: ndis += 1; print("SOLVER MISMATCH", c, P, R)
        d = [k for k in range(8) if P[k] != pr[k]]
        if not d: nag += 1
        else: diffs.append((c, [(LAB[k], pr[k], P[k]) for k in d]))
        verdict = "agree" if not d else "DIFFER at " + ", ".join(LAB[k] for k in d)
        fh.write(f"{c:22s} P {' '.join(P)}  ref3m {' '.join(R)}  pred {' '.join(pr)}  {verdict}\n")
npos = sum(len(x[1]) for x in diffs)
fav = {"Black": 0, "White": 0}
for c, lst in diffs:
    for lab, p, q in lst: fav["Black" if O[q] < O[p] else "White"] += 1
print(f"{tag}: contexts {len(names)}; agree {nag}; differ {len(diffs)}; positions differing {npos} of {8 * len(names)}; "
      f"in favour of {fav}; pk/ref3m mismatches {ndis}; predictor mismatches {npd}")
for c, lst in diffs: print("  DIFF", c, lst)
