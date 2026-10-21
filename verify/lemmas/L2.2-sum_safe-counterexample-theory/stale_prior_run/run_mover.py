"""Rows 4 and 5 under the MOVER race rule: local-e.p. S, global-e.p. S, and W (independent code)."""
import sys
sys.path.insert(0, ".")
from indep import B, parse, make_solvers
from run_ep_rows import sglob
for bk, text in [((8, 8, True, True), "W: a2 c4 e4 h2 / B: a6 b5 d7 e7"),
                 ((8, 8, True, True), "W: a5 b6 d2 e2 / B: a7 c7 e7")]:
    bd = B(*bk); x = parse(text)
    oW, oS, _, _ = make_solvers(bd, "mover", 256)
    print(bk, text, "[mover]  o(S local ep) =", oS(x), " o(S global ep) =", sglob(bd, "mover", 256)(x), " o(W) =", oW(x))
