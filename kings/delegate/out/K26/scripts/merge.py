#!/usr/bin/env python3
"""Merge the per-shard summaries in logs/ into logs/merged.json and print a table.
exactness of a merged minimum (type t2): every shard reached its own T >= the global minimum (or its minimum <= its T)."""
import glob, json, os, re, collections, sys
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(OUT, 'logs')
runs = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(LOG, '*_summary.json'))):
    name = os.path.basename(f)[:-len('_summary.json')]
    m = re.match(r'^(flat|cyl)_(\d+x\d+)_(\d)(\d)_(t1|t2)(?:_s(\d+)of(\d+))?$', name)
    if not m:
        continue
    kind, dims, nw, nb, typ, si, sn = m.groups()
    runs[(kind + ':' + dims, int(nw), int(nb), typ)].append((int(sn) if sn else 1, int(si) if si else 0, json.load(open(f)), name))

merged = {}
for key, lst in sorted(runs.items()):
    n = lst[0][0]
    ok_shards = sorted(s[1] for s in lst)
    complete = ok_shards == list(range(n))
    board, nw, nb, typ = key
    rec = {'board': board, 'limits': [nw, nb], 'type': typ, 'shards_done': len(lst), 'shards_total': n, 'complete': complete,
           'candidates': sum(s[2]['candidates'] for s in lst), 'configs': lst[0][2]['configs'],
           'illegal': sum(s[2]['illegal_candidates'] for s in lst), 'seconds': round(sum(s[2]['seconds'] for s in lst), 1)}
    if typ == 't2':
        h1 = collections.Counter()
        for s in lst:
            for k, v in s[2]['stage1_hist_total_leaks_at_roots_z0w0'].items():
                h1[int(k)] += v
        mins = [s[2]['min_total_leaks_8roots'] for s in lst if s[2]['min_total_leaks_8roots'] is not None]
        gmin = min(mins) if mins else None
        exact = all((s[2]['stage2_T_reached'] >= gmin) for s in lst) if gmin is not None else False
        h2 = collections.Counter()
        for s in lst:
            for k, v in s[2]['stage2_hist_total_leaks_8roots'].items():
                h2[int(k)] += v
        rec.update({'stage1_hist': dict(sorted(h1.items())), 'stage2_hist_evaluated': dict(sorted(h2.items())),
                    'stage2_hist_complete_up_to_total': min(s[2]['stage2_T_reached'] for s in lst),
                    'min_total_leaks_8roots': gmin, 'min_exact': exact,
                    'exact_dud': sum(s[2]['exact_dud'] for s in lst),
                    'exact_dud_with_no_textbook_passer': sum(s[2]['exact_dud_no_passer_filter_applied_to_value'] for s in lst),
                    'dud_by_pawns': {}})
        dp = collections.defaultdict(int)
        for s in lst:
            for k, v in s[2]['dud_by_pawns'].items():
                dp[k] += v.get('dud', 0)
        rec['dud_by_pawns'] = dict(dp)
    else:
        cl = collections.Counter()
        clnp = collections.Counter()
        for s in lst:
            for k, v in s[2]['classes'].items():
                cl[k] += v
            for k, v in s[2]['classes_no_passer_in_group'].items():
                clnp[k] += v
        mm = [s[2]['min_on_strong_miss_over_survivors'] for s in lst if s[2]['min_on_strong_miss_over_survivors'] is not None]
        rec.update({'classes': dict(cl), 'classes_no_textbook_passer': dict(clnp), 'over_pre': sum(s[2]['over_pre'] for s in lst),
                    'min_on_strong_miss': min(mm) if mm else None})
    merged[':'.join(map(str, key))] = rec
json.dump(merged, open(os.path.join(LOG, 'merged.json'), 'w'), indent=1)
for k, r in merged.items():
    if r['type'] == 't2':
        print('%-26s cands %9d shards %d/%d  min_total %s (exact %s)  exact_dud %d (no-passer %d)' % (
            k, r['candidates'], r['shards_done'], r['shards_total'], r['min_total_leaks_8roots'], r['min_exact'], r['exact_dud'],
            r['exact_dud_with_no_textbook_passer']))
    else:
        print('%-26s cands %9d shards %d/%d  %s  over_pre %d  minmiss_on %s' % (k, r['candidates'], r['shards_done'], r['shards_total'],
              r['classes'], r['over_pre'], r['min_on_strong_miss']))
