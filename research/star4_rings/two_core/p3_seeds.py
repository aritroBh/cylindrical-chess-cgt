# Stage A: width-5/6 truncations of the big (width 7/8) typed cores + known width-6 cores; probe 4 wall types each.
import sys
from p3lib import *
ev = Evaluator("results_p3.tsv", tbits=22, nodelim=2000000, extra=("results.tsv", "results_blocks.tsv"))
lg = Log("p3_hits.tsv")
big = json.load(open("lib_big_ok.json"))
seeds = []
cores = [x for x in big if x['v'] >= 1]
blocks = set()
for x in cores:
    t = x['block'].split(); w0 = len(t)
    for keep in (6, 5):
        if w0 <= keep: continue
        for idx in itertools.combinations(range(w0), keep):
            blocks.add(tuple(t[i] for i in idx))
        # also contiguous cyclic windows (cuts) are covered since idx combos include contiguous windows
for s in ("W5 B7 W4 W4B7 B6 W3B6", "W4 B7 W3B6 W3 W2B5 B5"):
    blocks.add(tuple(s.split()))
blocks = sorted(blocks, key=lambda b: (-len(b), b))
print(len(blocks), "truncation blocks", flush=True)
out = open("p3_seeds.tsv", "w")
cnt = 0
for blk in blocks:
    blk = list(blk)
    res = probe(ev, lg, "trunc", blk)
    # stable nimber >= 2 test at confirm lengths
    for (f, L), sig in res.items():
        v = nimber(sig)
        if isinstance(v, int) and v >= 2:
            f2, L2 = CONFIRM[(f, L)]
            full = blk + wall(L2, f2)
            s2 = ev.sig(full) if legal_start(full) else "ILLEGAL"
            out.write(f"{S(blk)}\t{f}\t{L}\t{sig}\t{f2}\t{L2}\t{s2}\n"); out.flush()
    cnt += 1
    if cnt % 200 == 0: print(cnt, dict(lg.hist), flush=True)
print("done", cnt, dict(lg.hist))
