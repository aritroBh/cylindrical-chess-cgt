"""Local certificate LC_T tools: local game (L1), promotion distance (L2, options A and B), real window game (L3)."""
import functools, sys
from kpgen import Board


class Cert:
    def __init__(self, B, FZ):
        self.B = B
        self.FZ = frozenset(FZ)            # set of files
        self.sq_in_FZ = lambda s: (s % B.W) in self.FZ
        self.cache = {}

    # ---------------- helpers
    def project(self, pos):
        """Q_Z: delete every pawn standing off F_Z; keep e.p. only if on F_Z."""
        wk, bk, wp, bp, stm, ep = pos
        wp = frozenset(p for p in wp if self.sq_in_FZ(p))
        bp = frozenset(p for p in bp if self.sq_in_FZ(p))
        if ep >= 0 and not self.sq_in_FZ(ep):
            ep = -1
        return (wk, bk, wp, bp, stm, ep)

    def queen_safe(self, B, after, q, promoter):
        """After a promotion by `promoter` onto q (position `after`, other side to move): can the opponent capture on q at once?"""
        wk, bk, wp, bp = after[0], after[1], after[2], after[3]
        opp = 1 - promoter
        # opponent king capture: king adjacent to q, q not attacked by promoter's pawns, not adjacent to promoter's king
        ok = wk if opp == 0 else bk
        pk = bk if opp == 0 else wk
        ppawns = bp if opp == 0 else wp
        opawns = wp if opp == 0 else bp
        if q in B.kn[ok]:
            if not B.adjacent(pk, q) and q not in B.pawn_attacked(ppawns, promoter):
                return False
        # opponent pawn captures q
        for p in opawns:
            if q in B.patt[opp][p]:
                return False
        return True

    # ---------------- (L1): local game
    def local_f(self, pos, t, sbar, qsafe, memo):
        """s-bar to move in the local game (position pos, pawns of F_Z only), t own moves left. True iff s-bar forces a win."""
        key = (pos, t, qsafe)
        if key in memo:
            return memo[key]
        B = self.B
        res = False
        for m in B.moves(pos):
            if m['kind'] == 'K' and not self.sq_in_FZ(m['to']):
                continue
            if m['promo']:
                if not qsafe or self.queen_safe(B, m['after'], m['to'], sbar):
                    res = True
                    break
                continue
            npos = m['pos']
            # s to move: mated?
            opts = B.moves(npos)
            if not opts and B.in_check(npos, 1 - sbar):
                res = True
                break
            if t >= 2 and self.local_g(npos, t - 1, sbar, qsafe, memo):
                res = True
                break
        memo[key] = res
        return res

    def local_g(self, pos, t, sbar, qsafe, memo):
        """s to move in the local game; s-bar has t moves left. True iff s-bar still wins whatever s does (s may pass if not in check)."""
        key = ('g', pos, t, qsafe)
        if key in memo:
            return memo[key]
        B = self.B
        s = 1 - sbar
        res = True
        opts = B.moves(pos)
        for m in opts:
            if m['promo']:
                res = False
                break
            if not self.local_f(m['pos'], t, sbar, qsafe, memo):
                res = False
                break
        if res and not B.in_check(pos, s):
            wk, bk, wp, bp, stm, ep = pos
            ppos = (wk, bk, wp, bp, 1 - stm, -1)
            if not self.local_f(ppos, t, sbar, qsafe, memo):
                res = False
        memo[key] = res
        return res

    def L1(self, Q, qsafe=False, Tmax=7):
        """Q: real position after m, r (s to move).  Return least T <= Tmax with (L1), or None."""
        sbar = 1 - Q[4]
        QZ = self.project(Q)
        memo = {}
        for T in range(1, Tmax + 1):
            if self.local_g(QZ, T, sbar, qsafe, memo):
                return T
        return None

    # ---------------- (L2): promotion distance of s (context pawns, or all pawns = option A)
    def mu(self, Q, include_Z):
        """Least number of consecutive s-moves promoting a pawn of s, with s-bar's Z-pieces removed, s-bar's context pawns fixed
        (they may be captured).  include_Z False: s's Z-pawns removed and only context-pawn promotions count (option B);
        include_Z True: s's Z-pawns stay and count (option A, original Definition 2.6)."""
        B = self.B
        s = Q[4]
        wk, bk, wp, bp, stm, ep = Q
        if s == 0:
            own, opp, ek, ok = set(wp), set(bp), bk, wk
        else:
            own, opp, ek, ok = set(bp), set(wp), wk, bk
        ownc = frozenset(p for p in own if not self.sq_in_FZ(p))
        ownz = frozenset(p for p in own if self.sq_in_FZ(p))
        oppc = frozenset(p for p in opp if not self.sq_in_FZ(p))
        if include_Z:
            start = (ok, ownc | ownz, oppc)
        else:
            start = (ok, ownc, oppc)
        # BFS over (king, own pawns, opp pawns); s-bar king and Z pawns of s-bar absent (placed off-board = no king)
        d = 1 if s == 0 else -1
        W, H = B.W, B.H
        pstart = 1 if s == 0 else H - 2
        last = H - 1 if s == 0 else 0
        frontier = [start]
        seen = {start}
        dist = 0
        while frontier:
            dist += 1
            nxt = []
            for (k, op, xp) in frontier:
                occ = set(op) | set(xp) | {k}
                # king moves
                att = B.pawn_attacked(xp, 1 - s)
                for n in B.kn[k]:
                    if n in op:
                        continue
                    nxp = xp - {n}
                    if n in B.pawn_attacked(nxp, 1 - s):
                        continue
                    st = (n, op, nxp)
                    if st not in seen:
                        seen.add(st)
                        nxt.append(st)
                # pawn moves
                for p in op:
                    t = p + d * W
                    if t not in occ:
                        if t // W == last:
                            return dist
                        st = (k, (op - {p}) | {t}, xp)
                        if st not in seen:
                            seen.add(st); nxt.append(st)
                        t2 = t + d * W
                        if p // W == pstart and t2 not in occ:
                            if t2 // W == last:
                                return dist
                            st = (k, (op - {p}) | {t2}, xp)
                            if st not in seen:
                                seen.add(st); nxt.append(st)
                    for c in B.patt[s][p]:
                        if c in xp:
                            if c // W == last:
                                return dist
                            st = (k, (op - {p}) | {c}, xp - {c})
                            if st not in seen:
                                seen.add(st); nxt.append(st)
            frontier = nxt
            if dist > 7:
                return 99
        return 99

    # ---------------- (L3): real window game with s-bar restricted to local-winning moves
    def L3(self, Q, T, qsafe=False):
        """exists sigma_Z (a local winning strategy) such that no real play consistent with it has s stalemated at an s-turn
        (and no s promotion occurs).  Returns (exists_version, forall_version, info)."""
        B = self.B
        sbar = 1 - Q[4]
        lmemo = {}
        rmemo_e, rmemo_a = {}, {}
        bad = []

        def real_g(pos, t):
            # s to move in real position; s-bar has t moves left
            key = (pos, t)
            if key in rmemo_e:
                return rmemo_e[key], rmemo_a[key]
            e = True; a = True
            opts = B.moves(pos)
            if not opts:
                if not B.in_check(pos, 1 - sbar):
                    e = False; a = False  # real stalemate of s
                    bad.append(pos)
            for m in opts:
                if m['promo']:
                    # s promotes: allowed only if (L2)/(L1) exclude it; flag
                    e = False; a = False
                    bad.append(('spromo', pos))
                    continue
                ee, aa = real_f(m['pos'], t)
                e = e and ee; a = a and aa
            rmemo_e[key] = e; rmemo_a[key] = a
            return e, a

        def real_f(pos, t):
            key = ('f', pos, t)
            if key in rmemo_e:
                return rmemo_e[key], rmemo_a[key]
            # s-bar to move: choose among local-winning moves
            e_any = False
            a_all = True
            found = False
            for m in B.moves(pos):
                if m['kind'] == 'K' and not self.sq_in_FZ(m['to']):
                    continue
                if m['promo']:
                    if not qsafe or self.queen_safe(B, m['after'], m['to'], sbar):
                        found = True
                        e_any = True
                    continue
                npos = m['pos']
                # is the local projection winning for s-bar with t-1 moves left (s to move)?
                loc = self.project(npos)
                lopts = B.moves(loc)
                lw = False
                if not lopts and B.in_check(loc, 1 - sbar):
                    lw = True
                elif t >= 2 and self.local_g(loc, t - 1, sbar, qsafe, lmemo):
                    lw = True
                if not lw:
                    continue
                found = True
                # real continuation
                ropts = B.moves(npos)
                if not ropts and B.in_check(npos, 1 - sbar):
                    ee, aa = True, True
                elif not ropts:
                    ee, aa = False, False
                    bad.append(npos)
                else:
                    ee, aa = real_g(npos, t - 1)
                e_any = e_any or ee
                a_all = a_all and aa
            if not found:
                e_any = False; a_all = False
            rmemo_e[key] = e_any; rmemo_a[key] = a_all
            return e_any, a_all

        # start: s to move at Q with s-bar having T moves
        e, a = real_g(Q, T)
        return e, a, bad[:2]
