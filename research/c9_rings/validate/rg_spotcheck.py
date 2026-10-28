#!/usr/bin/env python3
"""rg_spotcheck.py RINGS SIGS.gz N -- re-solve the first N rings of RINGS (enumeration order) with the ORIGINAL rg
(../../ring_family_proof/rg solve 3, TBITS=21, batches of 40, nice 15) and compare with the signatures the driver recorded
(sigs.gz, same order)."""
import sys, os, gzip, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
RG = os.path.join(HERE, "..", "..", "ring_family_proof", "rg")
rings = [l.strip() for l in open(sys.argv[1]) if l.strip()]
sigs = [l.strip() for l in gzip.open(sys.argv[2], "rt")]
n = int(sys.argv[3])
assert len(rings) == len(sigs), (len(rings), len(sigs))
step = max(1, len(rings) // n)
idx = list(range(0, len(rings), step))[:n]
bad = 0; checked = 0
for i in range(0, len(idx), 40):
    b = idx[i:i + 40]
    p = subprocess.run(["nice", "-n", "15", RG, "solve", "3"], input="\n".join(rings[j] for j in b) + "\n",
                       capture_output=True, text=True, env=dict(os.environ, TBITS="21"))
    out = [l.split()[0] for l in p.stdout.splitlines() if l.strip()]
    if p.returncode != 0 or len(out) != len(b):
        raise SystemExit("rg failed rc=%d outputs %d of %d" % (p.returncode, len(out), len(b)))
    for j, o in zip(b, out):
        checked += 1
        if o != sigs[j]:
            bad += 1
            print("MISMATCH", rings[j], sigs[j], o)
print("re-solved %d rings (every %d-th of %d) with the original rg: %d mismatches" % (checked, step, len(rings), bad))
