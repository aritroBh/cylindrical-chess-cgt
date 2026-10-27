"""K19: full-board values. Own P solver (fullp.py) on every position of the claims, and the input files for the
kp / kp_p runs (compare.py reads both). Usage: fullboard.py own <set>   |   fullboard.py list <set>
Sets: s51 (cyl:8x8), s52 (cyl:8x8), s52f (flat:8x8), s52a (cyl:7x6, the analogue Z_72, bare and sorties),
      s52h (cyl:7x6, Z_72 + Hp1), s55 (cyl:8x6)."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from k19engine import *
from fullp import solve_p, white_pov

HERE = os.path.dirname(os.path.abspath(__file__))


def both(txt):
    return [txt + ' w -', txt + ' b -']


def sets():
    S = {}
    # 5.1
    L = both('Kh5 Pa4 kb4 pa5')
    for s in ['g4', 'g5', 'g6', 'h6', 'a6']:
        L.append('K%s Pa4 kb4 pa5 b -' % s)
    for s in ['a3', 'b3', 'c3', 'c4', 'c5']:
        L.append('Kh5 Pa4 k%s pa5 w -' % s)
    S['s51'] = ('cyl:8x8', L)
    # 5.2 on 8x8 cylinder and flat
    L = both('Ke6 Pd7 kd8 pe7')
    for s in ['d5', 'e5', 'f5', 'f7']:
        L.append('K%s Pd7 kd8 pe7 b -' % s)
    S['s52'] = ('cyl:8x8', L)
    S['s52f'] = ('flat:8x8', list(L))
    # 6-rank analogue Z_72 = Kc4 Pb5 / kb6 pc5
    L = both('Kc4 Pb5 kb6 pc5')
    for s in ['b3', 'c3', 'd3', 'd5']:
        L.append('K%s Pb5 kb6 pc5 b -' % s)
    S['s52a'] = ('cyl:7x6', L)
    S['s52h'] = ('cyl:7x6', both('Kc4 Pb5 kb6 pc5 Pe2 Pe4 pe5'))
    # 5.5 Z_on
    L = both('Ka4 Pb2 kc4 pb3')
    for s in ['c5', 'd3', 'd4', 'd5']:
        L.append('Ka4 Pb2 k%s pb3 w -' % s)
    S['s55'] = ('cyl:8x6', L)
    return S


def main():
    S = sets()
    mode, name = sys.argv[1], sys.argv[2]
    spec, lines = S[name]
    if mode == 'list':
        print('\n'.join(lines))
        return
    B = parse_board(spec)
    roots = [parse_pos(B, l) for l in lines]
    res, n = solve_p(B, roots)
    out = {'board': spec, 'states': n, 'rows': []}
    for l, r in zip(lines, roots):
        out['rows'].append({'pos': l, 'P_white_pov': white_pov(r, res[r])})
        print(spec, l, 'P:', white_pov(r, res[r]), flush=True)
    json.dump(out, open(os.path.join(HERE, '..', 'own_P_%s.json' % name), 'w'), indent=1)


main()
