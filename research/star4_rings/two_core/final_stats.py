import glob, json
from collections import Counter
from lib import *
cache = {}
aborts = 0
for f in sorted(glob.glob("results*.tsv")):
    for line in open(f):
        p = line.rstrip("\n").split("\t")
        if len(p) < 3: continue
        if p[1] in ("ABORT", "FULL"): aborts += 1; continue
        cache[p[0]] = (p[1], int(p[2]))
print("unique canonical rings evaluated (decided):", len(cache), " budget-aborted evaluations (not counted):", aborts)
c = Counter(); lead = Counter()
star4 = []; nearly = []
for k, (s, n) in cache.items():
    v = nimber(s)
    c[v if isinstance(v, int) else ('N+' if v == 'N+' else 'non-nimber')] += 1
    if s == 'NNNNPNNN': star4.append(k)
    if sig_ok := (s[:4] == 'NNNN' and s != 'NNNNNNNN'): nearly.append((k, s))
    lead[lead_n(s)] += 1
print("counts by value:", dict(sorted(c.items(), key=lambda x: str(x[0]))))
print("leading N-run histogram:", dict(sorted(lead.items())))
print("star4 (NNNNPNNN):", star4)
print("signatures starting NNNN other than all-N:", nearly[:20], len(nearly))
nn = Counter(len(k.split()) for k in cache); print("by number of files:", dict(sorted(nn.items())))
json.dump(dict(total=len(cache), counts={str(k): v for k, v in c.items()}, aborts=aborts, star4=star4, nearly=nearly[:50]), open("final_stats.json", "w"))
