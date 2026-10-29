#!/usr/bin/env python3
"""Merge logs/audit_*_sXofN.json (audit_s1.py) per board and limit; compare with the main search (logs/merged.json and the
*_groups.jsonl of the main search).  Prints a table and writes logs/audit_merged.json."""
import collections, glob, json, os, re
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(OUT, 'logs')
runs = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(LOG, 'audit_*_s*of*.json'))):
    m = re.match(r'^audit_(flat|cyl)_(\d+x\d+)_(\d)(\d)_s(\d+)of(\d+)\.json$', os.path.basename(f))
    if not m:
        continue
    kind, dims, nw, nb, si, sn = m.groups()
    runs[(kind + ':' + dims, int(nw), int(nb))].append((int(si), int(sn), json.load(open(f))))
merged = {}
for key, lst in sorted(runs.items()):
    sn = lst[0][1]
    done = sorted(x[0] for x in lst)
    rec = {'board': key[0], 'limits': [key[1], key[2]], 'shards_done': len(lst), 'shards_total': sn, 'complete': done == list(range(sn)),
           'placements': sum(x[2]['placements'] for x in lst),
           'stage1_leak_count_disagreements': sum(x[2]['stage1_leak_count_disagreements_kpp_vs_ref3m'] for x in lst),
           'stage2_leak_count_disagreements': sum(x[2]['stage2_leak_count_disagreements'] for x in lst),
           'roots_compared_full_lists': sum(x[2]['full_list_mismatches'].get('roots', 0) for x in lst),
           'value_mismatches': sum(x[2]['full_list_mismatches'].get('value', 0) for x in lst),
           'move_list_mismatches': sum(x[2]['full_list_mismatches'].get('moves', 0) for x in lst),
           'illegal_roots': sum(x[2]['full_list_mismatches'].get('illegal_root', 0) for x in lst),
           'shuttle_not_exactly_once': sum(x[2]['full_list_mismatches'].get('shuttle_not_exactly_once', 0) for x in lst),
           'stage2_candidates': sum(x[2]['stage2_candidates'] for x in lst)}
    for solver in ('kpp', 'ref3m'):
        h = collections.Counter()
        for x in lst:
            for k, v in x[2]['stage2_hist_' + solver].items():
                h[int(k)] += v
        rec['hist8_' + solver] = {k: h[k] for k in (0, 1, 2)}
    rec['exact_duds'] = [d for x in lst for d in x[2]['exact_duds']]
    rec['total_1'] = [d for x in lst for d in x[2]['total_1']]
    merged[':'.join(map(str, [key[0], key[1], key[2]]))] = rec
json.dump(merged, open(os.path.join(LOG, 'audit_merged.json'), 'w'), indent=1)
print('| board | pawns | shards | placements | roots compared (full move lists) | value / move-list mismatches | leak-count disagreements (stage 1 / 2) | #total 0 (kpp / ref3m) | #total 1 (kpp / ref3m) | #total 2 (kpp / ref3m) |')
print('|---|---|---|---|---|---|---|---|---|---|')
for k, r in merged.items():
    h = lambda t: '%d / %d' % (r['hist8_kpp'][t], r['hist8_ref3m'][t])
    print('| %s | %d+%d | %d/%d | %s | %s | %d / %d | %d / %d | %s | %s | %s |' % (
        r['board'], r['limits'][0], r['limits'][1], r['shards_done'], r['shards_total'], '{:,}'.format(r['placements']),
        '{:,}'.format(r['roots_compared_full_lists']), r['value_mismatches'], r['move_list_mismatches'],
        r['stage1_leak_count_disagreements'], r['stage2_leak_count_disagreements'], h(0), h(1), h(2)))
