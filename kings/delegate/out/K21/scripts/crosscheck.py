"""K21: CHECKED-2 cross-check: Python (dsum.py) vs C (sumsolve.c) on the root tuple, D-result and CGT outcome."""
import sys, random, subprocess, json, os
from dsum import *
import run_tests as rt
N, seed, B = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)
here = os.path.dirname(os.path.abspath(__file__))
insts = []
for _ in range(N):
    comps = rt.rand_instance(rng)
    insts.append([c.prune() for c in comps])
def fmt(comps):
    s = "%d %d\n" % (B, len(comps))
    for c in comps:
        s += "%d %d\n" % (c.n, c.root)
        for x in range(c.n):
            s += "%d %s %d %s\n" % (len(c.L[x]), " ".join(map(str, c.L[x])), len(c.R[x]), " ".join(map(str, c.R[x])))
    return s
inp = "".join(fmt(c) for c in insts)
ALL = os.environ.get("K21_ALL")
out = subprocess.run([os.path.join(here, "..", "bin", "sumsolve")], input=inp, capture_output=True, text=True, env=dict(os.environ)).stdout.strip().split("\n")
assert len(out) == N, (len(out), N)
bad = 0; nonD = 0; ndiff = 0
import itertools
nstates = 0
for comps, line in zip(insts, out):
    if ALL:
        toks = line.split()
        d = d_results(comps); c_ = cgt_results(comps, B)
        ns = [c.n for c in comps]
        # mixed radix order: first component fastest
        idx = {}
        for tt, tup in enumerate(itertools.product(*[range(n) for n in reversed(ns)])):
            idx[tuple(reversed(tup))] = tt
        for tup in d_keys if False else {k[0] for k in d}:
            t = toks[idx[tup]]
            for m in (0, 1):
                nstates += 1
                if (d[(tup, m)], c_[(tup, m)]) != (t[m], t[2 + m]): bad += 1
        continue
    a = line.split()
    root = tuple(c.root for c in comps)
    d = d_results(comps); c_ = cgt_results(comps, B)
    py = [d[(root, 0)], d[(root, 1)], c_[(root, 0)], c_[(root, 1)]]
    if py != a: bad += 1
    if py[:2] != py[2:]: ndiff += 1
    if "D" in py: nonD += 1
print(json.dumps({"exp": "crosscheck_py_vs_c" + ("_all_states" if ALL else ""), "N": N, "seed": seed, "B": B, "states_compared": nstates, "disagreements": bad, "instances_with_D_vs_CGT_difference": ndiff, "instances_with_a_draw": nonD}))
