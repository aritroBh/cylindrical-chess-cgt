#!/usr/bin/env python3
"""kpm.py -- K30: my own move generator and exact solver for king-and-pawn positions in the promotion models.

Written from kings/SPEC.md only (no code of kpsolve.c, kp_p.c, mine.c, psolve.py was read for this file).

Models (a promotion ends the game at once; no officer ever stands on the board):
  P    the first promotion is a win for the promoter
  EPW  every promotion (by either side) is a White win
  EPB  every promotion (by either side) is a Black win
Checkmate is a win for the mating side, stalemate and infinite play are draws.

Colours: 0 = White (pawns move up), 1 = Black (pawns move down).
A position is a tuple (stm, wk, bk, wp, bp, ep): stm side to move, wk/bk king squares, wp/bp sorted tuples of pawn
squares, ep the e.p. target square or -1 (normalised: kept only if an enemy pawn could capture onto it).
Squares are r*W+f (f = 0 is file a, r = 0 is rank 1).
"""
import sys
from collections import deque

W_, L_, D_ = 'W', 'L', 'D'


class Board:
    def __init__(self, spec):
        kind, dims = spec.split(':')
        w, h = dims.split('x')
        if kind == 'flat7':  # never used
            raise ValueError
        self.cyl = (kind == 'cyl')
        self.W, self.H = int(w), int(h)
        self.N = self.W * self.H
        self.spec = spec
        self.kn = [self._king_nb(s) for s in range(self.N)]
        self.knset = [frozenset(x) for x in self.kn]
        # squares attacked by a pawn of colour c standing on s
        self.pa = [[self._pawn_att(s, c) for s in range(self.N)] for c in (0, 1)]

    def f(self, s): return s % self.W
    def r(self, s): return s // self.W

    def step(self, s, df, dr):
        f = s % self.W + df
        r = s // self.W + dr
        if r < 0 or r >= self.H:
            return -1
        if self.cyl:
            f %= self.W
        elif f < 0 or f >= self.W:
            return -1
        return r * self.W + f

    def _king_nb(self, s):
        out = []
        for dr in (-1, 0, 1):
            for df in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                t = self.step(s, df, dr)
                if t >= 0 and t not in out:
                    out.append(t)
        return out

    def _pawn_att(self, s, c):
        d = 1 if c == 0 else -1
        out = []
        for df in (-1, 1):
            t = self.step(s, df, d)
            if t >= 0 and t not in out:
                out.append(t)
        return tuple(out)

    def name(self, s):
        return 'abcdefgh'[s % self.W] + str(s // self.W + 1)

    def sq(self, name):
        return (int(name[1:]) - 1) * self.W + 'abcdefgh'.index(name[0])

    def last(self, c): return self.H - 1 if c == 0 else 0
    def start(self, c): return 1 if c == 0 else self.H - 2


def parse(B, text):
    """'Ke6 Pd7 kd8 pe7 w -' -> position tuple"""
    tok = text.split()
    wk = bk = -1
    wp, bp = [], []
    for t in tok[:-2]:
        s = B.sq(t[1:])
        if t[0] == 'K': wk = s
        elif t[0] == 'k': bk = s
        elif t[0] == 'P': wp.append(s)
        elif t[0] == 'p': bp.append(s)
        else: raise ValueError(t)
    stm = 0 if tok[-2] == 'w' else 1
    ep = -1 if tok[-1] == '-' else B.sq(tok[-1])
    return norm(B, (stm, wk, bk, tuple(sorted(wp)), tuple(sorted(bp)), ep))


def fmt(B, pos):
    stm, wk, bk, wp, bp, ep = pos
    parts = ['K' + B.name(wk)] + ['P' + B.name(s) for s in wp] + ['k' + B.name(bk)] + ['p' + B.name(s) for s in bp]
    return ' '.join(parts) + (' w ' if stm == 0 else ' b ') + (B.name(ep) if ep >= 0 else '-')


def norm(B, pos):
    stm, wk, bk, wp, bp, ep = pos
    if ep >= 0:
        # the pawn that double-stepped belongs to the side NOT to move; a capturer is a pawn of the side to move
        mine = wp if stm == 0 else bp
        c = stm
        ok = False
        for p in mine:
            if ep in B.pa[c][p]:
                ok = True
        if not ok:
            ep = -1
    return (stm, wk, bk, wp, bp, ep)


def attacked_by_pawns(B, sq, pawns, c):
    """is sq attacked by a pawn of colour c among 'pawns'?"""
    d = 1 if c == 0 else -1
    for df in (-1, 1):
        # pawn at (sq - (df,d)) attacks sq
        t = B.step(sq, -df, -d)
        if t >= 0 and t in pawns:
            return True
    return False


def in_check(B, pos, c):
    """is the king of colour c attacked in pos?"""
    stm, wk, bk, wp, bp, ep = pos
    if c == 0:
        return attacked_by_pawns(B, wk, bp, 1) or bk in B.knset[wk]
    return attacked_by_pawns(B, bk, wp, 0) or wk in B.knset[bk]


def legal(B, pos):
    """is pos a legal position (SPEC 7)?"""
    stm, wk, bk, wp, bp, ep = pos
    occ = [wk, bk] + list(wp) + list(bp)
    if len(set(occ)) != len(occ):
        return False
    if bk in B.knset[wk]:
        return False
    for s in wp:
        if B.r(s) in (0, B.H - 1): return False
    for s in bp:
        if B.r(s) in (0, B.H - 1): return False
    if in_check(B, pos, 1 - stm):
        return False
    return True


def gen(B, pos):
    """all legal moves of the side to move.  Returns a list of (label, kind, newpos):
       kind 'n' ordinary move (newpos is a position), 'p' promotion (newpos is None; the promoter is stm)."""
    stm, wk, bk, wp, bp, ep = pos
    c = stm
    out = []
    own_k = wk if c == 0 else bk
    en_k = bk if c == 0 else wk
    own_p = wp if c == 0 else bp
    en_p = bp if c == 0 else wp
    d = 1 if c == 0 else -1
    last = B.last(c)

    def make(nk, nown, nen, nep):
        if c == 0:
            return norm(B, (1, nk, bk, tuple(sorted(nown)), tuple(sorted(nen)), nep))
        return norm(B, (0, wk, nk, tuple(sorted(nen)), tuple(sorted(nown)), nep))

    def safe(nk, nen):
        # own king on nk must not be attacked by the enemy king or an enemy pawn (enemy pawns nen)
        if nk in B.knset[en_k]:
            return False
        if attacked_by_pawns(B, nk, nen, 1 - c):
            return False
        return True

    ownset = set(own_p)
    enset = set(en_p)
    # king moves
    for t in B.kn[own_k]:
        if t in ownset or t == en_k:
            continue
        nen = [x for x in en_p if x != t]
        if not safe(t, nen):
            continue
        out.append((B.name(own_k) + B.name(t) + ('x' if t in enset else ''), 'n', make(t, list(own_p), nen, -1)))
    # pawn moves
    occ = set([wk, bk]) | set(wp) | set(bp)
    for p in own_p:
        rest = [x for x in own_p if x != p]
        t = B.step(p, 0, d)
        if t >= 0 and t not in occ:
            if safe(own_k, en_p):
                if B.r(t) == last:
                    out.append((B.name(p) + B.name(t) + '=', 'p', None))
                else:
                    out.append((B.name(p) + B.name(t), 'n', make(own_k, rest + [t], list(en_p), -1)))
                if B.r(p) == B.start(c):
                    t2 = B.step(p, 0, 2 * d)
                    if t2 >= 0 and t2 not in occ:
                        if B.r(t2) == last:
                            out.append((B.name(p) + B.name(t2) + '=', 'p', None))
                        else:
                            out.append((B.name(p) + B.name(t2), 'n', make(own_k, rest + [t2], list(en_p), t)))
        for df in (-1, 1):
            t = B.step(p, df, d)
            if t < 0:
                continue
            cap = None
            if t in enset:
                cap = t
            elif t == ep and ep >= 0:
                cap = B.step(t, 0, -d)  # the pawn that double-stepped
                if cap not in enset:
                    cap = None
            if cap is None:
                continue
            nen = [x for x in en_p if x != cap]
            if not safe(own_k, nen):
                continue
            if B.r(t) == last:
                out.append((B.name(p) + B.name(t) + '=x', 'p', None))
            else:
                out.append((B.name(p) + B.name(t) + 'x', 'n', make(own_k, rest + [t], nen, -1)))
    return out


def promo_value(model, promoter):
    """result of a promotion, from White's view"""
    if model == 'P':
        return W_ if promoter == 0 else L_
    if model == 'EPW':
        return W_
    if model == 'EPB':
        return L_
    raise ValueError(model)


def solve(B, model, roots, limit=None, wfilter=None):
    """forward exploration from roots, then counting retrograde.  Returns (index, val, moves) where
       index: pos -> id, val[id] in 'WLD' (White's view), moves[id]: list of (label, kind, target id or terminal value)."""
    index = {}
    plist = []
    moves = []
    dq = deque()
    for r in roots:
        if r not in index:
            index[r] = len(plist); plist.append(r); dq.append(r)
    mv = {}
    while dq:
        p = dq.popleft()
        ms = gen(B, p)
        if wfilter is not None and p[0] == 0 and ms:
            ms2 = [m for m in ms if wfilter(B, p, m)]
            if not ms2:
                ms2 = [('dead', 'p', None)]   # no allowed move: White's strategy has failed (Black wins)
            ms = ms2
        lst = []
        for lab, kind, np_ in ms:
            if kind == 'p':
                lst.append((lab, 'p', (L_ if lab == 'dead' else promo_value(model, p[0]))))
            else:
                if np_ not in index:
                    index[np_] = len(plist); plist.append(np_); dq.append(np_)
                lst.append((lab, 'n', index[np_]))
        mv[p] = lst
        if limit and len(plist) > limit:
            raise RuntimeError('too many positions')
    n = len(plist)
    moves = [mv[p] for p in plist]
    # value from the mover's point of view: +1 win, -1 loss, 0 unknown
    res = [0] * n
    cnt = [0] * n
    preds = [[] for _ in range(n)]
    q = deque()
    for i, p in enumerate(plist):
        c = p[0]
        ms = moves[i]
        if not ms:
            if in_check(B, p, c):
                res[i] = -1; q.append(i)
            continue
        win = False
        nn = 0
        for lab, kind, tgt in ms:
            if kind == 'p':
                if (tgt == W_) == (c == 0):
                    win = True
            else:
                nn += 1
                preds[tgt].append(i)
        if win:
            res[i] = 1; q.append(i)
        elif nn == 0:
            res[i] = -1; q.append(i)   # every move is a losing promotion
        else:
            cnt[i] = nn
    while q:
        j = q.popleft()
        rj = res[j]
        for i in preds[j]:
            if res[i] != 0:
                continue
            if rj == -1:
                res[i] = 1; q.append(i)
            else:
                cnt[i] -= 1
                if cnt[i] == 0:
                    res[i] = -1; q.append(i)
    val = []
    for i, p in enumerate(plist):
        r = res[i]
        if r == 0:
            val.append(D_)
        else:
            win_white = (r == 1) == (p[0] == 0)
            val.append(W_ if win_white else L_)
    return index, plist, val, moves


def mover_val(plist, val, i):
    return val[i]


if __name__ == '__main__':
    spec = sys.argv[1]
    model = sys.argv[2]
    B = Board(spec)
    roots = [parse(B, line.strip()) for line in sys.stdin if line.strip() and not line.startswith('#')]
    index, plist, val, moves = solve(B, model, roots)
    print('# %s %s: %d positions' % (spec, model, len(plist)))
    for r in roots:
        i = index[r]
        s = ' '.join('%s:%s' % (lab, (val[t] if k == 'n' else t)) for lab, k, t in moves[i])
        print(fmt(B, r), '|', val[i], '|', s)
