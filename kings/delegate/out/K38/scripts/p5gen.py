# p5gen.py (K38) -- own move generator for kings + pawns, written from kings/SPEC.md only.
# No solver tables are read. Board W x H, flat or cylinder. Squares are (f, r) with f = 0..W-1 (file a = 0),
# r = 0..H-1 (rank 1 = 0). A position is (wk, bk, wp, bp, ep, stm): wp, bp frozensets of squares,
# ep = skipped square of the last double step or None, stm = 0 (White) / 1 (Black).
# A move is returned as (kind, child) with kind in {'K' king move, 'P' pawn move, 'Q' promotion (child None)}.
# Promotions are not expanded into pieces: the games used here (P, EPW, EPB) end at the first promotion.

class Board:
    def __init__(self, W, H, cyl):
        self.W, self.H, self.cyl = W, H, cyl

    def sq(self, f, r):
        if r < 0 or r >= self.H:
            return None
        if self.cyl:
            f %= self.W
        elif f < 0 or f >= self.W:
            return None
        return (f, r)

    def nbrs(self, s):
        out = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df or dr:
                    t = self.sq(s[0] + df, s[1] + dr)
                    if t is not None and t != s and t not in out:
                        out.append(t)
        return out

    def adj(self, a, b):
        return b in self.nbrs(a)

    def pawn_attacks(self, s, colour):
        """squares attacked by a pawn of `colour` standing on s"""
        d = 1 if colour == 0 else -1
        out = []
        for df in (-1, 1):
            t = self.sq(s[0] + df, s[1] + d)
            if t is not None:
                out.append(t)
        return out

    def attacked_by_pawns(self, s, pawns, colour):
        return any(s in self.pawn_attacks(p, colour) for p in pawns)

    def legal_position(self, pos):
        wk, bk, wp, bp, ep, stm = pos
        if wk == bk or self.adj(wk, bk):
            return False
        occ = [wk, bk] + list(wp) + list(bp)
        if len(set(occ)) != len(occ):
            return False
        for p in list(wp) + list(bp):
            if p[1] == 0 or p[1] == self.H - 1:
                return False
        # the side not to move must not be in check
        if stm == 0 and self.attacked_by_pawns(bk, wp, 0):
            return False
        if stm == 1 and self.attacked_by_pawns(wk, bp, 1):
            return False
        return True

    def in_check(self, pos):
        wk, bk, wp, bp, ep, stm = pos
        return self.attacked_by_pawns(wk, bp, 1) if stm == 0 else self.attacked_by_pawns(bk, wp, 0)

    def moves(self, pos):
        wk, bk, wp, bp, ep, stm = pos
        us = stm
        ok, ek = (wk, bk) if us == 0 else (bk, wk)
        own, opp = (wp, bp) if us == 0 else (bp, wp)
        d = 1 if us == 0 else -1
        last = self.H - 1 if us == 0 else 0
        second = 1 if us == 0 else self.H - 2
        out = []

        def make(nok, nown, nopp, nep):
            if us == 0:
                return (nok, ek, frozenset(nown), frozenset(nopp), nep, 1)
            return (ek, nok, frozenset(nopp), frozenset(nown), nep, 0)

        def king_safe(k, nopp):
            return not self.attacked_by_pawns(k, nopp, 1 - us)

        # king moves
        for n in self.nbrs(ok):
            if n in own or n == ek or self.adj(n, ek):
                continue
            nopp = opp - {n}
            if not king_safe(n, nopp):
                continue
            out.append(('K', make(n, own, nopp, None)))
        # pawn moves
        occ = set(own) | set(opp) | {wk, bk}
        for p in own:
            rest = own - {p}
            targets = []  # (dest, captured square or None, ep after)
            t1 = self.sq(p[0], p[1] + d)
            if t1 is not None and t1 not in occ:
                targets.append((t1, None, None))
                if p[1] == second:
                    t2 = self.sq(p[0], p[1] + 2 * d)
                    if t2 is not None and t2 not in occ:
                        targets.append((t2, None, t1 if t2[1] != last else None))
            for c in self.pawn_attacks(p, us):
                if c in opp:
                    targets.append((c, c, None))
                elif ep is not None and c == ep:
                    victim = self.sq(c[0], c[1] - d)
                    if victim in opp:
                        targets.append((c, victim, None))
            for dest, cap, nep in targets:
                nopp = opp - {cap} if cap is not None else opp
                if not king_safe(ok, nopp):
                    continue
                if dest[1] == last:
                    out.append(('Q', None))
                else:
                    out.append(('P', make(ok, rest | {dest}, nopp, nep)))
        return out


def parse(tokens, board):
    """'Kc4 Pb5 kb6 pc5 w -' -> position"""
    t = tokens.split()
    wk = bk = None
    wp, bp = set(), set()
    for x in t[:-2]:
        s = (ord(x[1]) - 97, int(x[2:]) - 1)
        if x[0] == 'K':
            wk = s
        elif x[0] == 'k':
            bk = s
        elif x[0] == 'P':
            wp.add(s)
        elif x[0] == 'p':
            bp.add(s)
    ep = None if t[-1] == '-' else (ord(t[-1][0]) - 97, int(t[-1][1:]) - 1)
    return (wk, bk, frozenset(wp), frozenset(bp), ep, 0 if t[-2] == 'w' else 1)


def name(s):
    return chr(97 + s[0]) + str(s[1] + 1)


def fmt(pos):
    wk, bk, wp, bp, ep, stm = pos
    toks = ['K' + name(wk)] + ['P' + name(p) for p in sorted(wp)] + ['k' + name(bk)] + ['p' + name(p) for p in sorted(bp)]
    return ' '.join(toks) + ' ' + ('w' if stm == 0 else 'b') + ' ' + (name(ep) if ep else '-')


def solve(board, roots, model):
    """Own solver of the games P, EPW, EPB on every position reachable from roots.
    model 'P': a promotion wins for the promoter; 'EPW': every promotion is a White win; 'EPB': a Black win.
    Mate wins, stalemate and infinite play draw (least fixed point). Returns {pos: 'W'/'D'/'L'} (White's view)."""
    seen, stack, succ = set(roots), list(roots), {}
    while stack:
        p = stack.pop()
        ms = board.moves(p)
        succ[p] = ms
        for k, c in ms:
            if c is not None and c not in seen:
                seen.add(c)
                stack.append(c)
    val = {}  # 'W' or 'L' from White's view

    def promo_val(stm):
        if model == 'P':
            return 'W' if stm == 0 else 'L'
        return 'W' if model == 'EPW' else 'L'

    for p, ms in succ.items():
        if not ms:
            if board.in_check(p):
                val[p] = 'L' if p[5] == 0 else 'W'
    changed = True
    while changed:
        changed = False
        for p, ms in succ.items():
            if p in val or not ms:
                continue
            good = 'W' if p[5] == 0 else 'L'
            vs = [promo_val(p[5]) if c is None else val.get(c) for k, c in ms]
            if good in vs:
                val[p] = good
                changed = True
            elif all(v is not None and v != good for v in vs):
                val[p] = 'L' if good == 'W' else 'W'
                changed = True
    return {p: val.get(p, 'D') for p in succ}
