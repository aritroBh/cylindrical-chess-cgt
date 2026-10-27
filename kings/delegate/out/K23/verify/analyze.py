import sys, collections
# analyze.py WIDTH PFILE FFILE : own analysis. context = pawn tokens after the first 4 Z tokens. Own passed-pawn test (textbook, context pawns only, cylinder wrap).
Wd = int(sys.argv[1]); P = {}; F = {}
def load(fn, d):
    for l in open(fn):
        pos, r = l.rstrip('\n').rsplit(' | ', 1); t = pos.split()
        d.setdefault(' '.join(t[:-2]), {})[t[-2]] = r.split()[0]
load(sys.argv[2], P); load(sys.argv[3], F)
def parse(k):
    t = k.split()[4:]
    wp = [(ord(x[1]) - 97, int(x[2:])) for x in t if x[0] == 'P']
    bp = [(ord(x[1]) - 97, int(x[2:])) for x in t if x[0] == 'p']
    return wp, bp
def passed(wp, bp):
    for f, r in wp:
        if not any((bf - f) % Wd in (0, 1, Wd - 1) and br > r for bf, br in bp): return True
    for f, r in bp:
        if not any((wf - f) % Wd in (0, 1, Wd - 1) and wr < r for wf, wr in wp): return True
    return False
n = len(P); diff = [k for k in P if (P[k]['w'], P[k]['b']) != (F[k]['w'], F[k]['b'])]
print('contexts', n, 'differ', len(diff), 'X results', sum(1 for k in P for s in 'wb' if P[k][s] == 'X'))
print('differ with passer', sum(1 for k in diff if passed(*parse(k))), 'passer-free differ', sum(1 for k in diff if not passed(*parse(k))))
pf = [k for k in P if not passed(*parse(k))]
print('passer-free contexts', len(pf))
eg = lambda k: any(f in (4, 6) for f, r in sum(parse(k), []))  # pawn on e or g
print('differ without a pawn on e or g:', sum(1 for k in diff if not eg(k)))
fonly = [k for k in P if all(f == 5 for f, r in sum(parse(k), []))]
print('contexts confined to f (incl. empty):', len(fonly), 'differ:', sum(1 for k in fonly if k in set(diff)))
# frozen LW passer-free that differ
lwd = [k for k in diff if not passed(*parse(k)) and (F[k]['w'], F[k]['b']) == ('L', 'W')]
print('passer-free, frozen (L,W), differ:', len(lwd))
pairs = 0
for k in lwd:
    if P[k]['w'] != 'L': pairs += 1
    if P[k]['b'] != 'W': pairs += 1
print('(context,stm) pairs where the frozen mover loses but not in P:', pairs)
import json; json.dump(lwd, open(sys.argv[2] + '.lwdiff.json', 'w'))
