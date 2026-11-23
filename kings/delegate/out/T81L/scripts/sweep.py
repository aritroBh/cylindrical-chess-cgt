import itertools, sys, time
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas import common as C

def usable(b, y):
    if not y.ep: return False
    side = y.ep[2]; f, r = y.ep[1]
    mine = y.white if side == "W" else y.black
    return any((g, r) in mine for g in (b.nb(f,-1), b.nb(f,1)) if g is not None)

def E_ok(b, x):
    for y in C.reachable(b, x):
        if C.terminal(b, y) is None and len(pawns.components(b, y)) > 1 and usable(b, y):
            return False
    return True

t0 = time.time()
for (nf, H, wrap) in [(3,4,False),(4,4,False),(4,4,True),(3,5,False),(4,5,False),(4,5,True)]:
    b = Board(nf, H, wrap, True)
    sqs = [(f, r) for f in range(nf) for r in range(2, H)]
    n = q = dis = multi = promo_roots = 0
    for nw in (1, 2):
        for nb in (1, 2):
            for ws in itertools.combinations(sqs, nw):
                rest = [s for s in sqs if s not in ws]
                for bs in itertools.combinations(rest, nb):
                    x = Pos(frozenset(ws), frozenset(bs))
                    if C.terminal(b, x) is not None: continue
                    n += 1
                    if not C.hereditarily_safe(b, x) or not E_ok(b, x): continue
                    q += 1
                    try:
                        oS = cgt.outcome(pawns.value(b, x)); oW = C.alt_outcome(b, x)
                    except pawns.RaceError: continue
                    if len(pawns.components(b, x)) > 1: multi += 1
                    # does any reachable position put a pawn on its last rank?
                    if any(any(r == H for _, r in y.white) or any(r == 1 for _, r in y.black) for y in C.reachable(b, x)):
                        promo_roots += 1
                    if oS != oW:
                        dis += 1; print("  DISAGREE", b, x, oS, oW)
    print(f"{'cyl' if wrap else 'flat'} {nf}x{H}: passer-free roots {n}, HSS+(E) {q} (multi-comp {multi}), "
          f"with a last-rank pawn reachable {promo_roots}, disagreements o(S) vs o(W) {dis}")
print("secs", round(time.time()-t0,1))
