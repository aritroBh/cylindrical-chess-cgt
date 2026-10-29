#!/usr/bin/env python3
"""K26 attempt 5: merge logs/f/audit/audit*_s*of8.json (fresh second-enumerator + second-solver audits) and compare with the fresh main searches (logs/k26f_*). Writes audit/audit_fresh.txt."""
import glob, json, os, re, collections
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(OUT, 'logs')
rows = collections.OrderedDict()
for f in sorted(glob.glob(os.path.join(L, 'f', 'audit', 'audit*_s*of8.json'))):
    nm = os.path.basename(f); d = json.load(open(f))
    typ = 't1' if nm.startswith('audit1_') else 't2'
    a = rows.setdefault((typ, d['board']), collections.Counter())
    a['shards'] += 1; a['placements'] += d['placements']
    mm = d.get('full_list_mismatches') or d.get('mismatches') or {}
    a['roots'] += mm.get('roots', 0); a['value_mm'] += mm.get('value', 0); a['moves_mm'] += mm.get('moves', 0)
    a['shuttle_not_once'] += mm.get('shuttle_not_exactly_once', 0); a['illegal_root'] += mm.get('illegal_root', 0)
    if typ == 't2':
        a['leakcount_disagree'] += d['stage1_leak_count_disagreements_kpp_vs_ref3m'] + d['stage2_leak_count_disagreements']
        for sv in ('kpp', 'ref3m'):
            for t, v in d['stage2_hist_' + sv].items():
                if int(t) <= 2: a['%s_tot%s' % (sv, t)] += v
    else:
        for t, v in d['classes'].items(): a[t] += v
out = []
for (typ, board), a in rows.items():
    if typ == 't2':
        out.append('t2 %-9s shards %d/8 placements %s roots compared (full move lists) %s | value mismatches %d, move-list mismatches %d, leak-count disagreements %d | total0 kpp/ref3m %d/%d total1 %d/%d total2 %d/%d' % (
            board, a['shards'], format(a['placements'], ','), format(a['roots'], ','), a['value_mm'], a['moves_mm'], a['leakcount_disagree'], a['kpp_tot0'], a['ref3m_tot0'], a['kpp_tot1'], a['ref3m_tot1'], a['kpp_tot2'], a['ref3m_tot2']))
    else:
        out.append('t1 %-9s shards %d/8 placements %s roots compared %s | value mismatches %d, move-list mismatches %d | classes %s' % (
            board, a['shards'], format(a['placements'], ','), format(a['roots'], ','), a['value_mm'], a['moves_mm'], {k: v for k, v in a.items() if k.startswith(('on_', 'over_'))}))
open(os.path.join(OUT, 'audit', 'audit_fresh.txt'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
