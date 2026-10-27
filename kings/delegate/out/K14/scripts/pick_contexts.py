"""Enumerate pawn-only contexts on files e..g of flat 7x6 (<= 2+2 pawns, ranks 2..5), solve G (+) dud_D with
dmodel.py, and print a spread of representatives (JSON lines): fields w, b (pawn names), dud, on."""
import itertools, json, sys, random
sys.path.insert(0, 'scripts')
from dmodel import Ctx, solve
W, H = 7, 6
ctx = Ctx(W, H, True)
sqn = [chr(97 + f) + str(r + 1) for f in (4, 5, 6) for r in range(1, 5)]
def S(ns): return {(int(n[1:]) - 1) * W + ord(n[0]) - 97 for n in ns}
reps = {}
random.seed(14)
allc = []
for kw in range(0, 3):
    for kb in range(0, 3):
        for wn in itertools.combinations(sqn, kw):
            for bn in itertools.combinations(sqn, kb):
                if set(wn) & set(bn): continue
                allc.append((wn, bn))
random.shuffle(allc)
cnt = {}
for wn, bn in allc:
    d = solve(ctx, S(wn), S(bn), -1, 'dud'); o = solve(ctx, S(wn), S(bn), -1, 'on')
    key = (d[0], d[1], o[0], o[1])
    cnt[key] = cnt.get(key, 0) + 1
    if len(reps.setdefault(key, [])) < 3: reps[key].append((wn, bn))
print(len(allc), file=sys.stderr)
for k, v in sorted(cnt.items()): print(k, v, file=sys.stderr)
for k, lst in sorted(reps.items()):
    for wn, bn in lst:
        print(json.dumps({'w': wn, 'b': bn, 'dud': k[:2], 'on': k[2:]}))
