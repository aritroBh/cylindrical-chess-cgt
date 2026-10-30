"""Pick 50 random pairs of matching 7x6 single-file components, embed them on cyl:8x6 (A on d, B on f, e empty),
write kp inputs and cylcgt predictions. Run: PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames .venv/bin/python gen.py"""
import json, re, random, os
from cylcgt import pawns, cgt
R = '/Users/aritro/Downloads/Research/Chessendgames'
OUT = R + '/research/sum_truth_cyl'
H = 6; W = 8
rows = [json.loads(l) for l in open(R + '/kings/results/exp_cyl7x6_epon_Q_conv.jsonl')]
def fl(r): return set(re.findall(r'([a-h])\d', r['P']))
cands = [r for r in rows if r['verdict'] == 'match' and r['verdict_ep-aware'] == 'match' and r['exact'] and len(fl(r)) == 1]
def parse(P):
    w, b = P.split('/')
    sq = lambda s: [(ord(t[0]) - 97, int(t[1])) for t in s.replace('W:', '').replace('B:', '').split()]
    return sq(w), sq(b)
def shift(P, tf):
    ws, bs = parse(P); f0 = ws[0][0] if ws else bs[0][0]
    return [(tf, r) for f, r in ws], [(tf, r) for f, r in bs]
def nm(f, r): return 'abcdefgh'[f] + str(r)
Z = ['Pa3', 'pa4', 'Kh4', 'kb3']
random.seed(20261029)
def locked(P):
    ws, bs = parse(P)
    b = pawns.Board(8, H, True, True)
    pos = pawns.Pos(frozenset(ws), frozenset(bs))
    return not pawns.moves(b, pos, 'W') and not pawns.moves(b, pos, 'B')
LK = [locked(r['P']) for r in rows_c] if False else [locked(r['P']) for r in cands]
print('locked shapes', [cands[i]['P'] for i in range(len(cands)) if LK[i]])
allpairs = [(i, j) for i in range(len(cands)) for j in range(len(cands)) if LK[i] or LK[j]]
print('population (>=1 locked)', len(allpairs), 'of', len(cands) ** 2)
pairs = random.sample(allpairs, 50)
def toks(comp):
    ws, bs = comp
    return ['P' + nm(*s) for s in ws] + ['p' + nm(*s) for s in bs]
def txt(comp):
    ws, bs = comp
    return 'W: ' + ' '.join(nm(*s) for s in ws) + ' / B: ' + ' '.join(nm(*s) for s in bs)
board = pawns.Board(W, H, True, True)
def cg(comps, aware):
    pawns.PASSED_RESPECTS_EP = aware
    pawns.value.cache_clear() if hasattr(pawns.value, 'cache_clear') else None
    ws = frozenset(s for c in comps for s in c[0]); bs = frozenset(s for c in comps for s in c[1])
    pos = pawns.Pos(ws, bs)
    try:
        g = pawns.value(board, pos)
    except pawns.RaceError:
        return {'value': None, 'outcome': 'race', 'sum_safe': None}
    return {'value': cgt.show(g), 'outcome': cgt.outcome(g), 'sum_safe': pawns.sum_safe(board, pos)}
items = []
for i, j in pairs:
    A = shift(cands[i]['P'], 3); B = shift(cands[j]['P'], 5)
    base = ' '.join(Z + toks(A) + toks(B))
    it = {'A_src': cands[i]['P'], 'B_src': cands[j]['P'], 'A': txt(A), 'B': txt(B), 'wtm': base + ' w -', 'btm': base + ' b -'}
    for aware, key in ((False, 'textbook'), (True, 'ep-aware')):
        it[key] = cg([A, B], aware)
        it[key + '_A'] = cg([A], aware); it[key + '_B'] = cg([B], aware)
    for tag, c in (('A', A), ('B', B)):
        b = ' '.join(Z + toks(c)); it['solo' + tag] = (b + ' w -', b + ' b -')
    items.append(it)
json.dump(items, open(OUT + '/pairs.json', 'w'), indent=1)
lines = []
zb = ' '.join(Z); lines += [zb + ' w -', zb + ' b -']
for it in items:
    for k in ('wtm', 'btm'): lines.append(it[k])
    for k in ('soloA', 'soloB'): lines += list(it[k])
lines = list(dict.fromkeys(lines))
open(OUT + '/in_all.txt', 'w').write('\n'.join(lines) + '\n')
print(len(items), len(lines))
