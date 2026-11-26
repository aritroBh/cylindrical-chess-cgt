"""K75: compare the P values of two solvers (pk, ref3m) with each other and with the D-sum prediction.
(Adapted from kings/delegate/out/K72/src/cmp.py: second predictor is K75's pred75.py; class-dependent verdict.)

Usage (repository root):  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K75/src/cmp.py G F NN
Reads in/G_F_NN.names, logs/G_F_NN_pk.out, logs/G_F_NN_ref3m.out, logs/dpred.txt (K63 referee's predictor, <= 2 + 2),
logs/pred75_33.txt (K75's predictor, <= 3 + 3); writes logs/G_F_NN_table.txt, prints one summary line (SUM ...) and
one DIFF line per failing context.
Values are White's view (W, L, D).  Positions per context: A b, A w, B b, B w, qA b, qA w, qB b, qB w.
Prediction: r(w (+) X) at both roots, r(X) at both q's.  For a group of class AUXL (Aux lost at one bad move) only
two statements are proved (Theorem 4.18 (a)): q has the results of 0_D, and root <= w; the table still compares with
r(w (+) X) and marks a root result below it "below" (inside the proved bound) and above it "ABOVE" (outside).
"""
import sys

V = "kings/delegate/out/K75"
LAB = ["A b", "A w", "B b", "B w", "qA b", "qA w", "qB b", "qB w"]
O = {"L": 0, "D": 1, "W": 2}
g, f, nn = sys.argv[1:4]
tag = f"{g}_{f}_{nn}"
cls = [l.split("|")[2] for l in open(f"{V}/in/groups48.txt") if l.startswith(g + "|")][0]
names = [l.strip() for l in open(f"{V}/in/{tag}.names") if l.strip()]
tohkey = lambda c: c if c == "empty" else " ".join(t[0] + "h" + t[2:] for t in c.split())

def readpred(fn):
    d = {}
    for line in open(fn):
        if line.startswith("#"): continue
        p = line.split(); d[" ".join(p[:-8])] = p[-8:]
    return d
pred2 = readpred(f"{V}/logs/pred75_33.txt")
pred1 = readpred(f"{V}/logs/dpred.txt" if nn in ("11", "22") else f"{V}/logs/dpred33.txt")

pk = [l.split()[-3] for l in open(f"{V}/logs/{tag}_pk.out") if l.strip()]
rf = [l.rstrip().split("|")[-1].strip() for l in open(f"{V}/logs/{tag}_ref3m.out") if l.strip()]
assert len(pk) == len(rf) == 8 * len(names), (len(pk), len(rf), len(names))
nag = 0; ndis = 0; npd = 0; diffs = []; both = 0; onecol_fail = 0; above = 0
kinds = {}
with open(f"{V}/logs/{tag}_table.txt", "w") as fh:
    fh.write(f"# {tag} ({cls}): context | P (pk) | P (ref3m) | prediction (A b, A w, B b, B w, qA b, qA w, qB b, qB w)"
             f" | verdict\n")
    for i, c in enumerate(names):
        P, R = pk[8 * i: 8 * i + 8], rf[8 * i: 8 * i + 8]
        pr = pred1[tohkey(c)]
        if pred2[tohkey(c)] != pr: npd += 1; print("PREDICTOR MISMATCH", c, pr, pred2[tohkey(c)])
        if P != R: ndis += 1; print("SOLVER MISMATCH", c, P, R)
        d = [k for k in range(8) if P[k] != pr[k]]
        if not d: nag += 1
        else:
            diffs.append((c, [(LAB[k], pr[k], P[k]) for k in d]))
            cols = {t[0] for t in c.split()}
            if cols != {"P", "p"}: onecol_fail += 1
            for k in d:
                key = ("root" if k < 4 else "q") + " " + LAB[k][-1] + " " + ("Black" if O[P[k]] < O[pr[k]] else "White")
                kinds[key] = kinds.get(key, 0) + 1
                if cls.startswith("AUXL") and k < 4 and O[P[k]] > O[pr[k]]: above += 1
        tags = []
        for k in d:
            t = LAB[k]
            if cls.startswith("AUXL") and k < 4: t += " (below)" if O[P[k]] < O[pr[k]] else " (ABOVE)"
            tags.append(t)
        verdict = "agree" if not d else "DIFFER at " + ", ".join(tags)
        fh.write(f"{c:22s} P {' '.join(P)}  ref3m {' '.join(R)}  pred {' '.join(pr)}  {verdict}\n")
npos = sum(len(x[1]) for x in diffs)
ks = "; ".join(f"{k} {v}" for k, v in sorted(kinds.items()))
print(f"SUM {tag} {cls} contexts {len(names)} agree {nag} fail {len(diffs)} posdiff {npos} of {8 * len(names)} "
      f"one-colour-fails {onecol_fail} aux-root-above {above} pk/ref3m-mismatch {ndis} predictor-mismatch {npd} "
      f"kinds [{ks}]")
for c, lst in diffs: print("  DIFF", tag, c, lst)
