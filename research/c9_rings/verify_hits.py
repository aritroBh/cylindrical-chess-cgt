#!/usr/bin/env python3
"""verify_hits.py DIR OUT.tsv -- re-solve every hit ring found under DIR with the ORIGINAL rg binary
(../ring_family_proof/rg, TBITS=21, fresh process per batch of <= 40 rings, nice 15) and check
(a) the signature equals the one recorded by drive.py,
(b) the colour-reversed ring (white <-> black, rank r <-> 9-r) gives the same signature with L and R exchanged (for hits: the same),
(c) whether the colour-reversed ring is itself among the recorded hits (5+5 only: the split is closed under colour reversal).
Writes OUT.tsv with one row per distinct hit orbit."""
import sys, os, glob, subprocess, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("merge", os.path.join(HERE, "merge.py")); mg = importlib.util.module_from_spec(spec); spec.loader.exec_module(mg)
RG = os.path.join(HERE, "..", "ring_family_proof", "rg")

def solve(rings):
    out = []
    for i in range(0, len(rings), 40):
        b = rings[i:i + 40]
        p = subprocess.run(["nice", "-n", "15", RG, "solve", "3"], input="\n".join(b) + "\n", capture_output=True, text=True,
                           env=dict(os.environ, TBITS="21"))
        sigs = [l.split()[0] for l in p.stdout.splitlines() if l.strip()]
        if p.returncode != 0 or len(sigs) != len(b):
            raise SystemExit("original rg failed on a batch (rc=%d, %d of %d outputs)" % (p.returncode, len(sigs), len(b)))
        out += sigs
    return out

def mirror(r):
    p = subprocess.run([sys.executable, "-I", os.path.join(HERE, "mirror.py")], input=r + "\n", capture_output=True, text=True)
    return p.stdout.strip()

root, outfn = sys.argv[1], sys.argv[2]
hits = {}
for fn in glob.glob(os.path.join(root, "**", "*.hits.tsv"), recursive=True):
    for l in open(fn):
        if l.strip():
            r, sig, nd = l.rstrip("\n").split("\t")
            hits[r] = sig
rings = sorted(hits)
orig = solve(rings)
mir = [mirror(r) for r in rings]
mirsig = solve(mir)
hs = set(mg.canon(r) for r in rings)
bad = 0
with open(outfn, "w") as f:
    f.write("ring\tsig_drive\tsig_original_rg\tmirror_ring\tsig_mirror\tmirror_in_hit_list\n")
    for r, o, m, ms in zip(rings, orig, mir, mirsig):
        ok = (o == hits[r]) and (ms == hits[r])
        bad += (not ok)
        f.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (r, hits[r], o, m, ms, "yes" if mg.canon(m) in hs else "no"))
print("hits %d, signature mismatches %d" % (len(rings), bad))
