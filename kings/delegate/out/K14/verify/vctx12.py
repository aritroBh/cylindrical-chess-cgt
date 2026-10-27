import json, sys, collections, subprocess
sys.path.insert(0, '.')
from vpawn import *
ctxs = [json.loads(l) for l in open('../logs/ctx12.jsonl')]
roots, meta = [], []
for i, c in enumerate(ctxs):
    x = (tuple(sorted(sq(n) for n in c['w'])), tuple(sorted(sq(n) for n in c['b'])), None)
    pred = closed(x)
    assert list(pred) == c['dud'], (c, pred)
    for a in ('a5', 'a6'):
        for b in ('c5', 'c6'):
            for s in 'wb':
                roots.append(' '.join(['K'+a, 'k'+b, 'Pb3', 'pb4', 'pb5'] + ['P'+n for n in c['w']] + ['p'+n for n in c['b']] + [s, '-']))
                meta.append((i, pred[0 if s == 'w' else 1]))
out = subprocess.run(['./kpp', '--board', 'flat:7x6', '--ep', 'on', '--promote', 'QRBN', '--cap', '1', '--pmodel'], input='\n'.join(roots)+'\n', capture_output=True, text=True).stdout.strip().split('\n')
bad_ctx = set(); bad_roots = 0
for (i, pred), l in zip(meta, out):
    A, B = l.split(' | ')[1].split()
    assert A == B
    if A != pred:
        bad_ctx.add(i); bad_roots += 1
print('contexts', len(ctxs), 'failing contexts', len(bad_ctx), 'failing roots', bad_roots, 'of', len(meta))
for i in sorted(bad_ctx): print(ctxs[i]['w'], ctxs[i]['b'], ctxs[i]['dud'])
