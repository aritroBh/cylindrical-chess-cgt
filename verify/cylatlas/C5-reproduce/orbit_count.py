"""Count symmetry orbits of raw ring atoms (independent enumeration) and compare
with the worker's ring counts (atlas records with ring=1, count/ep1).
  cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/cylatlas/C5-reproduce/orbit_count.py
"""
import os, sys, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_scan as S
HERE = os.path.dirname(os.path.abspath(__file__))
mine = collections.Counter()
for n in (3, 4, 5):
    S.CFG.clear(); S.CFG.update(n=n, wrap=True, ep=True, rule="count")
    grp = [tuple((s * f + k) % n for f in range(n)) for s in (1, -1) for k in range(n)]
    for np_ in range(2, 6):
        seen = set()
        for W, B in S.atoms(n, True, np_):
            Wf, Bf = frozenset(W), frozenset(B)
            if S.has_passer("W", Wf, Bf) or S.has_passer("B", Wf, Bf):
                continue
            key = min((tuple(sorted((g[f], r) for f, r in W)), tuple(sorted((g[f], r) for f, r in B))) for g in grp)
            seen.add(key)
        mine[n] += len(seen)
theirs = collections.Counter()
for fn in glob.glob(os.path.join(HERE, "ex_main/parts/cyl*_all_*.jsonl")):
    for line in open(fn):
        p = json.loads(line)
        if p["ring"]:
            theirs[p["n"]] += 1
for n in (3, 4, 5):
    print(f"cyl{n} rings w+b<=5: independent orbits={mine[n]}  worker atlas ring records={theirs[n]}")
