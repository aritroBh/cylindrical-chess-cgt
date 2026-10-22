"""Auditor B: class tables recomputed straight from the builder's jsonl files (own code)."""
import json, os, sys, collections
K4 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZES = ['3x4', '4x4', '3x5', '4x5', '5x5']

def load(kind, size):
    return {r['placement']: r for r in map(json.loads, open(os.path.join(K4, '%s_%s.jsonl' % (kind, size))))}

def refine(r):
    if r['cls'] != 'unmatched':
        return r['cls']
    pairs = {r['sig'][i:i+2] for i in range(0, 32, 2)}
    return 'unmatched T-indep %s' % pairs.pop() if len(pairs) == 1 else 'unmatched T-dep'

if __name__ == '__main__':
    for size in SIZES:
        F, C = load('flat', size), load('cyl', size)
        print('\n=== %s: flat %d quiet, cyl %d quiet' % (size, len(F), len(C)))
        for key in (lambda r: r['cls'], refine):
            cf = collections.Counter(key(r) for r in F.values()); cc = collections.Counter(key(r) for r in C.values())
            for c in sorted(set(cf) | set(cc)):
                exf = next((p for p, r in sorted(F.items()) if key(r) == c), '-')
                exc = next((p for p, r in sorted(C.items()) if key(r) == c), '-')
                print('  %-45s flat %5d %-16s cyl %5d %-16s' % (c, cf.get(c, 0), exf, cc.get(c, 0), exc))
            print('  ---')
        common = set(F) & set(C)
        ch = sum(refine(F[p]) != refine(C[p]) for p in common)
        print('  common quiet placements %d, change refined class: %d; change raw cls: %d' % (
            len(common), ch, sum(F[p]['cls'] != C[p]['cls'] for p in common)))
        print('  decisive W flat/cyl %d/%d ; decisive L %d/%d' % (
            sum(r['decisive'] == 'W' for r in F.values()), sum(r['decisive'] == 'W' for r in C.values()),
            sum(r['decisive'] == 'L' for r in F.values()), sum(r['decisive'] == 'L' for r in C.values())))
