"""myeng.py -- verify_compute: my own whole-board engine for the pawn game on the n-file cylinder (8 ranks).

Written from the rules of cylcgt/pawns.py (Elkies conventions, race rule "count", e.p. on, an e.p.-capturable pawn is
not passed).  NOT derived from rg.c and NOT a copy of the T50 verifier (ring_family_proof/verify/eng.py); it shares
with eng.py only the *position encoding* (a tuple of (white_mask, black_mask) per file, bit r-1 = rank r) so that node
sets can be compared directly.  Colours are the integers W = 0, B = 1 (eng.py uses the letters 'W', 'B').

  pos  : tuple of n pairs (w, b)
  ep   : None, or (file, stepper_colour): the pawn of colour `stepper` that has just double-stepped stands on that file
         (rank 4 for W, 5 for B) and an enemy pawn stands beside it, so the opponent may capture it e.p. on the very
         next move.  (pawns.py records the flag after every double step; a flag with no enemy beside the landing
         square has no effect on play, so it is dropped here -- diff_rules.py checks this equivalence.)

Two ways of treating the e.p. flag across a move in the nim heap (G + *h):
  'keep'   : the flag is a property of the pawn component and survives a heap move (this is the cylcgt sum semantics);
  'expire' : the flag is cleared by a heap move (textbook chess: the right lasts one ply).
"""
import sys
from collections import deque

sys.setrecursionlimit(1_000_000)

RANKS = 8
W, B = 0, 1
RACE_RULE = 'count'     # default of the task; 'mover' / 'opponent' only in run_race_rules.py
INF = 10 ** 6


def other(c):
    return 1 - c


def bits(m):
    """1-based ranks of the set bits of m."""
    r = 1
    while m:
        if m & 1:
            yield r
        m >>= 1
        r += 1


def lets(c):
    return 'W' if c == W else 'B'


def ep_letters(ep):
    return None if ep is None else (ep[0], lets(ep[1]))


# ---------------------------------------------------------------------------------------------------- passed pawns
def ep_protected(pos, ep, c, f, r):
    """True iff the pawn of colour c on (f, r) has just double-stepped and an enemy pawn stands beside it."""
    if ep is None:
        return False
    ef, stepper = ep
    if stepper != c or ef != f:
        return False
    if r != (4 if c == W else 5):
        return False
    n = len(pos)
    return bool((pos[(f - 1) % n][1 - c] | pos[(f + 1) % n][1 - c]) >> (r - 1) & 1)


def passed_pawns(pos, ep, c):
    """[(file, rank)] of the passed pawns of colour c: no enemy pawn strictly ahead on the same or an adjacent file,
    and not protected by the e.p. rule."""
    n = len(pos)
    e = 1 - c
    res = []
    for f in range(n):
        mine = pos[f][c]
        if not mine:
            continue
        foe = pos[f - 1][e] | pos[f][e] | pos[(f + 1) % n][e]
        for r in bits(mine):
            ahead = (foe >> r) if c == W else (foe & ((1 << (r - 1)) - 1))
            if ahead:
                continue
            if ep_protected(pos, ep, c, f, r):
                continue
            res.append((f, r))
    return res


def promo_dist(pos, ep, c):
    """race rule "count": best promotion distance over the passed pawns that are the front pawn of their file."""
    best = INF
    for f, r in passed_pawns(pos, ep, c):
        occ = pos[f][0] | pos[f][1]
        if c == W:
            if occ >> r:
                continue
            d = RANKS - r - (1 if r == 2 else 0)
        else:
            if occ & ((1 << (r - 1)) - 1):
                continue
            d = r - 1 - (1 if r == RANKS - 1 else 0)
        if d < best:
            best = d
    return best


def verdict(pos, ep, mover):
    """After `mover` has moved to (pos, ep): the colour that wins at once, or None if the game goes on."""
    wp = passed_pawns(pos, ep, W)
    bp = passed_pawns(pos, ep, B)
    if wp and bp:
        opp = 1 - mover
        if RACE_RULE == 'mover':          # variants of pawns.RACE_RULE, used only by run_race_rules.py
            return mover
        if RACE_RULE == 'opponent':
            return opp
        return opp if promo_dist(pos, ep, opp) <= promo_dist(pos, ep, mover) else mover
    if wp:
        return W
    if bp:
        return B
    return None


# ---------------------------------------------------------------------------------------------------------- moves
def _with(pos, f, c, newmask):
    lst = list(pos)
    pr = list(lst[f])
    pr[c] = newmask
    lst[f] = tuple(pr)
    return lst


def gen_moves(pos, ep, c, only=None):
    """all (newpos, newep) reachable by one pawn move of colour c (duplicates removed); only=(file, rank) restricts to
    the moves of that one pawn."""
    n = len(pos)
    e = 1 - c
    step = 1 if c == W else -1
    home = 2 if c == W else 7
    out = {}
    for f in range(n):
        mine = pos[f][c]
        if not mine or (only is not None and f != only[0]):
            continue
        occ = pos[f][0] | pos[f][1]
        for r in bits(mine):
            if only is not None and r != only[1]:
                continue
            r1 = r + step
            if r1 < 1 or r1 > RANKS:
                continue
            frm = 1 << (r - 1)
            to1 = 1 << (r1 - 1)
            if not (occ & to1):
                lst = _with(pos, f, c, (mine & ~frm) | to1)
                out[(tuple(lst), None)] = 1
                r2 = r + 2 * step
                if r == home and 1 <= r2 <= RANKS and not (occ & (1 << (r2 - 1))):
                    to2 = 1 << (r2 - 1)
                    lst = _with(pos, f, c, (mine & ~frm) | to2)
                    beside = (pos[(f - 1) % n][e] | pos[(f + 1) % n][e]) & to2
                    out[(tuple(lst), (f, c) if beside else None)] = 1
            for g in ((f - 1) % n, (f + 1) % n):
                if pos[g][e] & to1:                       # ordinary capture
                    lst = _with(pos, f, c, mine & ~frm)
                    pr = list(lst[g])
                    pr[c] |= to1
                    pr[e] &= ~to1
                    lst[g] = tuple(pr)
                    out[(tuple(lst), None)] = 1
                elif ep is not None and ep[1] == e and ep[0] == g and r1 == (3 if e == W else 6):
                    # e.p.: the enemy pawn that just double-stepped is on (g, r) beside our pawn
                    lst = _with(pos, f, c, mine & ~frm)
                    pr = list(lst[g])
                    pr[c] |= to1
                    pr[e] &= ~frm                          # frm has the same rank bit as the captured pawn (rank r)
                    lst[g] = tuple(pr)
                    out[(tuple(lst), None)] = 1
    return list(out)


def classify(pos, ep, c):
    """list of (kind, newpos, newep) for the moves of colour c; kind: 'T' (c wins at once), 'L' (c loses at once),
    'P' (non-terminal, but the opponent has a reply that wins at once), 'K' (everything else)."""
    e = 1 - c
    res = []
    for np_, ne in gen_moves(pos, ep, c):
        v = verdict(np_, ne, c)
        if v == c:
            k = 'T'
        elif v == e:
            k = 'L'
        else:
            k = 'K'
            for np2, ne2 in gen_moves(np_, ne, e):
                if verdict(np2, ne2, e) == e:
                    k = 'P'
                    break
        res.append((k, np_, ne))
    return res


# ------------------------------------------------------------------------- the full game G + *h (no poison pruning)
class Full:
    """exact outcome search of G + *h.  A heap move needs no pruning rule; pawn moves to terminal positions are decided
    on the spot, all others are searched (memoised)."""

    def __init__(self, ep_mode='keep'):
        assert ep_mode in ('keep', 'expire')
        self.mode = ep_mode
        self.memo = {}
        self.nodes = 0

    def wins(self, pos, ep, h, mover):
        key = (pos, ep, h, mover)
        v = self.memo.get(key)
        if v is not None:
            return v
        self.nodes += 1
        e = 1 - mover
        res = False
        later = []
        for np_, ne in gen_moves(pos, ep, mover):
            v2 = verdict(np_, ne, mover)
            if v2 == mover:
                res = True
                break
            if v2 is None:
                later.append((np_, ne))
        if not res:
            for np_, ne in later:
                if not self.wins(np_, ne, h, e):
                    res = True
                    break
        if not res and h:
            keep = ep if self.mode == 'keep' else None
            for h2 in range(h):
                if not self.wins(pos, keep, h2, e):
                    res = True
                    break
        self.memo[key] = res
        return res

    def signature(self, pos, hs):
        sig = ''
        for h in hs:
            a = self.wins(pos, None, h, W)
            b = self.wins(pos, None, h, B)
            sig += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
        return sig


# --------------------------------------------------------------------------------------- the reduced game graph
class Graph:
    """nodes reachable from the start by K-moves of either colour.  info[node][c] = (frozenset T-children,
    frozenset K-children, number of L-moves, number of P-moves)."""

    def __init__(self, pos0):
        self.start = (pos0, None)
        self.info = {}
        self.order = [self.start]
        seen = {self.start}
        q = deque([self.start])
        while q:
            nd = q.popleft()
            pos, ep = nd
            rec = {}
            for c in (W, B):
                cl = classify(pos, ep, c)
                T = frozenset((p, e) for k, p, e in cl if k == 'T')
                K = frozenset((p, e) for k, p, e in cl if k == 'K')
                nL = sum(1 for k, _, _ in cl if k == 'L')
                nP = sum(1 for k, _, _ in cl if k == 'P')
                rec[c] = (T, K, nL, nP)
                for ch in sorted(K, key=repr):
                    if ch not in seen:
                        seen.add(ch)
                        self.order.append(ch)
                        q.append(ch)
            self.info[nd] = rec

    def stats(self):
        n = len(self.start[0])
        nK = sum(len(self.info[nd][c][1]) for nd in self.order for c in (W, B))
        nT = sum(len(self.info[nd][c][0]) for nd in self.order for c in (W, B))
        flagged = sum(1 for nd in self.order if nd[1] is not None)
        p0 = self.start[0]
        zone = sorted({f for (p, _) in self.order for f in range(n) if p[f] != p0[f]})
        return dict(nodes=len(self.order), K=nK, T=nT, flagged=flagged, zone=zone)

    def signature(self, hs):
        memo = {}

        def win(nd, h, c):
            key = (nd, h, c)
            v = memo.get(key)
            if v is not None:
                return v
            T, K, _, _ = self.info[nd][c]
            res = bool(T)
            if not res:
                for ch in K:
                    if not win(ch, h, 1 - c):
                        res = True
                        break
            if not res:
                for h2 in range(h):
                    if not win(nd, h2, 1 - c):
                        res = True
                        break
            memo[key] = res
            return res

        sig = ''
        for h in hs:
            a = win(self.start, h, W)
            b = win(self.start, h, B)
            sig += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
        return sig


# ------------------------------------------------------------------------------------------------ the family P_n
def parse_file(tok):
    w = b = 0
    i = 0
    while i < len(tok):
        col = tok[i]
        i += 1
        j = i
        while j < len(tok) and tok[j].isdigit():
            j += 1
        for d in tok[i:j]:
            if col == 'W':
                w |= 1 << (int(d) - 1)
            else:
                b |= 1 << (int(d) - 1)
        i = j
    return (w, b)


def P_tokens(n):
    """P_n = W5 B7 W4 W4B7 B6 W3B6 (W2 B4)^((n-6)/2), n even >= 8 (file 0 first)."""
    assert n % 2 == 0 and n >= 8
    return ['W5', 'B7', 'W4', 'W4B7', 'B6', 'W3B6'] + ['W2', 'B4'] * ((n - 6) // 2)


def P_start(n):
    return tuple(parse_file(t) for t in P_tokens(n))


def npawns(pos):
    return sum(bin(w).count('1') + bin(b).count('1') for w, b in pos)


def ins(pos, c):
    """the Lemma-3 insertion: after file c put copies of files c+1 and c (in that order)."""
    return pos[:c + 1] + (pos[c + 1], pos[c]) + pos[c + 1:]
