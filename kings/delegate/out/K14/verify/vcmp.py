import json, collections
meta = json.load(open('ctx_meta.json'))
lines = [l.split(' | ') for l in open('ctx_P.out').read().strip().split('\n')]
assert len(lines) == len(meta)
ctxs = [json.loads(l) for l in open('../logs/small_contexts_fg.jsonl')]
per = collections.defaultdict(list)
for (pos, res), (i, a, b, s, pred) in zip(lines, meta):
    A, B = res.split()
    assert A == B, (pos, res)   # P model exact
    per[i].append((a, b, s, pred, A))
match = 0; mism_ctx = []; mism_roots = 0; contra = 0; mism_pred = collections.Counter()
for i, rows in per.items():
    bad = [r for r in rows if r[3] != r[4]]
    if not bad: match += 1
    else:
        mism_ctx.append(i); mism_roots += len(bad)
        for r in bad:
            mism_pred[r[3]] += 1
            if r[3] in ('W', 'L'): contra += 1
print('contexts', len(per), 'all-8-match', match, 'mismatching contexts', len(mism_ctx), 'mismatching roots', mism_roots)
print('mismatch predictions:', dict(mism_pred), 'W/L predictions contradicted:', contra)
# classify mismatching contexts by which decisive results occur among their mismatching roots
cat = collections.Counter()
for i in mism_ctx:
    res = set(r[4] for r in per[i] if r[3] != r[4])
    cat[tuple(sorted(res))] += 1
print('mismatching contexts by decisive result among mismatching roots (W=White wins, L=Black wins):', dict(cat))
for i in mism_ctx[:20]:
    print(ctxs[i]['w'], ctxs[i]['b'], ctxs[i]['dud'])
