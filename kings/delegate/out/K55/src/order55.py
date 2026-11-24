"""K55 part 2.2: order tests by the difference game.  For a candidate H, T = -H is looked up in the battery and
r(Z_O + T) is read at both roots.  G >= H: White (Left) survives Z_O + (-H) with Black to move first;
G <= H: Black (Right) survives it with White to move first.  'draws for Left': survive = W or D for White;
'draws for Right': White must win (W).  usage: python3 order55.py <za outputs...> -- <test files...> -- H1 H2 ..."""
import sys
from games55 import readT
from compare55 import read_za
_i = sys.argv.index('--'); _j = sys.argv.index('--', _i + 1) if sys.argv.count('--') > 1 else len(sys.argv)
Z = {}
for _f in sys.argv[1:_i]: Z.update(read_za(_f))
_tf = sys.argv[_i + 1:_j]; _extra = sys.argv[_j + 1:]
names = [n for _f in _tf for n, _ in readT(_f)]
def parts(n): return tuple(sorted(p for p in n.split('+') if p != '0')) if n != '0' else ()
key = {}
for n in names: key.setdefault(parts(n), n)
def negn(a):
    m = {'up': 'down', 'upstar': 'downstar', 'dbl_up': 'dbl_down', 'dbl_upstar': 'dbl_downstar', 'up2nd': 'down2nd', 'over': 'under', 'on': 'off', '*': '*', 'pm1': 'pm1', 'dud': 'dud'}
    m.update({v: k for k, v in list(m.items())})
    if a in m: return m[a]
    if a in ('tA', 'tB', 'tD', 'uD'): return 'neg' + a
    if a.startswith('negB'): return a[3:]
    if a.startswith('B'): return 'neg' + a
    if a.startswith('tiny'): return 'miny' + a[4:]
    if a.startswith('miny'): return 'tiny' + a[4:]
    if a.startswith('sw'):
        l, r = a[2:].split('/')
        return 'sw%s/%s' % (str(-int(r)), str(-int(l)))
    return str(-int(a))
for H in _extra:
    T = key.get(parts('+'.join(negn(p) for p in H.split('+'))))
    if T is None: print('%-12s -H not in the battery' % H); continue
    for r, rn in ((0, 'A'), (1, 'B')):
        w, b = Z[(T, r, 'w')][0], Z[(T, r, 'b')][0]
        ge_L, ge_R = b in 'WD', b == 'W'; le_R, le_L = w in 'LD', w == 'L'
        print('H = %-12s root %s: T = -H = %-12s r(Z+T) White first %s, Black first %s | G>=H: %s (draws Left) %s (draws Right) | G<=H: %s (draws Right) %s (draws Left)'
              % (H, rn, T, w, b, 'yes' if ge_L else 'no', 'yes' if ge_R else 'no', 'yes' if le_R else 'no', 'yes' if le_L else 'no'))
