"""Differential test of engine D against the project's reference rules cylcgt/pawns.py on positions of the odd families R_19, Qo_19:
all reduced nodes, all children of every move of every node (both colours), and a sample of grandchildren.
Compared: the set of positions reachable by one move of each side (with the e.p. flag counted only if an enemy pawn stands beside the
landing square, which is the only case where it matters), the passed-pawn predicate of each colour (e.p.-aware), and the terminal verdict
of a child (race rule 'count': pawns._child logic).  Run from the project root with PYTHONPATH=."""
import sys, random, time
sys.path.insert(0, 'research/ring_n_plus_2_proof/verify_logicOdd')
from common import *
from cylcgt import pawns as P

def to_cyl(pos, ep):
    n = len(pos)
    w = frozenset((f, r) for f in range(n) for r in pos[f][0])
    b = frozenset((f, r) for f in range(n) for r in pos[f][1])
    e = None
    if ep is not None:
        f, side = ep
        e = ((f, 3), (f, 4), 'B') if side == 'W' else ((f, 6), (f, 5), 'W')
    return P.Pos(w, b, e)

def eff_ep(board, p):
    """cylcgt Pos -> D-style ep (file, side) or None, only if an enemy pawn stands beside the landing square"""
    if p.ep is None: return None
    (tf, tr), (cf, cr), capt = p.ep
    side = 'W' if capt == 'B' else 'B'
    theirs = p.black if side == 'W' else p.white
    if any((g, cr) in theirs for g in ((cf - 1) % board.files, (cf + 1) % board.files)):
        return (cf, side)
    return None

def from_cyl(board, p):
    n = board.files
    return (tuple((tuple(sorted(r for (f, r) in p.white if f == j)), tuple(sorted(r for (f, r) in p.black if f == j))) for j in range(n)), eff_ep(board, p))

def cyl_status(board, p, mover):
    wp, bp = P.passed(board, p, 'W'), P.passed(board, p, 'B')
    if wp and bp:
        other_ = 'B' if mover == 'W' else 'W'
        win = other_ if P.promote_distance(board, p, other_) <= P.promote_distance(board, p, mover) else mover
        return win
    if wp: return 'W'
    if bp: return 'B'
    return None

def check(pos, ep, board, stats):
    cp = to_cyl(pos, ep)
    stats['pos'] += 1
    # passed predicate
    for s in 'WB':
        a = bool(passed_list(pos, ep, s)); b = P.passed(board, cp, s)
        if a != b: stats['bad_passed'] += 1; stats['ex'] = stats.get('ex') or ('passed', fmt(pos, ep), s)
    out = {}
    for side in 'WB':
        # cylcgt: when ep right belongs to the other side, the mover's moves are generated from the plain position
        use = cp if (cp.ep is None or cp.ep[2] == side) else P.Pos(cp.white, cp.black, None)
        A = {(c[0], c[1]) for c in (from_cyl(board, q) for q in P.moves(board, use, side))}
        Bm = {(c[0], c[1]) for c in ((npos, nep) for npos, nep, _, _ in moves(pos, ep, side))}
        if A != Bm:
            stats['bad_moves'] += 1; stats['ex'] = stats.get('ex') or ('moves', fmt(pos, ep), side, len(A), len(Bm))
        for npos, nep, _, _ in moves(pos, ep, side):
            d = status(npos, nep, side)
            e = cyl_status(board, to_cyl(npos, nep), side)
            stats['child'] += 1
            if d != e: stats['bad_status'] += 1; stats['ex'] = stats.get('ex') or ('status', fmt(npos, nep), side, d, e)
        out[side] = [(npos, nep) for npos, nep, _, _ in moves(pos, ep, side)]
    return out

def main(fam, n, nsample, seed):
    random.seed(seed)
    board = P.Board(n, 8, True, True)
    start = parse(TOKS[fam](n))
    order, edges = build(start)
    stats = {'pos': 0, 'child': 0, 'bad_passed': 0, 'bad_moves': 0, 'bad_status': 0}
    from collections import Counter
    stats = Counter(stats)
    t0 = time.time()
    kids = []
    for nd in order:
        o = check(nd[0], nd[1], board, stats)
        for s in 'WB': kids += o[s]
    print(fam, n, 'nodes', len(order), 'children collected', len(kids), dict(stats), '%.0fs' % (time.time() - t0), flush=True)
    random.shuffle(kids)
    gk = 0
    for (p, e) in kids[:nsample]:
        o = check(p, e, board, stats)
        for s in 'WB':
            for q in o[s]:
                if random.random() < 0.05:
                    gk += 1
                    check(q[0], q[1], board, stats)
    print(fam, n, 'after children + grandchildren sample:', dict(stats), 'grandchildren', gk, '%.0fs' % (time.time() - t0), flush=True)

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
