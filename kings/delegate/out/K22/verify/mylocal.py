# Independent referee implementation of the local game L_T(Q_Z) of LOOPY Definition 2.6 (k = infinity).
# White = s-bar (promotes at rank H, king confined to files 0..fzhi), Black = s (may pass).
# Written from the definition only; does not use K22's scripts. Requires H >= 5.
import sys

class Game:
    def __init__(self, board, W, H, fzhi, queen_clause=True):
        assert H >= 5
        self.cyl = (board == 'cyl'); self.Wd = W; self.H = H; self.fzhi = fzhi; self.qc = queen_clause
        self.memo = {}
        self.kn = {}
        for f in range(W):
            for r in range(1, H + 1):
                out = []
                for df in (-1, 0, 1):
                    for dr in (-1, 0, 1):
                        if df == 0 and dr == 0: continue
                        rr = r + dr
                        if not (1 <= rr <= H): continue
                        ff = self.nf(f + df)
                        if ff is None: continue
                        out.append((ff, rr))
                self.kn[(f, r)] = frozenset(out)
    def nf(self, f):
        if self.cyl: return f % self.Wd
        return f if 0 <= f < self.Wd else None
    def att_by_white(self, sq, wp, wk):
        f, r = sq
        for df in (-1, 1):
            g = self.nf(f + df)
            if g is not None and (g, r - 1) in wp: return True
        return sq in self.kn[wk]
    def att_by_black(self, sq, bp, bk):
        f, r = sq
        for df in (-1, 1):
            g = self.nf(f + df)
            if g is not None and (g, r + 1) in bp: return True
        return sq in self.kn[bk]
    # state = (wp, bp, wk, bk, ep) ; ep = target square of a pending e.p. capture (for the side to move)
    def black_moves(self, st):
        """list of successor states; 'PROMO' = promotion by black; returns (list, incheck). Pass included when legal."""
        wp, bp, wk, bk, ep = st
        H = self.H
        incheck = self.att_by_white(bk, wp, wk)
        occ = set(wp) | set(bp) | {wk, bk}
        cand = []   # (nwp, nbp, nbk, nep, promo)
        for t in self.kn[bk]:
            if t in bp: continue
            cand.append((wp - {t}, bp, t, None, False))
        for (f, r) in bp:
            rest = bp - {(f, r)}
            tr = r - 1
            if (f, tr) not in occ:
                if tr == 1: cand.append((wp, rest, bk, None, True))
                else:
                    cand.append((wp, rest | {(f, tr)}, bk, None, False))
                    if r == H - 1 and (f, r - 2) not in occ:
                        cand.append((wp, rest | {(f, r - 2)}, bk, (f, tr), False))
            for df in (-1, 1):
                g = self.nf(f + df)
                if g is None: continue
                tgt = (g, tr)
                if tgt in wp:
                    if tr == 1: cand.append((wp - {tgt}, rest, bk, None, True))
                    else: cand.append((wp - {tgt}, rest | {tgt}, bk, None, False))
                elif ep is not None and tgt == ep and (g, tr + 1) in wp:
                    cand.append((wp - {(g, tr + 1)}, rest | {tgt}, bk, None, False))
        out = []
        for nwp, nbp, nbk, nep, promo in cand:
            if self.att_by_white(nbk, nwp, wk): continue   # own king in check afterwards
            out.append('PROMO' if promo else (nwp, nbp, wk, nbk, nep))
        if not incheck: out.append((wp, bp, wk, bk, None))
        return out, incheck
    def white_moves(self, st):
        """successor states; 'WIN' = winning promotion, 'LOSE' = unsafe promotion (queen clause)."""
        wp, bp, wk, bk, ep = st
        H = self.H
        occ = set(wp) | set(bp) | {wk, bk}
        cand = []   # (nwp, nbp, nwk, nep, promo_square)
        for t in self.kn[wk]:
            if t[0] > self.fzhi or t in wp: continue
            cand.append((wp, bp - {t}, t, None, None))
        for (f, r) in wp:
            rest = wp - {(f, r)}
            tr = r + 1
            if (f, tr) not in occ:
                if tr == H: cand.append((rest, bp, wk, None, (f, tr)))
                else:
                    cand.append((rest | {(f, tr)}, bp, wk, None, None))
                    if r == 2 and (f, 4) not in occ:
                        cand.append((rest | {(f, 4)}, bp, wk, (f, 3), None))
            for df in (-1, 1):
                g = self.nf(f + df)
                if g is None: continue
                tgt = (g, tr)
                if tgt in bp:
                    if tr == H: cand.append((rest, bp - {tgt}, wk, None, tgt))
                    else: cand.append((rest | {tgt}, bp - {tgt}, wk, None, None))
                elif ep is not None and tgt == ep and (g, tr - 1) in bp:
                    cand.append((rest | {tgt}, bp - {(g, tr - 1)}, wk, None, None))
        out = []
        for nwp, nbp, nwk, nep, psq in cand:
            if self.att_by_black(nwk, nbp, bk): continue
            if psq is None: out.append((nwp, nbp, nwk, bk, nep))
            else:
                if not self.qc: out.append('WIN'); continue
                # black king is the only piece that can capture a queen on the last rank
                if psq in self.kn[bk] and not self.att_by_white(psq, nwp, nwk): out.append('LOSE')
                else: out.append('WIN')
        return out
    def W(self, st, t):     # white to move, t white moves left
        if t <= 0: return False
        key = (st, t, 1)
        v = self.memo.get(key)
        if v is not None: return v
        ok = False
        for m in self.white_moves(st):
            if m == 'WIN' or (m != 'LOSE' and self.B(m, t - 1)): ok = True; break
        self.memo[key] = ok
        return ok
    def B(self, st, t):     # black to move; white has t moves left afterwards
        key = (st, t, 0)
        v = self.memo.get(key)
        if v is not None: return v
        ms, incheck = self.black_moves(st)
        if not ms: r = incheck      # mated: white wins
        else:
            r = True
            for m in ms:
                if m == 'PROMO' or not self.W(m, t): r = False; break
        self.memo[key] = r
        return r
    def minT(self, wp, bp, wk, bk, ep=None, tmax=8):
        st = (frozenset(wp), frozenset(bp), wk, bk, ep)
        for T in range(1, tmax + 1):
            if self.B(st, T): return T
        return None
    def black_replies(self, wp, bp, wk, bk, T, ep=None):
        st = (frozenset(wp), frozenset(bp), wk, bk, ep)
        ms, _ = self.black_moves(st)
        res = []
        for m in ms:
            res.append((m if m == 'PROMO' else self.descr(st, m), m != 'PROMO' and self.W(m, T)))
        return res
    def descr(self, st, m):
        wp, bp, wk, bk, ep = st
        if m[1] == bp and m[3] == bk: return 'pass'
        if m[3] != bk: return 'K' + 'abcdefgh'[m[3][0]] + str(m[3][1])
        return 'pawn:' + str(sorted(bp - m[1])) + '->' + str(sorted(m[1] - bp))

FILES = 'abcdefgh'
def parse(s):
    wp = set(); bp = set(); wk = bk = None
    for tok in s.split():
        if tok in ('b', 'w', '-'): break
        p = tok[0]; f = FILES.index(tok[1]); r = int(tok[2:])
        if p == 'K': wk = (f, r)
        elif p == 'k': bk = (f, r)
        elif p == 'P': wp.add((f, r))
        elif p == 'p': bp.add((f, r))
    return wp, bp, wk, bk

if __name__ == '__main__':
    board, W, H, fzhi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    for line in sys.stdin.read().splitlines():
        if not line.strip(): continue
        wp, bp, wk, bk = parse(line)
        for qc in (False, True):
            g = Game(board, W, H, fzhi, qc)
            T = g.minT(wp, bp, wk, bk, tmax=10)
            print(line, '| queen_clause=%s' % qc, '| minT =', T)
            if T:
                print('   black replies (white wins in <=T?):', g.black_replies(wp, bp, wk, bk, T))
