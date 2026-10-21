"""Random positions: does 'textbook ab.c and e.p.-aware abx1 differ (result or nodes)' imply ab.c ep_events > 0?"""
import random, subprocess, sys
D = "/Users/aritro/Downloads/Research/Chessendgames/verify/bench/C3-reproduce"
rng = random.Random(int(sys.argv[1])); N = int(sys.argv[2])
def nb(W, wrap, f, d):
    g = f + d
    return g % W if wrap else (g if 0 <= g < W else None)
def passer(W, wrap, mine, theirs, white):
    for f, r in mine:
        fs = {f, nb(W, wrap, f, -1), nb(W, wrap, f, 1)} - {None}
        if not any(g in fs and ((s > r) if white else (s < r)) for g, s in theirs):
            return True
    return False
jobs = []
while len(jobs) < N:
    W = rng.randint(2, 7); wrap = rng.random() < 0.5
    nw, nbk = rng.randint(1, 4), rng.randint(1, 4)
    sqs = [(f, r) for f in range(W) for r in range(2, 8)]
    pick = rng.sample(sqs, min(len(sqs), nw + nbk))
    w, b = pick[:nw], pick[nw:]
    # bias: put some white pawns on rank 2 and black on rank 7 so double steps happen
    if passer(W, wrap, w, b, True) or passer(W, wrap, b, w, False):
        continue
    for side in (1, 0):
        for tt in (0, 1):
            jobs.append(f"{W} {int(wrap)} {side} {tt} 3000000 0 {len(w)} " + " ".join(f"{f} {r}" for f, r in sorted(w))
                        + f" {len(b)} " + " ".join(f"{f} {r}" for f, r in sorted(b)))
inp = "\n".join(jobs) + "\n"
A = subprocess.run([f"{D}/ab_mine"], input=inp, capture_output=True, text=True, check=True).stdout.split("\n")
X = subprocess.run([f"{D}/abx1"], input=inp, capture_output=True, text=True, check=True).stdout.split("\n")
from collections import Counter
c = Counter(); viol = []
for j, a, x in zip(jobs, A, X):
    a, x = a.split(), x.split()
    if a[0] == "0" or x[0] == "0":
        c["capped"] += 1; continue
    diff_res, diff_nodes, ev = a[0] != x[0], a[1] != x[1], int(a[3])
    c["jobs"] += 1
    c["result differs"] += diff_res
    c["nodes differ"] += diff_nodes
    c["counter>0"] += ev > 0
    c["counter>0 but identical"] += ev > 0 and not diff_nodes and not diff_res
    if (diff_res or diff_nodes) and ev == 0:
        viol.append(j)
print(dict(c), "VIOLATIONS:", len(viol))
for v in viol[:10]: print(v)
