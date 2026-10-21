"""Compare my independently computed value sets with the worker's C3 claim.

  cd /Users/aritro/Downloads/Research/Chessendgames/verify/cylatlas/C3-refute && \
  ../../../.venv/bin/python -I analyze_mine.py > analyze_mine.txt
"""
import json
from collections import defaultdict

R = json.load(open("results.json"))
A = R["atoms"]
S = R["sums"]


def atom(kind, s, p):
    return A.get(f"{kind}{s}_p{p}", {}).get("values", {})


big = {}
wit = {}
for name, d in A.items():
    for k, e in d["values"].items():
        big[k] = e["big"]
        wit.setdefault(k, (name, e["wit"]))
for k, e in S.items():
    big.setdefault(k, e["big"])
    assert big[k] == e["big"]
    wit.setdefault(k, ("sum", e["wit"]))


def flat(n, safe_only=False):
    out = set()
    for s in range(1, min(n, 5) + 1):
        for p in range(2, 6):
            out |= set(atom("flat", s, p))
    for k, e in S.items():
        w = e["min_width_safe"] if safe_only else e["min_width"]
        if w is not None and w <= n:
            out.add(k)
    return out


def ring(n):
    out = set()
    for p in range(n, 6):
        out |= set(atom("ring", n, p))
    return out


def cyl(n, safe_only=False):
    return flat(n - 1, safe_only) | ring(n)


nw = lambda X: sum(1 for k in X if not big[k])
print("## My T1 (value counts; w+b<=5, count rule, e.p. on)")
print("| n | cyl values | flat values | cyl-only nonW / W | flat-only nonW / W |")
for n in range(3, 9):
    Cn, Fn = cyl(n), flat(n)
    co, fo = Cn - Fn, Fn - Cn
    print(f"| {n} | {len(Cn)} | {len(Fn)} | {nw(co)} / {len(co)-nw(co)} | {nw(fo)} / {len(fo)-nw(fo)} |")
allC = set().union(*(cyl(n) for n in range(3, 9)))
allF = set().union(*(flat(n) for n in range(3, 9)))
glob = allC - allF
print(f"\nflat8 == union flats: {flat(8) == allF}; cyl8 == flat8: {cyl(8) == flat(8)}; cyl7 == flat7: {cyl(7) == flat(7)}")
print(f"cyl-only (union): {len(glob)} values, {nw(glob)} without W")
print(f"flat-only (union): {len(allF - allC)}")
by = defaultdict(list)
for k in glob:
    if big[k]:
        continue
    n0 = min(n for n in range(3, 9) if k in cyl(n))
    by[n0].append(k)
print("by smallest cylinder width:", {n: len(v) for n, v in sorted(by.items())})
for n in sorted(by):
    for k in sorted(by[n]):
        print(f"  n={n}  {k}   {wit[k]}")

# worker's sets, rebuilt from their data files (for comparison only)
idx = {}
for line in open("../../../atlas/cylinder/value_index.jsonl"):
    d = json.loads(line)
    idx[d["vid"]] = d
wsets = defaultdict(set)
for line in open("../../../atlas/cylinder/values.jsonl"):
    r = json.loads(line)
    if r["w"] + r["b"] > 5:
        continue
    wsets[(r["board"], r["n"])].add(idx[r["vid"]]["key"])
print("\n## exact comparison of value-key sets with the worker's values.jsonl")
for n in range(3, 9):
    for bd, mine in (("cyl", cyl(n)), ("flat", flat(n))):
        w = wsets[(bd, n)]
        print(f"{bd}{n}: mine={len(mine)} worker={len(w)} equal={mine == w} only_mine={len(mine - w)} only_worker={len(w - mine)}")
wC = set().union(*(wsets[("cyl", n)] for n in range(3, 9)))
wF = set().union(*(wsets[("flat", n)] for n in range(3, 9)))
wbig = {d["key"]: d["big"] for d in idx.values()}
wg = {k for k in wC - wF if not wbig[k]}
mg = {k for k in glob if not big[k]}
print(f"worker cyl-only nonW: {len(wg)}; mine: {len(mg)}; identical key sets: {wg == mg}")
print(f"has-W flags agree on all common keys: {all(wbig[k] == big[k] for k in set(big) & set(wbig))}")

# sensitivity: drop two-component flat roots whose components can reach opposite-colour passers
print("\n## sensitivity: exclude 'unsafe' flat sums (one summand can reach +W and the other -W)")
fs = set().union(*(flat(n, True) for n in range(3, 9)))
cs = set().union(*(cyl(n, True) for n in range(3, 9)))
g2 = {k for k in cs - fs if not big[k]}
print(f"cyl-only nonW with safe sums only: {len(g2)} (vs {len(mg)})")
for k in sorted(g2 - mg):
    print("  extra:", k, wit[k], S.get(k, {}).get("wit"))
# which nonW ring values are in the flat set only through sums
viasum = []
for n in (3, 4, 5):
    for k in ring(n):
        if big[k] or k in glob:
            continue
        single = any(k in atom("flat", s, p) for s in range(1, 6) for p in range(2, 6))
        if not single:
            viasum.append((n, k, S[k]["wit"], S[k]["min_width_safe"]))
print(f"nonW ring values present on flat strips only as two-component sums: {len(viasum)}")
for x in sorted(set(viasum)):
    print("  ", x)
