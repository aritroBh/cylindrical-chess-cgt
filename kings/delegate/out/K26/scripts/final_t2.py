#!/usr/bin/env python3
"""K26 final: merge the promotion-collapsed two-shuttle searches (logs/c2_*_t2*_summary.json, groups in logs/c2_*_groups.jsonl) into logs/final_t2.json
and print markdown tables: per board and pawn limit, the number of two-shuttle placements, of placements with total leaks 0, 1, 2 at all 8 roots (the counts are
complete for totals <= 2 because every shard reached T >= 2), their textbook-passer split, the minimum, and the examples of the smallest positive total.
A leak is a legal non-shuttle move of the side to move whose child is not lost for the mover (L for White, W for Black in the P model); a promotion counts once."""
import glob, json, os, re, collections
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(OUT, 'logs')
runs = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(LOG, 'c2_*_t2*_summary.json'))):
    name = os.path.basename(f)[:-len('_summary.json')]
    m = re.match(r'^c2_(flat|cyl)_(\d+x\d+)_(\d)(\d)_t2(?:_s(\d+)of(\d+))?$', name)
    if not m:
        continue
    kind, dims, nw, nb, si, sn = m.groups()
    runs[(kind + ':' + dims, int(nw), int(nb))].append((int(sn) if sn else 1, int(si) if si else 0, name, json.load(open(f))))
res = {}
order = ['flat:7x6', 'cyl:7x6', 'cyl:8x6', 'flat:8x6', 'flat:7x7']
for key in sorted(runs, key=lambda k: (order.index(k[0]), -k[1] - k[2], k[1])):
    lst = runs[key]
    n = lst[0][0]
    complete = sorted(s[1] for s in lst) == list(range(n))
    hist = collections.Counter()
    cand = 0
    exact_all = True
    for (_, _, name, s) in lst:
        cand += s['candidates']
        for t, c in s['stage2_hist_total_leaks_8roots'].items():
            hist[int(t)] += c
        exact_all &= s['min_is_exact_over_all_candidates'] and s['stage2_T_reached'] >= 2
    gr = collections.defaultdict(list)
    for (_, _, name, s) in lst:
        for line in open(os.path.join(LOG, name + '_groups.jsonl')):
            d = json.loads(line)
            gr[d['total']].append(d)
    split = {}
    for t in (0, 1, 2):
        p = sum(1 for d in gr[t] if d['passW'] or d['passB'])
        split[t] = (p, len(gr[t]) - p)
    mn = min(hist) if hist else None
    pos = [t for t in (1, 2) if gr[t]]
    ex = []
    if pos:
        for d in sorted(gr[pos[0]], key=lambda d: (''.join(d['wp']) + '/' + ''.join(d['bp']))) [:6]:
            ex.append({'total': d['total'], 'W': d['W'], 'B': d['B'], 'wp': d['wp'], 'bp': d['bp'], 'roots': [r[0] for r in d['roots']],
                       'first_leaks': [[tuple(x) for x in rl] for rl in d.get('leaks', [])][:2]})
    res['%s %d+%d' % key] = {'board': key[0], 'limits': [key[1], key[2]], 'complete': complete, 'placements': cand,
                             'total0': hist[0], 'total1': hist[1], 'total2': hist[2], 'min_total': mn, 'counts_complete_for_totals_le_2': exact_all,
                             'passer_split_(with,without)': {str(t): split[t] for t in split}, 'examples_of_smallest_positive_total': ex}
json.dump(res, open(os.path.join(LOG, 'final_t2.json'), 'w'), indent=1)
print('| board | pawns W+B | placements | total 0 (passer / none) | total 1 (passer / none) | total 2 (passer / none) | min total |')
print('|---|---|---|---|---|---|---|')
for k, r in res.items():
    s = r['passer_split_(with,without)']
    print('| %s | %d+%d | %s | %d (%d / %d) | %d (%d / %d) | %d (%d / %d) | %s |%s' % (
        r['board'], r['limits'][0], r['limits'][1], format(r['placements'], ','), r['total0'], s['0'][0], s['0'][1], r['total1'], s['1'][0], s['1'][1],
        r['total2'], s['2'][0], s['2'][1], r['min_total'], '' if r['complete'] else '  (INCOMPLETE)'))
