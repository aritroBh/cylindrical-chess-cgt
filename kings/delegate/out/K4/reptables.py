"""Table builders for REPORT.md that need the recomputed numbers of claims.py (see mkreport.py).

Every function takes C = claims.compute() and returns a markdown string.
"""

import ast
import collections
import os
import re

import testgames as tg
from claims import KINDS, SIZES, MAIN
from tables import HERE, pn, order_key

UNM_DEP = 'unmatched, T-dependent'
UNM_IND = 'unmatched, T-independent (White first: W, Black first: D)'
CLASSES = ['WHITE-WINS-ALL', 'BLACK-WINS-ALL', 'on/on+*', 'off/off+*', 'dud', UNM_DEP, UNM_IND]


def boards():
    return [(k, s) for s in SIZES for k in KINDS]


def name(b):
    return '%s %s' % b


def class_summary(C):
    head = ['board', 'quiet placements', 'WHITE-WINS-ALL', 'BLACK-WINS-ALL', 'on/on+*', 'off/off+*', 'dud',
            'unmatched, T-dependent', 'unmatched, T-independent (W first: W, B first: D)']
    out = ['| ' + ' | '.join(head) + ' |', '|---|' + '---:|' * (len(head) - 1)]
    for b in boards():
        c = C['refined'][b]
        assert set(c) <= set(CLASSES), set(c) - set(CLASSES)
        out.append('| %s | %d | ' % (name(b), C['quiet'][b]) + ' | '.join(str(c.get(k, 0)) for k in CLASSES) + ' |')
    return '\n'.join(out)


def changed_table(C):
    out = ['| board size | placements quiet on both boards | class changes (refined classes) | class changes (raw classes) |',
           '|---|---:|---:|---:|']
    for s in SIZES:
        out.append('| %s | %d | %d (%.1f%%) | %d |' % (s, C['common'][s], C['changed'][s],
                                                       100.0 * C['changed'][s] / C['common'][s], C['changed_raw'][s]))
    return '\n'.join(out)


def t0_table(C):
    out = ['| board | quiet placements | x (+) 0 differs from the chess result (stalemate = draw) | share |', '|---|---:|---:|---:|']
    for b in boards():
        out.append('| %s | %d | %d | %.1f%% |' % (name(b), C['quiet'][b], C['t0_differs'][b],
                                                  100.0 * C['t0_differs'][b] / C['quiet'][b]))
    return '\n'.join(out)


def chess_share(C):
    """For on/on+*, dud and WHITE-WINS-ALL: how many placements are chess draws (or wins) with either side to move."""
    out = ['| board | on/on+*: placements | of which chess DD | dud: placements | of which chess DD | '
           'WHITE-WINS-ALL: placements | chess WW | chess WD |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    for b in boards():
        ch = C['chess_by_class'][b]
        g = lambda cls, pair: ch.get(cls, {}).get(pair, 0)
        tot = lambda cls: sum(ch.get(cls, {}).values())
        out.append('| %s | %d | %d | %d | %d | %d | %d | %d |' % (
            name(b), tot('on/on+*'), g('on/on+*', 'DD'), tot('dud'), g('dud', 'DD'),
            tot('WHITE-WINS-ALL'), g('WHITE-WINS-ALL', 'WW'), g('WHITE-WINS-ALL', 'WD')))
    return '\n'.join(out)


def off_table(C):
    out = ['| board | off/off+* placements | of which White-to-move stalemates (0 legal moves, not in check) | placements |',
           '|---|---:|---:|---|']
    for b in boards():
        n, ok = C['off'][b]
        ex = ', '.join('`%s`' % p for p, r in sorted(C['rows'][b].items()) if r['cls'] == 'off/off+*')
        out.append('| %s | %d | %d | %s |' % (name(b), n, ok, ex or '-'))
    return '\n'.join(out)


def candidate_short(C):
    cols = boards()
    cnt = {b: collections.Counter(v for r in C['rows'][b].values() for v in r['matched']) for b in cols}
    out = ['| candidate V | ' + ' | '.join(name(b) for b in cols) + ' |', '|---|' + '---:|' * len(cols)]
    zero = []
    for v, _ in tg.candidates():
        if any(cnt[b].get(v, 0) for b in cols):
            out.append('| `%s` | ' % tg.pretty(v).replace('|', '\\|') + ' | '.join(str(cnt[b].get(v, 0)) for b in cols) + ' |')
        else:
            zero.append(tg.pretty(v).replace('|', '\\|'))
    out.append('| the other %d candidates: %s | ' % (len(zero), ', '.join('`%s`' % z for z in zero)) + ' | '.join('0' for _ in cols) + ' |')
    return '\n'.join(out)


def tempo_profiles(C):
    cols = boards()
    prof = set()
    for b in cols:
        prof |= set(C['tempo'][b]['profiles'])
    out = ['| results for n = -2, -1, 0, 1, 2 (White starts, Black starts) | ' + ' | '.join(name(b) for b in cols) + ' |',
           '|---|' + '---:|' * len(cols)]
    for p in sorted(prof, key=lambda p: (-sum(C['tempo'][b]['profiles'].get(p, 0) for b in cols), p)):
        out.append('| `%s` | ' % p + ' | '.join(str(C['tempo'][b]['profiles'].get(p, 0)) or '0' for b in cols) + ' |')
    out.append('| **placements with a change, total** | ' + ' | '.join(str(C['tempo'][b]['n']) for b in cols) + ' |')
    out.append('| quiet placements | ' + ' | '.join(str(C['quiet'][b]) for b in cols) + ' |')
    return '\n'.join(out)


def _log(path):
    p = os.path.join(HERE, 'fixlogs', path)
    return open(p).read().splitlines() if os.path.exists(p) else []


def verify_table(C):
    """Independent re-implementations, board by board: verify_A (result_*.json), verify_B (fixlogs/vB_*.log)."""
    vb_run = {}
    for line in _log('vB_run.log'):
        m = re.match(r'(\S+) quiet placements mine/jsonl (\d+) (\d+) mismatches (\{.*\})', line)
        if m:
            vb_run[m.group(1)] = (int(m.group(2)), sum(ast.literal_eval(m.group(4)).values()))
    vb_c1 = {}
    for line in _log('vB_check1.log'):
        m = re.match(r'MY check1 (\S+) compared (\d+) .* differences (\d+)', line)
        if m:
            vb_c1[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    A = {a['board']: a for a in C['verify_A']}
    head = ['board', 'A: placements compared', 'A: differences (signature, matched set, decisive, difference test, chess)',
            'A: nodes compared with kpsolve', 'A: kpsolve differences', 'B: placements compared', 'B: differences',
            'B: nodes compared with kpsolve', 'B: kpsolve differences']
    out = ['| ' + ' | '.join(head) + ' |', '|---|' + '---:|' * (len(head) - 1)]
    tot = [0] * 8
    for b in boards():
        k = '%s:%s' % b
        a = A[k]
        da = a['sig_diff'] + a['matched_diff'] + a['decisive_diff'] + a['diff_test_diff'] + a['chess_diff']
        row = [a['compared'], da, a['kpsolve']['compared_all_nodes'], a['kpsolve']['diffs_all'],
               vb_run.get(k, (0, 0))[0], vb_run.get(k, (0, 0))[1], vb_c1.get(k, (0, 0))[0], vb_c1.get(k, (0, 0))[1]]
        tot = [x + y for x, y in zip(tot, row)]
        out.append('| %s | ' % name(b) + ' | '.join(str(x) for x in row) + ' |')
    out.append('| **all 10 boards** | ' + ' | '.join('**%d**' % x for x in tot) + ' |')
    return '\n'.join(out), tot


def unreachable_total():
    n = [int(m.group(1)) for line in _log('vA_nodecheck.log') for m in [re.search(r'unreachable (\d+) extra', line)] if m]
    return sum(n), n


def check2_table():
    from checks import check2
    out = ['| fact | expected (White starts, Black starts) | computed | reading | |', '|---|---|---|---|---|']
    ok = 0
    for desc, exp, got, reading, good in check2():
        out.append('| `%s` | %s | %s | %s | %s |' % (desc, exp, got, reading, 'pass' if good else 'FAIL'))
        ok += good
    return '\n'.join(out), ok
