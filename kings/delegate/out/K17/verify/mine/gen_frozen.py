import sys, itertools, json
from myd import *
spec, files, maxp, pre = sys.argv[1], [int(x) for x in sys.argv[2].split(',')], int(sys.argv[3]), sys.argv[4]
kind, dims = spec.split(':'); w, h = map(int, dims.split('x')); bd = Bd(w, h, kind == 'cyl'); whole = make(bd)
sqs = [(f, r) for f in files for r in range(2, h)]
def nm(s): return 'abcdefgh'[s[0]] + str(s[1])
nctx = 0; hits = []
for nw in range(1, maxp + 1):
    for ws in itertools.combinations(sqs, nw):
        rest = [s for s in sqs if s not in ws]
        for nb in range(1, maxp + 1):
            for bs in itertools.combinations(rest, nb):
                pos = (frozenset(ws), frozenset(bs), None)
                if passed(bd, pos[0], pos[1], None, 'W') or passed(bd, pos[0], pos[1], None, 'B'): continue
                nctx += 1
                if whole(pos, 'B') == 'B':
                    toks = ['Ka1', 'kb4', 'Pa3', 'pa4'] + ['P' + nm(s) for s in sorted(ws)] + ['p' + nm(s) for s in sorted(bs)]
                    hits.append(' '.join(toks) + ' b -')
json.dump(hits, open(pre + '.hits.json', 'w'))
print(spec, 'contexts', nctx, 'D(Black first)=Black', len(hits))
