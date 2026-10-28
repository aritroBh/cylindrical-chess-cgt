"""neighbours.py -- all legal root rings at 'distance 1' from the 4 hit classes (one pawn moved one rank), solved by the original rg (fresh builds identical); used to pick near-miss controls."""
import os, sys, subprocess
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ringtools as rt
RG = os.path.join(HERE, "..", "..", "ring_family_proof", "rg")
classes = [l.split("\t")[1] for l in open(os.path.join(HERE, "classes.tsv")).read().splitlines()[1:]]
out = []
for ci, c in enumerate(classes):
    ring = rt.parse(c); seen = set()
    for f, (w, b) in enumerate(ring):
        for side in (0, 1):
            for r in (w, b)[side]:
                for dr in (-1, 1):
                    nw, nb = list(w), list(b)
                    ls = (nw, nb)[side]; ls.remove(r); ls.append(r + dr)
                    new = list(ring); new[f] = (tuple(sorted(nw)), tuple(sorted(nb)))
                    new = tuple(new)
                    if rt.legality(new, 9, 10): continue
                    k = rt.canon_dihedral(new)
                    if k in seen: continue
                    seen.add(k); out.append((ci + 1, rt.fmt(new)))
inp = "\n".join(t for _, t in out) + "\n"
res = []
for i in range(0, len(out), 40):
    p = subprocess.run(["nice", "-n", "15", RG, "solve", "3"], input="\n".join(t for _, t in out[i:i+40]) + "\n", capture_output=True, text=True, env=dict(os.environ, TBITS="22"))
    res += [l.split() for l in p.stdout.splitlines() if l.strip()]
assert len(res) == len(out)
with open(os.path.join(HERE, "neighbours.tsv"), "w") as f:
    for (ci, t), r in zip(out, res):
        f.write("H%d\t%s\t%s\t%s\n" % (ci, t, r[0], r[1]))
import collections
print(collections.Counter((ci, r[0]) for (ci, _), r in zip(out, res)))
