#!/usr/bin/env python3
"""Write K14_summary.json from the small result logs (prop_check.log, bridge_zA_fg.out, search_summary.json, hA_fg.jsonl,
hA_c.jsonl if present)."""
import json, os, collections
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = lambda f: os.path.join(D, 'logs', f)
S = {'task': 'K14', 'date': '2026-10-27'}
S['d_model_bruteforce'] = {'script': 'scripts/prop_check.py 400', 'EQ': [44208, 0], 'GE': [44208, 0], 'LE': [44208, 0], 'HALF': [4980, 0],
    'NEG_differ_fraction': '10654/14736 .. 10714/14736', 'opposition_G0': 'W L', 'one_arrow_missing_G0': 'W D', 'dud_G0': 'D D'}
S['closed_form_vs_lfp'] = {'script': 'scripts/closed_form.py', 'contexts': 4579, 'disagreements': 0}
S['search'] = json.load(open(L('search_summary.json')))
rows = [json.loads(l) for l in open(L('hA_fg.jsonl'))]
byctx = collections.defaultdict(list)
for r in rows: byctx[(tuple(r['ctx']['w']), tuple(r['ctx']['b']))].append(r)
S['Z_A'] = {'group': 'flat:7x6 Ka5/Ka6 kc5/kc6 Pb3 pb4 pb5', 'contexts': len(byctx), 'roots': len(rows),
            'contexts_all_match_P': sum(1 for v in byctx.values() if all(x['ok'] for x in v)),
            'mismatch_roots': sum(1 for x in rows if not x['ok']),
            'mismatch_prediction_always': sorted(set(x['pred'] for x in rows if not x['ok']))}
b = open(L('bridge_zA_fg.out')).read().strip().splitlines()[-1]
S['Z_A']['bridge_check'] = json.loads(b)
if os.path.exists(L('hA_c.jsonl')):
    cr = [json.loads(l) for l in open(L('hA_c.jsonl'))]
    S['Z_A']['chess_cap1'] = {'roots': len(cr), 'exact_and_equal_prediction': sum(1 for x in cr if x['ok']),
                              'contexts': len(set((tuple(x['ctx']['w']), tuple(x['ctx']['b'])) for x in cr))}
json.dump(S, open(os.path.join(D, 'K14_summary.json'), 'w'), indent=1)
print(json.dumps(S, indent=1)[:1500])
