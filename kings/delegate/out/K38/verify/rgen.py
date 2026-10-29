# rgen.py -- K38 referee's own move generator, written from kings/SPEC.md only (kings + pawns, no officers).
# Not derived from K38's p5gen.py.  A position is a tuple (wk, bk, wp, bp, stm, ep):
#   squares are (file, rank) pairs, 0-based; wp, bp are frozensets of squares; stm 0 = White, 1 = Black;
#   ep = the skipped square of a double step just made (target for an e.p. capture) or None.
# moves(pos) yields (kind, child_or_None, label): kind 'n' normal move, 'promo' a promotion (the game ends there in
# P / EPW / EPB; the caller decides who wins).

class Board:
    def __init__(self, W, H, wrap):
        self.W, self.H, self.wrap = W, H, wrap

    def sq(self, f, r):
        if r < 0 or r >= self.H:
            return None
        if self.wrap:
            f %= self.W
        elif f < 0 or f >= self.W:
            return None
        return (f, r)

    def nbrs(self, s):
        out = set()
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df or dr:
                    t = self.sq(s[0] + df, s[1] + dr)
                    if t is not None and t != s:
                        out.add(t)
        return out

    def adj(self, a, b):
        return b in self.nbrs(a)

    def pawn_att(self, s, colour):
        d = 1 if colour == 0 else -1
        out = set()
        for df in (-1, 1):
            t = self.sq(s[0] + df, s[1] + d)
            if t is not None:
                out.add(t)
        return out

    def attacked(self, s, by, pos):
        wk, bk, wp, bp = pos[0], pos[1], pos[2], pos[3]
        k = wk if by == 0 else bk
        if self.adj(k, s):
            return True
        for p in (wp if by == 0 else bp):
            if s in self.pawn_att(p, by):
                return True
        return False

    def name(self, s):
        return 'abcdefgh'[s[0]] + str(s[1] + 1)

    def parse(self, txt):
        toks = txt.split()
        wk = bk = None; wp = set(); bp = set()
        for t in toks[:-2]:
            s = ('abcdefgh'.index(t[1]), int(t[2:]) - 1)
            if t[0] == 'K': wk = s
            elif t[0] == 'k': bk = s
            elif t[0] == 'P': wp.add(s)
            elif t[0] == 'p': bp.add(s)
            else: raise ValueError(t)
        stm = 0 if toks[-2] == 'w' else 1
        ep = None if toks[-1] == '-' else ('abcdefgh'.index(toks[-1][0]), int(toks[-1][1:]) - 1)
        return (wk, bk, frozenset(wp), frozenset(bp), stm, ep)

    def fmt(self, pos):
        wk, bk, wp, bp, stm, ep = pos
        t = ['K' + self.name(wk)] + ['P' + self.name(p) for p in sorted(wp)] + ['k' + self.name(bk)] + \
            ['p' + self.name(p) for p in sorted(bp)]
        return ' '.join(t) + (' w ' if stm == 0 else ' b ') + ('-' if ep is None else self.name(ep))

    def legal_pos(self, pos):
        wk, bk, wp, bp, stm, ep = pos
        sqs = [wk, bk] + list(wp) + list(bp)
        if len(set(sqs)) != len(sqs) or self.adj(wk, bk):
            return False
        for p in wp:
            if p[1] in (0, self.H - 1): return False
        for p in bp:
            if p[1] in (0, self.H - 1): return False
        other = 1 - stm
        return not self.in_check(pos, other)

    def in_check(self, pos, colour):
        k = pos[0] if colour == 0 else pos[1]
        return self.attacked(k, 1 - colour, pos)

    def moves(self, pos):
        """All legal moves of the side to move."""
        wk, bk, wp, bp, stm, ep = pos
        out = []
        me = stm
        myk = wk if me == 0 else bk
        myp = wp if me == 0 else bp
        opp = bp if me == 0 else wp
        occ = {wk, bk} | wp | bp

        def mk(nwk, nbk, nwp, nbp, nep):
            return (nwk, nbk, frozenset(nwp), frozenset(nbp), 1 - stm, nep)

        def ok(child):  # own king not attacked after the move
            return not self.in_check(child, me)

        # king moves
        for t in self.nbrs(myk):
            if t in myp or t == (bk if me == 0 else wk):
                continue
            nopp = set(opp) - {t}
            if me == 0:
                c = mk(t, bk, wp, nopp, None)
            else:
                c = mk(wk, t, nopp, bp, None)
            if ok(c):
                out.append(('n', c, 'K' + self.name(myk) + self.name(t)))
        # pawn moves
        d = 1 if me == 0 else -1
        last = self.H - 1 if me == 0 else 0
        second = 1 if me == 0 else self.H - 2
        for p in myp:
            targets = []
            one = self.sq(p[0], p[1] + d)
            if one is not None and one not in occ:
                targets.append((one, None, None))
                two = self.sq(p[0], p[1] + 2 * d)
                if p[1] == second and two is not None and two not in occ:
                    targets.append((two, None, one))
            for t in self.pawn_att(p, me):
                if t in opp:
                    targets.append((t, t, None))
                elif ep is not None and t == ep:
                    # e.p.: the captured pawn stands behind ep from the mover's view
                    cap = (t[0], t[1] - d)
                    if cap in opp:
                        targets.append((t, cap, None))
            for (t, cap, nep) in targets:
                nmy = (set(myp) - {p})
                nopp = set(opp) - ({cap} if cap else set())
                if t[1] == last:
                    # promotion: legality = own king not attacked after the pawn left (new piece placed on t;
                    # it can only block, and the new piece is on t, so treat t as occupied by an own pawn-like blocker)
                    blk = nmy | {t}
                    if me == 0:
                        c = mk(wk, bk, blk, nopp, None)
                    else:
                        c = mk(wk, bk, nopp, blk, None)
                    # attacks on own king come only from kings/pawns here, which a blocker never stops; so just test
                    if ok(c):
                        out.append(('promo', None, 'P' + self.name(p) + self.name(t) + '='))
                    continue
                nmy.add(t)
                if me == 0:
                    c = mk(wk, bk, nmy, nopp, nep)
                else:
                    c = mk(wk, bk, nopp, nmy, nep)
                if ok(c):
                    out.append(('n', c, 'P' + self.name(p) + self.name(t)))
        return out


def solve(B, roots, model):
    """Retrograde least fixed point over positions reachable from roots.
    model: 'P' (promotion wins for the promoter), 'EPW' (every promotion a White win), 'EPB' (Black win).
    Returns dict pos -> 'W'/'D'/'L' from White's point of view."""
    seen = {}
    stack = list(roots)
    for r in roots:
        seen[r] = None
    order = []
    while stack:
        p = stack.pop()
        order.append(p)
        ms = B.moves(p)
        seen[p] = ms
        for k, c, _ in ms:
            if c is not None and c not in seen:
                seen[c] = None
                stack.append(c)
    # value for side to move: +1 win, -1 loss, 0 undecided
    val = {}
    for p in order:
        ms = seen[p]
        if not ms:
            val[p] = -1 if B.in_check(p, p[4]) else 0  # mate / stalemate (0 = draw, final)
    changed = True
    # simple iteration until fixed point (sets are small)
    def promo_val(p):
        me = p[4]
        if model == 'P': return 1
        winner = 0 if model == 'EPW' else 1
        return 1 if winner == me else -1
    final = {p for p in val}
    while changed:
        changed = False
        for p in order:
            if p in final: continue
            ms = seen[p]
            allwin = True; v = None
            for k, c, _ in ms:
                cv = promo_val(p) if k == 'promo' else (-val[c] if c in final else None)
                if k == 'promo':
                    if cv == 1: v = 1; break
                    continue
                if cv == 1: v = 1; break
                if cv != -1: allwin = False
            if v is None and allwin:
                v = -1
            if v is not None:
                val[p] = v; final.add(p); changed = True
    res = {}
    for p in order:
        v = val.get(p, 0) if p in final else 0
        if p not in final: v = 0
        w = v if p[4] == 0 else -v
        res[p] = 'W' if w == 1 else ('L' if w == -1 else 'D')
    return res, seen
