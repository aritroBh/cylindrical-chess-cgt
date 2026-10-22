"""Independent re-implementation (K7 round 2, counterexample hunt) of:
  - pawn/king move generator (flat or cylinder), e.p. as in SPEC.md
  - local game L_T(Q_Z) of Definition 2.6 (L1), (L1_P) variants
  - mu_s of (L2) with the e.p. clause (context pawns + king, Q° with Z-pieces deleted)
  - (L3) over real play of a guided strategy
Squares sq = rank*W + file (rank 0 = rank 1). Colours 0 White (moves up), 1 Black.
Position = (wk, bk, wp, bp, stm, ep) ; wp,bp frozensets ; ep = skipped square or -1.
"""
import sys
sys.setrecursionlimit(10000)

class Geo:
    def __init__(self, W, H, wrap):
        self.W, self.H, self.wrap = W, H, wrap
        self.N = W * H
        self.kn = []
        self.patt = ([], [])   # squares attacked by a pawn of colour c standing on sq
        self.back = ([], [])   # squares from which a pawn of colour c attacks sq  (inverse)
        for s in range(self.N):
            lst = []
            for df in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    if df or dr:
                        t = self.step(s, df, dr)
                        if t >= 0 and t != s and t not in lst:
                            lst.append(t)
            self.kn.append(tuple(lst))
        self.knset = [frozenset(x) for x in self.kn]
        for c in (0, 1):
            dr = 1 if c == 0 else -1
            for s in range(self.N):
                lst = []
                for df in (-1, 1):
                    t = self.step(s, df, dr)
                    if t >= 0 and t != s and t not in lst:
                        lst.append(t)
                self.patt[c].append(tuple(lst))
        self.attackers = ([set() for _ in range(self.N)], [set() for _ in range(self.N)])
        for c in (0, 1):
            for s in range(self.N):
                for t in self.patt[c][s]:
                    self.attackers[c][t].add(s)

    def step(self, s, df, dr):
        f, r = s % self.W + df, s // self.W + dr
        if r < 0 or r >= self.H:
            return -1
        if self.wrap:
            f %= self.W
        elif f < 0 or f >= self.W:
            return -1
        return r * self.W + f

    def name(self, s):
        return "abcdefgh"[s % self.W] + str(s // self.W + 1)

    def sq(self, n):
        return (int(n[1:]) - 1) * self.W + "abcdefgh".index(n[0])

    def fdist(self, f1, f2):
        d = abs(f1 - f2)
        return min(d, self.W - d) if self.wrap else d

    def text(self, pos):
        wk, bk, wp, bp, stm, ep = pos
        t = ["K" + self.name(wk), "k" + self.name(bk)] + ["P" + self.name(p) for p in sorted(wp)] + ["p" + self.name(p) for p in sorted(bp)]
        return " ".join(t) + (" w" if stm == 0 else " b") + (" " + self.name(ep) if ep >= 0 else " -")

    def parse(self, line):
        tok = line.split()
        wk = bk = None; wp = []; bp = []
        for x in tok[:-2]:
            s = self.sq(x[1:])
            if x[0] == 'K': wk = s
            elif x[0] == 'k': bk = s
            elif x[0] == 'P': wp.append(s)
            else: bp.append(s)
        return (wk, bk, frozenset(wp), frozenset(bp), 0 if tok[-2] == 'w' else 1, -1 if tok[-1] == '-' else self.sq(tok[-1]))

    # ---------- attacks
    def attacked_by_pawns(self, sq, pawns, colour):
        """is sq attacked by a pawn of `colour` among `pawns`"""
        for a in self.attackers[colour][sq]:
            if a in pawns:
                return True
        return False

    def in_check(self, pos, c):
        wk, bk, wp, bp = pos[0], pos[1], pos[2], pos[3]
        if c == 0:
            return self.attacked_by_pawns(wk, bp, 1)
        return self.attacked_by_pawns(bk, wp, 0)

    def legal(self, pos):
        wk, bk, wp, bp, stm, ep = pos
        if wk == bk or bk in self.knset[wk]:
            return False
        occ = [wk, bk] + list(wp) + list(bp)
        if len(set(occ)) != len(occ):
            return False
        for p in occ[2:]:
            if p // self.W in (0, self.H - 1):
                return False
        if self.in_check(pos, 1 - stm):
            return False
        return True

    # ---------- moves.  tuple: (kind, frm, to, promo, newpos|None, after|None)
    def moves(self, pos):
        W, H = self.W, self.H
        wk, bk, wp, bp, stm, ep = pos
        us = stm; them = 1 - us
        ok, ek = (wk, bk) if us == 0 else (bk, wk)
        own, opp = (wp, bp) if us == 0 else (bp, wp)
        occ = set(wp) | set(bp) | {wk, bk}
        out = []
        # king
        for n in self.kn[ok]:
            if n in own or n == ek or n in self.knset[ek]:
                continue
            nopp = opp - {n} if n in opp else opp
            if self.attacked_by_pawns(n, nopp, them):
                continue
            if us == 0:
                np_ = (n, bk, wp, nopp, them, -1)
            else:
                np_ = (wk, n, nopp, bp, them, -1)
            out.append(('K', ok, n, False, np_, None))
        d = 1 if us == 0 else -1
        start = 1 if us == 0 else H - 2
        last = H - 1 if us == 0 else 0
        for s in own:
            t = s + d * W
            if t not in occ:
                self._pm(out, pos, s, t, None, us, last)
                if s // W == start:
                    t2 = t + d * W
                    if t2 not in occ:
                        self._pm(out, pos, s, t2, 'dbl', us, last)
            for c in self.patt[us][s]:
                if c in opp:
                    self._pm(out, pos, s, c, c, us, last)
                elif c == ep and ep >= 0:
                    self._pm(out, pos, s, c, c - d * W, us, last, ep_cap=True)
        return out

    def _pm(self, out, pos, s, to, cap, us, last, ep_cap=False):
        wk, bk, wp, bp, stm, ep = pos
        them = 1 - us
        own, opp = (wp, bp) if us == 0 else (bp, wp)
        capsq = None
        if cap == 'dbl' or cap is None:
            pass
        else:
            capsq = cap
        nopp = opp - {capsq} if capsq is not None else opp
        nown = own - {s}
        promo = (to // self.W == last)
        if not promo:
            nown = nown | {to}
        ownk = wk if us == 0 else bk
        if self.attacked_by_pawns(ownk, nopp, them):
            return
        nwp, nbp = (nown, nopp) if us == 0 else (nopp, nown)
        if promo:
            out.append(('P', s, to, True, None, (wk, bk, nwp, nbp, them, -1)))
            return
        nep = -1
        if cap == 'dbl':
            skip = (s + to) // 2
            if any(skip in self.patt[them][p] for p in nopp):
                nep = skip
        out.append(('P', s, to, False, (wk, bk, nwp, nbp, them, nep), None))

    def pass_(self, pos):
        wk, bk, wp, bp, stm, ep = pos
        return (wk, bk, wp, bp, 1 - stm, -1)


class Cert:
    """Certificate machinery for a king group Z with file set FZ (frozenset of file indices) on geometry g."""
    def __init__(self, g, FZ):
        self.g = g
        self.FZ = frozenset(FZ)
        self.inFZ = [(s % g.W) in self.FZ for s in range(g.N)]
        W = g.W
        self.ctxfiles = [f for f in range(W) if min(g.fdist(f, z) for z in self.FZ) >= 2]
        self.bufffiles = [f for f in range(W) if f not in self.FZ and min(g.fdist(f, z) for z in self.FZ) == 1]

    def project(self, pos):
        wk, bk, wp, bp, stm, ep = pos
        inFZ = self.inFZ
        return (wk, bk, frozenset(p for p in wp if inFZ[p]), frozenset(p for p in bp if inFZ[p]), stm, ep if (ep >= 0 and inFZ[ep]) else -1)

    # ----- queen safety after promotion by `pr` landing on q; `after` has the opponent to move
    def qsafe(self, after, q, pr):
        g = self.g
        wk, bk, wp, bp = after[0], after[1], after[2], after[3]
        opp = 1 - pr
        ok = wk if opp == 0 else bk       # capturer king
        pk = bk if opp == 0 else wk       # promoter's king
        ppawns = bp if opp == 0 else wp   # promoter's pawns
        opawns = wp if opp == 0 else bp   # opponent's pawns
        # opponent pawn captures q
        if g.attacked_by_pawns(q, opawns, opp):
            return False
        # opponent king captures q: q adjacent to ok, not adjacent to promoter's king, not attacked by promoter's pawns
        if q in g.knset[ok] and q not in g.knset[pk] and not g.attacked_by_pawns(q, ppawns, pr):
            return False
        return True

    # ----- (L1)
    def make_L1(self, sbar, queen_clause):
        key = (sbar, queen_clause)
        if not hasattr(self, '_l1cache'):
            self._l1cache = {}
        if key not in self._l1cache:
            self._l1cache[key] = self._make_L1(sbar, queen_clause)
        return self._l1cache[key]

    def _make_L1(self, sbar, queen_clause):
        g = self.g
        inFZ = self.inFZ
        memo_f = {}
        memo_g = {}
        cert = self

        def f(pos, t):
            """sbar to move; t own moves left (>=1).  True iff sbar wins."""
            key = (pos, t)
            r = memo_f.get(key)
            if r is not None:
                return r
            res = False
            s = 1 - sbar
            for kind, frm, to, promo, npos, after in g.moves(pos):
                if kind == 'K' and not inFZ[to]:
                    continue
                if promo:
                    if (not queen_clause) or cert.qsafe(after, to, sbar):
                        res = True
                        break
                    continue
                # mate of s ?
                if g.in_check(npos, s) and not g.moves(npos):
                    res = True
                    break
                if t >= 2 and gg(npos, t - 1):
                    res = True
                    break
            memo_f[key] = res
            return res

        def gg(pos, t):
            """s to move; sbar has t moves left.  True iff sbar wins against everything."""
            key = (pos, t)
            r = memo_g.get(key)
            if r is not None:
                return r
            res = True
            ms = g.moves(pos)
            for kind, frm, to, promo, npos, after in ms:
                if promo:
                    res = False
                    break
                if not f(npos, t):
                    res = False
                    break
            if res and not g.in_check(pos, 1 - sbar):
                if not f(g.pass_(pos), t):
                    res = False
            memo_g[key] = res
            return res

        return f, gg

    def L1_T(self, Q, queen_clause, Tmax):
        """least T <= Tmax with (L1) at Q (s to move), else None."""
        sbar = 1 - Q[4]
        QZ = self.project(Q)
        f, gg = self.make_L1(sbar, queen_clause)
        for T in range(1, Tmax + 1):
            if gg(QZ, T):
                return T
        return None

    # ----- (L2): mu_s (context pawns), e.p. clause.  returns exact value if <= cap else cap+1
    def mu(self, Q, cap, ep_clause=True):
        g = self.g
        W, H = g.W, g.H
        wk, bk, wp, bp, stm, ep = Q
        s = stm
        inFZ = self.inFZ
        own, opp = (set(wp), set(bp)) if s == 0 else (set(bp), set(wp))
        ok = wk if s == 0 else bk
        ownc = frozenset(p for p in own if not inFZ[p])
        oppc = frozenset(p for p in opp if not inFZ[p])
        d = 1 if s == 0 else -1
        pstart = 1 if s == 0 else H - 2
        last = H - 1 if s == 0 else 0
        them = 1 - s
        start = (ok, ownc, oppc)
        seen = {start}
        frontier = [start]
        dist = 0
        # first-move e.p. option (only at the first move)
        first_ep = []
        if ep_clause and ep >= 0 and not inFZ[ep]:
            capsq = ep - d * W
            if capsq in oppc:
                for p in ownc:
                    if ep in g.patt[s][p]:
                        # capture lands on ep (not last rank), removes capsq
                        first_ep.append((ok, (ownc - {p}) | {ep}, oppc - {capsq}))
        while frontier and dist < cap:
            dist += 1
            nxt = []
            for (k, op, xp) in frontier:
                occ = set(op) | set(xp) | {k}
                for n in g.kn[k]:
                    if n in op:
                        continue
                    nxp = xp - {n} if n in xp else xp
                    if g.attacked_by_pawns(n, nxp, them):
                        continue
                    st = (n, op, nxp)
                    if st not in seen:
                        seen.add(st); nxt.append(st)
                for p in op:
                    t = p + d * W
                    if t not in occ:
                        if t // W == last:
                            return dist
                        st = (k, (op - {p}) | {t}, xp)
                        if st not in seen:
                            seen.add(st); nxt.append(st)
                        if p // W == pstart:
                            t2 = t + d * W
                            if t2 not in occ:
                                if t2 // W == last:
                                    return dist
                                st = (k, (op - {p}) | {t2}, xp)
                                if st not in seen:
                                    seen.add(st); nxt.append(st)
                    for c in g.patt[s][p]:
                        if c in xp:
                            if c // W == last:
                                return dist
                            st = (k, (op - {p}) | {c}, xp - {c})
                            if st not in seen:
                                seen.add(st); nxt.append(st)
            if dist == 1:
                for st in first_ep:
                    if st not in seen:
                        seen.add(st); nxt.append(st)
            frontier = nxt
        return cap + 1

    # ----- (L3)
    def L3(self, Q, T, queen_clause, want_log=False):
        """exists guided strategy of sbar (winning local moves only) such that in every real play s is never stalemated
        at one of its turns in the window.  Also reports an ANOMALY if s can promote in some play (should be impossible
        when (L1),(L2) hold).  returns (ok, anomaly)"""
        g = self.g
        inFZ = self.inFZ
        sbar = 1 - Q[4]
        s = Q[4]
        cert = self
        f_loc, g_loc = self.make_L1(sbar, queen_clause)
        anomaly = []
        memo_g = {}
        memo_f = {}

        def local_win_after(npos, t_left_for_sbar):
            # npos: real position after an sbar move, s to move; sbar has t_left_for_sbar moves left
            loc = cert.project(npos)
            if g.in_check(loc, s) and not g.moves(loc):
                return True
            if t_left_for_sbar >= 1 and g_loc(loc, t_left_for_sbar):
                return True
            return False

        def rg(pos, t):
            """s to move in real position, sbar has t moves left.  True iff no stalemate / no s-promotion in all plays"""
            key = (pos, t)
            r = memo_g.get(key)
            if r is not None:
                return r
            res = True
            ms = g.moves(pos)
            if not ms and not g.in_check(pos, s):
                res = False
            for kind, frm, to, promo, npos, after in ms:
                if promo:
                    anomaly.append(g.text(pos))     # s promotes: not a stalemate; recorded (Step 4 says it cannot happen under L1+L2)
                    continue
                if not rf(npos, t):
                    res = False
                    break
            memo_g[key] = res
            return res

        def rf(pos, t):
            key = (pos, t)
            r = memo_f.get(key)
            if r is not None:
                return r
            res = False
            for kind, frm, to, promo, npos, after in g.moves(pos):
                if kind == 'K' and not inFZ[to]:
                    continue
                if kind == 'P' and not inFZ[frm]:
                    continue         # sbar plays Z-moves only: no context-pawn moves
                if promo:
                    if (not queen_clause) or cert.qsafe(after, to, sbar):
                        res = True   # sbar wins at once, game over
                        break
                    continue
                if not local_win_after(npos, t - 1):
                    continue
                # real continuation
                nm = g.moves(npos)
                if not nm and g.in_check(npos, s):
                    res = True; break           # real mate: sbar wins
                if t - 1 < 1:
                    # winning local move at the last move must have been mate or promotion; mate handled above
                    continue
                if rg(npos, t - 1):
                    res = True
                    break
            memo_f[key] = res
            return res

        ok = rg(Q, T)
        return ok, anomaly[:2]


def tcheck_perft(g, pos, depth):
    if depth == 0:
        return 1
    n = 0
    for kind, frm, to, promo, npos, after in g.moves(pos):
        if promo:
            n += 1
        else:
            n += tcheck_perft(g, npos, depth - 1)
    return n
