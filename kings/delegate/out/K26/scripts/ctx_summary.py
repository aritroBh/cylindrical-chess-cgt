#!/usr/bin/env python3
"""Aggregate the context tests (same row selection as ctx_table.py) by reservoir read and board; prints a markdown table and writes logs/ctx_summary.json."""
import glob, json, os, collections
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(OUT, 'logs')
rows = {}
for f in [os.path.join(L, 'ctx_phase1.json'), os.path.join(L, 'ctx_phase2.json')] + sorted(glob.glob(os.path.join(L, 'ctx_over_*.json'))) + [os.path.join(L, 'ctx_cyl8_ef.json')]:
    if os.path.exists(f):
        for r in json.load(open(f)):
            key = r['id'] + ('@ef' if r.get('context_files') == 'ef' and r['board'] == 'cyl:8x6' else '')
            rows[key] = r
agg = collections.defaultdict(lambda: collections.Counter())
for k, r in rows.items():
    kind = 'dud-blocked(no passer)' if 'a2c4-a3c5' in k or 'a4c2-a5c3' in k else r['reservoir']
    key = (r['reservoir'] if kind == r['reservoir'] else kind, r['board'], r['context_files'])
    a = agg[key]
    a['group-orientations'] += 1
    a['contexts'] += r['contexts']; a['roots'] += r['roots']; a['agree'] += r['roots_agree_with_D_model']
    a['contexts_differ'] += r['contexts_with_a_disagreement']; a['ref3m_roots'] += r['roots_checked_by_checker']
    a['ref3m_mismatch'] += r['kpp_vs_checker_value_mismatches']
    a['p46_prem'] += r['prop46_premise_roots']; a['p46_ok'] += r['prop46_conclusion_holds']
print('| reading | board | ctx files | group-orientations | contexts | roots | roots = prediction | contexts with a difference | ref3m roots (mismatches) | Prop 4.6 premise roots / conclusion holds |')
print('|---|---|---|---|---|---|---|---|---|---|')
for k in sorted(agg):
    a = agg[k]
    print('| %s | %s | %s | %d | %d | %d | %d | %d | %d (%d) | %d / %d |' % (k[0], k[1], k[2], a['group-orientations'], a['contexts'], a['roots'], a['agree'], a['contexts_differ'], a['ref3m_roots'], a['ref3m_mismatch'], a['p46_prem'], a['p46_ok']))
json.dump({'|'.join(k): dict(v) for k, v in agg.items()}, open(os.path.join(L, 'ctx_summary.json'), 'w'), indent=1)
