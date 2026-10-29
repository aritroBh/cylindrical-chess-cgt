#!/usr/bin/env python3
"""K26 attempt 5 (copy of final_ctx.py reading only the FRESH context runs logs/f/ctx and logs/f/exh): one table of every context test (the later file overrides an earlier one for the same group id and context files):
logs/ctx_phase1.json, ctx_phase2.json, ctx_over_*.json, ctx_cyl8_ef.json, topup/ctx_*.json  (sampled contexts: <= 2+2 pawns on two files at distance >= 2 from F_Z; each
root solved with kpp, the first 'ref3 roots' of them also with ref3; prediction by the D-model of dmodel.py: dud, on, off, under, over)
and logs/exh/*.json (exhaustive contexts: every placement of <= 3 context pawns, either colour, on the files given).
Writes logs/final_ctx.json and prints markdown."""
import glob, json, os, collections, ast
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(OUT, 'logs')
rows = collections.OrderedDict()
files = sorted(glob.glob(os.path.join(L, 'f', 'ctx', 'ctx_final_*.json')))
for f in files:
    if os.path.exists(f):
        for r in json.load(open(f)):
            rows[(r['id'], r['context_files'])] = dict(r, src=os.path.relpath(f, L))
print('### Sampled contexts (<= 2+2 context pawns on two files)')
print('| group (orientation ~ = colour mirror) | board | kings W / B | pawns W / B | reading | ctx files | contexts | roots | roots = D-model | contexts with a difference | ref3 roots (mismatches) | Prop 4.6 conclusion holds / premise roots |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|')
agg = collections.defaultdict(collections.Counter)
for (gid, cf), r in rows.items():
    print('| %s | %s | %s / %s | %s / %s | %s | %s | %d | %d | %d | %d | %d (%d) | %d / %d |' % (
        gid, r['board'], ' '.join(r['wk']), ' '.join(r['bk']), ' '.join(r['wp']), ' '.join(r['bp']), r['reservoir'], cf, r['contexts'], r['roots'],
        r['roots_agree_with_D_model'], r['contexts_with_a_disagreement'], r['roots_checked_by_checker'], r['kpp_vs_checker_value_mismatches'],
        r['prop46_conclusion_holds'], r['prop46_premise_roots']))
    cls = 'dud(blocked, Z_C-type)' if ('a2c4-a3c5' in gid or 'a4c2-a5c3' in gid) else r['reservoir']
    a = agg[(cls, r['board'], cf)]
    a['group-orientations'] += 1
    a['contexts'] += r['contexts']; a['roots'] += r['roots']; a['agree'] += r['roots_agree_with_D_model']; a['ctx_differ'] += r['contexts_with_a_disagreement']
    a['ref3_roots'] += r['roots_checked_by_checker']; a['ref3_mismatch'] += r['kpp_vs_checker_value_mismatches']
    a['p46_prem'] += r['prop46_premise_roots']; a['p46_ok'] += r['prop46_conclusion_holds']
base = [(k, r) for k, r in rows.items() if not k[0].endswith('~')]
print()
print('groups tested in the sampled runs: %d group ids (base orientation) + %d colour mirrors; base orientations with >= 60 contexts: %d of %d' % (
    len(base), len(rows) - len(base), sum(1 for k, r in base if r['contexts'] >= 60), len(base)))
print()
print('### Aggregates of the sampled runs by reading, board, files')
print('| reading | board | files | group-orientations | contexts | roots | roots = prediction | contexts differ | ref3 roots (mismatches) | Prop 4.6 conclusion holds / premise roots |')
print('|---|---|---|---|---|---|---|---|---|---|')
for k, a in sorted(agg.items()):
    print('| %s | %s | %s | %d | %d | %d | %d | %d | %d (%d) | %d / %d |' % (k[0], k[1], k[2], a['group-orientations'], a['contexts'], a['roots'], a['agree'], a['ctx_differ'], a['ref3_roots'], a['ref3_mismatch'], a['p46_ok'], a['p46_prem']))
exh = collections.defaultdict(lambda: collections.Counter())
exh_bad = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(L, 'f', 'exh', '*_m3_s*.json'))):
    d = json.load(open(f))
    key = (d['group'], d['board'], d['files'])
    rr = d['rows']
    if isinstance(rr, str):
        rr = ast.literal_eval(rr)
    e = exh[key]
    e['shards'] += 1
    e['contexts'] += d['contexts']; e['bad'] += d['bad_contexts']
    for r in rr:
        e['roots'] += len(r['P'])
        e['roots_differ'] += sum(1 for p, q in zip(r['P'], r['D']) if p != q)
        if r['bad'] and len(exh_bad[key]) < 6 and (len(r['W']) + len(r['B'])) <= 2:
            exh_bad[key].append(r)
print()
print('### Exhaustive contexts (every placement of <= 3 context pawns, either colour, ranks 2..H-1; D-model prediction for dud_D)')
print('| group | board | context files | shards done | contexts | contexts with a difference | roots | roots that differ |')
print('|---|---|---|---|---|---|---|---|')
for k, e in sorted(exh.items()):
    print('| %s | %s | %s | %d | %d | %d | %d | %d |' % (k[0], k[1], k[2], e['shards'], e['contexts'], e['bad'], e['roots'], e['roots_differ']))
json.dump({'sampled': {'%s|%s' % k: {kk: vv for kk, vv in r.items() if kk != 'disagreement_examples'} for k, r in rows.items()},
           'exhaustive': {'%s|%s|%s' % k: dict(e) for k, e in exh.items()},
           'exhaustive_small_differences_examples': {'%s|%s|%s' % k: v for k, v in exh_bad.items()}}, open(os.path.join(L, 'f', 'final_ctx_fresh.json'), 'w'), indent=1)
