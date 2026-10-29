#!/usr/bin/env python3
"""K26 audit: compare the fresh runs of this attempt (logs/k26f_*) with the reused merged results of the earlier attempt (logs/merged.json).
Writes audit/compare_fresh.txt (also printed).  Compares per (board, limits, type): candidate count, stage-1 histogram (t2), stage-2 histogram up to total 2 (t2),
class counts (t1), and the SET of exact groups (t2: total 0; t1: on_strong) from the *_groups.jsonl files."""
import glob, json, os, re, collections, sys
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(OUT, 'logs')
old = json.load(open(os.path.join(LOG, 'merged.json')))
runs = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(LOG, 'k26f_*_summary.json'))):
    name = os.path.basename(f)[:-len('_summary.json')]
    m = re.match(r'^k26f_(flat|cyl)_(\d+x\d+)_(\d)(\d)_(t1|t2)(?:_s(\d+)of(\d+))?$', name)
    if not m:
        continue
    kind, dims, nw, nb, typ, si, sn = m.groups()
    runs[(kind + ':' + dims, int(nw), int(nb), typ)].append((int(sn) if sn else 1, int(si) if si else 0, json.load(open(f)), name))
def groups_of(name, typ):
    S = set()
    for line in open(os.path.join(LOG, name + '_groups.jsonl')):
        d = json.loads(line)
        if typ == 't2':
            if d['total'] == 0 and all(r[0] == 'D' for r in d['roots']):
                S.add((tuple(d['W']), tuple(d['B']), tuple(d['wp']), tuple(d['bp'])))
        elif d.get('class') == 'on_strong':
            S.add((tuple(d['W']), (d['b0'],), tuple(d['wp']), tuple(d['bp'])))
    return S
out = []
allok = True
for key, lst in sorted(runs.items()):
    board, nw, nb, typ = key
    n = lst[0][0]
    complete = sorted(s[1] for s in lst) == list(range(n))
    o = old.get('%s:%d:%d:%s' % key)
    cand = sum(s[2]['candidates'] for s in lst)
    G = set()
    for s in lst:
        G |= groups_of(s[3], typ)
    msg = '%-10s %d+%d %s shards %d/%d cand %d' % (board, nw, nb, typ, len(lst), n, cand)
    ok = complete and o is not None and o['candidates'] == cand
    if typ == 't2':
        h1 = collections.Counter(); h2 = collections.Counter()
        for s in lst:
            for k, v in s[2]['stage1_hist_total_leaks_at_roots_z0w0'].items(): h1[int(k)] += v
            for k, v in s[2]['stage2_hist_total_leaks_8roots'].items(): h2[int(k)] += v
        mins = [s[2]['min_total_leaks_8roots'] for s in lst]
        msg += ' | min total %s | exact duds %d | total-1 %d total-2 %d' % (min(mins), len(G), h2[1], h2[2])
        if o:
            ok &= (o['stage1_hist'] == {str(k): v for k, v in sorted(h1.items())})
            ok &= (min(mins) == o['min_total_leaks_8roots']) and len(G) == o['exact_dud']
            ok &= all(h2[t] == o['stage2_hist_evaluated'].get(str(t), 0) for t in (0, 1, 2))
    else:
        cl = collections.Counter()
        for s in lst:
            for k, v in s[2]['classes'].items(): cl[k] += v
        msg += ' | classes %s | on_strong groups %d' % (dict(cl), len(G))
        if o:
            ok &= dict(cl) == o['classes'] and len(G) == o['classes'].get('on_strong', 0)
    # group sets against the old jsonl files
    if o:
        oldnames = [os.path.basename(f)[:-len('_groups.jsonl')] for f in glob.glob(os.path.join(LOG, '%s_%s_%d%d_%s*_groups.jsonl' % (board.split(':')[0], board.split(':')[1], nw, nb, typ)))]
        oldnames = [x for x in oldnames if '_nf' not in x]
        OG = set()
        for nm in oldnames:
            OG |= groups_of(nm, typ)
        ok &= (OG == G)
        msg += ' | group sets equal to earlier attempt: %s' % (OG == G)
    msg += ' | MATCH' if ok else ' | **DIFFERENCE**'
    allok &= ok
    out.append(msg)
out.append('ALL MATCH' if allok else 'SOME DIFFERENCE')
open(os.path.join(OUT, 'audit', 'compare_fresh.txt'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
