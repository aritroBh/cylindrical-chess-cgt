"""Referee's own local-game solver (Definition 2.6), written from LOOPY text only.
state: (wk, bk, wp(frozenset), bp(frozenset), ep) with squares as (f,r); side given separately.
D = defender s (may pass), A = attacker sbar (confined king)."""
import sys, functools
sys.setrecursionlimit(10000)

class Game:
    def __init__(self, W, H, wrap, attacker, FZ, queen=True, mate=True, confine=True, kmax=None):
        self.W, self.H, self.wrap = W, H, wrap
        self.A = attacker          # 'w' or 'b'
        self.D = 'b' if attacker == 'w' else 'w'
        self.FZ = set(FZ); self.queen = queen; self.mate = mate; self.confine = confine
        self.kmax = kmax  # None = infinite
        self.memo = {}
    def nb(self, sq):
        f, r = sq; out = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0: continue
                nr = r + dr
                if not (0 <= nr < self.H): continue
                nf = f + df
                if self.wrap: nf %= self.W
                elif not (0 <= nf < self.W): continue
                out.append((nf, nr))
        return out
    def fstep(self, f, d):
        nf = f + d
        if self.wrap: return nf % self.W
        return nf if 0 <= nf < self.W else None
    def pawn_att(self, c, sq):  # squares attacked by pawn of colour c on sq
        f, r = sq; dr = 1 if c == 'w' else -1; nr = r + dr
        if not (0 <= nr < self.H): return []
        out = []
        for d in (-1, 1):
            nf = self.fstep(f, d)
            if nf is not None: out.append((nf, nr))
        return out
    def attacked(self, sq, by, ks, ps):
        # is sq attacked by colour 'by' (king ks, pawns ps)
        if sq in self.nbset(ks): return True
        for p in ps:
            if sq in self.pawn_att(by, p): return True
        return False
    @functools.lru_cache(maxsize=None)
    def nbset(self, sq): return frozenset(self.nb(sq))
    def in_check(self, side, st):
        wk, bk, wp, bp, ep = st
        if side == 'w': return self.attacked(wk, 'b', bk, bp)
        return self.attacked(bk, 'w', wk, wp)
    def moves(self, side, st, confineK=False):
        """legal moves: list of (newstate, kind) kind in 'move','promo'. promotion newstate has promoted pawn removed, extra info sq."""
        wk, bk, wp, bp, ep = st
        res = []
        own_k, en_k = (wk, bk) if side == 'w' else (bk, wk)
        own_p, en_p = (wp, bp) if side == 'w' else (bp, wp)
        def mk(nk, nop, nep_, newep):
            if side == 'w': return (nk, bk, nop, nep_, newep)
            return (wk, nk, nep_, nop, newep)
        # king
        for t in self.nb(own_k):
            if t in own_p or t == en_k: pass
            if t in own_p: continue
            if t in self.nbset(en_k): continue
            nen = en_p - {t}
            if any(t in self.pawn_att('b' if side == 'w' else 'w', p) for p in nen): continue
            if confineK and t[0] not in self.FZ: continue
            res.append((mk(t, own_p, nen, None), 'move', None))
        dr = 1 if side == 'w' else -1
        start = 1 if side == 'w' else self.H - 2
        last = self.H - 1 if side == 'w' else 0
        occ = {wk, bk} | wp | bp
        for p in own_p:
            f, r = p
            def legal_after(nop, nen):
                # own king must not be attacked by enemy pawns (nen) / enemy king
                if own_k in self.nbset(en_k): return False
                return not any(own_k in self.pawn_att('b' if side == 'w' else 'w', q) for q in nen)
            # pushes
            t = (f, r + dr)
            if 0 <= t[1] < self.H and t not in occ:
                nop = (own_p - {p}) | ({t} if t[1] != last else set())
                if legal_after(nop, en_p):
                    if t[1] == last: res.append((mk(own_k, own_p - {p}, en_p, None), 'promo', t))
                    else: res.append((mk(own_k, nop, en_p, None), 'move', None))
                if r == start:
                    t2 = (f, r + 2 * dr)
                    if t2 not in occ:
                        nop2 = (own_p - {p}) | {t2}
                        if legal_after(nop2, en_p): res.append((mk(own_k, nop2, en_p, (f, r + dr)), 'move', None))
            for tt in self.pawn_att(side, p):
                if tt in en_p:
                    nen = en_p - {tt}
                    if legal_after(None, nen):
                        if tt[1] == last: res.append((mk(own_k, own_p - {p}, nen, None), 'promo', tt))
                        else: res.append((mk(own_k, (own_p - {p}) | {tt}, nen, None), 'move', None))
                elif ep is not None and tt == ep and tt not in occ:
                    victim = (tt[0], tt[1] - dr)
                    if victim in en_p:
                        nen = en_p - {victim}
                        if legal_after(None, nen):
                            res.append((mk(own_k, (own_p - {p}) | {tt}, nen, None), 'move', None))
        return res
    def queen_safe(self, st, q):
        """after A promotes on q (state st has pawn removed), does D have NO legal capture of q?"""
        D = self.D
        wk, bk, wp, bp, ep = st
        dk, ak = (wk, bk) if D == 'w' else (bk, wk)
        dp, ap = (wp, bp) if D == 'w' else (bp, wp)
        # D king captures q
        if q in self.nbset(dk):
            if q not in self.nbset(ak) and not any(q in self.pawn_att(self.A, p) for p in ap):
                return False
        for p in dp:
            if q in self.pawn_att(D, p):
                # pawn capture legal if D king not attacked by A king/pawns after
                if not self.attacked(dk, self.A, ak, ap):
                    return False
        return True
    # win(st, side_to_move, t, k): can A win within t A-moves. side=='D' => D to move.
    def winD(self, st, t, k):
        key = ('D', st, t, k)
        if key in self.memo: return self.memo[key]
        D = self.D
        opts = []
        chk = self.in_check(D, st)
        for ns, kind, q in self.moves(D, st):
            if kind == 'promo': return self._s(key, False)   # D promotes: failure for A
            opts.append(ns)
        passes = False
        if not chk and (k is None or k > 0):
            passes = True
        if not opts and not passes:
            if chk: return self._s(key, self.mate)       # mated D -> A wins (if mate rule on)
            return self._s(key, False)                   # stalemate of D: failure
        if t <= 0: return self._s(key, False)
        ok = True
        for ns in opts:
            if not self.winA(ns, t, k): ok = False; break
        if ok and passes:
            ns = st[:4] + (None,)
            if not self.winA(ns, t, None if k is None else k - 1): ok = False
        return self._s(key, ok)
    def winA(self, st, t, k):
        key = ('A', st, t, k)
        if key in self.memo: return self.memo[key]
        A = self.A
        if t <= 0: return self._s(key, False)
        ms = self.moves(A, st, confineK=self.confine)
        if not ms: return self._s(key, False)
        for ns, kind, q in ms:
            if kind == 'promo':
                if (not self.queen) or self.queen_safe(ns, q):
                    return self._s(key, True)
                continue
            # mate of D?
            if self.mate and self.in_check(self.D, ns) and not self.moves(self.D, ns):
                return self._s(key, True)
            if self.winD(ns, t - 1, k): return self._s(key, True)
        return self._s(key, False)
    def _s(self, key, v):
        self.memo[key] = v; return v
    def T(self, st, k, tmax=24):
        for t in range(1, tmax + 1):
            if self.winD(st, t, k): return t
        return None

def parse(s):
    """'Kg4 ka4 pa5' style, files a.., ranks 1.."""
    wk = bk = None; wp = set(); bp = set()
    for tok in s.split():
        c, f, r = tok[0], ord(tok[1]) - 97, int(tok[2:]) - 1
        if c == 'K': wk = (f, r)
        elif c == 'k': bk = (f, r)
        elif c == 'P': wp.add((f, r))
        elif c == 'p': bp.add((f, r))
    return (wk, bk, frozenset(wp), frozenset(bp), None)
