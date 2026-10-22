import sys, glob, collections
sys.path.insert(0, "research/ring_family")
from ringlib import *
rows = []
for f in sorted(glob.glob("research/star26_rings/c7/p10_5_5/c*.hits.tsv")) + sorted(glob.glob("research/star26_rings/c7/p10_4_6/c*.hits.tsv")):
    for l in open(f):
        l = l.rstrip("\n")
        if l and not l.startswith("#"):
            p = l.split("\t"); rows.append((p[0], p[3]))
cls = collections.defaultdict(list)
for t, v in rows: cls[(canon(to_ring(t, 7)), v)].append(t)
print(len(rows), "hit rows (5+5 and 4+6 so far),", len(cls), "classes (rotation/reflection/colour reversal)")
by = collections.Counter(v for (c, v) in cls)
print(dict(by))
# verify with ringeval
bad = 0
for (c, v), ts in sorted(cls.items(), key=lambda kv: (kv[0][1], cstr(kv[0][0]))):
    r = evaluate([c])[0]
    ok = (f"{r[0]},{r[1]}" == v)
    if not ok: bad += 1
    print(v, len(ts), cstr(c), "" if ok else f"  MISMATCH {r}")
print("mismatches", bad)
