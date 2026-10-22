"""Auditor B: independent move generator for K+P vs K (White pawn) and K+officer vs K / K vs K,
written from kings/SPEC.md only (does not import kings/ref).  Square = rank*W + file.
Position (stm, wk, bk, wp, off) with wp = square or -1, off = (colour, type, square) or None
(type 0..3 = Q R B N).  Only one officer can exist (one pawn promotes once, Black has no pawn).
"""
ROOK_D = [(1, 0), (-1, 0), (0, 1), (0, -1)]
BISH_D = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
KING_D = ROOK_D + BISH_D
KN_D = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]


class Geo:
    def __init__(self, board):
        kind, size = board.split(':')
        self.W, self.H = [int(x) for x in size.split('x')]
        self.cyl = kind == 'cyl'
        assert kind in ('flat', 'cyl')

    def sq(self, f, r):
        return r * self.W + f

    def step(self, s, df, dr):
        """square after a (df,dr) step or None"""
        f, r = s % self.W, s // self.W
        r += dr
        if not 0 <= r < self.H:
            return None
        f += df
        if self.cyl:
            f %= self.W
        elif not 0 <= f < self.W:
            return None
        return r * self.W + f

    def ray(self, s, df, dr, occ):
        """squares along a ray from s; includes the first occupied square (as last).  Stops before
        returning to s."""
        out, cur = [], s
        while True:
            cur = self.step(cur, df, dr)
            if cur is None or cur == s:
                return out
            out.append(cur)
            if cur in occ:
                return out

    def nbrs(self, s):
        return [t for t in (self.step(s, a, b) for a, b in KING_D) if t is not None]

    def knight(self, s):
        return {t for t in (self.step(s, a, b) for a, b in KN_D) if t is not None}

    def slider_targets(self, ty, s, occ):
        dirs = (ROOK_D if ty == 1 else BISH_D if ty == 2 else KING_D)
        res = set()
        for df, dr in dirs:
            res.update(self.ray(s, df, dr, occ))
        return res

    def off_targets(self, ty, s, occ):
        return self.knight(s) if ty == 3 else self.slider_targets(ty, s, occ)


def occupied(pos):
    stm, wk, bk, wp, off = pos
    o = {wk, bk}
    if wp >= 0:
        o.add(wp)
    if off:
        o.add(off[2])
    return o


def attacked(G, pos, side):
    """is the king of `side` attacked by the other colour in `pos`?"""
    stm, wk, bk, wp, off = pos
    k = wk if side == 0 else bk
    okq = bk if side == 0 else wk
    if k in G.nbrs(okq):
        return True
    occ = occupied(pos)
    if side == 1 and wp >= 0:            # white pawn attacks (f+-1, r+1)
        if k in [G.step(wp, 1, 1), G.step(wp, -1, 1)]:
            return True
    if off and off[0] != side:
        if k in G.off_targets(off[1], off[2], occ):   # ray includes first occupied square = king
            return True
    return False


def moves(G, pos):
    """legal successor positions (list)"""
    stm, wk, bk, wp, off = pos
    occ = occupied(pos)
    out = []
    def finish(npos):
        if not attacked(G, npos, stm):
            out.append(npos)
    mk = wk if stm == 0 else bk
    ok = bk if stm == 0 else wk
    # king
    for t in G.nbrs(mk):
        if t == ok:
            continue
        if stm == 0 and (t == wp or (off and off[2] == t)):
            continue                      # own piece
        if stm == 1 and (off and off[0] == 1 and off[2] == t):
            continue
        nwp = -1 if (stm == 1 and t == wp) else wp
        noff = None if (off and off[2] == t) else off
        npos = (1 - stm, t, bk, nwp, noff) if stm == 0 else (1 - stm, wk, t, nwp, noff)
        finish(npos)
    # officer
    if off and off[0] == stm:
        c, ty, s = off
        for t in G.off_targets(ty, s, occ):
            if t == ok:
                continue
            if t == mk or (t == wp and stm == 0):
                continue
            nwp = -1 if (t == wp) else wp
            finish((1 - stm, wk, bk, nwp, (c, ty, t)))
    # pawn (white only)
    if stm == 0 and wp >= 0:
        f, r = wp % G.W, wp // G.W
        last = G.H - 1
        dests = []
        t = G.step(wp, 0, 1)
        if t is not None and t not in occ:
            dests.append(t)
            if r == 1:
                t2 = G.step(t, 0, 1)
                if t2 is not None and t2 not in occ:
                    dests.append(t2)
        for df in (-1, 1):
            t = G.step(wp, df, 1)
            if t is not None and t in occ and t != bk and t != wk:
                dests.append(t)           # capture (only an enemy officer can stand there)
        for t in dests:
            noff = off if not (off and off[2] == t) else None
            if t // G.W == last:
                for ty in range(4):
                    finish((1, wk, bk, -1, (0, ty, t)))
            else:
                finish((1, wk, bk, t, noff))
    return out


def initial(G):
    out = []
    for wk in range(G.W * G.H):
        for bk in range(G.W * G.H):
            if wk == bk or bk in G.nbrs(wk):
                continue
            for wp in range(G.W * G.H):
                if wp in (wk, bk) or wp // G.W in (0, G.H - 1):
                    continue
                for stm in (0, 1):
                    p = (stm, wk, bk, wp, None)
                    if not attacked(G, p, 1 - stm):
                        out.append(p)
    return out


def build(board):
    """returns dict(nodes=list, idx=dict, succ=list of lists, stm, incheck, flip)"""
    G = Geo(board)
    nodes, idx = [], {}
    todo = []
    def add(p):
        i = idx.get(p)
        if i is None:
            i = idx[p] = len(nodes)
            nodes.append(p)
            todo.append(i)
        return i
    for p in initial(G):
        add(p)
    succ, incheck, flip = {}, {}, {}
    while todo:
        i = todo.pop()
        p = nodes[i]
        succ[i] = [add(q) for q in moves(G, p)]
        incheck[i] = attacked(G, p, p[0])
        flip[i] = -1 if incheck[i] else add((1 - p[0],) + p[1:])
    n = len(nodes)
    return dict(G=G, nodes=nodes, idx=idx, succ=[succ[i] for i in range(n)],
                incheck=[incheck[i] for i in range(n)], flip=[flip[i] for i in range(n)],
                stm=[p[0] for p in nodes])


def name(G, s):
    return 'abcdefgh'[s % G.W] + str(s // G.W + 1)


def kpline(G, p):
    stm, wk, bk, wp, off = p
    toks = ['K' + name(G, wk), 'k' + name(G, bk)]
    if wp >= 0:
        toks.append('P' + name(G, wp))
    if off:
        ch = 'QRBN'[off[1]]
        toks.append((ch if off[0] == 0 else ch.lower()) + name(G, off[2]))
    return ' '.join(toks) + (' w -' if stm == 0 else ' b -')
