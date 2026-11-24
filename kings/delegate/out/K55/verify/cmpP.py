"""K55 referee: compare P values (T = 0) of za (dump), kp_p --pmodel, rz and rv55 on the sampled positions."""
za = {}
for l in open('sampleP_za.txt'):
    pos, v = l.rstrip('\n').split(' | '); za[pos] = v
kp = {}
for l in open('logs/kpp_sample.out'):
    pos, rest = l.split(' | ', 1); t = rest.split()
    kp[pos] = t[0] if t[0] == t[1] else '?' + t[0] + t[1]
roots = [l.strip() for l in open('sampleP_roots.txt') if l.strip()]
def solver(fn):
    line = [l for l in open(fn) if l.startswith('0 ')][0]
    cells = [c.strip().split()[0] for c in line.split('|')[1:]]
    out = {}
    for r, c in zip(roots, cells): out[r + ' w -'] = c[0]; out[r + ' b -'] = c[1]
    return out
rz = solver('logs/rz_sample.out'); rv = solver('logs/rv_sample.out')
n = dz = dr = dv = 0; nep = 0; bad = []
for pos, v in za.items():
    n += 1; k = kp[pos]
    if k != v: dz += 1; bad.append(('za/kpp', pos, v, k))
    if pos.endswith(' -'):
        if rz[pos] != k: dr += 1; bad.append(('rz/kpp', pos, rz[pos], k))
        if rv[pos] != k: dv += 1; bad.append(('rv/kpp', pos, rv[pos], k))
    else: nep += 1
print('positions %d (e.p. %d); kp_p bounds exact at %d' % (n, nep, sum(1 for p in za if not kp[p].startswith('?'))))
print('za vs kp_p differences %d; rz vs kp_p %d (of %d without e.p.); rv55 vs kp_p %d' % (dz, dr, n - nep, dv))
from collections import Counter
print('kp_p values', Counter(kp[p] for p in za))
for b in bad: print(b)
