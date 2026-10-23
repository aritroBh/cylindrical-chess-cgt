"""compare_logs.py -- compare my logs (verify_compute/logs) with the writer's saved logs (../logs) line by line.
Prints every difference; prints OK lines for what agrees.  Run from anywhere:  python -B compare_logs.py"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(HERE, '..', 'logs')
L = os.path.join(HERE, 'logs')
diffs = 0


def rd(p):
    return open(p).read().splitlines()


# ---- reduced graphs (writer: pump_P_8_60.txt, pump_P_fixc12.txt; mine: b_reduced_8_60.txt)
wr = {}
for fn in ('pump_P_8_60.txt', 'pump_P_fixc12.txt'):
    for ln in rd(os.path.join(W, fn)):
        m = re.match(r'n=\s*(\d+) pawns=(\d+) nodes=(\d+) kept=(\d+) T=(\d+) zone=(\[.*?\]) ep=(\d+) sig=(\w+)', ln)
        if m:
            n = int(m.group(1))
            rec = tuple(m.groups()[1:])
            if n in wr and wr[n] != rec:
                print('writer logs disagree with each other at n=%d: %s vs %s' % (n, wr[n], rec)); diffs += 1
            wr[n] = rec
mine = {}
for ln in rd(os.path.join(L, 'b_reduced_8_60.txt')):
    m = re.match(r'n=\s*(\d+) pawns=(\d+) nodes=(\d+) K=(\d+) T=(\d+) flagged=(\d+) zone=(\[.*?\]) passed-nodes=(\d+) sig\(h<8\) T50=(\w+) mine=(\w+)', ln)
    if m:
        g = m.groups()
        assert g[8] == g[9]
        assert 'graphs identical (nodes, T-sets, K-sets, L+P counts): True' in ln and 'stats equal: True' in ln
        mine[int(g[0])] = (g[1], g[2], g[3], g[4], g[6], g[5], g[8])
cnt = 0
for n in sorted(wr):
    if n not in mine:
        print('n=%d missing in my log' % n); diffs += 1; continue
    a, b = wr[n], mine[n]
    # writer: (pawns, nodes, kept, T, zone, ep, sig)   mine: (pawns, nodes, K, T, zone, flagged, sig)
    if a != b:
        print('DIFF reduced graph n=%d: writer %s mine %s' % (n, a, b)); diffs += 1
    else:
        cnt += 1
print('reduced graphs (pawns, nodes, kept K-edges, T edges, zone, #flagged, signature h<8): %d of %d values of n identical to the writer\'s rg logs' % (cnt, len(wr)))

# ---- unreduced signatures
wu = [re.match(r'(\w+) nodes=(\d+)', l).group(1) for l in rd(os.path.join(W, 'unreduced_P_8_60.txt')) if l.startswith('N') or l.startswith('P') or l.startswith('L') or l.startswith('R')]
mu = {}
for fn in ('a_outcomes_8_30.txt', 'a_outcomes_32_60.txt'):
    for ln in rd(os.path.join(L, fn)):
        m = re.match(r'n=\s*(\d+) pawns=\d+ T50=(\w+) .*mine-keep=(\w+) .*mine-expire=(\w+)', ln)
        if m:
            assert m.group(2) == m.group(3) == m.group(4), ln
            mu[int(m.group(1))] = m.group(2)
ns = list(range(8, 61, 2))
if len(wu) != len(ns):
    print('writer unreduced log has %d lines, expected %d' % (len(wu), len(ns))); diffs += 1
ok = 0
for n, s in zip(ns, wu):
    if n not in mu:
        print('n=%d missing in my outcome log' % n); diffs += 1
    elif mu[n][:4] != s:
        print('DIFF unreduced n=%d: writer %s mine %s' % (n, s, mu[n])); diffs += 1
    else:
        ok += 1
print('unreduced G+*h signatures (h<=3): %d of %d values of n identical (mine have h<=7: all NNPNNNNN: %s)' % (ok, len(ns), all(v == 'NNPNNNNN' for v in mu.values())))

# ---- insertion (c=12)
wins = {}
for ln in rd(os.path.join(W, 'pump_P_fixc12.txt')):
    m = re.match(r'n=\s*(\d+) .*\[cut c=12: start->start (\w+), nodes onto (\w+), kept\+T edges equal (\w+)\]', ln)
    if m:
        wins[int(m.group(1))] = (m.group(2), m.group(3), m.group(4))
mi = {}
for ln in rd(os.path.join(L, 'c_insertion_8_60.txt')):
    m = re.match(r'(T50 |mine)\s+n=\s*(\d+) -> \s*\d+ cut c=12: ok=(\w+)', ln)
    if m:
        mi.setdefault(int(m.group(2)) + 2, []).append(m.group(3))
ok = 0
for n2 in sorted(wins):
    if all(x == 'True' for x in wins[n2]) and mi.get(n2) == ['True', 'True']:
        ok += 1
    else:
        print('DIFF insertion c=12 into n=%d: writer %s mine %s' % (n2, wins[n2], mi.get(n2))); diffs += 1
print('insertion c=12 R_n -> R_{n+2}: %d of %d steps agree (writer all True; mine both engines ok=True)' % (ok, len(wins)))
print('TOTAL DIFFERENCES:', diffs)
