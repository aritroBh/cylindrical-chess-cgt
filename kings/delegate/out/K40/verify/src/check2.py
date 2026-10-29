import sys, collections, re
SP = sys.argv[1]
INT = list(range(-12, 13)); IX = {n: n + 12 for n in INT}
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
def ip(r): return ''.join(r[IX[n]] for n in INT)
def parse(p):
    t = p.split(); d = {x[0]: x[1:] for x in t[:3]}; return d['K'], d['P'], d['k'], t[3]
def fd(a, b, W):
    x = abs(ord(a[0]) - ord(b[0])); return min(x, W - x)
C8 = load(f'{SP}/C_8x8.txt')
for p in ['Ka1 Pa2 ka3 w', 'Ka2 Pf2 kb4 w', 'Ka3 Pg4 kb5 w', 'Ka6 Pa7 ka8 b']:
    print(p, 'C ints -12..12:', ip(C8[p]), 'rest', C8[p][25:])
# parity predicate checks
def chk(p, f):
    return all((C8[p][IX[n]] == 'W') == f(n) for n in INT)
print('Ka2 Pf2 kb4 w  W iff n>=-1 or odd:', chk('Ka2 Pf2 kb4 w', lambda n: n >= -1 or n % 2 != 0))
print('Ka3 Pg4 kb5 w  W iff n>=-2 or even:', chk('Ka3 Pg4 kb5 w', lambda n: n >= -2 or n % 2 == 0))
print('Ka6 Pa7 ka8 b  W iff n<0 odd:', chk('Ka6 Pa7 ka8 b', lambda n: n < 0 and n % 2 != 0))
# Prop 5 family exactness and fortress geometry, all boards
pat5 = ''.join('W' if (n < 0 and n % 2) else 'D' for n in INT)
for h in (6, 7, 8):
    for w in range(3, 9):
        b = f'{w}x{h}'; C = load(f'{SP}/C_{b}.txt'); N = load(f'{SP}/N_{b}.txt'); NK = load(f'{SP}/NK_{b}.txt')
        fam = [p for p in C if ip(C[p]) == pat5]
        ok = all(parse(p)[0][0] == parse(p)[1][0] == parse(p)[2][0] and parse(p)[0][1:] == str(h - 2) and parse(p)[1][1:] == str(h - 1) and parse(p)[2][1:] == str(h) and p.endswith('b') for p in fam)
        # also: does the full row of family members have other features
        fort = [p for p in N if cls(N[p]) == 'DUD' and NK[p][25] != 'L']
        geo = collections.Counter((fd(parse(p)[0], parse(p)[1], w), fd(parse(p)[2], parse(p)[1], w), parse(p)[0][0] == parse(p)[2][0]) for p in fort)
        # nonmono patterns under C (excluding DEC/DUD/ON)
        pats = collections.Counter(ip(C[p]) for p in C if cls(C[p]) == 'OTHER')
        nonmono = {k: v for k, v in pats.items() if any(k[i] == 'W' and k[i + 1] != 'W' for i in range(24))}
        print(b, 'fam5', len(fam), 'shape_ok', ok, 'fortress', len(fort), 'geom(dK,dk,samefile)', dict(geo), 'n_nonmono_patterns', len(nonmono))
        if b in ('8x8', '5x6', '7x7'):
            for k, v in sorted(nonmono.items(), key=lambda kv: -kv[1]): print('   ', k, v)
