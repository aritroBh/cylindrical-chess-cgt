"""Build 10 pairs of two LIVE non-passer nonzero components (3 pawns each) on cyl:8x6 (A on d, B on f).
Run: PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames ../../.venv/bin/python gen2.py"""
import json, itertools
from cylcgt import pawns, cgt
R = '/Users/aritro/Downloads/Research/Chessendgames'; OUT = R + '/research/sum_truth_cyl'
H = 6; W = 8
SRC = {'1': 'W: d2 d4 / B: d5', '-1': 'W: d2 / B: d3 d5', 'h': 'W: d2 d3 / B: d5', '-h': 'W: d2 / B: d4 d5'}
def parse(P):
    w, b = P.split('/')
    sq = lambda s: [(ord(t[0]) - 97, int(t[1])) for t in s.replace('W:', '').replace('B:', '').split()]
    return sq(w), sq(b)
def shift(P, tf):
    ws, bs = parse(P); return [(tf, r) for f, r in ws], [(tf, r) for f, r in bs]
nm = lambda f, r: 'abcdefgh'[f] + str(r)
Z = ['Pa3', 'pa4', 'Kh4', 'kb3']
toks = lambda c: ['P' + nm(*s) for s in c[0]] + ['p' + nm(*s) for s in c[1]]
txt = lambda c: 'W: ' + ' '.join(nm(*s) for s in c[0]) + ' / B: ' + ' '.join(nm(*s) for s in c[1])
board = pawns.Board(W, H, True, True)
def cg(comps, aware):
    pawns.PASSED_RESPECTS_EP = aware
    pawns.value.cache_clear() if hasattr(pawns.value, 'cache_clear') else None
    pos = pawns.Pos(frozenset(s for c in comps for s in c[0]), frozenset(s for c in comps for s in c[1]))
    try: g = pawns.value(board, pos)
    except pawns.RaceError: return {'value': None, 'outcome': 'race', 'sum_safe': None}
    return {'value': cgt.show(g), 'outcome': cgt.outcome(g), 'sum_safe': pawns.sum_safe(board, pos)}
combos = [('1','-1'),('1','h'),('1','-h'),('-1','h'),('-1','-h'),('h','-h'),('h','h'),('-h','-h'),('1','1'),('-1','-1')]
items = []
for a, b in combos:
    A = shift(SRC[a], 3); B = shift(SRC[b], 5)
    base = ' '.join(Z + toks(A) + toks(B))
    it = {'tags': [a, b], 'A': txt(A), 'B': txt(B), 'wtm': base + ' w -', 'btm': base + ' b -'}
    for aware, key in ((False, 'textbook'), (True, 'ep-aware')):
        it[key] = cg([A, B], aware); it[key + '_A'] = cg([A], aware); it[key + '_B'] = cg([B], aware)
    for tag, c in (('A', A), ('B', B)):
        s = ' '.join(Z + toks(c)); it['solo' + tag] = (s + ' w -', s + ' b -')
    items.append(it)
json.dump(items, open(OUT + '/pairs2.json', 'w'), indent=1)
for i, it in enumerate(items): print(i, it['tags'], it['ep-aware'], it['ep-aware_A']['value'], it['ep-aware_B']['value'], it['textbook']['outcome'])
