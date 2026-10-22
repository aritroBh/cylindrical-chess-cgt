"""Print every number and table that the K4 report quotes, recomputed from the output files of this directory.

    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K4/mkreport.py > tables_for_report.txt

Stops if claims.check() fails.  It writes no file: the prose of the report is written by hand around this output.
"""

import os
import sys

import checks
import claims
import extras
import reptables as rt
import tables
from claims import SIZES, KINDS

HERE = os.path.dirname(os.path.abspath(__file__))


def fmt(n):
    return '{:,}'.format(n)


def per_board():
    out = []
    for i, size in enumerate(SIZES):
        flat, cyl = tables.load('flat', size), tables.load('cyl', size)
        tab, cf, cc = tables.class_table(flat, cyl, tables.refined)
        out += ['### 4.%d  %s' % (i + 1, size), '', tab, '', tables.one_board(flat, cyl, cf, cc, tables.refined, size), '',
                tables.transitions(flat, cyl, tables.refined), '']
    return '\n'.join(out)


def values(C):
    V = {}
    b = rt.boards()
    V['quiet_total'] = fmt(C['quiet_total'])
    V['c1_kpk'], V['c1_other'] = fmt(C['c1_kpk']), fmt(C['c1_other'])
    V['c1_total'] = fmt(C['c1_kpk'] + C['c1_other'])
    V['c1_diff'] = str(C['c1_diff'])
    V['xrun_total'] = fmt(sum(x[0] for x in C['xrun']))
    V['xrun_bad'] = str(sum(x[1] for x in C['xrun']))
    V['diff_run'] = fmt(C['diff_run'])
    V['changed_line'] = ', '.join('%d of %d (%s)' % (C['changed'][s], C['common'][s], s) for s in SIZES)
    V['off_line'] = 'flat ' + '/'.join(str(C['off'][('flat', s)][0]) for s in SIZES) + '; cyl ' + \
        '/'.join(str(C['off'][('cyl', s)][0]) for s in SIZES) + ' (3x4, 4x4, 3x5, 4x5, 5x5)'
    V['on_line'] = ', '.join('%d vs %d (%s)' % (C['raw'][('flat', s)]['on/on+*'], C['raw'][('cyl', s)]['on/on+*'], s)
                             for s in SIZES)
    V['wwa_line'] = ', '.join('%d vs %d (%s)' % (C['raw'][('flat', s)]['WHITE-WINS-ALL'], C['raw'][('cyl', s)]['WHITE-WINS-ALL'], s)
                              for s in SIZES)
    V['dud_line'] = ', '.join('%d vs %d (%s)' % (C['raw'][('flat', s)]['dud'], C['raw'][('cyl', s)]['dud'], s) for s in SIZES)
    unreach, per = rt.unreachable_total()
    V['unreach_total'] = str(unreach)
    V['unreach_flat34'] = str(per[0]) if per else '?'
    vt, tot = rt.verify_table(C)
    V['verify_table'] = vt
    V['va_compared'], V['va_nodes'] = fmt(tot[0]), fmt(tot[2])
    V['vb_compared'], V['vb_nodes'] = fmt(tot[4]), fmt(tot[6])
    V['v_diffs'] = str(tot[1] + tot[3] + tot[5] + tot[7])
    c2, ok2 = rt.check2_table()
    V['check2_table'], V['check2_ok'] = c2, '%d/%d' % (ok2, len(checks.FACTS))
    V['class_summary'] = rt.class_summary(C)
    V['changed_table'] = rt.changed_table(C)
    V['per_board'] = per_board()
    V['check1_table'] = extras.check1_table(SIZES)
    V['candidate_short'] = rt.candidate_short(C)
    V['off_table'] = rt.off_table(C)
    V['t0_table'] = rt.t0_table(C)
    V['chess_share'] = rt.chess_share(C)
    V['chess_full'] = extras.chess_vs_class(SIZES)
    V['diff_summary'] = extras.diff_summary(SIZES)
    V['finite_insensitive'] = extras.finite_insensitive(SIZES)
    V['tempo_table'] = extras.tempo_table()
    V['tempo_profiles'] = rt.tempo_profiles(C)
    V['sig_only'] = '\n\n'.join('#### %s\n\n%s' % (s, extras.sig_only(s)) for s in SIZES)
    # the share of chess draws among the on/on+* placements, smallest board
    sh = {x: C['chess_by_class'][x].get('on/on+*', {}).get('DD', 0) / max(1, sum(C['chess_by_class'][x].get('on/on+*', {}).values()))
          for x in b}
    lo = min(sh, key=sh.get)
    V['on_dd_min'] = '%.0f%% (%s %s)' % (100 * sh[lo], lo[0], lo[1])
    V['on_dd_all'] = ', '.join('%s %s' % x for x in b if sh[x] == 1.0)
    V['t0_range'] = '%d%% to %d%%' % (min(100 * C['t0_differs'][x] / C['quiet'][x] for x in b),
                                      max(100 * C['t0_differs'][x] / C['quiet'][x] for x in b))
    V['ex_profile'] = ' '.join(claims.profile(C['rows'][('flat', '3x4')]['Ka3 Pa2 kc3']['sig']))
    V['tempo_flat'] = ', '.join('%d of %d (%s)' % (C['tempo'][('flat', s)]['n'], C['quiet'][('flat', s)], s) for s in SIZES)
    V['tempo_cyl'] = ', '.join('%d of %d (%s)' % (C['tempo'][('cyl', s)]['n'], C['quiet'][('cyl', s)], s) for s in SIZES)
    return V


SECTIONS = [          # (heading, key in values())
    ('Check 1 totals', 'check1_table'), ('Check 2 facts (%s pass)', 'check2_table'),
    ('Class counts, all boards (refined classes)', 'class_summary'), ('Per-board tables (flat vs cyl)', 'per_board'),
    ('Placements that change class when the edges go', 'changed_table'),
    ('Candidate occurrence (placements whose signature equals the candidate)', 'candidate_short'),
    ('off/off+* placements are White-to-move stalemates', 'off_table'),
    ('x (+) 0 against the chess result (stalemate = draw)', 't0_table'),
    ('Chess results inside on/on+*, dud and WHITE-WINS-ALL', 'chess_share'),
    ('Integer scan x (+) n, n = -10..10', 'tempo_table'), ('Profiles of the placements with a tempo threshold', 'tempo_profiles'),
    ('Placements insensitive to every finite test game', 'finite_insensitive'),
    ('Difference tests', 'diff_summary'), ('Independent re-implementations', 'verify_table'),
    ('Appendix A: chess result against class', 'chess_full'), ('Appendix B: signatures on one board only', 'sig_only'),
]


def main():
    """Print the recomputed numbers and all generated tables to stdout (nothing is written to a file)."""
    C = claims.compute()
    bad = claims.check(C)
    if bad:
        sys.exit('claims.check failed: %r' % bad)
    V = values(C)
    print('## Numbers\n')
    for k in sorted(V):
        if '\n' not in V[k]:
            print('- %s: %s' % (k, V[k]))
    for head, key in SECTIONS:
        print('\n## %s\n' % (head % V['check2_ok'] if '%s' in head else head))
        print(V[key])


if __name__ == '__main__':
    main()
