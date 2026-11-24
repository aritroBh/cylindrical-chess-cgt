"""K48 referee: read the raw search logs of implementations A (p45a) and R (r48) and compare counters and hit sets.
Reads logs/flat/*.out(.xz) and logs/tall/*.out(.xz) of the investigator directly (not flat_table.txt).
usage: python3 cmp_logs.py <K48 dir>"""
import glob, lzma, os, re, sys
D = sys.argv[1]

def read(p):
    if os.path.exists(p): return open(p).read()
    if os.path.exists(p + '.xz'): return lzma.open(p + '.xz', 'rt').read()
    return None

def a_parse(txt):
    res = {}; hits = {0: set(), 1: set()}
    for line in txt.splitlines():
        if line.startswith('RESULT'):
            o = 'under' if 'white(under)' in line else 'over'
            g = lambda k: int(re.search(re.escape(k) + r'=(\d+)', line).group(1))
            res[o] = (g('placements'), g('F1(U1 at both shuttler roots)'), g('promoFreeze'), g('F2(U2)'), g('F3(U3 loose)'), g('F4(exact U4)'))
        elif line.startswith('HIT '):
            m = re.match(r'HIT sh=(\d) (.*) [wb] -\s+shuttle (\w\d)(\w\d)', line)
            sh = int(m.group(1)); pcs = m.group(2).split()
            hits[sh].add((frozenset(pcs), frozenset([m.group(3), m.group(4)])))
    return res, hits

def r_parse(txt):
    summ = None; hits = set()
    for line in txt.splitlines():
        if line.startswith('SUMMARY'):
            g = lambda k: int(re.search(r' ' + re.escape(k) + r' (\d+)', line).group(1))
            summ = (g('placements'), g('U1'), g('promoFreeze'), g('U1+U2'), g('loose'), g('exact'))
        elif line.startswith('HIT under'):
            m = re.match(r'HIT under: shuttle (\w\d)-(\w\d), Black king (\w\d), (.*)$', line)
            z0, z1, bk, pcs = m.groups()
            hits.add((frozenset(pcs.split() + ['K' + z0, 'k' + bk]), frozenset([z0, z1])))
    return summ, hits

tot = {}
bad = 0
for sub in ('flat', 'tall'):
    for ap in sorted(glob.glob(os.path.join(D, 'logs', sub, 'A_*.out*'))):
        name = os.path.basename(ap).replace('.xz', '').replace('.out', '')[2:]
        at = read(os.path.join(D, 'logs', sub, 'A_' + name + '.out'))
        rt = read(os.path.join(D, 'logs', sub, 'R_' + name + '.out'))
        ares, ahits = a_parse(at)
        if rt is None: print('%-22s R missing' % name); bad += 1; continue
        rsum, rhits = r_parse(rt)
        ok = ('under' in ares and 'over' in ares and ares['under'] == ares['over'] == rsum)
        # A's under hits (White king shuttles) must equal R's hits (R reports under groups with the White king on z0;
        # the pair {z0,z1} is the same, the root square may differ, so compare pawns, Black king and pair).
        norm = lambda h: set((frozenset(x for x in p if x[0] != 'K'), z) for p, z in h)
        hok = norm(ahits[0]) == norm(rhits)
        print('%-22s A_under %s A_over %s R %s  counters %s  hits A_under=%d A_over=%d R=%d sets %s' % (
            name, ares.get('under'), ares.get('over'), rsum, 'EQUAL' if ok else 'DIFFER', len(ahits[0]), len(ahits[1]), len(rhits),
            'EQUAL' if hok else 'DIFFER'))
        for p, z in sorted(ahits[1], key=str): print('      A over hit: %s  shuttle %s' % (' '.join(sorted(p)), '-'.join(sorted(z))))
        if not (ok and hok): bad += 1
        board = name.split('_')[0]
        t = tot.setdefault(board, [0] * 6)
        for i in range(6): t[i] += rsum[i]
for b, t in tot.items(): print('TOTAL %s (R, per orientation): placements %d U1 %d promoFreeze %d U1+U2 %d loose %d exact %d' % (b, *t))
print('classes with any difference:', bad)
