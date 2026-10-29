#!/usr/bin/env python3
"""Markdown table of the context tests: logs/ctx_phase1.json, ctx_phase2.json, ctx_over_*.json (later files override earlier ones
for the same group id; phase 1 and 2 used the same seed, so a repeated group gives the same numbers)."""
import glob, json, os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(OUT, 'logs')
rows = {}
for f in [os.path.join(L, 'ctx_phase1.json'), os.path.join(L, 'ctx_phase2.json')] + sorted(glob.glob(os.path.join(L, 'ctx_over_*.json'))) + [os.path.join(L, 'ctx_cyl8_ef.json')]:
    if os.path.exists(f):
        for r in json.load(open(f)):
            key = r['id'] + ('  [files %s]' % r['context_files'] if r.get('context_files') == 'ef' and r['board'] == 'cyl:8x6' else '')
            rows[key] = r
print('| group id | board | kings W / B | pawns W / B | reservoir read | contexts | roots | roots = D-model | roots differing (contexts) | ref3 re-solved roots (mismatches) | Prop 4.6 premise roots / conclusion holds |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
tot = [0, 0, 0, 0, 0]
for gid, r in rows.items():
    print('| %s | %s | %s / %s | %s / %s | %s | %d | %d | %d | %d (%d) | %d (%d) | %d / %d |' % (
        gid, r['board'], ' '.join(r['wk']), ' '.join(r['bk']), ' '.join(r['wp']), ' '.join(r['bp']), r['reservoir'], r['contexts'], r['roots'],
        r['roots_agree_with_D_model'], r['roots_disagree'], r['contexts_with_a_disagreement'], r['roots_checked_by_checker'],
        r['kpp_vs_checker_value_mismatches'], r['prop46_premise_roots'], r['prop46_conclusion_holds']))
    tot[0] += r['contexts']; tot[1] += r['roots']; tot[2] += r['roots_agree_with_D_model']; tot[3] += r['roots_disagree']; tot[4] += r['roots_checked_by_checker']
print()
print('total: %d group-orientations, %d contexts, %d roots, %d agree, %d differ, %d roots re-solved by ref3' % (len(rows), tot[0], tot[1], tot[2], tot[3], tot[4]))
