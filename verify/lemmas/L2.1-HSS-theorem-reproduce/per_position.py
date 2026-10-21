"""Per-position comparison, worker code (lemmas.common / cylcgt) vs independent indep_l21, on the
first N seed-1 samples: o(S), o(W), HSS, and sample identity."""
import sys
sys.path.insert(0, "verify/lemmas/L2.1-HSS-theorem-reproduce")
import indep_l21 as IL
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas.common import S, W, alt_outcome, hereditarily_safe
N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
mism = 0
for i, (bd, x, rule) in enumerate(IL.samples(1500, 1)):
    if i >= N: break
    b = Board(bd.n, bd.m, bd.wrap, bd.ep); p = Pos(x[0], x[1], None)
    ws, ww, wa, wh = cgt.outcome(S(b, p, rule)), cgt.outcome(W(b, p, rule)), alt_outcome(b, p, rule), hereditarily_safe(b, p)
    ms, mw = IL.o_S(bd, x, rule), IL.o_W(bd, x, rule)
    mh = IL.analyse(bd, x)[0]
    if (ws, ww, wa, wh) != (ms, mw, mw, mh):
        mism += 1; print("MISMATCH", i, bd, IL.show(x), rule, (ws, ww, wa, wh), (ms, mw, mh), flush=True)
    if (i + 1) % 100 == 0: print("progress", i + 1, "mismatches", mism, flush=True)
print("compared", min(N, 1500), "mismatches", mism)
