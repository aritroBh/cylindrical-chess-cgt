import itertools, json, sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
from cylcgt import pawns, cgt
D = '/Users/aritro/Downloads/Research/Chessendgames/research/sum_truth_cyl/planB'
H = 6; board = pawns.Board(8, H, True, True)
nm = lambda f, r: 'abcdefgh'[f] + str(r)
Z = ['Pa3', 'pa4', 'Kh4', 'kb3']
comps = []
for f in (3, 5):
    sq = [(f, r) for r in range(2, H)]
    for nw, nb in ((1, 1), (2, 1), (1, 2)):
        for ws in itertools.combinations(sq, nw):
            rest = [s for s in sq if s not in ws]
            for bs in itertools.combinations(rest, nb): comps.append((ws, bs))
def toks(c): return ['P' + nm(*s) for s in c[0]] + ['p' + nm(*s) for s in c[1]]
def txt(c): return 'W: ' + ' '.join(nm(*s) for s in c[0]) + ' / B: ' + ' '.join(nm(*s) for s in c[1])
info = []
for c in comps:
    d = {'P': txt(c), 'ws': c[0], 'bs': c[1], 'npawn': len(c[0]) + len(c[1]), 'wtm': ' '.join(Z + toks(c)) + ' w -', 'btm': ' '.join(Z + toks(c)) + ' b -'}
    for aware, key in ((False, 'textbook'), (True, 'ep-aware')):
        pawns.PASSED_RESPECTS_EP = aware
        try:
            g = pawns.value(board, pawns.Pos(frozenset(c[0]), frozenset(c[1])))
            d[key] = {'value': cgt.show(g), 'outcome': cgt.outcome(g)}
        except pawns.RaceError: d[key] = {'value': None, 'outcome': 'race'}
    info.append(d)
json.dump(info, open(D + '/small_comps.json', 'w'), indent=1)
jobs = {}
jobs['Z'] = [' '.join(Z) + ' w -', ' '.join(Z) + ' b -']
for i in range(0, len(info), 6):
    jobs[f'solo{i//6:02d}'] = [x for d in info[i:i+6] for x in (d['wtm'], d['btm'])]
json.dump(jobs, open(D + '/jobs_solo.json', 'w'))
print(len(info), len(jobs))
