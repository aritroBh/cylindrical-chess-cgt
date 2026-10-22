"""Minimal K+P move generator, same rules as kings/SPEC.md (pawns and kings only).
Squares: sq = rank*W + file.  Colours: 0 = White, 1 = Black.
Position: (wk, bk, wp, bp, stm, ep) with wp, bp frozensets and ep the skipped square or -1.
A promotion is returned as a move with promo=True and no new position (P semantics: terminal)."""
import functools

class Board:
    def __init__(self, W, H, wrap):
        self.W, self.H, self.wrap = W, H, wrap
        self.N = W * H
        self.kn = [self._kingn(s) for s in range(self.N)]
        # squares attacked by a pawn of colour c standing on s
        self.patt = [[self._patt(c, s) for s in range(self.N)] for c in (0, 1)]

    def step(self, s, df, dr):
        f, r = s % self.W + df, s // self.W + dr
        if r < 0 or r >= self.H:
            return -1
        if self.wrap:
            f %= self.W
        elif f < 0 or f >= self.W:
            return -1
        return r * self.W + f

    def _kingn(self, s):
        out = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                t = self.step(s, df, dr)
                if t >= 0 and t not in out:
                    out.append(t)
        return tuple(out)

    def _patt(self, c, s):
        dr = 1 if c == 0 else -1
        out = []
        for df in (-1, 1):
            t = self.step(s, df, dr)
            if t >= 0 and t not in out:
                out.append(t)
        return tuple(out)

    def fname(self, s):
        return "abcdefgh"[s % self.W] + str(s // self.W + 1)

    def sq(self, name):
        return (int(name[1:]) - 1) * self.W + "abcdefgh".index(name[0])

    # ---- attacks
    def pawn_attacked(self, pawns_of_attacker, colour_attacker):
        a = set()
        for p in pawns_of_attacker:
            a.update(self.patt[colour_attacker][p])
        return a

    def in_check(self, pos, colour):
        wk, bk, wp, bp = pos[0], pos[1], pos[2], pos[3]
        if colour == 0:
            return wk in self.pawn_attacked(bp, 1)
        return bk in self.pawn_attacked(wp, 0)

    def adjacent(self, a, b):
        return b in self.kn[a]

    # ---- moves.  returns list of dict(kind, frm, to, promo, pos) ; pos None for promotion
    def moves(self, pos):
        W, H = self.W, self.H
        wk, bk, wp, bp, stm, ep = pos
        us, them = stm, 1 - stm
        ok, ek = (wk, bk) if us == 0 else (bk, wk)
        ownP, oppP = (wp, bp) if us == 0 else (bp, wp)
        out = []
        occ = set(wp) | set(bp) | {wk, bk}

        def mk(nwk, nbk, nwp, nbp, nep):
            return (nwk, nbk, frozenset(nwp), frozenset(nbp), them, nep)

        # king
        for n in self.kn[ok]:
            if n in ownP or n == ek or self.adjacent(ek, n):
                continue
            noppP = oppP - {n}
            if n in self.pawn_attacked(noppP, them):
                continue
            nwp, nbp = (ownP, noppP) if us == 0 else (noppP, ownP)
            nk = (n, bk) if us == 0 else (wk, n)
            out.append(dict(kind='K', frm=ok, to=n, promo=False, cap=(n in oppP),
                            pos=mk(nk[0], nk[1], nwp, nbp, -1)))
        # pawns
        d = 1 if us == 0 else -1
        start = 1 if us == 0 else H - 2
        last = H - 1 if us == 0 else 0
        for s in sorted(ownP):
            r = s // W
            t = s + d * W
            # single step
            if t not in occ:
                self._pawn(out, pos, s, t, -1, mk, us, last, ownP, oppP)
                # double
                t2 = t + d * W
                if r == start and t2 not in occ:
                    if t2 // W == last:
                        self._pawn(out, pos, s, t2, -1, mk, us, last, ownP, oppP)
                    else:
                        nown = (ownP - {s}) | {t2}
                        nwp, nbp = (nown, oppP) if us == 0 else (oppP, nown)
                        npos = (wk, bk, frozenset(nwp), frozenset(nbp), them, -1)
                        if not self.in_check((wk, bk, nwp, nbp), us):
                            nep = -1
                            if any(c in oppP for c in self.patt[us][t]):  # opp pawn attacks skipped sq? (pawn of them attacks t)
                                pass
                            # an enemy pawn captures onto t if it attacks t: enemy pawn p with t in patt[them][p]
                            if any(t in self.patt[them][p] for p in oppP):
                                nep = t
                            out.append(dict(kind='P', frm=s, to=t2, promo=False, cap=False,
                                            pos=(wk, bk, frozenset(nwp), frozenset(nbp), them, nep)))
            for c in self.patt[us][s]:
                if c in oppP:
                    self._pawn(out, pos, s, c, c, mk, us, last, ownP, oppP)
                elif c == ep and ep >= 0:
                    self._pawn(out, pos, s, c, c - d * W, mk, us, last, ownP, oppP)
        return out

    def _pawn(self, out, pos, s, to, capsq, mk, us, last, ownP, oppP):
        wk, bk = pos[0], pos[1]
        nown = ownP - {s}
        nopp = oppP - {capsq} if capsq >= 0 else oppP
        promo = (to // self.W == last)
        if not promo:
            nown = nown | {to}
        nwp, nbp = (nown, nopp) if us == 0 else (nopp, nown)
        if self.in_check((wk, bk, nwp, nbp), us):
            return
        if promo:
            out.append(dict(kind='P', frm=s, to=to, promo=True, cap=(capsq >= 0), pos=None,
                            after=(wk, bk, frozenset(nwp), frozenset(nbp), 1 - us, -1)))
        else:
            out.append(dict(kind='P', frm=s, to=to, promo=False, cap=(capsq >= 0),
                            pos=mk(wk, bk, nwp, nbp, -1)))

    # ---- legality of a whole position (as kpsolve legal_state)
    def legal_pos(self, pos):
        wk, bk, wp, bp, stm, ep = pos
        if wk == bk or self.adjacent(wk, bk):
            return False
        occ = [wk, bk] + list(wp) + list(bp)
        if len(set(occ)) != len(occ):
            return False
        for p in list(wp) + list(bp):
            if p // self.W in (0, self.H - 1):
                return False
        # side not to move must not be in check
        if self.in_check(pos, 1 - stm):
            return False
        return True

    def to_text(self, pos):
        wk, bk, wp, bp, stm, ep = pos
        toks = ["K" + self.fname(wk), "k" + self.fname(bk)]
        toks += ["P" + self.fname(p) for p in sorted(wp)]
        toks += ["p" + self.fname(p) for p in sorted(bp)]
        return " ".join(toks) + (" w" if stm == 0 else " b") + (" " + self.fname(ep) if ep >= 0 else " -")
