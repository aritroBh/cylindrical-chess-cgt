# Unbiased baseline: uniformly random legal blocks (tokens uniform over V35, width 4/5/6, wall type uniform over W4,B4,W5,B5),
# time-limited.  Gives the density of nimbers among width<=6 single-core rings.
import sys, time
from p3lib import *
LIM = float(sys.argv[1]) * 60; SEED = int(sys.argv[2])
random.seed(SEED)
ev = Evaluator("results_p3s.tsv", tbits=22, nodelim=2000000, extra=("results.tsv", "results_blocks.tsv"))
lg = Log("p3_sample_hits.tsv")
t0 = time.time(); n = 0; hist = {4: Counter(), 5: Counter(), 6: Counter()}; tried = 0
while time.time() - t0 < LIM:
    w = random.choice((4, 5, 6)); blk = [random.choice(V35) for _ in range(w)]; f, L = random.choice(TYPES)
    tried += 1
    full = blk + wall(L, f)
    if not legal_start(full): continue
    sig = ev.sig(full); lg.rec("sample", blk, f, L, sig); n += 1
    v = nimber(sig); hist[w][v if isinstance(v, int) else ('N+' if v == 'N+' else 'other')] += 1
    if sig[:5] == 'NNNNP': print("STAR4-PATTERN", S(blk), f, L, sig, flush=True)
    if n % 2000 == 0: print(n, tried, {k: dict(v) for k, v in hist.items()}, flush=True)
print("done legal", n, "tried", tried, {k: dict(v) for k, v in hist.items()})
