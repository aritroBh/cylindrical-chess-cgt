# differential test: my move generator / passed / race status against cylcgt.pawns on random cylinder positions
import sys, random
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
from cylcgt import pawns
from eng import *

def to_cyl(pos, ep):
    n = len(pos)
    W = frozenset((f, r) for f in range(n) for r in range(1, 9) if pos[f][0] >> (r - 1) & 1)
    B = frozenset((f, r) for f in range(n) for r in range(1, 9) if pos[f][1] >> (r - 1) & 1)
    e = None
    if ep is not None:
        f, s = ep
        if s == 'W': e = ((f, 3), (f, 4), 'B')
        else: e = ((f, 6), (f, 5), 'W')
    return pawns.Pos(W, B, e)

def from_cyl(cp, n):
    w = [0] * n; b = [0] * n
    for f, r in cp.white: w[f] |= 1 << (r - 1)
    for f, r in cp.black: b[f] |= 1 << (r - 1)
    pos = tuple(zip(w, b))
    ep = None
    if cp.ep is not None:
        (f, r1), (f2, r2), capt = cp.ep
        s = 'B' if capt == 'W' else 'W'  # stepper
        # normalise: keep only if an enemy pawn is beside
        en = 1 if s == 'W' else 0
        n_ = n
        if pos[(f - 1) % n_][en] >> (r2 - 1) & 1 or pos[(f + 1) % n_][en] >> (r2 - 1) & 1:
            ep = (f, s)
    return pos, ep

def rand_pos(rng, n):
    w = [0] * n; b = [0] * n
    npw = rng.randint(2, 2 * n); 
    for _ in range(npw):
        f = rng.randrange(n); r = rng.randint(2, 7)
        if rng.random() < 0.5: w[f] |= 1 << (r - 1)
        else: b[f] |= 1 << (r - 1)
    for f in range(n):  # no overlap
        both = w[f] & b[f]; w[f] &= ~both
    pos = tuple(zip(w, b))
    ep = None
    if rng.random() < 0.3:
        f = rng.randrange(n); s = rng.choice('WB')
        r2 = 4 if s == 'W' else 5; r1 = 3 if s == 'W' else 6; r0 = 2 if s == 'W' else 7
        lst = list(pos); a = list(lst[f])
        # clear file squares r0,r1,r2 then put stepper pawn on r2
        occ_mask = (1 << (r0 - 1)) | (1 << (r1 - 1)) | (1 << (r2 - 1))
        a[0] &= ~occ_mask; a[1] &= ~occ_mask
        a[0 if s == 'W' else 1] |= 1 << (r2 - 1)
        lst[f] = tuple(a); pos = tuple(lst)
        # put an enemy beside sometimes
        if rng.random() < 0.7:
            g = (f + rng.choice((-1, 1))) % n
            lst = list(pos); a = list(lst[g])
            en = 1 if s == 'W' else 0
            a[0] &= ~(1 << (r2 - 1)); a[1] &= ~(1 << (r2 - 1))
            a[en] |= 1 << (r2 - 1); lst[g] = tuple(a); pos = tuple(lst)
        ep = (f, s)
        # normalise
        en = 1 if s == 'W' else 0
        if not (pos[(f - 1) % n][en] >> (r2 - 1) & 1 or pos[(f + 1) % n][en] >> (r2 - 1) & 1): ep = None
    return pos, ep

def cyl_status(board, cp, mover):
    wp, bp = pawns.passed(board, cp, 'W'), pawns.passed(board, cp, 'B')
    if wp and bp:
        oth = 'B' if mover == 'W' else 'W'
        return oth if pawns.promote_distance(board, cp, oth) <= pawns.promote_distance(board, cp, mover) else mover
    if wp: return 'W'
    if bp: return 'B'
    return None

rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
N = int(sys.argv[1])
bad = 0; nm = 0; nrace = 0; nst = 0
for it in range(N):
    n = rng.randint(5, 11)
    board = pawns.Board(n, 8, True, True)
    pos, ep = rand_pos(rng, n)
    cp = to_cyl(pos, ep)
    for side in 'WB':
        # passed
        if bool(passed_ranks(pos, ep, side)) != bool(pawns.passed(board, cp, side)):
            bad += 1; print('PASSED MISMATCH', cp, side)
        # moves, as a set of (pos, ep), cylcgt uses plain for non-capturing side: moves() already handles
        mine = set(moves(pos, ep, side))
        theirs = set(from_cyl(c, n) for c in pawns.moves(board, cp, side))
        nm += len(mine)
        if mine != theirs:
            bad += 1; print('MOVES MISMATCH', cp, side, len(mine), len(theirs))
        # statuses of the children
        for c in pawns.moves(board, cp, side):
            p2, e2 = from_cyl(c, n)
            a = status(p2, e2, side); b = cyl_status(board, c, side)
            nst += 1
            if pawns.passed(board, c, 'W') and pawns.passed(board, c, 'B'): nrace += 1
            if a != b:
                bad += 1; print('STATUS MISMATCH', c, side, a, b)
print('positions', N, 'moves', nm, 'statuses', nst, 'races', nrace, 'mismatches', bad)
