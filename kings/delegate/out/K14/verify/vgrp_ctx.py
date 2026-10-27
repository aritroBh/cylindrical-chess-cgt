import json, sys, collections, subprocess
sys.path.insert(0, '.')
from vpawn import *
grp = json.loads(sys.argv[1]); ctxfile = sys.argv[2]
ctxs = [json.loads(l) for l in open(ctxfile)]
roots, meta = [], []
for i, c in enumerate(ctxs):
    x = (tuple(sorted(sq(n) for n in c['w'])), tuple(sorted(sq(n) for n in c['b'])), None)
    pred = closed(x)
    for a in (0, 1):
        for b in (0, 1):
            for s in 'wb':
                roots.append(' '.join(['K' + grp['KW'][a], 'k' + grp['KB'][b]] + grp['ZP'] + ['P' + n for n in c['w']] + ['p' + n for n in c['b']] + [s, '-']))
                meta.append((i, pred[0 if s == 'w' else 1]))
out = subprocess.run(['./kpp', '--board', 'flat:7x6', '--ep', 'on', '--promote', 'QRBN', '--cap', '1', '--pmodel'], input='\n'.join(roots)+'\n', capture_output=True, text=True).stdout.strip().split('\n')
bad_ctx = set(); bad_roots = 0; contra = 0
for (i, pred), l in zip(meta, out):
    A, B = l.split(' | ')[1].split()
    assert A == B and A != 'X', l
    if A != pred:
        bad_ctx.add(i); bad_roots += 1
        if pred != 'D': contra += 1
print(ctxfile, 'contexts', len(ctxs), 'failing contexts', len(bad_ctx), 'failing roots', bad_roots, 'of', len(meta), 'predicted W/L contradicted:', contra)
