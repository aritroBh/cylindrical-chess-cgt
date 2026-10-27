# Original rg on every width<=6 core ring (nimber 2 or 3 at some wall length 4..9) and on the width<=6 rings with the largest values.
import subprocess, os, glob
from lib import *
cache = {}
for f in glob.glob("results*.tsv"):
    for line in open(f):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 3 and p[1] not in ("ABORT", "FULL"): cache[p[0]] = p[1]
sel = []
for fn in ("cores_w6_nimber3.tsv", "cores_w6_nimber2.tsv"):
    for line in list(open(fn))[1:]:
        blk, w, f, vals, stable = line.rstrip("\n").split("\t")
        for L in range(4, 10):
            full = R(blk) + wall(L, f)
            if legal_start(full) and canon(full) in cache: sel.append(canon(full))
sel = list(dict.fromkeys(sel))
print("verifying", len(sel), flush=True)
def run(batch):
    env = dict(os.environ, TBITS="23")
    p = subprocess.run(["nice", "-n", "15", "./rg", "solve", "7"], input="\n".join(batch) + "\n", text=True, capture_output=True, env=env)
    return [l.split()[0] for l in p.stdout.splitlines() if l.strip()]
mism = []; done = 0; bystat = {}
for i in range(0, len(sel), 30):
    batch = sel[i:i + 30]; out = run(batch)
    if len(out) != len(batch):
        out = []
        for s in batch:
            o = run([s]); out.append(o[0] if o else "FAIL")
    for s, o in zip(batch, out):
        done += 1
        if o != cache[s]: mism.append((s, cache[s], o))
        v = nimber(o); bystat[v if isinstance(v, int) else 'nonnim'] = bystat.get(v if isinstance(v, int) else 'nonnim', 0) + 1
print("checked", done, "mismatches", len(mism), "original-rg value histogram", bystat)
for m in mism[:10]: print(m)
open("verify2_result.txt", "w").write(f"checked {done} width<=6 core rings with the original rg; mismatches {len(mism)}; histogram {bystat}\n" + "\n".join(map(str, mism)) + "\n")
