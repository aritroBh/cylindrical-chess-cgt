import json, sys, itertools
sys.path.insert(0, '.')
from vpawn import *
ctxs = [json.loads(l) for l in open('../logs/small_contexts_fg.jsonl')]
print(len(ctxs), 'contexts in file')
pairs = {}
roots = []
meta = []
for i, c in enumerate(ctxs):
    wn = tuple(sorted(sq(n) for n in c['w'])); bn = tuple(sorted(sq(n) for n in c['b']))
    x = (wn, bn, None)
    pred = closed(x)
    O, stage = solve(x)
    pred2 = (res_of(stage, (x, 0)), res_of(stage, (x, 1)))
    assert pred == pred2, (c, pred, pred2)
    pairs[pred] = pairs.get(pred, 0) + 1
    if list(pred) != c['dud']:
        print('PRED MISMATCH vs agent', c, pred)
    for a in ('a5', 'a6'):
        for b in ('c5', 'c6'):
            for s in 'wb':
                roots.append(' '.join(['K' + a, 'k' + b, 'Pb3', 'pb4', 'pb5'] + ['P' + n for n in c['w']] + ['p' + n for n in c['b']] + [s, '-']))
                meta.append((i, a, b, s, pred[0 if s == 'w' else 1]))
open('ctx_roots.txt', 'w').write('\n'.join(roots) + '\n')
json.dump(meta, open('ctx_meta.json', 'w'))
print('outcome pairs among contexts:', pairs, 'roots', len(roots))
