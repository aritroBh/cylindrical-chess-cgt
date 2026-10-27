# Re-run selected rings with the ORIGINAL rg binary (built from the unmodified copy of rg.c, -DMAXN=64) and compare with the cached rgy/rgx signatures.
import subprocess, os, sys, random, glob, csv
from lib import *
random.seed(99)
cache = {}
for f in glob.glob("results*.tsv"):
    for line in open(f):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 3 and p[1] not in ("ABORT", "FULL"): cache[p[0]] = p[1]
sel = []
# (1) every ring that is a nimber >= 3 anywhere in the caches, and a sample of *2
by = {}
for k, s in cache.items():
    v = nimber(s)
    if isinstance(v, int): by.setdefault(v, []).append(k)
print({v: len(x) for v, x in sorted(by.items())})
sel += by.get(3, [])
sel += random.sample(by.get(2, []), min(60, len(by.get(2, []))))
sel += random.sample(by.get(1, []), min(40, len(by.get(1, []))))
sel += by.get(4, []) + by.get(5, []) + by.get(6, []) + by.get(7, [])
# (2) the minimal non-additive example and its length scan
A, B = R("W4 B7"), R("W4B6")
for L1 in (3, 5, 9, 11):
    sel.append(canon(A + wall(L1, 'B') + B + wall(3, 'W')))
# (3) sample of two-core rows
hdr = open("rows_header.txt").read().rstrip("\n").split("\t")
rows = []
for f in sorted(glob.glob("rows*_[0-9].tsv")):
    for line in open(f):
        p = line.rstrip("\n").split("\t")
        if len(p) == len(hdr): rows.append(dict(zip(hdr, p)))
good = [r for r in rows if r['ring_sig'] not in ('ILLEGAL', 'ABORT', 'FULL') and int(r['n']) <= 18]
nim = [r for r in good if r['ring_val'] != 'None']; dec = [r for r in good if r['ring_val'] == 'None']
for r in random.sample(nim, min(80, len(nim))) + random.sample(dec, min(60, len(dec))): sel.append(canon(r['ring'].split()))
sel = list(dict.fromkeys(sel))
sel = [s for s in sel if s in cache]
print("verifying", len(sel), "rings", flush=True)
bad = 0; done = 0
def run(batch):
    env = dict(os.environ, TBITS="23")
    p = subprocess.run(["nice", "-n", "15", "./rg", "solve", "7"], input="\n".join(batch) + "\n", text=True, capture_output=True, env=env)
    return [l.split()[0] for l in p.stdout.splitlines() if l.strip()]
mism = []
for i in range(0, len(sel), 30):
    batch = sel[i:i + 30]
    out = run(batch)
    if len(out) != len(batch):             # table full: fall back to one per call
        out = []
        for s in batch:
            o = run([s]); out.append(o[0] if o else "FAIL")
    for s, o in zip(batch, out):
        done += 1
        if o != cache[s]: mism.append((s, cache[s], o))
print("checked", done, "mismatches", len(mism))
for m in mism[:10]: print(m)
open("verify_result.txt", "w").write(f"checked {done} rings with the original rg; mismatches {len(mism)}\n" + "\n".join(map(str, mism)) + "\n")
