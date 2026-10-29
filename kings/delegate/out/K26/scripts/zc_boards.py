#!/usr/bin/env python3
"""K26 final: on which boards do Z_B and Z_C keep zero leaks?  All 8 roots of each group, P model, solver kpp or ref3m (env K26_SOLVER, default kpp;
kpp has an 8-file limit, ref3m does not).  Leaks are non-shuttle moves of the mover that do not lose at once for the mover (L for White, W for Black),
promotions counted once per (from, to).  Quick runs (< 1 CPU-s per board).  Prints one line per board and group."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k26lib import *
safe_nice()
SOLVER = os.environ.get('K26_SOLVER', 'kpp')
GROUPS = {
 'Z_C': (['c2', 'c3'], ['a4', 'a5'], ['a2', 'c4'], ['a3', 'c5']),
 'Z_B': (['b2', 'c3'], ['a4', 'b5'], ['a3', 'b4'], ['b3', 'c4']),
}
BOARDS = ['flat:5x6', 'flat:6x6', 'flat:7x6', 'flat:8x6', 'flat:9x6', 'flat:7x7', 'flat:7x5',
          'cyl:5x6', 'cyl:6x6', 'cyl:7x6', 'cyl:8x6', 'cyl:9x6', 'cyl:10x6', 'cyl:12x6', 'cyl:8x5', 'cyl:8x7', 'cyl:8x8', 'cyl:7x7', 'cyl:6x7', 'cyl:9x7']


def parse_any(line):
    parts = line.split(' | ')
    pos = parts[0].split()
    stm = pos[-2]
    rest = ' | '.join(parts[1:]).replace(' | ', ' ').split()
    val = rest[0]
    mv = []
    for tok in rest[1:]:
        if ':' in tok and not tok.startswith('A:'):
            nm, v = tok.rsplit(':', 1)
            mv.append((nm, v))
    return stm, val, mv


for b in (sys.argv[1:] or BOARDS):
    for gname, (wk, bk, wp, bp) in GROUPS.items():
        lines = ['K%s k%s %s %s %s -' % (w, k, ' '.join('P' + x for x in wp), ' '.join('p' + x for x in bp), s)
                 for w in wk for k in bk for s in 'wb']
        try:
            res, err = run_solver(lines, b, SOLVER, moves=True)
        except Exception as e:
            print('%-9s %-4s solver error %s' % (b, gname, str(e)[:60].replace('\n', ' ')))
            continue
        tot = 0
        leaks = []
        vals = []
        bad = False
        for l in res:
            stm, val, mv = parse_any(l)
            vals.append(val)
            if val == 'X':
                bad = True
                continue
            sh = set(wk) if stm == 'w' else set(bk)
            lose = 'L' if stm == 'w' else 'W'
            seen = set()
            nsh = 0
            for nm, v in mv:
                if nm[0] == 'K' and {nm[1:3], nm[3:5]} == sh:
                    nsh += 1
                    continue
                key = (nm.split('=')[0], v if '=' not in nm else v)
                if '=' in nm:
                    if (nm.split('=')[0]) in seen:
                        continue
                    seen.add(nm.split('=')[0])
                if v != lose:
                    tot += 1
                    leaks.append('%s %s:%s' % (stm, nm, v))
            if nsh != 1:
                bad = True
        print('%-9s %-4s %s total leaks %2d  root values %s  %s' % (b, gname, 'ILLEGAL-OR-NO-SHUTTLE' if bad else '', tot, ''.join(vals), ' '.join(leaks[:5])))
