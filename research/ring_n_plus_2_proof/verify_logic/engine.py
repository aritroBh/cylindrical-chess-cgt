"""Fresh whole-board pawn engine for the logic audit (written from the rules in the task text, not copied from rg.c / eng.py).

Representation: a position is a tuple with one entry per file; an entry is (W, B) where W / B are tuples of sorted ranks.
Flag: None or (file, colour) = the pawn of that colour on that file has just made a double step and carries an e.p. flag.
Rules (default setting): white moves up, black moves down; single step onto an empty square; double step from rank 2 (white)
or rank 7 (black) over two empty squares; capture diagonally forward (files wrap); e.p. capture only right after the double
step (the flag is created only if an enemy pawn stands beside the landing square; it survives heap moves, and is cleared by
every pawn move that is not itself a flag-creating double step).  A pawn is passed if no enemy pawn with a larger (white) /
smaller (black) rank stands on its own or an adjacent file; a pawn that can still be taken e.p. is not passed.  The game ends
at the first passed pawn.  Race 'count': if both sides have a passed pawn after a move, the side with the smaller distance
(white 8-r-[r=2], black r-1-[r=7]; minimum over passed pawns that are the front pawn of their file and not e.p.-capturable)
wins; a tie goes to the side that did NOT just move.
"""
import sys
from collections import deque

def parse_file(tok):
    if tok == '-':
        return ((), ())
    w = []; b = []; cur = None
    for ch in tok:
        if ch in 'WB':
            cur = ch
        else:
            (w if cur == 'W' else b).append(int(ch))
    return (tuple(sorted(w)), tuple(sorted(b)))

def parse(toks):
    return tuple(parse_file(t) for t in toks)

def fmt_file(fl):
    w, b = fl
    if not w and not b:
        return '-'
    return ('W' + ''.join(map(str, w)) if w else '') + ('B' + ''.join(map(str, b)) if b else '')

def fmt(pos, ep=None):
    s = ' '.join(fmt_file(f) for f in pos)
    return s + ('' if ep is None else ' ep%s=%d' % (ep[1], ep[0]))

def other(s):
    return 'B' if s == 'W' else 'W'

def idx(s):
    return 0 if s == 'W' else 1

# ---------------------------------------------------------------- passed pawns
def passed_list(pos, ep, side):
    n = len(pos)
    res = []
    for f in range(n):
        mine = pos[f][idx(side)]
        if not mine:
            continue
        for r in mine:
            if side == 'W':
                blocked = any(rr > r for g in (f - 1, f, f + 1) for rr in pos[g % n][1])
            else:
                blocked = any(rr < r for g in (f - 1, f, f + 1) for rr in pos[g % n][0])
            if not blocked:
                res.append((f, r))
    if ep is not None and ep[1] == side:
        ef = ep[0]
        rs = 4 if side == 'W' else 5
        res = [x for x in res if x != (ef, rs)]
    return res

def front_dist(pos, ep, side):
    best = 10 ** 6
    for f, r in passed_list(pos, ep, side):
        w, b = pos[f]
        if side == 'W':
            if any(x > r for x in w + b):
                continue
            d = 8 - r - (1 if r == 2 else 0)
        else:
            if any(x < r for x in w + b):
                continue
            d = r - 1 - (1 if r == 7 else 0)
        best = min(best, d)
    return best

def status(pos, ep, mover):
    """result of the position reached after `mover` moved: mover / other(mover) / None (non-terminal)."""
    wp = passed_list(pos, ep, 'W'); bp = passed_list(pos, ep, 'B')
    if wp and bp:
        opp = other(mover)
        return opp if front_dist(pos, ep, opp) <= front_dist(pos, ep, mover) else mover
    if wp:
        return 'W'
    if bp:
        return 'B'
    return None

# ---------------------------------------------------------------- moves
def _put(pos, f, side, ranks):
    l = list(pos)
    w, b = l[f]
    l[f] = (ranks, b) if side == 'W' else (w, ranks)
    return l

def moves(pos, ep, side):
    """list of (newpos, newep, srcfile, kind) ; kind in step/double/cap/epcap"""
    n = len(pos)
    d = 1 if side == 'W' else -1
    start = 2 if side == 'W' else 7
    i = idx(side); j = 1 - i
    out = []
    for f in range(n):
        mine = pos[f][i]
        for r in mine:
            r1 = r + d
            if not (1 <= r1 <= 8):
                continue
            own_new = lambda nr: tuple(sorted([x for x in mine if x != r] + [nr]))
            occ = pos[f][0] + pos[f][1]
            if r1 not in occ:
                l = _put(pos, f, side, own_new(r1))
                out.append((tuple(l), None, f, 'step'))
                r2 = r + 2 * d
                if r == start and r2 not in occ:
                    l = _put(pos, f, side, own_new(r2))
                    beside = any(r2 in pos[g % n][j] for g in (f - 1, f + 1))
                    out.append((tuple(l), (f, side) if beside else None, f, 'double'))
            for g in ((f - 1) % n, (f + 1) % n):
                if r1 in pos[g][j]:
                    l = _put(pos, f, side, tuple(x for x in mine if x != r))
                    gw, gb = l[g]
                    if side == 'W':
                        l[g] = (tuple(sorted(gw + (r1,))), tuple(x for x in gb if x != r1))
                    else:
                        l[g] = (tuple(x for x in gw if x != r1), tuple(sorted(gb + (r1,))))
                    out.append((tuple(l), None, f, 'cap'))
                elif ep is not None and ep[1] != side and ep[0] == g and r in pos[g][j] and r1 == (r + d):
                    # e.p.: the enemy stepper stands beside us on rank r (rank 5 for white captor, rank 4 for black captor)
                    if r == (5 if side == 'W' else 4):
                        l = _put(pos, f, side, tuple(x for x in mine if x != r))
                        gw, gb = l[g]
                        if side == 'W':
                            l[g] = (tuple(sorted(gw + (r1,))), tuple(x for x in gb if x != r))
                        else:
                            l[g] = (tuple(x for x in gw if x != r), tuple(sorted(gb + (r1,))))
                        out.append((tuple(l), None, f, 'epcap'))
    return out

# ---------------------------------------------------------------- classification
_cache = {}
def classify(pos, ep, side):
    """list of (cls, newpos, newep, srcfile, kind, reply) with cls in T/L/P/K; reply = a poisoning reply (for P) or None"""
    key = (pos, ep, side)
    v = _cache.get(key)
    if v is not None:
        return v
    y = other(side)
    out = []
    for npos, nep, src, kind in moves(pos, ep, side):
        st = status(npos, nep, side)
        if st == side:
            out.append(('T', npos, nep, src, kind, None))
        elif st == y:
            out.append(('L', npos, nep, src, kind, None))
        else:
            pr = None
            for p2, e2, s2, k2 in moves(npos, nep, y):
                if status(p2, e2, y) == y:
                    pr = (s2, k2, p2, e2)
                    break
            out.append(('P' if pr else 'K', npos, nep, src, kind, pr))
    _cache[key] = out
    return out

def build(start):
    """reduced game: BFS over K-moves.  returns (order, edges) ; edges[(node, side)] = (hasT, [K children])"""
    s0 = (start, None)
    order = [s0]; seen = {s0}
    edges = {}
    dq = deque([s0])
    while dq:
        nd = dq.popleft()
        for side in 'WB':
            cl = classify(nd[0], nd[1], side)
            ks = []
            seenk = set()
            for c, npos, nep, src, kind, pr in cl:
                if c == 'K' and (npos, nep) not in seenk:
                    seenk.add((npos, nep)); ks.append((npos, nep))
            hasT = any(c == 'T' for c, *_ in cl)
            edges[(nd, side)] = (hasT, ks)
            for k in ks:
                if k not in seen:
                    seen.add(k); order.append(k); dq.append(k)
    return order, edges

def solve_sig(order, edges, hs=(0, 1, 2, 3)):
    memo = {}
    sys.setrecursionlimit(1000000)
    def win(nd, h, mover):
        key = (nd, h, mover)
        if key in memo:
            return memo[key]
        hasT, ks = edges[(nd, mover)]
        res = hasT
        if not res:
            for k in ks:
                if not win(k, h, other(mover)):
                    res = True; break
        if not res:
            for h2 in range(h):
                if not win(nd, h2, other(mover)):
                    res = True; break
        memo[key] = res
        return res
    sig = ''
    for h in hs:
        a = win(order[0], h, 'W'); b = win(order[0], h, 'B')
        sig += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
    return sig

# ---------------------------------------------------------------- family P and insertion
def P_toks(n):
    assert n % 2 == 0 and n >= 8
    return ['W5', 'B7', 'W4', 'W4B7', 'B6', 'W3B6'] + ['W2', 'B4'] * ((n - 6) // 2)

def ins(pos, c):
    return pos[:c + 1] + (pos[c + 1], pos[c]) + pos[c + 1:]

def ins_nd(nd, c):
    pos, ep = nd
    if ep is None:
        return (ins(pos, c), None)
    f, s = ep
    return (ins(pos, c), (f if f <= c else f + 2, s))
