"""run_calibration.py -- calibration of myeng.py on T50's own families (known results from proof.tex): O_n (odd n >= 5) and
E_n (even n >= 6) are *2 (signature NNPN...), the reduced game of O_17 has 144 nodes and that of E_16 has 104 nodes
(proof.tex, C1).  Token functions are taken from the T50 engine (t50/eng.py)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 't50'))
import myeng as M
import eng as T

HS = tuple(range(8))
for kind, ns in (('O', range(5, 22, 2)), ('E', range(6, 21, 2)), ('F', list(range(7, 22)))):
    for n in ns:
        try:
            toks = {'O': T.O_toks, 'E': T.E_toks, 'F': T.F_toks}[kind](n)
        except AssertionError:
            continue
        pos = tuple(M.parse_file(t) for t in toks)
        assert pos == T.parse(toks)
        sm = M.Full('keep').signature(pos, HS)
        st, _ = T.outcomes(pos, HS)
        extra = ''
        if (kind, n) in (('O', 17), ('E', 16), ('F', 18), ('F', 19)):
            g = M.Graph(pos)
            extra = ' reduced game: %s sig %s' % (g.stats(), g.signature(HS))
        print('%s n=%2d pawns=%2d mine=%s T50=%s%s' % (kind, n, M.npawns(pos), sm, st, extra), flush=True)
