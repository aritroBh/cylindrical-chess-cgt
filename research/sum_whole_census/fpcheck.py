"""Re-check the sum_safe()-True but S != W positions with cylcgt and sumsolver (both modes)."""
import sys
sys.argv = ['x']
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/research/sum_whole_census')
import analyze, importlib.util
R0 = '/Users/aritro/Downloads/Research/Chessendgames'
sys.path.insert(0, R0); sys.path.insert(0, R0 + '/sumtest'); sys.setrecursionlimit(10**6)
from lemmas import common as C
from cylcgt import pawns, cgt
from cylcgt.pawns import Pos, Board
import sumsolver as SS
T, small, thm = analyze.main()
for test in (0, 1):
    for rule in ("count", "mover", "opponent"):
        L = small[('fp', analyze.TESTS[test], rule)]
        pawns.PASSED_RESPECTS_EP = bool(test); pawns.RACE_RULE = rule; pawns._value.cache_clear(); C._W_memo.clear()
        for x in sorted(L):
            text = x[1]
            w = 5
            b = Board(w, 8, False, True); p = Pos.parse(text)
            geo = SS.Geometry(w, False); rules = SS.Rules(geo, ep=True, ep_aware=bool(test), race_rule=rule, race_double=True)
            res = {}
            for mode in ('comp', 'whole'):
                Tr = SS.Trees(); z = Tr.node(); sol = SS.SumSolver(rules, Tr, mode=mode, ep_scope='component')
                W_, B_ = geo.parse(text); res[mode] = sol.outcomes(W_, B_, [z])[0]
            print(analyze.TESTS[test], rule, text, 'fast S/W', x[2], x[3], '| cylcgt S', cgt.outcome(pawns.value(b, p)), 'W', cgt.outcome(C.W(b, p, rule)),
                  '| sumsolver comp', res['comp'], 'whole', res['whole'], '| sum_safe', x[5], 'hss', x[4], 'ncomp', x[6])
