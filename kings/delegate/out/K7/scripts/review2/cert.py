"""Independent implementation of the certificate LC_T of Definition 2.6 (final version), written from the text."""
from kb import B

class Cert:
    def __init__(s, Bd, FZ):
        s.B = Bd; s.FZ = frozenset(FZ)
        fz = s.FZ
        s.dist_to_fz = lambda f: min(Bd.fdist(f, g) for g in fz)
        s.buffer = frozenset(f for f in range(Bd.W) if f not in fz and s.dist_to_fz(f) == 1)
        s.ctx = frozenset(f for f in range(Bd.W) if s.dist_to_fz(f) >= 2)
        s.lmemo = {}
    def inz(s, x): return (x % s.B.W) in s.FZ
    def proj(s, pos):
        wk, bk, wp, bp, stm, ep = pos
        return (wk, bk, frozenset(p for p in wp if s.inz(p)), frozenset(p for p in bp if s.inz(p)), stm, ep if (ep >= 0 and s.inz(ep)) else -1)
    # ---- queen safety (only for the chess clause)
    def qsafe(s, after, q, promoter):
        Bd = s.B
        wk, bk, wp, bp = after[:4]
        opp = 1 - promoter
        ok, pk = (wk, bk) if opp == 0 else (bk, wk)
        opawns, ppawns = (wp, bp) if opp == 0 else (bp, wp)
        if q in Bd.kn[ok] and q not in Bd.kn[pk] and q not in Bd.attacked_by_pawns(ppawns, promoter): return False
        for p in opawns:
            if q in Bd.att[opp][p]:
                # pawn capture legal? own king must not be attacked after capture
                nopp = ppawns - {q}
                if ok not in Bd.attacked_by_pawns(nopp, promoter): return False
        return True
    # ---- L1
    def lf(s, pos, t, sb, qs):
        key = ('f', pos, t, qs)
        r = s.lmemo.get(key)
        if r is not None: return r
        Bd = s.B; res = False
        for kind, frm, to, promo, nxt in Bd.moves(pos):
            if kind == 'K' and not s.inz(to): continue
            if promo:
                if (not qs) or s.qsafe(nxt[1], to, sb): res = True; break
                continue
            # mate of s?
            if Bd.check(nxt, 1 - sb) and not Bd.moves(nxt): res = True; break
            if t >= 2 and s.lg(nxt, t - 1, sb, qs): res = True; break
        s.lmemo[key] = res
        return res
    def lg(s, pos, t, sb, qs):
        key = ('g', pos, t, qs)
        r = s.lmemo.get(key)
        if r is not None: return r
        Bd = s.B; res = True; sd = 1 - sb
        mv = Bd.moves(pos)
        for kind, frm, to, promo, nxt in mv:
            if promo or not s.lf(nxt, t, sb, qs): res = False; break
        if res and not Bd.check(pos, sd):
            wk, bk, wp, bp, stm, ep = pos
            if not s.lf((wk, bk, wp, bp, 1 - stm, -1), t, sb, qs): res = False
        s.lmemo[key] = res
        return res
    def minT(s, Q, Tmax, qs=False):
        sb = 1 - Q[4]; QZ = s.proj(Q)
        for T in range(1, Tmax + 1):
            if s.lg(QZ, T, sb, qs): return T
        return None
    # ---- L2
    def mu(s, Q, use_ep=True, cap=9):
        Bd = s.B; W, H = Bd.W, Bd.H
        wk, bk, wp, bp, stm, ep = Q
        sd = stm; sb = 1 - sd
        own, opp = (wp, bp) if sd == 0 else (bp, wp)
        ok = wk if sd == 0 else bk
        ownc = frozenset(p for p in own if not s.inz(p)); oppc = frozenset(p for p in opp if not s.inz(p))
        d = 1 if sd == 0 else -1; start = 1 if sd == 0 else H - 2; last = H - 1 if sd == 0 else 0
        st0 = (ok, ownc, oppc)
        front = [st0]; seen = {st0}; dist = 0
        while front and dist < cap:
            dist += 1; nxt = []
            for (k, op, xp) in front:
                occ = set(op) | set(xp) | {k}
                for n in Bd.kn[k]:
                    if n in op: continue
                    nx = xp - {n}
                    if n in Bd.attacked_by_pawns(nx, sb): continue
                    st = (n, op, nx)
                    if st not in seen: seen.add(st); nxt.append(st)
                for p in op:
                    t1 = p + d * W
                    if t1 not in occ:
                        if t1 // W == last: return dist
                        st = (k, (op - {p}) | {t1}, xp)
                        if st not in seen: seen.add(st); nxt.append(st)
                        t2 = t1 + d * W
                        if p // W == start and t2 not in occ:
                            if t2 // W == last: return dist
                            st = (k, (op - {p}) | {t2}, xp)
                            if st not in seen: seen.add(st); nxt.append(st)
                    for c in Bd.att[sd][p]:
                        if c in xp:
                            if c // W == last: return dist
                            st = (k, (op - {p}) | {c}, xp - {c})
                            if st not in seen: seen.add(st); nxt.append(st)
                if dist == 1 and use_ep and ep >= 0 and not s.inz(ep):
                    # e.p. capture available at the first move only
                    for p in op:
                        if ep in Bd.att[sd][p] and (ep - d * W) in xp:
                            st = (k, (op - {p}) | {ep}, xp - {ep - d * W})
                            if st not in seen: seen.add(st); nxt.append(st)
            front = nxt
        return 99
    # ---- L3
    def L3(s, Q, T, qs=False):
        """returns (holds, info).  holds: exists guided strategy with no stalemate of s at an s-turn; info: set of flags seen."""
        Bd = s.B; sb = 1 - Q[4]; sd = Q[4]
        memo = {}; flags = set()
        def rg(pos, t):
            key = ('g', pos, t)
            if key in memo: return memo[key]
            mv = Bd.moves(pos); ok = True
            if not mv and not Bd.check(pos, sd): flags.add('stale'); ok = False
            for kind, frm, to, promo, nxt in mv:
                if promo: flags.add('spromo'); continue
                if not rf(nxt, t): ok = False
            memo[key] = ok; return ok
        def rf(pos, t):
            key = ('f', pos, t)
            if key in memo: return memo[key]
            found = False; res = False
            for kind, frm, to, promo, nxt in Bd.moves(pos):
                if kind == 'K' and not s.inz(to): continue
                if kind == 'P' and not s.inz(frm): continue   # s-bar plays Z-moves only
                if promo:
                    if (not qs) or s.qsafe(nxt[1], to, sb): found = True; res = True
                    continue
                pj = s.proj(nxt)
                lm = Bd.moves(pj)
                if Bd.check(pj, sd) and not lm: lw = True
                else: lw = (t >= 2 and s.lg(pj, t - 1, sb, qs))
                if not lw: continue
                found = True
                rm = Bd.moves(nxt)
                if Bd.check(nxt, sd) and not rm: r2 = True
                elif not rm: flags.add('stale'); r2 = False
                else: r2 = rg(nxt, t - 1)
                res = res or r2
            memo[key] = res
            return res
        h = rg(Q, T)
        return h, flags
