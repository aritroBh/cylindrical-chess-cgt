"""Recompute from the K4 output files every number that the K4 report quotes, and assert the structural claims.

    PYTHONPATH=. .venv/bin/python kings/delegate/out/K4/claims.py          (prints a summary, exit 1 on failure)

Reads <flat|cyl>_<W>x<H>.jsonl, meta_*.json, tempo_scan.jsonl, xrun_*.log and (if present) verify_A/result_*.json;
uses the reference move generator only to re-check that every off placement is a stalemate.
mkreport.py and reptables.py import compute() from here, so the printed tables and the checks use the same numbers.
"""

import collections
import glob
import json
import os
import re

import testgames as tg
from tables import HERE, load, refined, sig_kind

SIZES = ['3x4', '4x4', '3x5', '4x5', '5x5']
KINDS = ['flat', 'cyl']
MAIN = {'on', 'on+*', 'off', 'off+*', 'dud'}          # the only candidates that any placement matches
CLASSES = {'WHITE-WINS-ALL', 'on/on+*', 'off/off+*', 'dud', 'unmatched, T-dependent',
           'unmatched, T-independent (White first: W, Black first: D)'}      # BLACK-WINS-ALL never occurs (checked)


def profile(sig):
    """Results against the integers n = -2, -1, 0, 1, 2 as five 2-letter strings."""
    p = {n: sig[2 * i:2 * i + 2] for i, n in enumerate((0, 1, 2, -1, -2))}
    return [p[n] for n in (-2, -1, 0, 1, 2)]


def stalemate_check(kind, size, rows):
    """Number of off placements, and how many are White-to-move stalemates (no move, no check)."""
    from kings.ref.solve import make_solver
    sv = make_solver(board='%s:%s' % (kind, size), ep='on', promote='QRBN', cap=1)
    g = sv.g
    offs = [r for r in rows.values() if r['cls'] == 'off/off+*']
    ok = 0
    for r in offs:
        pos = (0, g.parse_square(r['wk']), g.parse_square(r['bk']), (), 1 << g.parse_square(r['p']), 0, -1)
        nq, quiet, exits = sv.moves(pos, full=True)
        ok += (len(quiet) + len(exits) == 0 and not sv.in_check(pos))
    return len(offs), ok


def logsum(name):
    tot = bad = 0
    for line in open(os.path.join(HERE, name)):
        m = re.match(r'(\S+): (\d+) games, (\d+) comparisons, (\d+) mismatches', line)
        if m:
            tot += int(m.group(3))
            bad += int(m.group(4))
    return tot, bad


def compute():
    C = {}
    R = {(k, s): load(k, s) for s in SIZES for k in KINDS}
    C['rows'] = R
    C['quiet'] = {b: len(r) for b, r in R.items()}
    C['quiet_total'] = sum(C['quiet'].values())
    C['raw'] = {b: collections.Counter(r['cls'] for r in rows.values()) for b, rows in R.items()}
    C['refined'] = {b: collections.Counter(refined(r) for r in rows.values()) for b, rows in R.items()}
    # candidates other than on/off/dud (and their +*): numbers, nimbers, ups, over, under, {a|b}
    C['other_matches'] = sum(1 for rows in R.values() for r in rows.values() if set(r['matched']) - MAIN)
    C['black_wins_all'] = sum(1 for rows in R.values() for r in rows.values() if r['decisive'] == 'L')
    # same placement, other board
    C['common'], C['changed'], C['changed_raw'] = {}, {}, {}
    for s in SIZES:
        f, c = R[('flat', s)], R[('cyl', s)]
        com = sorted(set(f) & set(c))
        C['common'][s] = len(com)
        C['changed'][s] = sum(refined(f[p]) != refined(c[p]) for p in com)
        C['changed_raw'][s] = sum(f[p]['cls'] != c[p]['cls'] for p in com)
    # check 1 / xrun / difference tests
    meta = {b: json.load(open(os.path.join(HERE, 'meta_%s_%s.json' % b))) for b in R}
    C['meta'] = meta
    C['c1_kpk'] = sum(m['check1']['kpk'] for m in meta.values())
    C['c1_other'] = sum(m['check1']['other'] for m in meta.values())
    C['c1_diff'] = sum(m['check1_differences'] for m in meta.values())
    C['xrun'] = [logsum('xrun_small.log'), logsum('xrun_large.log')]
    C['diff_run'] = sum(len(r['diff']) for rows in R.values() for r in rows.values())
    C['diff_ok'] = sum(d['second_player'] for rows in R.values() for r in rows.values() for d in r['diff'].values())
    C['diff_dd'] = sum((d['white_starts'], d['black_starts']) == ('D', 'D')
                       for rows in R.values() for r in rows.values() for d in r['diff'].values())
    # stalemate: off placements, and T = 0 sum versus chess
    C['off'] = {b: stalemate_check(b[0], b[1], rows) for b, rows in R.items()}
    C['t0_differs'] = {b: sum(r['sig'][:2] != ''.join(r['chess']) for r in rows.values()) for b, rows in R.items()}
    C['t0_differs_by_class'] = {b: collections.Counter(r['cls'] for r in rows.values() if r['sig'][:2] != ''.join(r['chess']))
                                for b, rows in R.items()}
    C['chess_by_class'] = {b: {c: collections.Counter(''.join(r['chess']) for r in rows.values() if r['cls'] == c)
                               for c in {r['cls'] for r in rows.values()}} for b, rows in R.items()}
    C['finite_insens'] = {b: sum(len({r['sig'][i:i + 2] for i in range(0, 22, 2)}) == 1 for r in rows.values())
                          for b, rows in R.items()}
    # finite-tempo scan: placements whose results against n = -2..2 are not constant
    C['tempo'] = {}
    for b, rows in R.items():
        prof = {p: profile(r['sig']) for p, r in rows.items()}
        var = [p for p, pr in prof.items() if len(set(pr)) > 1]
        C['tempo'][b] = dict(
            n=len(var), cls=collections.Counter(refined(rows[p]) for p in var),
            profiles=collections.Counter(' '.join(prof[p]) for p in var),
            wl_jump=sum(any({a[i], b2[i]} == {'W', 'L'} for i in (0, 1)) for p in var
                        for a, b2 in zip(prof[p], prof[p][1:])))
    C['scan'] = {d['board']: d for d in map(json.loads, open(os.path.join(HERE, 'tempo_scan.jsonl')))}
    va = sorted(glob.glob(os.path.join(HERE, 'verify_A', 'result_*.json')))
    C['verify_A'] = [json.load(open(f)) for f in va]
    return C


def check(C):
    """Assertions behind the claims in REPORT.md; returns a list of failures."""
    bad = []
    expect = lambda ok, what: ok or bad.append(what)
    expect(C['other_matches'] == 0, 'a placement matches a candidate other than on/off/dud')
    expect(C['black_wins_all'] == 0, 'BLACK-WINS-ALL occurs')
    expect(C['c1_diff'] == 0, 'check 1 differences')
    expect(all(x[1] == 0 for x in C['xrun']), 'xrun mismatches')
    expect(C['diff_run'] == C['diff_ok'] == C['diff_dd'], 'difference tests not all D/D survivals')
    for b, (n, ok) in C['off'].items():
        expect(n == ok, 'off placement that is not a stalemate on %s' % (b,))
    for b, t in C['tempo'].items():
        sc = C['scan']['%s:%s' % b]
        nj = sc['number_of_jumps']
        expect(t['n'] == C['quiet'][b] - nj.get('0', 0), 'tempo count disagrees with tempo_scan on %s' % (b,))
        expect(sc['placements_with_a_jump_beyond_pm2'] == 0, 'tempo jump beyond +-2')
        expect(t['wl_jump'] == 0, 'a W<->L jump between adjacent integers on %s' % (b,))
        expect(set(t['cls']) <= {'unmatched, T-dependent'}, 'varying profile outside unmatched T-dependent on %s' % (b,))
    for s in SIZES:        # the small numbers that REPORT.template.md states by hand
        expect(C['off'][('flat', s)][0] == 4, 'flat off count %s' % s)
        expect(C['off'][('cyl', s)][0] == (8 if s in ('4x4', '4x5') else 0), 'cyl off count %s' % s)
        wd = lambda k: C['chess_by_class'][(k, s)]['WHITE-WINS-ALL'].get('WD', 0)
        expect(wd('flat') == 8 and wd('cyl') == (20 if s in ('4x4', '4x5') else 0), 'WHITE-WINS-ALL chess WD %s' % s)
        if s in ('3x4', '3x5', '5x5'):
            expect(C['tempo'][('cyl', s)]['n'] == 0 and C['finite_insens'][('cyl', s)] == C['quiet'][('cyl', s)],
                   'odd-width cylinder %s is not insensitive to every finite test' % s)
    for b, t in C['tempo'].items():
        expect(all(set(pr.replace(' ', '')) <= {'D', 'W'} for pr in t['profiles']), 'a profile with a Black win on %s' % (b,))
    expect(profile(C['rows'][('flat', '3x4')]['Ka3 Pa2 kc3']['sig']) == ['DD', 'DD', 'DW', 'WW', 'WW'],
           'example profile flat 3x4 Ka3 Pa2 kc3')
    for b, rows in C['rows'].items():
        expect(all(refined(r) in CLASSES for r in rows.values()), 'unexpected refined class on %s' % (b,))
    for a in C['verify_A']:
        expect(a['sig_diff'] == a['matched_diff'] == a['decisive_diff'] == a['diff_test_diff'] == a['chess_diff'] == 0
               and not a['only_mine'] and not a['only_builder'], 'verify_A difference on %s' % a['board'])
    return bad


if __name__ == '__main__':
    C = compute()
    print('quiet placements', C['quiet_total'], C['quiet'])
    print('check 1: %d KPK + %d other positions, %d differences' % (C['c1_kpk'], C['c1_other'], C['c1_diff']))
    print('xrun (small, large): comparisons/mismatches', C['xrun'], 'total', sum(x[0] for x in C['xrun']))
    print('difference tests run/ok/D-D', C['diff_run'], C['diff_ok'], C['diff_dd'])
    print('off placements (n, stalemates)', C['off'])
    print('T=0 sum differs from chess (placements)', C['t0_differs'])
    print('changed class (refined)', C['changed'], 'of', C['common'], '| raw', C['changed_raw'])
    for b, t in C['tempo'].items():
        print('tempo', b, t['n'], dict(t['cls']), dict(t['profiles']))
    print('verify_A: placements compared', sum(a['compared'] for a in C['verify_A']),
          'kpsolve nodes', sum(a['kpsolve']['compared_all_nodes'] for a in C['verify_A']))
    bad = check(C)
    print('FAILURES:' if bad else 'all claim checks pass', bad if bad else '')
    raise SystemExit(1 if bad else 0)
