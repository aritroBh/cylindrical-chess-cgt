import sys, json, time
sys.path.insert(0, '.')
import psolve
d = json.load(open('../logs/B3_f86_5.json'))['diffs']
pb = psolve.Board(8, 6, False)
n = int(sys.argv[1]); 
import re
out = []
t0 = time.time()
roots = []; meta = []
for x in d[:n]:
    txt = x['ctx']; pos, ep = txt.split(' (ep ')
    ep = ep[:-1]
    w, b = pos.split(' / ')
    wt = w.split(':')[1].split(); bt = b.split(':')[1].split()
    toks = ['Ka1', 'ka5'] + ['P' + t for t in wt] + ['p' + t for t in bt]
    q = ' '.join(toks) + (' w ' if x['stm'] == 'W' else ' b ') + ep
    roots.append(psolve.parse(pb, q)); meta.append((q, x))
S = psolve.Solver(pb, frozen=True); S.explore(roots); S.solve()
print('states', len(S.succ), 'time %.0f' % (time.time() - t0))
aw = af = 0
for r, (q, x) in zip(roots, meta):
    P = S.white_view(r)
    aw += (P == x['D_whole']); af += (P == x['D_fix'])
    print(q, 'P', P, 'D_whole', x['D_whole'], 'D_fix', x['D_fix'])
print('n', len(roots), 'P==D_whole', aw, 'P==D_fix', af)
