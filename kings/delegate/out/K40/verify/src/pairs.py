import sys, collections
SP = sys.argv[1]
def load(fn):
    d = {}
    for ln in open(fn):
        if ln.startswith('#'): continue
        p, r = ln.rstrip('\n').split('\t'); d[p] = r
    return d
def cls(r):
    if set(r) == {'W'}: return 'DEC'
    if set(r) == {'D'}: return 'DUD'
    if all(r[i] == 'W' for i in range(35) if i not in (26, 27)) and r[26] == 'D' and r[27] == 'D': return 'ON'
    return 'OTHER'
for h in (6, 7, 8):
    for w in (3, 5, 6, 7, 8):
        N = load(f'{SP}/N_{w}x{h}.txt')
        pairs = collections.Counter()
        for p in N:
            if p.endswith(' w'):
                q = p[:-1] + 'b'
                pairs[(cls(N[p]), cls(N[q]))] += 1
        offdud = all((N[p][26] == 'W') == (N[p][27] == 'W') for p in N)
        print(f'{w}x{h}', dict(pairs), 'W(off)==W(dud):', offdud)
