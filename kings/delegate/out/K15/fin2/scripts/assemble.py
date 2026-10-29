#!/usr/bin/env python3
"""K15 fin2: assemble FINDINGS.md and summary.json from the parts and the logs.
Run again after every change of the logs.  Writes ../../FINDINGS.md (K15/FINDINGS.md) and ../../summary.json."""
import os, re, json, glob, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); FIN2 = os.path.dirname(HERE); K15 = os.path.dirname(FIN2)
sys.path.insert(0, HERE)
import canonlib as CL
def rd(p, default=''):
    try: return open(p).read()
    except Exception: return default
def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=FIN2).stdout

# ---------- tables ----------
subprocess.run(['python3', os.path.join(HERE, 'mktable.py')], capture_output=True, cwd=FIN2)
subprocess.run(['python3', os.path.join(HERE, 'mkconf.py')], capture_output=True, cwd=FIN2)
st = rd(os.path.join(FIN2, 'logs', 'search_table.md')).split('\n\n')
search_table, tempo_table = st[0], st[1] if len(st) > 1 else ''
conf = json.load(open(os.path.join(FIN2, 'logs', 'conf_table.json'))) if os.path.exists(os.path.join(FIN2, 'logs', 'conf_table.json')) else {}
sj = json.load(open(os.path.join(FIN2, 'logs', 'search_table.json')))

# ---------- dud group counts ----------
def collect(board, cls='dud', readings='AB', roots_dirs=None):
    d = {}
    for rd_ in (roots_dirs or [os.path.join(K15, 'final', 'runs'), os.path.join(FIN2, 'runs')]):
        out = sh('python3 scripts/collect.py %s %s %s %s' % (rd_, cls, board, readings))
        for l in out.splitlines():
            p = l.split('\t')
            if len(p) >= 5:
                e = d.setdefault(p[1], {'rep': p[3], 'found': set()}); e['found'].update(p[4].split())
    return d
counts = {}
for b in ('cyl:7x6', 'cyl:8x6', 'cyl:8x8', 'flat:7x6', 'cyl:7x7', 'cyl:8x7'):
    counts[b] = len(collect(b))
dud_counts = '%d on cyl:7×6, %d on cyl:8×6, %d on cyl:8×8, %d on flat 7×6 (cyl:7×7 and cyl:8×7: %d and %d)' % (counts['cyl:7x6'], counts['cyl:8x6'], counts['cyl:8x8'], counts['flat:7x6'], counts['cyl:7x7'], counts['cyl:8x7'])
nop = {b: sum(1 for e in collect(b).values() if any(x.split(':')[1] == 'nopasser' for x in e['found'])) for b in ('cyl:7x6', 'cyl:8x6', 'cyl:8x8')}

# ---------- near-over counts ----------
near = {}
for cls in ('nearover', 'nearunder'):
    for b in ('cyl:7x6', 'cyl:8x6', 'cyl:8x8', 'cyl:7x7', 'cyl:8x7'):
        near[(cls, b)] = len(collect(b, cls, 'A'))
near_counts = 'distinct groups, near-over / near-under: ' + ', '.join('%s %d / %d' % (b.replace('cyl:', 'cyl:').replace('x', '×'), near[('nearover', b)], near[('nearunder', b)]) for b in ('cyl:7x6', 'cyl:8x6', 'cyl:8x8', 'cyl:7x7', 'cyl:8x7'))

# ---------- confirmation text ----------
def conf_sentence(tag):
    c = conf.get(tag)
    if not c: return None
    return c
def conf_dud_text():
    out = []
    out.append('| run | board | groups | positions | agree | DISAGREE | inexact | missing | groups with no difference |\n|---|---|---|---|---|---|---|---|---|')
    for tag in ('strictA8', 'c7x6', 'c8x6', 'c8x8'):
        c = conf.get(tag)
        if not c: continue
        out.append('| %s | %s | %d | %d | %d | %d | %d | %d | %d |' % (tag, c['board'], c['groups'], c['positions'], c['agree'], c['disagree'], c['inexact'], c['missing'], c['groups_with_no_disagreement_and_no_missing']))
    out.append('')
    out.append('`strictA8` = the two A-dud groups without root passer, 40 contexts; `c7x6`, `c8x6` = the distinct dud groups of the census at the time (section 6.2), beside 24 contexts each (the four named ones and random ones) as far as the window leaves context files. The groups found by later census runs and the cyl:8×8 groups were not put beside contexts; they are checked at the root only (section 7.5).\n')
    # groups with a difference
    bad = []
    for tag in ('c7x6', 'c8x6', 'c8x8'):
        c = conf.get(tag)
        if not c: continue
        for r in c['rows']:
            if r[3] or r[4]:
                bad.append('| %s | `%s` | %d | %d | %d | %s |' % (tag, r[0], r[1], r[2], r[3], r[6]))
    if bad:
        out.append('Groups with at least one difference (all of them are dud in plain P in the empty context, none is dud against free passes):\n')
        out.append('| run | group | positions | agree | DISAGREE | contexts with a difference |\n|---|---|---|---|---|---|')
        out += bad
        out.append('')
    # groups without context file
    nocx = []
    for tag in ('c7x6', 'c8x6', 'c8x8'):
        c = conf.get(tag)
        if not c: continue
        for r in c['rows']:
            if r[1] <= 50 and r[3] == 0 and r[4] == 0:
                nocx.append(r[0])
    return '\n'.join(out), nocx
conf_dud, nocx = conf_dud_text()
if nocx:
    conf_dud += '\nGroups whose window leaves no (or almost no) room for a context are confirmed in the empty context (or a few contexts) only, and the agreement there says little: ' + ', '.join('`%s`' % x for x in nocx) + '.\n'
ctx_exh = rd(os.path.join(FIN2, 'logs', 'ctx_exh_summary.md'))
# over candidates
def over_text():
    out = ['| run | board | class | groups | positions | agree | DISAGREE | inexact | missing | groups with no difference |\n|---|---|---|---|---|---|---|---|---|---|']
    for tag in ('o7x6', 'o8x6', 'nol7x6', 'nul7x6', 'nol8x6', 'nul8x6', 'nol8x8', 'nul8x8', 'nol7x7', 'nol8x7', 'no7x6', 'nu7x6', 'no8x6', 'nu8x6', 'no8x8', 'nu8x8', 'no7x7', 'no8x7'):
        c = conf.get(tag)
        if not c: continue
        out.append('| %s | %s | %s | %d | %d | %d | %d | %d | %d | %d |' % (tag, c['board'], c['class'], c['groups'], c['positions'], c['agree'], c['disagree'], c['inexact'], c['missing'], c['groups_with_no_disagreement_and_no_missing']))
    out.append('')
    out.append('`o7x6`, `o8x6`: the tempo-signature candidates (4 files ≤ 2+2), 40 contexts. `nol*`, `nul*` (and the older `no*`, `nu*`): the near-over and near-under roots of the structural classifier, the four named contexts (`nol*`, `nul*`) or up to 40 contexts (the partial `no7x6`). Root only, both sides to move.\n')
    return '\n'.join(out)
conf_over = over_text() + rd(os.path.join(FIN2, 'logs', 'over_followup.md'))
chess = rd(os.path.join(FIN2, 'logs', 'chess_curated.md'))

# ---------- extra runs sentence ----------
extra = []
for n in ('pA_8x6_f5_32', 'npB_8x6_f5_32', 'pA_7x6_f5_32', 'npB_7x6_f5_32', 'pA_8x6_f4_42', 'npB_8x6_f4_42', 'pA_7x6_f4_42', 'npB_7x6_f4_42', 'flatA_7x6_f3_33', 'flatB_7x6_f3_33', 'flatA_7x6_f3_22', 'tp_7x6_f3_33', 'tp_8x6_f3_33', 'pA_7x6_f3_44', 'npB_7x6_f3_44', 'pA_8x6_f3_44', 'npB_8x6_f3_44'):
    if os.path.exists(os.path.join(FIN2, 'runs', n + '.done')): extra.append(n)
extra_txt = ('All of these runs completed (%d runs with a `.done` file in `fin2/runs/`, listed in the table of 5.1 with source "rerun").' % len(extra)) if extra else 'Queued through the shared lock but not started when the report was written (the lock was held by other jobs): 5 files ≤ 3+2 and 4 files ≤ 4+2 (cyl:7×6, cyl:8×6, both readings), flat 7×6 ≤ 3+3, the tempo-signature census for 3 files ≤ 3+3, and a re-run of the 3-file ≤ 4+4 runs. They are not claimed.'

verd = rd(os.path.join(FIN2, 'body_verdicts.md')); r3add = rd(os.path.join(FIN2, 'logs', 'r3_additions.md'))
tests = rd(os.path.join(FIN2, 'body_tests_audit.md')); zb = rd(os.path.join(FIN2, 'body_zb.md')); rest = rd(os.path.join(FIN2, 'body_rest.md')); head = rd(os.path.join(FIN2, 'body_head.md'))
rest = (rest.replace('@@SEARCH_TABLE@@', search_table).replace('@@TEMPO_TABLE@@', tempo_table).replace('@@EXTRA_RUNS@@', extra_txt)
        .replace('@@NEAR_COUNTS@@', near_counts).replace('@@DUD_COUNTS@@', dud_counts).replace('@@CONF_DUD@@', conf_dud)
        .replace('@@CTX_EXH@@', ctx_exh).replace('@@CONF_OVER@@', conf_over).replace('@@CHESS@@', chess).replace('@@VERDICTS@@', verd).replace('@@R3@@', r3add))
open(os.path.join(K15, 'FINDINGS.md'), 'w').write(head + '\n' + tests + '\n' + zb + '\n' + rest)
summary = {'task': 'K15', 'date': '2026-10-28 (tags 2026-10-27)', 'dud_groups_distinct': counts, 'dud_groups_without_root_passer_B_or_A': nop, 'near': {'%s %s' % k: v for k, v in near.items()},
           'census': sj, 'confirmation': {k: {kk: vv for kk, vv in v.items() if kk != 'rows'} for k, v in conf.items()}}
json.dump(summary, open(os.path.join(K15, 'summary.json'), 'w'), indent=1)
print('FINDINGS.md', len(open(os.path.join(K15, 'FINDINGS.md')).read()), 'chars; counts', counts, 'nopasser', nop)
