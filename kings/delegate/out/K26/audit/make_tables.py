#!/usr/bin/env python3
"""K26: markdown tables for FINDINGS.md from the FRESH runs of this attempt (logs/k26f_*, logs/k26c_*, logs/k26f_over3_*).  Writes audit/tables.md."""
import glob, json, os, re, collections
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(OUT, 'logs')
def load(prefix, typ):
    runs = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(LOG, prefix + '_*_summary.json'))):
        name = os.path.basename(f)[:-len('_summary.json')]
        m = re.match(r'^%s_(flat|cyl)_(\d+x\d+)_(\d)(\d)_(t1|t2)(?:_s(\d+)of(\d+))?$' % prefix, name)
        if not m: continue
        kind, dims, nw, nb, t, si, sn = m.groups()
        if t != typ: continue
        runs[(kind + ':' + dims, int(nw), int(nb))].append((int(sn) if sn else 1, int(si) if si else 0, json.load(open(f)), name))
    return runs
BOARDS = ['flat:7x6', 'cyl:7x6', 'cyl:8x6', 'flat:8x6', 'flat:7x7']
def key(k): return (BOARDS.index(k[0]), k[1] + k[2], k[1])
L = []
def P(*a): L.append(' '.join(str(x) for x in a))
fm = lambda x: format(x, ',')
# ---------------------------------------------------------------- t2
for prefix, title in (('k26f', 'per promotion piece (kpp lists Q, R, B, N separately: a promotion that does not lose counts as 4 leaks)'),
                      ('k26c', 'promotions counted once (a promotion push or capture is one move)')):
    runs = load(prefix, 't2')
    P('### T2 (both kings shuttle), fresh runs, leaks %s' % title)
    P('')
    P('| board | pawns W+B | placements | shards | exact duds (total 0) | total 1 | total 2 | min total | exact duds with textbook passer / without |')
    P('|---|---|---|---|---|---|---|---|---|')
    groups = {}
    for k in sorted(runs, key=key):
        lst = runs[k]; n = lst[0][0]
        done = sorted(s[1] for s in lst) == list(range(n))
        if not done:
            continue     # unfinished shard sets are not tabulated (section 8 lists what was not re-run)
        h = collections.Counter(); cand = 0
        for s in lst:
            cand += s[2]['candidates']
            for a, b in s[2]['stage2_hist_total_leaks_8roots'].items(): h[int(a)] += b
        mins = min(s[2]['min_total_leaks_8roots'] for s in lst)
        T = min(s[2]['stage2_T_reached'] for s in lst)
        recs = []
        for s in lst:
            for line in open(os.path.join(LOG, s[3] + '_groups.jsonl')):
                recs.append(json.loads(line))
        duds = [r for r in recs if r['total'] == 0]
        wp = sum(1 for r in duds if r['passW'] or r['passB']); np_ = len(duds) - wp
        groups[k] = (recs, duds)
        P('| %s | %d+%d | %s | %d/%d%s | %d | %d | %d | %d | %d / %d |' % (k[0], k[1], k[2], fm(cand), len(lst), n, '' if done else ' (INCOMPLETE)', len(duds), h[1] if T >= 1 else -1, h[2] if T >= 2 else -1, mins, wp, np_))
    P('')
    if prefix == 'k26f':
        P('### Every exact dud found (fresh runs; each listed once per board, with the smallest pawn limits at which it appeared)')
        P('')
        P('| board | White king shuttle | Black king shuttle | White pawns | Black pawns | textbook passer | first found at |')
        P('|---|---|---|---|---|---|---|')
        seen = {}
        for k in sorted(groups, key=key):
            for r in groups[k][1]:
                kk = (k[0], tuple(r['W']), tuple(r['B']), tuple(r['wp']), tuple(r['bp']))
                if kk not in seen:
                    seen[kk] = (r, '%d+%d' % (k[1], k[2]))
        for kk, (r, lim) in seen.items():
            P('| %s | %s | %s | %s | %s | %s | %s |' % (kk[0], '/'.join(r['W']), '/'.join(r['B']), ' '.join(r['wp']), ' '.join(r['bp']), 'yes' if (r['passW'] or r['passB']) else 'no', lim))
        P('')
        P('### Examples of the smallest non-zero leak counts (per piece convention)')
        P('')
        P('| board | pawns | total | White king shuttle | Black king shuttle | White pawns | Black pawns | the non-losing non-shuttle moves (one root) |')
        P('|---|---|---|---|---|---|---|---|')
        for k in sorted(groups, key=key):
            recs = groups[k][0]
            pos = sorted([r for r in recs if r['total'] > 0], key=lambda r: (r['total'], r['W'], r['wp'], r['bp']))
            for r in pos[:2]:
                lk = [x for x in r['leaks']][:1]
                P('| %s | %d+%d | %d | %s | %s | %s | %s | %s |' % (k[0], k[1], k[2], r['total'], '/'.join(r['W']), '/'.join(r['B']), ' '.join(r['wp']), ' '.join(r['bp']), ' '.join('%s:%s' % tuple(x) for x in lk[0]) if lk else ''))
        P('')
# ---------------------------------------------------------------- t1
runs = load('k26f', 't1')
P('### T1 (White king shuttles, Black king on one square; Black-shuttler versions are the colour mirror), fresh runs')
P('')
P('| board | pawns W+B | placements | exact on (on_strong) | on_weak (Black frozen only) | loose under/over (old class over_exact: (U1)-(U3) as tested there, exactly one freeze at each Black-to-move root; section 3) |')
P('|---|---|---|---|---|---|')
for k in sorted(runs, key=key):
    lst = runs[k]; n = lst[0][0]
    done = sorted(s[1] for s in lst) == list(range(n))
    cl = collections.Counter(); cand = 0
    for s in lst:
        cand += s[2]['candidates']
        for a, b in s[2]['classes'].items(): cl[a] += b
    P('| %s | %d+%d | %s%s | %d | %s | %d |' % (k[0], k[1], k[2], fm(cand), '' if done else ' (INCOMPLETE)', cl['on_strong'], fm(cl['on_weak']), cl['over_exact']))
P('')
# ---------------------------------------------------------------- over3
P('### Exact under/over, mutual zugzwang (U1)-(U4)')
P('')
P('| source | board | pawns W+B | files | placements | survivors of (king filter and) (U1)-(U3) at one root | at all four roots | dropped at (U4) | dropped (a freeze is a promotion) | exact groups |')
P('|---|---|---|---|---|---|---|---|---|---|')
for src, pat in (('fresh (over3.py, king filter)', 'k26f_over3_*.json'), ('earlier attempt, reused (over3.py, king filter)', 'over3_*.json'), ('earlier attempt, reused (over2.py, NO king filter)', 'over2_*.json')):
    agg = collections.OrderedDict()
    for f in sorted(glob.glob(os.path.join(LOG, pat))):
        d = json.load(open(f))
        k = (d['board'], d['limits'][0], d['limits'][1], d['nf'])
        a = agg.setdefault(k, collections.Counter()); a['files'] += 1
        a['cand'] += d['candidates']; a['A'] += d['stageA_survivors']; a['B'] += d['stageB_survivors']
        c = d['classes']; a['u4'] += c.get('stageB_survivors_dropped_by_stageC_first_failure:U4', 0)
        a['promo'] += c.get('stageB_survivors_dropped_by_stageC_first_failure:promotion', 0)
        a['groups'] += len(d['groups'])
    for k, a in sorted(agg.items(), key=lambda kv: (BOARDS.index(kv[0][0]), kv[0][3], kv[0][1] + kv[0][2])):
        P('| %s | %s | %d+%d | %s | %s | %s | %s | %s | %s | %d |' % (src, k[0], k[1], k[2], 'a-%s' % 'abcd'[k[3] - 1], fm(a['cand']), fm(a['A']), fm(a['B']), fm(a['u4']), fm(a['promo']), a['groups']))
P('')
open(os.path.join(OUT, 'audit', 'tables.md'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
