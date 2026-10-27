"""oddeng.py -- verify_computeOdd: a fresh whole-board engine for the pawn game on the n-file cylinder (8 ranks).

Written from the RULES (PROOF.md section 1, cylcgt/pawns.py docstrings and the task text), NOT from rg.c, myeng.py
(program E) or check3/eng.py (program C).  Differences of design on purpose:
  * a position is a tuple of n small ints, one per file:  s = w | (b << 8)   (bit r-1 of w = white pawn on rank r,
    bit 8+r-1 = black pawn on rank r); E and C use a tuple of (w, b) pairs.  `to_pairs` converts for comparisons.
  * colour is handled by a shift (8*c) so that one code path serves both sides;
  * passed pawns by the "extreme enemy rank among the three files" threshold; moves by XOR on the file int.
  * the en-passant flag is either CANONICAL (recorded after a double step only if an enemy pawn stands beside the landing
    square -- otherwise it can never matter) or RAW (recorded after every double step, as cylcgt/pawns.py does); node
    identity differs between the two, the game does not.

Rules (race rule "count", e.p. on):
  * move: one step on an empty square; a double step from the home rank (W rank 2, B rank 7) over two empty squares;
    capture diagonally forward onto an enemy pawn (cylinder: files mod n); e.p. capture of an enemy pawn that has just
    double-stepped and stands beside the capturer, usable only as the very next move;
  * passed pawn: no enemy pawn strictly ahead on the same or an adjacent file; a pawn that has just double-stepped and can
    be taken e.p. is NOT passed;
  * the game ends at the first move after which some side has a passed pawn; if only one side has one it wins; if both do,
    the "count" race: promotion distance d = 8-r-[r=2] (white), r-1-[r=7] (black), minimum over the side's passed pawns that
    are the front pawn of their file (no pawn of either colour ahead on the file); the opponent of the mover wins ties;
  * G + *h: normal play, a side with no move loses; heap moves *h -> *h' (h' < h).  Flag across a heap move: 'keep'
    (cylcgt sum semantics, the flag stays usable until a pawn move) or 'expire' (cleared by a heap move).
Colours: WH = 0, BL = 1 (same integers as myeng.py).  flag = None or (file, colour of the stepper).
"""
import sys
from collections import deque

sys.setrecursionlimit(1_000_000)

WH, BL = 0, 1
INF = 10 ** 6


# ------------------------------------------------------------------------------------------------ construction
def tok_to_file(tok):
    s = 0
    col = None
    for ch in tok:
        if ch == 'W':
            col = WH
        elif ch == 'B':
            col = BL
        else:
            s |= 1 << (8 * col + int(ch) - 1)
    return s


def parse(tokens):
    return tuple(tok_to_file(t) for t in tokens)


def to_pairs(pos):
    """the (w, b) pair-per-file encoding used by myeng.py / check3/eng.py."""
    return tuple((s & 255, s >> 8) for s in pos)


def from_pairs(pairs):
    return tuple(w | (b << 8) for w, b in pairs)


def npawns(pos):
    return sum(bin(s).count('1') for s in pos)


def ins(pos, c):
    """Lemma-3 insertion: after file c put (copy of file c+1, copy of file c)."""
    return pos[:c + 1] + (pos[c + 1], pos[c]) + pos[c + 1:]


# --------------------------------------------------------------------------------------------------- families
def tokens_R(n):
    assert n % 2 == 1 and n >= 9
    return ['W5', 'B7'] + ['W2', 'B4'] * ((n - 9) // 2) + ['W2', 'W3B6', 'W3', 'W2B5', 'B5', 'W2', 'B4']


def tokens_Qo(n):
    assert n % 2 == 1 and n >= 9
    return ['W4', 'B7'] + ['W2', 'B4'] * ((n - 9) // 2) + ['W2', 'W3B6', 'W3', 'W2B5', 'B5', 'W2', 'B4']


def start(fam, n):
    return parse({'R': tokens_R, 'Qo': tokens_Qo}[fam](n))


# ------------------------------------------------------------------------------------------------ passed pawns
def _protected(pos, flag, c, f, r):
    """the pawn of colour c on (f, r) has just double-stepped and an enemy pawn stands beside it: e.p.-capturable."""
    if flag is None or flag[1] != c or flag[0] != f or r != (4 if c == WH else 5):
        return False
    n = len(pos)
    se = 8 * (1 - c)
    return bool(((pos[f - 1] | pos[(f + 1) % n]) >> (se + r - 1)) & 1)


def passed(pos, flag, c):
    """list of (file, rank) of the passed pawns of colour c."""
    n = len(pos)
    sc = 8 * c
    se = 8 - sc
    res = []
    for f in range(n):
        mine = (pos[f] >> sc) & 255
        if not mine:
            continue
        foe = ((pos[f - 1] | pos[f] | pos[(f + 1) % n]) >> se) & 255
        if c == WH:
            t = foe.bit_length()                    # highest enemy rank on the three files (0: none)
            cand = ((mine >> (t - 1)) << (t - 1)) if t else mine       # ranks r >= t
        else:
            t = (foe & -foe).bit_length() if foe else 9                # lowest enemy rank (9: none)
            cand = mine & ((1 << t) - 1)                               # ranks r <= t
        while cand:
            low = cand & -cand
            cand ^= low
            r = low.bit_length()
            if flag is not None and _protected(pos, flag, c, f, r):
                continue
            res.append((f, r))
    return res


def promo_dist(pos, flag, c):
    best = INF
    for f, r in passed(pos, flag, c):
        occ = (pos[f] | (pos[f] >> 8)) & 255
        if c == WH:
            if occ >> r:
                continue
            d = 8 - r - (1 if r == 2 else 0)
        else:
            if occ & ((1 << (r - 1)) - 1):
                continue
            d = r - 1 - (1 if r == 7 else 0)
        if d < best:
            best = d
    return best


def verdict(pos, flag, mover):
    """after `mover` has moved to (pos, flag): the colour that wins on the spot, or None."""
    wp = passed(pos, flag, WH)
    bp = passed(pos, flag, BL)
    if wp and bp:
        opp = 1 - mover
        return opp if promo_dist(pos, flag, opp) <= promo_dist(pos, flag, mover) else mover
    if wp:
        return WH
    if bp:
        return BL
    return None


# ------------------------------------------------------------------------------------------------------ moves
def gen(pos, flag, c, raw=False, only=None):
    """list of (pos', flag') reachable by one move of colour c (distinct); only=(file, rank): that pawn's moves only."""
    n = len(pos)
    e = 1 - c
    sc = 8 * c
    se = 8 * e
    up = 1 if c == WH else -1
    home = 2 if c == WH else 7
    out = {}
    for f in range(n):
        if only is not None and f != only[0]:
            continue
        s = pos[f]
        mine = (s >> sc) & 255
        if not mine:
            continue
        occ = (s | (s >> 8)) & 255
        for r in range(1, 9):
            if not (mine >> (r - 1)) & 1:
                continue
            if only is not None and r != only[1]:
                continue
            r1 = r + up
            if r1 < 1 or r1 > 8:
                continue
            frm = 1 << (sc + r - 1)
            if not (occ >> (r1 - 1)) & 1:
                t = list(pos)
                t[f] = s ^ frm ^ (1 << (sc + r1 - 1))
                out[(tuple(t), None)] = 1
                if r == home:
                    r2 = r + 2 * up
                    if not (occ >> (r2 - 1)) & 1:
                        t = list(pos)
                        t[f] = s ^ frm ^ (1 << (sc + r2 - 1))
                        beside = (((pos[f - 1] | pos[(f + 1) % n]) >> se) >> (r2 - 1)) & 1
                        out[(tuple(t), (f, c) if (beside or raw) else None)] = 1
            for g in ((f - 1) % n, (f + 1) % n):
                gs = pos[g]
                if (gs >> (se + r1 - 1)) & 1:
                    t = list(pos)
                    t[f] = s ^ frm
                    t[g] = gs ^ (1 << (se + r1 - 1)) ^ (1 << (sc + r1 - 1))
                    out[(tuple(t), None)] = 1
                elif (flag is not None and flag[1] == e and flag[0] == g and r == (4 if e == WH else 5)
                      and (gs >> (se + r - 1)) & 1):
                    t = list(pos)
                    t[f] = s ^ frm
                    t[g] = gs ^ (1 << (se + r - 1)) ^ (1 << (sc + r1 - 1))
                    out[(tuple(t), None)] = 1
    return list(out)


def kind_of(child, c, raw=False):
    """T / L / P / K of the move of colour c that leads to child = (pos, flag)."""
    cp, cf = child
    v = verdict(cp, cf, c)
    if v == c:
        return 'T'
    if v is not None:
        return 'L'
    e = 1 - c
    for p2, f2 in gen(cp, cf, e, raw):
        if verdict(p2, f2, e) == e:
            return 'P'
    return 'K'


def classify(pos, flag, c, raw=False):
    return [(kind_of(ch, c, raw), ch) for ch in gen(pos, flag, c, raw)]


# ----------------------------------------------------------------------------------- full game G + *h (no pruning)
class Full:
    """exact outcome of G + *h by memoised search over the whole game tree.  A pawn move into a decided position is
    decided on the spot; everything else is searched.  exhaustive=True evaluates EVERY child and every heap move of every
    reached state (no short-circuit), the plain definition of the outcome."""

    def __init__(self, mode='keep', exhaustive=False, raw=False):
        assert mode in ('keep', 'expire')
        self.mode, self.exh, self.raw = mode, exhaustive, raw
        self.memo = {}

    def wins(self, pos, flag, h, mover):
        key = (pos, flag, h, mover)
        got = self.memo.get(key)
        if got is not None:
            return got
        e = 1 - mover
        res = False
        carried = flag if self.mode == 'keep' else None
        if self.exh:
            for ch in gen(pos, flag, mover, self.raw):
                v = verdict(ch[0], ch[1], mover)
                if v == mover:
                    r_ = True
                elif v is not None:
                    r_ = False
                else:
                    r_ = not self.wins(ch[0], ch[1], h, e)
                res = res or r_
            for h2 in range(h):
                r_ = not self.wins(pos, carried, h2, e)
                res = res or r_
        else:
            later = []
            for ch in gen(pos, flag, mover, self.raw):
                v = verdict(ch[0], ch[1], mover)
                if v == mover:
                    res = True
                    break
                if v is None:
                    later.append(ch)
            if not res:
                for ch in later:
                    if not self.wins(ch[0], ch[1], h, e):
                        res = True
                        break
            if not res:
                for h2 in range(h):
                    if not self.wins(pos, carried, h2, e):
                        res = True
                        break
        self.memo[key] = res
        return res

    def signature(self, pos, hs):
        sig = ''
        for h in hs:
            a = self.wins(pos, None, h, WH)
            b = self.wins(pos, None, h, BL)
            sig += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
        return sig


# ------------------------------------------------------------------------------------------- reduced game graph
class Graph:
    """nodes = positions reachable from the start by K-moves of either colour.
    info[node][c] = (frozenset of T-children, frozenset of K-children, #L moves, #P moves)."""

    def __init__(self, pos0, raw=False):
        self.raw = raw
        self.start = (pos0, None)
        self.info = {}
        self.order = [self.start]
        seen = {self.start}
        q = deque([self.start])
        while q:
            nd = q.popleft()
            pos, flag = nd
            rec = {}
            for c in (WH, BL):
                T, K = set(), set()
                nl = npz = 0
                for k, ch in classify(pos, flag, c, raw):
                    if k == 'T':
                        T.add(ch)
                    elif k == 'K':
                        K.add(ch)
                    elif k == 'L':
                        nl += 1
                    else:
                        npz += 1
                rec[c] = (frozenset(T), frozenset(K), nl, npz)
                for ch in sorted(K, key=repr):
                    if ch not in seen:
                        seen.add(ch)
                        self.order.append(ch)
                        q.append(ch)
            self.info[nd] = rec

    def stats(self):
        n = len(self.start[0])
        nK = sum(len(self.info[nd][c][1]) for nd in self.order for c in (WH, BL))
        nT = sum(len(self.info[nd][c][0]) for nd in self.order for c in (WH, BL))
        nTpairs = sum(1 for nd in self.order for c in (WH, BL) if self.info[nd][c][0])
        flagged = sum(1 for nd in self.order if nd[1] is not None)
        p0 = self.start[0]
        zone = sorted({f for (p, _) in self.order for f in range(n) if p[f] != p0[f]})
        return dict(nodes=len(self.order), K=nK, T=nT, Tpairs=nTpairs, flagged=flagged, zone=zone)

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
            a = win(self.start, h, WH)
            b = win(self.start, h, BL)
            sig += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
        return sig

    def canonical(self):
        """normalised form for comparing with other engines: node = (pairs, flag letters or None);
        per colour letter: (frozenset T children, frozenset K children)."""
        def cv(nd):
            return (to_pairs(nd[0]), None if nd[1] is None else (nd[1][0], 'WB'[nd[1][1]]))
        out = {}
        for nd, rec in self.info.items():
            out[cv(nd)] = {'WB'[c]: (frozenset(cv(x) for x in rec[c][0]), frozenset(cv(x) for x in rec[c][1]))
                           for c in (WH, BL)}
        return cv(self.start), out
