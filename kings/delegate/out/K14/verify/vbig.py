import json, sys, subprocess, resource, itertools, collections
sys.path.insert(0, '.')
from vpawn import *
grp = json.loads(sys.argv[1]); name = sys.argv[2]; files = [int(x) for x in sys.argv[3].split(',')]; maxp = int(sys.argv[4]); chunk = int(sys.argv[5])
ctxs = list(contexts(files, maxp, maxp))
print(name, 'contexts', len(ctxs), file=sys.stderr)
def lim(): resource.setrlimit(resource.RLIMIT_CPU, (90, 90))
tot = collections.Counter(); badlist = []
for lo in range(0, len(ctxs), chunk):
    roots, meta = [], []
    for wn, bn in ctxs[lo:lo + chunk]:
        x = (wn, bn, None); pred = closed(x)
        for a in (0, 1):
            for b in (0, 1):
                for s in 'wb':
                    roots.append(' '.join(['K' + grp['KW'][a], 'k' + grp['KB'][b]] + grp['ZP'] + ['P' + chr(96 + f) + str(r) for f, r in wn] + ['p' + chr(96 + f) + str(r) for f, r in bn] + [s, '-']))
                    meta.append((wn, bn, pred[0 if s == 'w' else 1]))
    r = subprocess.run(['nice', '-n', '10', './kpp', '--board', 'flat:7x6', '--ep', 'on', '--promote', 'QRBN', '--cap', '1', '--pmodel'], input='\n'.join(roots) + '\n', capture_output=True, text=True, preexec_fn=lim)
    out = r.stdout.strip().split('\n')
    if len(out) != len(meta): print('CHUNK FAILED', lo, r.returncode, file=sys.stderr); tot['failed_chunks'] += 1; continue
    badc = set()
    for (wn, bn, pred), l in zip(meta, out):
        A, B = l.split(' | ')[1].split()
        assert A == B and A != 'X', l
        tot['roots'] += 1
        if A != pred:
            tot['bad_roots'] += 1; badc.add((wn, bn))
            if pred != 'D': tot['W/L predictions contradicted'] += 1
            else: tot['pred D, decisive result'] += 1
    tot['contexts'] += len(ctxs[lo:lo + chunk]); tot['bad_contexts'] += len(badc)
    print(name, lo, dict(tot), file=sys.stderr, flush=True)
print(name, files, maxp, dict(tot))
