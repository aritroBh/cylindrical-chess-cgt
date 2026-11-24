"""K56: compare pr56 --sum output (roots A_w A_b B_w B_b) with r(over_D (+) T) from over56.py.
usage: cmp56.py <pr56 sum output> <test file>   Prints differences and a count."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import over56
ov = {}
for l in open(sys.argv[2]):
    if '|' in l:
        r = over56.results(l); ov[r[0]] = (r[1], r[2])
n = d = 0; dlist = []
for l in open(sys.argv[1]):
    if not l.startswith('SUM '): continue
    name, r = l[4:].rsplit('|', 1); name = name.strip(); r = r.split()
    for c, v in zip(['A_w', 'A_b', 'B_w', 'B_b'], r):
        o = ov[name][0 if c.endswith('w') else 1]; n += 1
        if o != v: d += 1; dlist.append('%s %s G=%s over=%s' % (name, c, v, o))
for x in dlist: print('DIFF', x)
print('%s: %d results, %d differ from over' % (sys.argv[1], n, d))
