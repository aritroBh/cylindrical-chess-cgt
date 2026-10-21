"""Compare raw pawn-level results (v2_pawn_20_23.out) with my own octal g and the claim."""
import re, importlib.util, sys
spec = importlib.util.spec_from_file_location('o', __file__.replace('v2_compare.py', 'v2_octal.py'))
src = open(spec.origin).read().replace('\nmain()\n', '\n')
ns = {}; exec(src, ns)
g = ns['octal']('0.137', 100)
flat, ring = {}, {}
for line in open(__file__.replace('v2_compare.py', 'v2_pawn_20_23.out')):
    m = re.match(r'(flat|ring)\s+(\d+)\s+(\d+)\s+N:(\w+)/(\w+)\s+M:(\w+)/(\w+)', line)
    if m:
        d = flat if m[1] == 'flat' else ring
        d[int(m[2])] = dict(NW=m[4], NB=m[5], MW=m[6], MB=m[7], line=line)
bad = []
for n, r in flat.items():
    if r['NW'] != r['NB'] or r['MW'] != r['MB']: bad.append(('flat colour', n))
    if (r['NW'] == 'win') != (g[n] != 0): bad.append(('flat normal vs g', n))
for n, r in ring.items():
    if r['NW'] != r['NB'] or r['MW'] != r['MB']: bad.append(('ring colour', n))
    if (r['NW'] == 'win') != (g[n - 3] == 0): bad.append(('ring normal vs g(n-3)=0', n))
    if (r['MW'] == 'win') != (flat[n - 3]['MW'] == 'loss'): bad.append(('ring misere vs flat(n-3) misere P', n))
    if 'lemma 1,1' not in r['line']: bad.append(('lemma', n))
    tail = r['line'].split('|')[-1].split()
    if tail[0] != '0' or tail[1] != '0': bad.append(('promo/dbl_quiet', n))
for n, r in flat.items():
    tail = r['line'].split()[-3:]
    if tail[0] != '0' or tail[1] != '0': bad.append(('flat promo/dbl_quiet', n))
print('flat n:', min(flat), '..', max(flat), ' ring n:', min(ring), '..', max(ring))
print('mismatches:', bad)
print('raw ring normal first-player wins:', [n for n in sorted(ring) if ring[n]['NW'] == 'win'])
print('raw ring misere first-player wins:', [n for n in sorted(ring) if ring[n]['MW'] == 'win'])
print('raw flat misere P (first player loses):', [n for n in sorted(flat) if flat[n]['MW'] == 'loss'])
worker_ring_mis = [4, 5, 9, 10, 14, 18, 19, 23]
print('worker misere ring list (n<=23) equal:', [n for n in sorted(ring) if ring[n]['MW'] == 'win'] == worker_ring_mis)
