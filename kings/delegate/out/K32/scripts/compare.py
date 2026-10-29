"""Compare pyref.py's class table with the per-node results of an eval run (stopsA 'eval p' or stopsB) on a graph dump.
Usage: compare.py graphs.txt results.txt pyref_classes.txt"""
import sys, ast
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K32/scripts")
from pyref import canon
graphs = [l.split() for l in open(sys.argv[1]) if l.strip()]
results = [l for l in open(sys.argv[2]) if l.startswith("G")]
ref = {}
for l in open(sys.argv[3]):
    if "|" not in l or l.startswith("classes"): continue
    k, r = l.rsplit("|", 1)
    ref[ast.literal_eval(k.strip())] = r.split()[:4]
assert len(graphs) == len(results), (len(graphs), len(results))
bad = checked = 0; seen = set()
for g, res in zip(graphs, results):
    n = int(g[0]); L = [[j for j in range(n) if int(g[1 + 2 * i]) >> j & 1] for i in range(n)]; R = [[j for j in range(n) if int(g[2 + 2 * i]) >> j & 1] for i in range(n)]
    toks = [t.split("]")[0].split() for t in res.split("[")[1:]]
    assert len(toks) == n
    for i in range(n):
        k = canon(L, R, i)
        want = ref[k]; got = toks[i]; checked += 1; seen.add(k)
        if [("99" if str(w) == "inf" else str(w)) for w in want] != got: bad += 1; print("MISMATCH", g, i, want, got)
print("node instances checked %d, distinct classes covered %d of %d, mismatches %d" % (checked, len(seen), len(ref), bad))
