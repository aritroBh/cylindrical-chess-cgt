"""Auditor B: are the builder's test games / candidates / negations / integers bisimilar to my
spec-derived ones?  (Greatest-fixed-point bisimulation on rooted two-player graphs.)"""
import sys, os
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); K4 = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, K4)
import v_games as vg
import testgames as tg

def mine_to_lists(g):
    root, d = g
    names = list(d); ix = {k: i for i, k in enumerate(names)}
    return ([[ix[x] for x in d[k][0]] for k in names], [[ix[x] for x in d[k][1]] for k in names], ix[root])

def theirs_to_lists(g):
    return (g.lopts, g.ropts, g.start)

def bisimilar(A, B):
    la, ra, sa = A; lb, rb, sb = B
    rel = {(i, j) for i in range(len(la)) for j in range(len(lb))}
    changed = True
    while changed:
        changed = False
        for (i, j) in list(rel):
            ok = True
            for oa, ob in ((la, lb), (ra, rb)):
                if not all(any((x, y) in rel for y in ob[j]) for x in oa[i]): ok = False
                if not all(any((x, y) in rel for x in oa[i]) for y in ob[j]): ok = False
            if not ok:
                rel.discard((i, j)); changed = True
    return (sa, sb) in rel

bad = 0
for t in vg.TESTS:
    ok = bisimilar(mine_to_lists(vg.GAMES[t]), theirs_to_lists(tg.GAMES[t]))
    bad += not ok; print('test game %-5s bisimilar: %s' % (t, ok))
mc = dict(vg.candidates()); tc = dict(tg.candidates())
assert list(mc) == list(tc), (list(mc), list(tc))
for n in mc:
    ok = bisimilar(mine_to_lists(mc[n]), theirs_to_lists(tc[n])); bad += not ok
    ok2 = bisimilar(mine_to_lists(vg.neg(mc[n])), theirs_to_lists(tg.neg(tc[n]))); bad += not ok2
    print('candidate %-9s V bisimilar: %s   -V bisimilar: %s' % (n, ok, ok2))
for k in range(-10, 11):
    ok = bisimilar(mine_to_lists(vg.integer(k)), theirs_to_lists(tg.integer(k))); bad += not ok
print('integers -10..10 bisimilar:', bad == 0 or 'see above')
print('NOT bisimilar count:', bad)
