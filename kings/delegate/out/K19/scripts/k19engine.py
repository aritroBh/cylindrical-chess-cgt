"""K19 independent engine: geometry, move generation, position I/O for kings + pawns.

Written for task K19 without reading kings/ref/ or any K7/K10 script. Rules follow kings/SPEC.md:
cylinder (files wrap) or flat board, kings, pawns (single/double step, capture, en passant,
promotion), no officers on the board: in every game below the first promotion ends the game, so a
promoted piece is never represented, only the promotion square is remembered.

Position = (wk, bk, wp, bp, ep, stm): squares are f + W*r (file f from 0 = 'a', rank index r from 0 = rank 1),
wp, bp are sorted tuples of squares, ep is the e.p. target square (the square skipped by the last double
step) or -1, stm = 0 for White to move, 1 for Black.
"""
import re


class Board:
    def __init__(self, W, H, cyl):
        self.W, self.H, self.cyl = W, H, cyl
        self.N = W * H
        N = self.N
        self.file = [s % W for s in range(N)]
        self.rank = [s // W for s in range(N)]
        self.kn = [None] * N          # king neighbours
        for s in range(N):
            f, r = s % W, s // W
            out = []
            for df in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    if df == 0 and dr == 0:
                        continue
                    t = self.step(s, df, dr)
                    if t is not None and t != s and t not in out:
                        out.append(t)
            self.kn[s] = tuple(out)
        # pcap[c][s] = squares a pawn of colour c standing on s attacks (c=0 white moves up)
        # pfrom[c][s] = squares on which a pawn of colour c attacks s
        self.pcap = [[None] * N, [None] * N]
        self.pfrom = [[None] * N, [None] * N]
        for c in (0, 1):
            dr = 1 if c == 0 else -1
            for s in range(N):
                out = []
                for df in (-1, 1):
                    t = self.step(s, df, dr)
                    if t is not None and t not in out:
                        out.append(t)
                self.pcap[c][s] = tuple(out)
            for s in range(N):
                out = []
                for df in (-1, 1):
                    t = self.step(s, df, -dr)
                    if t is not None and t not in out:
                        out.append(t)
                self.pfrom[c][s] = tuple(out)

    def step(self, s, df, dr):
        f, r = s % self.W + df, s // self.W + dr
        if r < 0 or r >= self.H:
            return None
        if self.cyl:
            f %= self.W
        elif f < 0 or f >= self.W:
            return None
        return r * self.W + f

    def sq(self, name):
        return (int(name[1:]) - 1) * self.W + (ord(name[0]) - 97)

    def name(self, s):
        return chr(97 + s % self.W) + str(s // self.W + 1)


def parse_board(spec):
    kind, dims = spec.split(':')
    W, H = map(int, dims.split('x'))
    return Board(W, H, kind == 'cyl')


def parse_pos(B, text):
    """kpsolve syntax: 'Ka1 ka6 Pc2 pd3 w -' (no officers)."""
    toks = text.split()
    stm = 0 if toks[-2] == 'w' else 1
    epn = toks[-1]
    wk = bk = None
    wp, bp = [], []
    for t in toks[:-2]:
        c, sq = t[0], B.sq(t[1:])
        if c == 'K':
            wk = sq
        elif c == 'k':
            bk = sq
        elif c == 'P':
            wp.append(sq)
        elif c == 'p':
            bp.append(sq)
        else:
            raise ValueError('officer in position: ' + t)
    ep = -1 if epn == '-' else B.sq(epn)
    return (wk, bk, tuple(sorted(wp)), tuple(sorted(bp)), ep, stm)


def fmt_pos(B, pos):
    wk, bk, wp, bp, ep, stm = pos
    parts = ['K' + B.name(wk), 'k' + B.name(bk)]
    parts += ['P' + B.name(p) for p in wp]
    parts += ['p' + B.name(p) for p in bp]
    parts.append('w' if stm == 0 else 'b')
    parts.append('-' if ep < 0 else B.name(ep))
    return ' '.join(parts)


def attacked(B, sq, by, wk, bk, wp, bp):
    """Is square sq attacked by side 'by' (0 white, 1 black) given the pieces listed?"""
    if by == 0:
        if sq in B.kn[wk]:
            return True
        for p in B.pfrom[0][sq]:
            if p in wp:
                return True
        return False
    if sq in B.kn[bk]:
        return True
    for p in B.pfrom[1][sq]:
        if p in bp:
            return True
    return False


def in_check(B, pos):
    wk, bk, wp, bp, ep, stm = pos
    if stm == 0:
        return attacked(B, wk, 1, wk, bk, wp, bp)
    return attacked(B, bk, 0, wk, bk, wp, bp)


def legal_position(B, pos):
    wk, bk, wp, bp, ep, stm = pos
    if wk == bk or bk in B.kn[wk]:
        return False
    occ = [wk, bk] + list(wp) + list(bp)
    if len(set(occ)) != len(occ):
        return False
    H = B.H
    for p in wp + bp:
        if B.rank[p] in (0, H - 1):
            return False
    # side not to move may not be in check
    if stm == 0:
        return not attacked(B, bk, 0, wk, bk, wp, bp)
    return not attacked(B, wk, 1, wk, bk, wp, bp)


def _tup_remove(t, x):
    return tuple(y for y in t if y != x)


def _tup_replace(t, x, y):
    return tuple(sorted(y if z == x else z for z in t))


class Mv:
    """A legal move. kind 'n' normal, 'p' promotion (game-ending in all our games)."""
    __slots__ = ('kind', 'pos', 'frm', 'to', 'cap')

    def __init__(self, kind, pos, frm, to, cap):
        self.kind, self.pos, self.frm, self.to, self.cap = kind, pos, frm, to, cap


def legal_moves(B, pos, ep_on=True):
    """All legal moves of the side to move. A promotion yields Mv('p', ...) whose pos is the position with
    the pawn removed and the other side to move (the promoted piece is NOT on the board; callers that care
    about its safety use promo_capturable)."""
    wk, bk, wp, bp, ep, stm = pos
    W, H = B.W, B.H
    out = []
    if stm == 0:
        # king
        for t in B.kn[wk]:
            if t in wp or t == bk:
                continue
            nbp = bp
            cap = False
            if t in bp:
                nbp = _tup_remove(bp, t)
                cap = True
            if t in B.kn[bk] or attacked(B, t, 1, t, bk, wp, nbp):
                continue
            out.append(Mv('n', (t, bk, wp, nbp, -1, 1), wk, t, cap))
        occ = set((wk, bk) + wp + bp)
        for p in wp:
            r = B.rank[p]
            t = p + W
            if r + 1 < H and t not in occ:
                if r + 1 == H - 1:
                    npos = (wk, bk, _tup_remove(wp, p), bp, -1, 1)
                    if not attacked(B, wk, 1, wk, bk, npos[2], bp):
                        out.append(Mv('p', npos, p, t, False))
                else:
                    npos = (wk, bk, _tup_replace(wp, p, t), bp, -1, 1)
                    if not attacked(B, wk, 1, wk, bk, npos[2], bp):
                        out.append(Mv('n', npos, p, t, False))
                    if r == 1:
                        t2 = t + W
                        if t2 not in occ:
                            if r + 2 == H - 1:
                                npos = (wk, bk, _tup_remove(wp, p), bp, -1, 1)
                                if not attacked(B, wk, 1, wk, bk, npos[2], bp):
                                    out.append(Mv('p', npos, p, t2, False))
                            else:
                                npos = (wk, bk, _tup_replace(wp, p, t2), bp, t if (ep_on and any(q in bp for q in B.pfrom[1][t])) else -1, 1)
                                if not attacked(B, wk, 1, wk, bk, npos[2], bp):
                                    out.append(Mv('n', npos, p, t2, False))
            for t in B.pcap[0][p]:
                if t in bp:
                    nbp = _tup_remove(bp, t)
                    if r + 1 == H - 1:
                        npos = (wk, bk, _tup_remove(wp, p), nbp, -1, 1)
                        if not attacked(B, wk, 1, wk, bk, npos[2], nbp):
                            out.append(Mv('p', npos, p, t, True))
                    else:
                        npos = (wk, bk, _tup_replace(wp, p, t), nbp, -1, 1)
                        if not attacked(B, wk, 1, wk, bk, npos[2], nbp):
                            out.append(Mv('n', npos, p, t, True))
                elif ep_on and t == ep and ep >= 0:
                    victim = t - W
                    if victim in bp:
                        nbp = _tup_remove(bp, victim)
                        npos = (wk, bk, _tup_replace(wp, p, t), nbp, -1, 1)
                        if not attacked(B, wk, 1, wk, bk, npos[2], nbp):
                            out.append(Mv('n', npos, p, t, True))
    else:
        for t in B.kn[bk]:
            if t in bp or t == wk:
                continue
            nwp = wp
            cap = False
            if t in wp:
                nwp = _tup_remove(wp, t)
                cap = True
            if t in B.kn[wk] or attacked(B, t, 0, wk, t, nwp, bp):
                continue
            out.append(Mv('n', (wk, t, nwp, bp, -1, 0), bk, t, cap))
        occ = set((wk, bk) + wp + bp)
        for p in bp:
            r = B.rank[p]
            t = p - W
            if r - 1 >= 0 and t not in occ:
                if r - 1 == 0:
                    npos = (wk, bk, wp, _tup_remove(bp, p), -1, 0)
                    if not attacked(B, bk, 0, wk, bk, wp, npos[3]):
                        out.append(Mv('p', npos, p, t, False))
                else:
                    npos = (wk, bk, wp, _tup_replace(bp, p, t), -1, 0)
                    if not attacked(B, bk, 0, wk, bk, wp, npos[3]):
                        out.append(Mv('n', npos, p, t, False))
                    if r == H - 2:
                        t2 = t - W
                        if t2 not in occ:
                            if r - 2 == 0:
                                npos = (wk, bk, wp, _tup_remove(bp, p), -1, 0)
                                if not attacked(B, bk, 0, wk, bk, wp, npos[3]):
                                    out.append(Mv('p', npos, p, t2, False))
                            else:
                                npos = (wk, bk, wp, _tup_replace(bp, p, t2), t if (ep_on and any(q in wp for q in B.pfrom[0][t])) else -1, 0)
                                if not attacked(B, bk, 0, wk, bk, wp, npos[3]):
                                    out.append(Mv('n', npos, p, t2, False))
            for t in B.pcap[1][p]:
                if t in wp:
                    nwp = _tup_remove(wp, t)
                    if r - 1 == 0:
                        npos = (wk, bk, nwp, _tup_remove(bp, p), -1, 0)
                        if not attacked(B, bk, 0, wk, bk, nwp, npos[3]):
                            out.append(Mv('p', npos, p, t, True))
                    else:
                        npos = (wk, bk, nwp, _tup_replace(bp, p, t), -1, 0)
                        if not attacked(B, bk, 0, wk, bk, nwp, npos[3]):
                            out.append(Mv('n', npos, p, t, True))
                elif ep_on and t == ep and ep >= 0:
                    victim = t + W
                    if victim in wp:
                        nwp = _tup_remove(wp, victim)
                        npos = (wk, bk, nwp, _tup_replace(bp, p, t), -1, 0)
                        if not attacked(B, bk, 0, wk, bk, nwp, npos[3]):
                            out.append(Mv('n', npos, p, t, True))
    return out


def promo_capturable(B, pos_after_promo, mover, sq, ep_on=True):
    """After 'mover' promotes on sq (pos_after_promo: pawn removed, other side to move), can the opponent
    capture the new piece at once with a legal move? The piece itself does not defend itself."""
    wk, bk, wp, bp, ep, stm = pos_after_promo
    opp = 1 - mover
    if opp == 0:
        # white to move tries to capture a black piece on sq
        # king capture
        if sq in B.kn[wk]:
            if not (sq in B.kn[bk]) and not attacked(B, sq, 1, sq, bk, wp, bp):
                return True
        for p in B.pfrom[0][sq]:
            if p in wp:
                nwp = _tup_replace(wp, p, sq) if B.rank[sq] != B.H - 1 else _tup_remove(wp, p)
                if not attacked(B, wk, 1, wk, bk, nwp, bp):
                    return True
        return False
    if sq in B.kn[bk]:
        if not (sq in B.kn[wk]) and not attacked(B, sq, 0, wk, sq, wp, bp):
            return True
    for p in B.pfrom[1][sq]:
        if p in bp:
            nbp = _tup_replace(bp, p, sq) if B.rank[sq] != 0 else _tup_remove(bp, p)
            if not attacked(B, bk, 0, wk, bk, wp, nbp):
                return True
    return False


def pass_move(pos):
    wk, bk, wp, bp, ep, stm = pos
    return (wk, bk, wp, bp, -1, 1 - stm)
