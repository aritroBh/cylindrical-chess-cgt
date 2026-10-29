#!/usr/bin/env python3
"""K26: assemble FINDINGS.md from audit/F_*.md and the generated tables (audit/tables.md, audit/named_table.md, final_ctx_fresh.py output)."""
import os, re, subprocess, sys
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(OUT, 'audit')
PY = '/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python'
env = dict(os.environ, PYTHONPATH='/Users/aritro/Downloads/Research/Chessendgames')
subprocess.run([PY, os.path.join(A, 'audit_merge_fresh.py')], check=True, stdout=subprocess.DEVNULL, env=env)
subprocess.run([PY, os.path.join(A, 'make_tables.py')], check=True, stdout=subprocess.DEVNULL, env=env)
tab = open(os.path.join(A, 'tables.md')).read()
parts = re.split(r'^### ', tab, flags=re.M)[1:]
def sec(prefix):
    for p in parts:
        if p.startswith(prefix):
            return p.split('\n', 1)[1].strip('\n')
    return '(missing: %s)' % prefix
T = {
 'T2_FRESH': sec('T2 (both kings shuttle), fresh runs, leaks per promotion piece'),
 'T2_COLLAPSED': sec('T2 (both kings shuttle), fresh runs, leaks promotions counted once'),
 'DUD_LIST': sec('Every exact dud found'),
 'LEAK_EX': sec('Examples of the smallest non-zero leak counts'),
 'T1': sec('T1 (White king shuttles'),
 'OVER3': sec('Exact under/over, mutual zugzwang'),
 'NAMED': open(os.path.join(A, 'named_table.md')).read().strip('\n'),
}
ctx = subprocess.run([PY, os.path.join(A, 'final_ctx_fresh.py')], capture_output=True, text=True, env=env).stdout
cparts = re.split(r'^### ', ctx, flags=re.M)[1:]
def csec(prefix):
    for p in cparts:
        if p.startswith(prefix):
            return p.split('\n', 1)[1].strip('\n')
    return '(missing: %s)' % prefix
T['AUDIT'] = open(os.path.join(A, 'audit_fresh.txt')).read().strip('\n')
T['CTX_SAMPLED'] = 'Sampled contexts (fresh run, 20 groups, both orientations; reading = the D-model reservoir that was compared):\n\n' + csec('Sampled contexts') + '\n\nAggregates by reading, board, files:\n\n' + csec('Aggregates')
T['CTX_EXH'] = csec('Exhaustive contexts')
if T['CTX_EXH'].count('\n') < 2:     # no fresh exhaustive shards: use the earlier attempt's complete table (logs/final_ctx.json)
    import json
    ex = json.load(open(os.path.join(OUT, 'logs', 'final_ctx.json')))['exhaustive']
    rows = ['| group | board | context files | shards done | contexts | contexts with a difference | roots | roots that differ |', '|---|---|---|---|---|---|---|---|']
    for k, e in sorted(ex.items()):
        g, b, f = k.split('|')
        rows.append('| %s | %s | %s | %d | %d | %d | %d | %d |' % (g, b, f, e['shards'], e['contexts'], e['bad'], e['roots'], e['roots_differ']))
    T['CTX_EXH'] = '\n'.join(rows)
T['CTX_STATS'] = subprocess.run([PY, os.path.join(A, 'ctx_stats.py')], capture_output=True, text=True, env=env).stdout.strip('\n')
body = ''
for f in ('F_head.md', 'F_defs.md', 'F_results.md', 'F_over.md', 'F_on.md', 'F_min.md', 'F_ctx.md', 'F_verdict.md', 'F_reuse.md', 'F_end.md'):
    p = os.path.join(A, f)
    if os.path.exists(p):
        body += open(p).read().rstrip('\n') + '\n\n'
for k, v in T.items():
    body = body.replace('@@%s@@' % k, v)
left = re.findall(r'@@[A-Z0-9_]+@@', body)
open(os.path.join(OUT, 'FINDINGS.md'), 'w').write(body)
print('FINDINGS.md', len(body), 'bytes; unresolved placeholders:', left)
