"""Independent K+P engine (written for the K7 round-2 counterexample hunt; not derived from the drafter's kpgen).
Square = f + W*r  (file f, rank index r; White moves to larger r).  Position = (wk, bk, wp, bp, stm, ep)
with wp,bp frozensets; ep = skipped square or -1 (kept only if an enemy pawn attacks it, as kpsolve does)."""
import random

class B:
    def __init__(s, W, H, wrap):
        s.W, s.H, s.wrap = W, H, wrap
        s.N = W * H
        s.kn = [tuple(sorted({s.sq(f + df, r + dr) for df in (-1, 0, 1) for dr in (-1, 0, 1) if (df or dr)
                              and s.sq(f + df, r + dr) is not None and s.sq(f + df, r + dr) != f + W * r}))
                for r in range(H) for f in range(W)]
        # attackers' target squares of a pawn of colour c on square x
        s.att = [[tuple(sorted({y for df in (-1, 1) for y in [s.sq(x % W + df, x // W + (1 if c == 0 else -1))] if y is not None and y != x}))
                  for x in range(s.N)] for c in (0, 1)]
        # inverse: squares from which a pawn of colour c attacks y
        s.attby = [[tuple(x for x in range(s.N) if y in s.att[c][x]) for y in range(s.N)] for c in (0, 1)]
    def sq(s, f, r):
        if r < 0 or r >= s.H: return None
        if s.wrap: f %= s.W
        elif f < 0 or f >= s.W: return None
        return f + s.W * r
    def name(s, x): return "abcdefgh"[x % s.W] + str(x // s.W + 1)
    def num(s, n): return "abcdefgh".index(n[0]) + s.W * (int(n[1:]) - 1)
    def fdist(s, a, b):
        d = abs(a % s.W - b % s.W)
        return min(d, s.W - d) if s.wrap else d
    def kdist(s, a, b):
        return max(s.fdist(a, b), abs(a // s.W - b // s.W))
    def attacked_by_pawns(s, pawns, c):
        a = set()
        for p in pawns: a.update(s.att[c][p])
        return a
    def text(s, pos):
        wk, bk, wp, bp, stm, ep = pos
        t = ["K" + s.name(wk), "k" + s.name(bk)] + ["P" + s.name(p) for p in sorted(wp)] + ["p" + s.name(p) for p in sorted(bp)]
        return " ".join(t) + (" w " if stm == 0 else " b ") + (s.name(ep) if ep >= 0 else "-")
    def parse(s, line):
        t = line.split(); wp = set(); bp = set()
        for x in t[:-2]:
            if x[0] == 'K': wk = s.num(x[1:])
            elif x[0] == 'k': bk = s.num(x[1:])
            elif x[0] == 'P': wp.add(s.num(x[1:]))
            else: bp.add(s.num(x[1:]))
        return (wk, bk, frozenset(wp), frozenset(bp), 0 if t[-2] == 'w' else 1, -1 if t[-1] == '-' else s.num(t[-1]))
    def check(s, pos, c):
        wk, bk, wp, bp = pos[:4]
        return (wk in s.attacked_by_pawns(bp, 1)) if c == 0 else (bk in s.attacked_by_pawns(wp, 0))
    def legal_pos(s, pos):
        wk, bk, wp, bp, stm, ep = pos
        occ = [wk, bk, *wp, *bp]
        if len(set(occ)) != len(occ) or bk in s.kn[wk]: return False
        for p in (*wp, *bp):
            if p // s.W in (0, s.H - 1): return False
        return not s.check(pos, 1 - stm)
    def moves(s, pos):
        """list of (kind, frm, to, promo, newpos|None) ; for a promotion newpos is None and 'after' the position (other side to move)"""
        W, H = s.W, s.H
        wk, bk, wp, bp, stm, ep = pos
        us = stm; them = 1 - us
        ok, ek = (wk, bk) if us == 0 else (bk, wk)
        own, opp = (wp, bp) if us == 0 else (bp, wp)
        occ = set(wp) | set(bp) | {wk, bk}
        out = []
        def mk(nok, nown, nopp, nep=-1):
            if us == 0: return (nok, ek, frozenset(nown), frozenset(nopp), 1, nep)
            return (ek, nok, frozenset(nopp), frozenset(nown), 0, nep)
        for n in s.kn[ok]:
            if n in own or n == ek or n in s.kn[ek]: continue
            nopp = opp - {n}
            if n in s.attacked_by_pawns(nopp, them): continue
            out.append(('K', ok, n, False, mk(n, own, nopp)))
        d = 1 if us == 0 else -1
        start = 1 if us == 0 else H - 2
        last = H - 1 if us == 0 else 0
        for p in sorted(own):
            t = p + d * W
            def push(to, capsq, nepsq=-1):
                nown = own - {p}; nopp = opp - {capsq} if capsq >= 0 else opp
                if to // W == last:
                    if ok in s.attacked_by_pawns(nopp, them): return
                    out.append(('P', p, to, True, ('after', mk(ok, nown, nopp))))
                    return
                nown = nown | {to}
                if ok in s.attacked_by_pawns(nopp, them): return
                out.append(('P', p, to, False, mk(ok, nown, nopp, nepsq)))
            if t not in occ:
                push(t, -1)
                t2 = t + d * W
                if p // W == start and t2 not in occ:
                    if t2 // W == last: push(t2, -1)
                    else:
                        nep = t if any(t in s.att[them][q] for q in opp) else -1
                        push(t2, -1, nep)
            for c in s.att[us][p]:
                if c in opp: push(c, c)
                elif c == ep and ep >= 0: push(c, c - d * W)
        return out

def promo_row_ok(Bd, pos): return True
