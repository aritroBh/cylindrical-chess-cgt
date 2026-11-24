# compare two "<pos> | V" files line by line (first letter after the last '|'); prints counts and differences
import sys, collections
a = [l.rstrip('\n') for l in open(sys.argv[1]) if '|' in l]; b = [l.rstrip('\n') for l in open(sys.argv[2]) if '|' in l]
assert len(a) == len(b), (len(a), len(b))
d = 0; c = collections.Counter()
for x, y in zip(a, b):
    px, vx = x.rsplit('|', 1); py, vy = y.rsplit('|', 1)
    assert px.strip() == py.strip()
    c[vx.strip()] += 1
    if vx.strip() != vy.strip(): d += 1; print('DIFF', x, '/', y)
print('positions', len(a), 'differences', d, 'values', dict(c))
