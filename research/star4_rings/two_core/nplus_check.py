# The all-N signature (G+*h is N for h=0..7) is ambiguous: it also covers nimbers *8 and above.  Re-run all-N single-core rings
# of width <= 6 with H=11 (h up to 11) and look for a P at h = 8..11.  Time-limited random order.
import sys, glob, random, time
from lib import *
random.seed(4)
LIM = float(sys.argv[1]) * 60
cands = []
for f in ("results_p3.tsv", "results_p3_0.tsv", "results_p3_r2.tsv") + tuple(sorted(glob.glob("results_p3b_*.tsv"))) + ("results_blocks.tsv",):
    if not os.path.exists(f): continue
    for line in open(f):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 3 and p[1] == "NNNNNNNN": cands.append(p[0])
cands = list(dict.fromkeys(cands)); random.shuffle(cands)
# prefer rings that came from the p3 stages (they contain wide blocks): keep order random but put n>=9 first
print(len(cands), "all-N rings", flush=True)
w = Worker(tbits=22, nodelim=1000000, H=11)
out = open("nplus_h11.tsv", "a"); t0 = time.time(); n = 0; hist = {}
for ring in cands:
    if time.time() - t0 > LIM: break
    sig, nodes = w.eval(ring)
    out.write(f"{ring}\t{sig}\t{nodes}\n"); n += 1
    key = sig if sig.count('P') else ("allN" if set(sig) == {'N'} else "other:" + sig[:6])
    hist[key] = hist.get(key, 0) + 1
    if 'P' in sig or sig.count('N') != len(sig): print("INTERESTING", ring, sig, flush=True)
    if n % 500 == 0: out.flush(); print(n, hist, flush=True)
out.close(); w.close()
print("checked", n, "of", len(cands), hist)
