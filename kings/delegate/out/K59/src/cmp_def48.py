"""K59: compare two def48.py logs (ref3m and kp_p): verdict per group, failure lines, and every move value printed."""
import sys, re
def read(fn):
    G = {}; cur = None
    for l in open(fn):
        m = re.match(r'^(PASS|FAIL) \S+ (\S+) shuttler \S+ z=(\S+) f0=\S+ pieces "([^"]+)"', l)
        if m: cur = (m.group(2), m.group(4)); G[cur] = {'v': m.group(1), 'fails': set(), 'lines': set()}; continue
        if cur is None: continue
        s = l.strip()
        if l.startswith('    (') or l.startswith('    K'): G[cur]['fails'].add(s)
        elif s.startswith('root') or s.startswith('q '):
            # normalise move order and case of the mover letter (solvers print K/P for both colours)
            pos, rest = s.split(' : ', 1) if ' : ' in s else (s, '')
            t = rest.split(); val = t[0] if t else ''; mv = sorted(x.upper() for x in t[1:])
            G[cur]['lines'].add((pos, val, tuple(mv)))
    return G
A, B = read(sys.argv[1]), read(sys.argv[2])
for k in sorted(set(A) | set(B)):
    a, b = A.get(k), B.get(k)
    if not a or not b: print('MISSING', k); continue
    same = a['v'] == b['v'] and a['lines'] == b['lines']
    print('%s %-40s ref3m %s kp_p %s  %s' % (k[0], k[1], a['v'], b['v'], 'move values identical' if same else 'DIFFER'))
    if not same:
        for x in sorted(a['lines'] ^ b['lines']): print('     ', x)
