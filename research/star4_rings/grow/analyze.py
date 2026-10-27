"""analyze.py -- summary tables from cache.tsv (no engine calls)."""
import sys, os, collections, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from growlib import *
from grow import load_cache, kind

cache = load_cache()
rows = list(cache.values())

print('== evaluations per round and value ==')
byr = collections.defaultdict(collections.Counter)
for f in rows:
    byr[int(f[4])][kind(f[1])] += 1
keys = ['*0', '*1', '*2', '*3', '*4', '*5', '*6', '*7', 'allN', 'non', 'ABORT', 'ERR']
print('round\tevaluated\t' + '\t'.join(keys))
tot = collections.Counter()
for r in sorted(byr):
    print('%d\t%d\t%s' % (r, sum(byr[r].values()), '\t'.join(str(byr[r][k]) for k in keys)))
    tot.update(byr[r])
print('all\t%d\t%s' % (sum(tot.values()), '\t'.join(str(tot[k]) for k in keys)))

print('\n== per move class (first class that produced the ring), rounds 1-3 ==')
byc = collections.defaultdict(collections.Counter)
for f in rows:
    if f[5] == 'seed':
        continue
    byc[f[5]][kind(f[1])] += 1
print('class\tevaluated\t*0\t*1\t*2\t*3\tallN\tnon\tABORT\t*3 yield')
for c, _ in [(n, 0) for n, _ in __import__('growlib').MOVE_CLASSES]:
    k = byc[c]
    n = sum(k.values())
    if n:
        print('%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%.2f%%' % (c, n, k['*0'], k['*1'], k['*2'], k['*3'], k['allN'], k['non'], k['ABORT'], 100.0 * k['*3'] / n))

print('\n== *3 rings by number of files / pawns (all rounds incl. seeds) ==')
s3 = [f for f in rows if f[1] == 'NNNPNNNN']
bn = collections.Counter(len(f[0].split()) for f in s3)
print('files', dict(sorted(bn.items())))
bp = collections.Counter(npawns(parse(f[0])) for f in s3)
print('pawns', dict(sorted(bp.items())))
ring = [f for f in s3 if is_ring(parse(f[0]))]
print('*3 total', len(s3), 'of which every file occupied (rings)', len(ring), 'with an empty file', len(s3) - len(ring))
print('new *3 (not seeds):', sum(1 for f in s3 if f[5] != 'seed'))

print('\n== signatures: anything with first non-N at index >= 4, or P not alone ==')
odd = [f for f in rows if kind(f[1]) in ('*4', '*5', '*6', '*7')]
print('nimbers >= *4:', len(odd))
for f in odd[:50]:
    print('\t'.join(f))
near = [f for f in rows if f[1].startswith('NNNN') and f[1] != 'NNNNNNNN' and 'ABORT' not in f[1]]
print('signatures NNNN + non-N afterwards (near *4):', len(near))
cn = collections.Counter(f[1] for f in near)
print(dict(cn))
# signatures with prefix NNN then a one-sided win at index 3 (near *3)
cnear3 = collections.Counter(f[1] for f in rows if f[1].startswith('NNN') and f[1] != 'NNNNNNNN' and f[1] != 'NNNPNNNN' and 'ABORT' not in f[1])
print('signatures NNN+... other than *3 and all-N:', dict(cnear3))
print('\n== all distinct signatures (top 25) ==')
cs = collections.Counter(f[1] for f in rows)
for s, n in cs.most_common(25):
    print(s, n)
