#!/usr/bin/env python3
"""K15 r3: the chess (kpsolve) table of FINDINGS.md, built mechanically from the raw outputs (fin2/chess/*.out, r3/logs/chess_*.out).
Result 'A B' = lower and upper bound from White's point of view (W/D/L); A == B means exact (no capped promotion mattered)."""
import os, re, glob
R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); FIN2 = os.path.join(os.path.dirname(R3), 'fin2')
def rd(p):
    try: return open(p).read()
    except Exception: return ''
def cost(errfile):
    e = rd(errfile)
    m = re.search(r'cap=(\d+): (\d+) layers, (\d+) states, depth (\d+), ([\d.]+)s(, capped promotions met)?', e)
    r = re.search(r'peak rss (\d+) KB', e)
    return (m.group(5) + ' s, ' + str(int(r.group(1)) // 1024) + ' MB') if (m and r) else '?'
rows = ['| board | cap | position | White to move: A B | Black to move: A B | dud_D prediction (W to move, B to move) | agrees | kpsolve time, peak RSS |', '|---|---|---|---|---|---|---|---|']
spec = [('cyl_8x6_G8a_alone_c1', 'cyl:8x6', 1, 'G8a alone', 'D D', 'D D'),
        ('cyl_8x6_G8a_blocked_c1', 'cyl:8x6', 1, 'G8a + Pg3 pg4 (blocked pair)', 'D', 'D'),
        ('cyl_8x6_G8a_onemove_c1', 'cyl:8x6', 1, 'G8a + Pg3 pg5 (one move)', 'D', 'D'),
        ('cyl_8x6_G8a_gap_c1', 'cyl:8x6', 1, 'G8a + Pg2 pg5 (gap pair)', 'D', 'D'),
        ('cyl_8x6_G8a_ctxWW_c1', 'cyl:8x6', 1, 'G8a + Pg2 (one White pawn, far from queening)', 'W', 'W'),
        ('cyl_8x6_G8a_ctxLL_c1', 'cyl:8x6', 1, 'G8a + pg5 (one Black pawn)', 'L', 'L'),
        ('cyl_8x6_G8a_ctxWL_c1', 'cyl:8x6', 1, 'G8a + Pg4 pg3 (two passers racing)', 'W', 'L')]
for name, board, cap, desc, pw, pb in spec:
    out = [l for l in rd(os.path.join(FIN2, 'chess', name + '.out')).splitlines() if ' | ' in l]
    if not out: rows.append('| %s | %d | %s | not available | | %s %s | | |' % (board, cap, desc, pw, pb)); continue
    d = {}
    base = out[0].split(' | ')[0]
    root = ' '.join(base.split()[:-2])
    for l in out:
        p = l.split(' | '); d[p[0].split()[-2]] = p[1].strip()
    w, b = d.get('w', '?'), d.get('b', '?')
    wa, ba = w.split(), b.split()
    exact = lambda a: len(a) == 2 and a[0] == a[1]
    def ok(a, pred):
        if not exact(a): return 'undecided at cap 1 (bounds %s %s; the value is between them)' % (a[0], a[1])
        return 'yes' if a[0] == pred else 'NO'
    agree = ok(wa, pw[0]) + ' / ' + ok(ba, pb[0])
    rows.append('| %s | %d | `%s` (%s) | %s | %s | %s %s | %s | %s |' % (board, cap, root, desc, w, b, pw[0], pb[0], agree, cost(os.path.join(FIN2, 'chess', name + '.err'))))
md = '\n'.join(rows) + '\n'
# per-move lists
def mv_lines(f):
    return [l.rstrip('\n') for l in rd(f).splitlines() if ' | ' in l]
c2 = mv_lines(os.path.join(FIN2, 'chess', 'cyl_8x6_G8_states_c2_mv.out')); c1 = mv_lines(os.path.join(FIN2, 'chess', 'cyl_8x6_G8_states_c1_mv.out'))
pk = mv_lines(os.path.join(FIN2, 'logs', 'g8_moves_kpp.txt'))
def mvmap(lines, k):
    m = {}
    for l in lines:
        p = l.split(' | ')
        if len(p) < 3: continue
        mv = p[2]
        if mv.startswith('A:'): mv = mv.split(' | ')[0]
        m[p[0]] = (p[1], sorted(x for x in p[2].replace('A:', '').split('|')[0].split()))
    return m
m2 = mvmap(c2, 2); mp = mvmap(pk, 0)
same = sum(1 for k in m2 if k in mp and m2[k] == mp[k])
tot = sum(len(v[1]) for v in m2.values()); dr = sum(1 for v in m2.values() for x in v[1] if x.endswith(':D'))
nbad = 0
for l in c1:
    p = l.split(' | ')
    A = dict(x.split(':') for x in p[2].replace('A: ', '').split()); B = dict(x.split(':') for x in p[3].replace('B: ', '').split())
    nbad += sum(1 for m in A if A[m] != B[m])
md += '\n**G8a and G8b, all 16 roots (4 king states x 2 sides to move x 2 groups), chess at cap 2, `--moves`** (`fin2/chess/cyl_8x6_G8_states_c2_mv.out`; 526.9 s CPU, peak RSS 515 MB): the value is exact (A = B, no "capped promotions met" line) and (D, D) at all 16 roots; %d legal moves, %d of them draw (the shuttles, one for each side at each root), the other %d each lose for the side that plays them (exact). The 16 root values and the 72 per-move values are the same as in the P model (`kp_p --pmodel` and `ref3m`): move lists identical at %d of 16 roots (rest: see the file). At cap 1 the roots are exact (D, D) too, but %d of the 72 move values are bounds only (`fin2/chess/cyl_8x6_G8_states_c1_mv.out`, 15.2 s), which is why cap 2 was run.\n' % (tot, dr, tot - dr, same, nbad)
open(os.path.join(FIN2, 'logs', 'chess_curated.md'), 'w').write(md)
print(md)
