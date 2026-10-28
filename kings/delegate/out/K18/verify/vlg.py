"""Referee's own local-game solver (K18 verification), written from LOOPY Definition 2.6 and kings/SPEC.md.
Nothing here is taken from K18/scripts.  Explicit memoised search of 'sbar wins within t moves'.

State: (K_s_side..)  we keep absolute colours: 0 = White, 1 = Black.  sq = rank*W + file (rank 0 = rank 1).
pos = (wk, bk, wp, bp, ep)   wp, bp = sorted tuples of squares; ep = target square or -1.
s = colour of the side that may pass (the 'sortie' side); sb = 1 - s (confined king, promotes to win).
"""
import sys
from functools import lru_cache


class Board:
    def __init__(self, W, H, wrap, fz_files):
        self.W, self.H, self.wrap = W, H, wrap
        self.fz = set(fz_files)
        self.fzsq = frozenset(r * W + f for r in range(H) for f in self.fz)
        n = W * H
        self.kn = [None] * n
        self.att = [[None] * n for _ in range(2)]  # att[c][sq] = squares attacked by a pawn of colour c on sq
        self.back = [[None] * n for _ in range(2)]  # back[c][sq] = squares from which a pawn of colour c attacks sq
        for sq in range(n):
            f, r = sq % W, sq // W
            L = []
            for df in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    if df == 0 and dr == 0:
                        continue
                    t = self.step(f, r, df, dr)
                    if t is not None:
                        L.append(t)
            self.kn[sq] = tuple(sorted(set(L)))
            for c in (0, 1):
                dr = 1 if c == 0 else -1
                A = []
                for df in (-1, 1):
                    t = self.step(f, r, df, dr)
                    if t is not None:
                        A.append(t)
                self.att[c][sq] = tuple(sorted(set(A)))
        for c in (0, 1):
            for sq in range(n):
                self.back[c][sq] = tuple(p for p in range(n) if sq in self.att[c][p])

    def step(self, f, r, df, dr):
        r2 = r + dr
        if r2 < 0 or r2 >= self.H:
            return None
        f2 = f + df
        if self.wrap:
            f2 %= self.W
        elif f2 < 0 or f2 >= self.W:
            return None
        return r2 * self.W + f2


def parse(B, text):
    """'Kh5 Pa4 kb4 pa5' -> (wk,bk,wp,bp)"""
    wk = bk = None
    wp, bp = [], []
    for tok in text.split():
        pc, f, r = tok[0], ord(tok[1]) - 97, int(tok[2:]) - 1
        sq = r * B.W + f
        if pc == 'K':
            wk = sq
        elif pc == 'k':
            bk = sq
        elif pc == 'P':
            wp.append(sq)
        elif pc == 'p':
            bp.append(sq)
    return (wk, bk, tuple(sorted(wp)), tuple(sorted(bp)), -1)


def name(B, sq):
    return chr(97 + sq % B.W) + str(sq // B.W + 1)


def fmt(B, pos):
    wk, bk, wp, bp, ep = pos
    s = 'K' + name(B, wk) + ' k' + name(B, bk)
    for p in wp:
        s += ' P' + name(B, p)
    for p in bp:
        s += ' p' + name(B, p)
    return s


class Game:
    def __init__(self, B, s, queen_clause=True):
        self.B = B
        self.s = s
        self.sb = 1 - s
        self.qc = queen_clause
        self.memo = {}

    # --- basic geometry -------------------------------------------------
    def attacked_by(self, pos, c, sq, removed=-1):
        """is sq attacked by pawn or king of colour c (ignoring a piece captured on 'removed')"""
        B = self.B
        wk, bk, wp, bp, ep = pos
        k = wk if c == 0 else bk
        if sq in B.kn[k]:
            return True
        pawns = wp if c == 0 else bp
        for p in B.back[c][sq]:
            if p in pawns and p != removed:
                return True
        return False

    def in_check(self, pos, c):
        wk, bk, wp, bp, ep = pos
        k = wk if c == 0 else bk
        pawns = bp if c == 0 else wp
        for p in self.B.back[1 - c][k]:
            if p in pawns:
                return True
        return False

    def moves(self, pos, c, confine=False):
        """legal moves of colour c: list of (newpos, promo_flag).  promo -> newpos has the pawn removed, no queen kept."""
        B = self.B
        wk, bk, wp, bp, ep = pos
        out = []
        mk, ok = (wk, bk) if c == 0 else (bk, wk)
        mp, op = (wp, bp) if c == 0 else (bp, wp)
        occ = {wk, bk} | set(wp) | set(bp)
        dr = 1 if c == 0 else -1
        last = B.H - 1 if c == 0 else 0
        startr = 1 if c == 0 else B.H - 2

        def mk_pos(nmk, nmp, nop, nep):
            if c == 0:
                return (nmk, ok, tuple(sorted(nmp)), tuple(sorted(nop)), nep)
            return (ok, nmk, tuple(sorted(nop)), tuple(sorted(nmp)), nep)

        # king moves
        for d in B.kn[mk]:
            if d in mp:
                continue
            if confine and d not in B.fzsq:
                continue
            if d in B.kn[ok]:
                continue
            nop = op
            cap = -1
            if d in op:
                cap = d
                nop = tuple(x for x in op if x != d)
            # attacked by enemy pawn after capture?
            bad = False
            for p in B.back[1 - c][d]:
                if p in nop:
                    bad = True
                    break
            if bad:
                continue
            out.append((mk_pos(d, mp, nop, -1), False, -1))
        # pawn moves
        f_of = lambda sq: sq % B.W
        for p in mp:
            f, r = p % B.W, p // B.W
            nr = r + dr
            if nr < 0 or nr >= B.H:
                continue
            others = [x for x in mp if x != p]
            tgt = nr * B.W + f
            cands = []
            if tgt not in occ:
                cands.append((tgt, None, -1))
                if r == startr:
                    t2 = (nr + dr) * B.W + f
                    if t2 not in occ:
                        cands.append((t2, None, tgt))
            for t in B.att[c][p]:
                if t in op:
                    cands.append((t, t, -1))
                elif t == ep and ep >= 0:
                    # e.p. capture: the captured pawn stands on same rank as p, file of t
                    cp = r * B.W + t % B.W
                    if cp in op:
                        cands.append((t, cp, -1))
            for (t, capsq, newep) in cands:
                nop = op if capsq is None else tuple(x for x in op if x != capsq)
                promo = (t // B.W == last)
                nmp = others if promo else others + [t]
                # legality: own king not attacked by enemy pawns afterwards
                npos = mk_pos(mk, nmp, nop, newep if not promo else -1)
                if self.in_check(npos, c):
                    continue
                out.append((npos, promo, t if promo else -1))
        return out

    # --- local game -------------------------------------------------------
    def sb_moves(self, pos):
        """moves of sbar, confined.  returns list of (kind, newpos); kind 'win' for a safe promotion, 'fail' unsafe."""
        B = self.B
        c = self.sb
        res = []
        wk, bk, wp, bp, ep = pos
        sk = wk if self.s == 0 else bk
        sbk = bk if self.s == 0 else wk
        for (npos, promo, tsq) in self.moves(pos, c, confine=True):
            if promo:
                safe = True
                if self.qc:
                    # can s capture the new queen at once?  only the king (pawns of s cannot capture on s-bar's last rank)
                    if tsq in B.kn[sk]:
                        # king capture legal if dest not adjacent to sbar king and not attacked by sbar pawns (remaining)
                        if tsq not in B.kn[sbk]:
                            rem = npos[3] if c == 1 else npos[2]
                            attacked = any(p in rem for p in B.back[c][tsq])
                            if not attacked:
                                safe = False
                    # s pawn capture of the queen: a white pawn captures upward onto rank >= 2, impossible on rank 1;
                    # a black pawn captures downward, impossible on the last rank.  (also e.p. cannot apply)
                res.append(('win' if safe else 'fail', npos))
            else:
                res.append(('move', npos))
        return res

    def s_moves(self, pos, k):
        """moves of s.  returns (list of newpos, s_promotes?, n_legal_nonpass).  k = passes left (None=inf)."""
        c = self.s
        mv = self.moves(pos, c, confine=False)
        for (npos, promo, _t) in mv:
            if promo:
                return None, True
        lst = [npos for (npos, promo, _t) in mv]
        return lst, False

    def Vs(self, pos, t, k):
        """s to move, s-bar must win within t of its own moves.  k = passes left for s (None = unlimited)."""
        key = (pos, t, k)
        m = self.memo.get(key)
        if m is not None:
            return m
        lst, prom = self.s_moves(pos, k)
        incheck = self.in_check(pos, self.s)
        if prom:
            r = False
        else:
            canpass = (not incheck) and (k is None or k > 0)
            if not lst and not canpass:
                r = incheck   # mate: win for sbar; stalemate: failure
            elif t == 0:
                r = False
            else:
                r = True
                for np_ in lst:
                    if not self.Ub(np_, t, k):
                        r = False
                        break
                if r and canpass:
                    pp = (pos[0], pos[1], pos[2], pos[3], -1)
                    if not self.Ub(pp, t, None if k is None else k - 1):
                        r = False
        self.memo[key] = r
        return r

    def Ub(self, pos, t, k):
        """s-bar to move with t >= 1 moves left."""
        key = ('U', pos, t, k)
        m = self.memo.get(key)
        if m is not None:
            return m
        r = False
        for kind, npos in self.sb_moves(pos):
            if kind == 'win':
                r = True
                break
            if kind == 'fail':
                continue
            if self.Vs(npos, t - 1, k):
                r = True
                break
        self.memo[key] = r
        return r

    def least_T(self, pos, k, Tmax=14):
        """least T such that sbar wins from pos (s to move) within T moves; None if none up to Tmax."""
        for T in range(0, Tmax + 1):
            if self.Vs(pos, T, k):
                return T
        return None


def sortie_table(B, y_pos, s, k, qc=True, Tmax=14, verbose=False):
    """For root y_pos (s to move, as a pos tuple) list s's non-promoting moves m and, for each, least T over admissible replies r.
    r admissible: legal, not a promotion, leaves sbar's king on F_Z (a Z-move: king or Z-pawn move; all pawns are Z-pawns here)."""
    G = Game(B, s, qc)
    res = []
    for (npos, promo, _t) in G.moves(y_pos, s, confine=False):
        if promo:
            continue
        best = None
        for (qpos, qpromo, _t) in G.moves(npos, 1 - s, confine=True):
            if qpromo:
                continue
            # s-bar's reply must leave s not already mated? (then s-bar has won; T=0)
            T = G.least_T(qpos, k, Tmax)
            if T is not None and (best is None or T < best):
                best = T
        res.append((npos, best))
    return res, G


if __name__ == '__main__':
    pass
