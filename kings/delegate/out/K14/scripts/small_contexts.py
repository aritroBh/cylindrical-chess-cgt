"""All contexts with <= 3 pawns in total on files e..g (flat 7x6), solved in the D-model (dud and on); prints
representatives per outcome class, preferring few pawns.  Output JSON lines for harness.py."""
import itertools, json, sys
sys.path.insert(0, 'scripts')
from dmodel import Ctx, solve
W, H = 7, 6; ctx = Ctx(W, H, True)
sqn = [chr(97 + f) + str(r + 1) for f in (4, 5, 6) for r in range(1, 5)]
def S(ns): return {(int(n[1:]) - 1) * W + ord(n[0]) - 97 for n in ns}
reps = {}
for tot in range(0, 4):
    for kw in range(tot + 1):
        kb = tot - kw
        for wn in itertools.combinations(sqn, kw):
            for bn in itertools.combinations(sqn, kb):
                if set(wn) & set(bn): continue
                d = solve(ctx, S(wn), S(bn), -1, 'dud'); o = solve(ctx, S(wn), S(bn), -1, 'on')
                key = (d[0], d[1], o[0], o[1])
                if len(reps.setdefault(key, [])) < 4: reps[key].append((wn, bn))
for k, lst in sorted(reps.items()):
    for wn, bn in lst:
        print(json.dumps({'w': wn, 'b': bn, 'dud': k[:2], 'on': k[2:]}))
