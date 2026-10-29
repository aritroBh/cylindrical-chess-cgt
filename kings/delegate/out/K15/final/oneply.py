#!/usr/bin/env python3
"""K15 final: the ONE-PLY classifier of the brief, written from scratch (own move generator, flat or cylinder),
used for the Z_B regression test.  It is NOT the classifier behind the census (that is grp.c, the exact local game);
it exists to show exactly how one-ply tests differ from the exact P test.

Position: wk, bk = (file, rank) with files 0..W-1, ranks 1..H; wp, bp = sets of (file, rank).
Tests (all one ply deep, "decisive" = an immediate event of the one-ply kind):
  imm(s, y)      : side s, to move at y, has an immediate decisive reply:
                   (a) a promotion move, or
                   (b) a legal move after which s has a passed pawn (cylcgt.passed, files f-1,f,f+1, e.p. ignored at
                       the roots tested) and the other side has none.
  suicide(s, m)  : the Z-move m of side s leads to y' with imm(other, y').
  safe shuttle(s): a non-capturing king move u->v with u, v on the group files, legal, such that at y' = y after
                   the move the reverse move v->u is legal for s (a 2-cycle), and the opponent has no immediate
                   decisive reply at y' (one ply).
  frozen(s)      : every legal Z-move of s at y is a suicide.
Labels (brief, task item 1):
  frozen : both sides frozen at the root
  on     : White has a safe shuttle and Black is frozen at both ends of it (mirror: off)
  dud    : both sides have a safe shuttle, and every non-shuttle Z-move of either side, at every state of the
           closure under the two shuttles, is a suicide
  over   : Black has a safe shuttle, every other Black move is a suicide, and White has exactly one non-suicide
           move, which leads to a frozen position (mirror: under)
  other  : anything else
"""
import sys, itertools

def mk(W, H, flat):
    def nb(f, d):
        g = f + d
        if flat:
            return g if 0 <= g < W else None
        return g % W
    return nb

class G:
    def __init__(self, W, H, flat):
        self.W, self.H, self.flat = W, H, flat
        self.nb = mk(W, H, flat)
    def kadj(self, a, b):
        df = abs(a[0] - b[0]) if self.flat else min((a[0] - b[0]) % self.W, (b[0] - a[0]) % self.W)
        return df <= 1 and abs(a[1] - b[1]) <= 1
    def pawn_att(self, pawns, color, sq):
        """is sq attacked by pawns of `color` ('W' or 'B')?"""
        f, r = sq
        rr = r - 1 if color == 'W' else r + 1
        for d in (-1, 1):
            g = self.nb(f, d)
            if g is not None and (g, rr) in pawns:
                return True
        return False
    def passed(self, wp, bp, side):
        mine, theirs = (wp, bp) if side == 'W' else (bp, wp)
        for (f, r) in mine:
            files = {f}
            for d in (-1, 1):
                g = self.nb(f, d)
                if g is not None: files.add(g)
            if side == 'W': bl = any(g in files and s > r for g, s in theirs)
            else: bl = any(g in files and s < r for g, s in theirs)
            if not bl: return True
        return False
    def king_moves(self, pos, side):
        wk, bk, wp, bp = pos
        k, ok = (wk, bk) if side == 'W' else (bk, wk)
        own, opp = (wp, bp) if side == 'W' else (bp, wp)
        oc = 'B' if side == 'W' else 'W'
        out = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0: continue
                g = self.nb(k[0], df); r = k[1] + dr
                if g is None or not (1 <= r <= self.H): continue
                t = (g, r)
                if t in own or t == ok or self.kadj(t, ok): continue
                cap = t in opp
                opp2 = opp - {t} if cap else opp
                if self.pawn_att(opp2, oc, t): continue
                npos = (t, bk, wp, opp2) if side == 'W' else (wk, t, opp2, bp)
                out.append((('K', k, t, cap), npos))
        return out
    def pawn_moves(self, pos, side):
        wk, bk, wp, bp = pos
        own, opp = (wp, bp) if side == 'W' else (bp, wp)
        k = wk if side == 'W' else bk
        oc = 'B' if side == 'W' else 'W'
        d = 1 if side == 'W' else -1
        start = 2 if side == 'W' else self.H - 1
        last = self.H if side == 'W' else 1
        occ = wp | bp
        out = []
        def own_king_safe(opp2):
            return not self.pawn_att(opp2, oc, k)
        for (f, r) in own:
            r1 = r + d
            if (f, r1) not in occ and (f, r1) != wk and (f, r1) != bk:
                if r1 == last:
                    if own_king_safe(opp): out.append((('P', (f, r), (f, r1), 'promo'), None))
                else:
                    np_ = (own - {(f, r)}) | {(f, r1)}
                    out.append((('P', (f, r), (f, r1), False), (np_, opp)))
                    r2 = r + 2 * d
                    if r == start and (f, r2) not in occ and (f, r2) != wk and (f, r2) != bk:
                        np2 = (own - {(f, r)}) | {(f, r2)}
                        out.append((('P', (f, r), (f, r2), False), (np2, opp)))
            for dd in (-1, 1):
                g = self.nb(f, dd)
                if g is None: continue
                t = (g, r1)
                if t in opp and 1 <= r1 <= self.H:
                    if r1 == last:
                        if own_king_safe(opp - {t}): out.append((('P', (f, r), t, 'promo'), None))
                    else:
                        np_ = (own - {(f, r)}) | {t}
                        out.append((('P', (f, r), t, True), (np_, opp - {t})))
        res = []
        for m, v in out:
            if v is None:
                res.append((m, None)); continue
            mine, theirs = v
            if not own_king_safe(theirs): continue
            npos = (wk, bk, mine, theirs) if side == 'W' else (wk, bk, theirs, mine)
            res.append((m, npos))
        return res
    def moves(self, pos, side):
        return self.king_moves(pos, side) + self.pawn_moves(pos, side)
    def imm(self, pos, side):
        """side to move at pos has an immediate decisive reply (one-ply)."""
        o = 'B' if side == 'W' else 'W'
        for m, npos in self.moves(pos, side):
            if npos is None: return True
            if self.passed(npos[2], npos[3], side) and not self.passed(npos[2], npos[3], o): return True
        return False

def in_check(g, pos, side):
    wk, bk, wp, bp = pos
    return g.pawn_att(bp, 'B', wk) if side == 'W' else g.pawn_att(wp, 'W', bk)

def analyse(g, pos, gf, side):
    """returns dict: moves list with (move, npos, kind) kind in {'shuttle','suicide','other'}"""
    o = 'B' if side == 'W' else 'W'
    res = []
    for m, npos in g.moves(pos, side):
        if npos is None:
            res.append((m, npos, 'promotion')); continue
        kind = 'other'
        if g.imm(npos, o): kind = 'suicide'
        shut = False
        if m[0] == 'K' and not m[3] and m[1][0] in gf and m[2][0] in gf:
            back = [mm for mm, p2 in g.king_moves(npos, side) if mm[1] == m[2] and mm[2] == m[1] and not mm[3]]
            if back and kind != 'suicide': shut = True
        res.append((m, npos, 'shuttle' if shut else kind))
    return res

def label(g, pos, gf):
    """one-ply label of the root `pos` (White to move or not does not matter: both sides analysed)"""
    seen = set(); stack = [pos]; ok = True; wsh = bsh = False; info = []
    root = pos
    while stack and ok:
        y = stack.pop()
        if y in seen: continue
        seen.add(y)
        for side in 'WB':
            a = analyse(g, y, gf, side)
            for m, npos, kind in a:
                if kind == 'promotion': ok = False
                elif kind == 'other': ok = False
                elif kind == 'shuttle':
                    if y == root:
                        if side == 'W': wsh = True
                        else: bsh = True
                    stack.append(npos)
            if not ok: break
    # classification by shuttle presence at the root, then the "everything else is a suicide" test over the closure
    def count(y, side, kinds):
        return sum(1 for m, p, k in analyse(g, y, gf, side) if k in kinds)
    nshW = count(root, 'W', ('shuttle',)); nshB = count(root, 'B', ('shuttle',))
    noth = count(root, 'W', ('other', 'promotion')) + count(root, 'B', ('other', 'promotion'))
    if not (nshW or nshB) and noth == 0:
        return 'frozen', nshW, nshB, noth, ok
    if ok and nshW and nshB: return 'dud', nshW, nshB, noth, ok
    if ok and nshW and not nshB: return 'on', nshW, nshB, noth, ok
    if ok and nshB and not nshW: return 'off', nshW, nshB, noth, ok
    return 'other', nshW, nshB, noth, ok

def parse(s):
    wk = bk = None; wp = set(); bp = set()
    for t in s.split():
        if t[0] in 'KkPp' and len(t) >= 3 and t[1].isalpha():
            sq = (ord(t[1]) - 97, int(t[2:]))
            if t[0] == 'K': wk = sq
            elif t[0] == 'k': bk = sq
            elif t[0] == 'P': wp.add(sq)
            else: bp.add(sq)
    return (wk, bk, frozenset(wp), frozenset(bp))

def nm(sq): return chr(97 + sq[0]) + str(sq[1])

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--W', type=int, default=7); ap.add_argument('--H', type=int, default=6)
    ap.add_argument('--flat', action='store_true'); ap.add_argument('--F', type=int, default=3)
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('pos', nargs='+')
    a = ap.parse_args()
    g = G(a.W, a.H, a.flat); gf = set(range(a.F))
    for p in a.pos:
        pos = parse(p)
        print('==', p, '(flat)' if a.flat else '(cyl)')
        print('   label (one-ply):', label(g, pos, gf)[:4], ' closure ok=', label(g, pos, gf)[4])
        for side in 'WB':
            for m, npos, kind in analyse(g, pos, gf, side):
                print('   %s %s %s->%s%s : %s' % (side, m[0], nm(m[1]), nm(m[2]), 'x' if m[3] is True else ('=Q' if m[3] == 'promo' else ''), kind))
