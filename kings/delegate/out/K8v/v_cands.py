import json, sys
import v_games as g
mine = {n: g.signature(V) for n, V in g.candidates()}
theirs = json.load(open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K8/candidates.json'))['candidates']
print('candidates mine/theirs:', len(mine), len(theirs))
bad = [n for n in mine if mine[n] != theirs.get(n)]
print('mismatching candidate signatures:', bad)
# equal-signature groups
inv = {}
for n, s in mine.items():
    inv.setdefault(s, []).append(n)
for s, ns in inv.items():
    if len(ns) > 1: print('same signature:', ns)
