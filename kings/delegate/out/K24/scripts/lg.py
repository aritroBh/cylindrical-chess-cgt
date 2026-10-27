"""K24: the local game L_T(Q_Z) of LOOPY Definition 2.6 (condition (L1)), computed exactly on the explicit graph.

Roles: s = the side that made the Z-move m (it is to move at Q), s-bar = the side that replied r and wants to
promote.  Rules implemented (Definition 2.6, items 1-5):
  1. the first promotion ends the game; a promotion by s is a win for s (failure for s-bar); a promotion by s-bar wins
     iff no legal move of s captures the new queen (queen clause; "P" variant: every promotion by s-bar wins);
  2. s may pass whenever it is not in check (unlimited); s-bar may not pass;
  3. s-bar's king may only step onto squares of the files FZ; its pawns are not restricted;
  4. s in check without a legal move is mated: win for s-bar; s-bar with no permitted move: failure;
  5. s-bar must win within its first T moves (promotion as in 1, or a move that mates s).
T_min = the least T for which s-bar wins from Q_Z (s to move).  Also: (L3_F) of Definition 2.6, checked along every line in
which s-bar plays only winning moves (given T = T_min).
Pawns in Q_Z must not stand on their start rank (no double steps / e.p. are implemented; asserted).

Usage as a module: lg.solve(board, qz, s_color, FZ, queen_clause) -> (Tmin or None, info)
"""
import sys
from functools import lru_cache

class B:
    def __init__(self, W, H, wrap):
        self.W, self.H, self.wrap = W, H, wrap
    def sq(self, f, r):
        if r < 0 or r >= self.H: return None
        if self.wrap: f %= self.W
        elif f < 0 or f >= self.W: return None
        return r * self.W + f
    def f(self, s): return s % self.W
    def r(self, s): return s // self.W
    def adj(self, a, b):
        if a == b: return True
        if abs(self.r(a) - self.r(b)) > 1: return False
        d = abs(self.f(a) - self.f(b))
        if self.wrap: d = min(d, self.W - d)
        return d <= 1
    def kingsteps(self, s):
        out = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df or dr:
                    t = self.sq(self.f(s) + df, self.r(s) + dr)
                    if t is not None and t != s and t not in out: out.append(t)
        return out

def parse(board, text):
    """'Kh5 Pa4 kb4 pa5' -> (wk, bk, wp tuple, bp tuple)"""
    wk = bk = None; wp = []; bp = []
    for t in text.split():
        s = board.sq(ord(t[1]) - 97, int(t[2:]) - 1)
        c = t[0]
        if c == 'K': wk = s
        elif c == 'k': bk = s
        elif c == 'P': wp.append(s)
        elif c == 'p': bp.append(s)
    return (wk, bk, tuple(sorted(wp)), tuple(sorted(bp)))

def name(board, s): return "abcdefgh"[board.f(s)] + str(board.r(s) + 1)

class Game:
    def __init__(self, board, s_white, FZ, queen_clause=True):
        self.b = board; self.sw = s_white; self.FZ = set(FZ); self.qc = queen_clause
        # colours: index 0 white, 1 black.  role s -> colour 0 if s_white else 1
        self.cs = 0 if s_white else 1; self.cb = 1 - self.cs
    def dir(self, c): return 1 if c == 0 else -1
    def last(self, c): return self.b.H - 1 if c == 0 else 0
    def start(self, c): return 1 if c == 0 else self.b.H - 2

    # state: (kings(2), pawns(2), side) with colour indexing; side = colour to move
    def pawn_attacks(self, c, p, t):
        r0 = self.b.r(t) - self.dir(c)
        if r0 != self.b.r(p): return False
        for df in (-1, 1):
            if self.b.sq(self.b.f(t) + df, r0) == p: return True
        return False
    def attacked_by_pawns(self, c, pawns, t):
        return any(self.pawn_attacks(c, p, t) for p in pawns)
    def in_check(self, k, p, c):  # king of colour c in check?
        return self.attacked_by_pawns(1 - c, p[1 - c], k[c])

    def moves(self, k, p, c, confine=False):
        """legal non-promoting moves of colour c as (newk, newp, text), and promotions as (square, text, capture?)"""
        b = self.b; e = 1 - c; d = self.dir(c); out = []; promos = []
        for t in b.kingsteps(k[c]):
            if confine and b.f(t) not in self.FZ: continue
            if t in p[c] or b.adj(t, k[e]): continue
            ep = tuple(x for x in p[e] if x != t)
            if self.attacked_by_pawns(e, ep, t): continue
            nk = list(k); nk[c] = t; np_ = [p[0], p[1]]; np_[e] = ep
            out.append((tuple(nk), tuple(np_), "K" + name(b, k[c]) + name(b, t)))
        occ = set(k) | set(p[0]) | set(p[1])
        for s in p[c]:
            one = b.sq(b.f(s), b.r(s) + d)
            targets = []
            if one is not None and one not in occ: targets.append((one, False))
            if b.r(s) == self.start(c) and one is not None and one not in occ:
                two = b.sq(b.f(s), b.r(s) + 2 * d)
                if two is not None and two not in occ and b.r(two) != self.last(c):
                    # double step: allowed; an e.p. right would matter only if an enemy pawn stands beside `two`
                    for df in (-1, 1):
                        q = b.sq(b.f(two) + df, b.r(two))
                        assert q is None or q not in p[e], "e.p. not implemented"
                    targets.append((two, False))
            for df in (-1, 1):
                t = b.sq(b.f(s) + df, b.r(s) + d)
                if t is not None and t in p[e]: targets.append((t, True))
            for t, cap in targets:
                np_ = [list(p[0]), list(p[1])]
                if cap: np_[e].remove(t)
                np_[c].remove(s)
                promo = (b.r(t) == self.last(c))
                if not promo: np_[c].append(t)
                np2 = (tuple(sorted(np_[0])), tuple(sorted(np_[1])))
                if self.attacked_by_pawns(e, np2[e], k[c]): continue
                if promo: promos.append((t, "P" + name(b, s) + ("x" if cap else "") + name(b, t) + "=", np2))
                else: out.append((k, np2, "P" + name(b, s) + ("x" if cap else "") + name(b, t)))
        return out, promos

    def queen_capturable(self, k, np_, t, c_prom):
        """new queen of colour c_prom on t (pawn removed already in np_); can the other side capture it at once?"""
        b = self.b; e = 1 - c_prom
        # e's king captures: adjacent, t not protected by c_prom king/pawns (queen removed after capture; own pawns protect)
        if b.adj(k[e], t) and not b.adj(k[c_prom], t) and not self.attacked_by_pawns(c_prom, np_[c_prom], t):
            return True
        # e's pawn captures: a pawn of e attacks t; legality: after capture e's king must not be attacked by remaining c_prom pawns
        for q in np_[e]:
            if self.pawn_attacks(e, q, t):
                np2 = [list(np_[0]), list(np_[1])]; np2[e].remove(q); np2[e].append(t)
                if not self.attacked_by_pawns(c_prom, tuple(np2[c_prom]), k[e]): return True
        return False

    # ---- exact solution on the explicit graph ----
    def solve(self, k0, p0, want_l3=True):
        cs, cb = self.cs, self.cb
        # nodes: ('S', k, p) s to move; ('B', k, p) s-bar to move.  Edges and immediate outcomes.
        sn = {}; bn = {}
        stack = [('S', k0, p0)]
        sopts = {}; bopts = {}  # node -> list of successor nodes; plus flags
        sflag = {}; bflag = {}
        seen = set()
        while stack:
            node = stack.pop()
            if node in seen: continue
            seen.add(node)
            typ, k, p = node
            if typ == 'S':
                mv, pr = self.moves(k, p, cs)
                chk = self.in_check(k, p, cs)
                if pr:      # s promotes: failure for s-bar; modelled as an option that loses for s-bar
                    sflag[node] = 'spromo'
                succ = [('B', nk, np_) for nk, np_, _ in mv]
                if not chk: succ.append(('B', k, p))   # pass
                sopts[node] = succ
                if not mv and not pr and chk: sflag[node] = sflag.get(node, '') + 'mated'
                for s_ in succ: stack.append(s_)
            else:
                mv, pr = self.moves(k, p, cb, confine=True)
                win_now = False
                for t, txt, np_ in pr:
                    if (not self.qc) or not self.queen_capturable(k, np_, t, cb): win_now = True
                succ = []
                for nk, np_, txt in mv:
                    # does the move mate s?
                    child = ('S', nk, np_)
                    succ.append(child)
                bopts[node] = succ
                bflag[node] = win_now
                for s_ in succ: stack.append(s_)
        # mated S-nodes: s in check, no legal move, no promotion
        def s_has_move(node):
            typ, k, p = node
            mv, pr = self.moves(k, p, cs)
            return bool(mv or pr)
        Ws = {}  # node -> min T with s-bar winning from S-node  (T = number of s-bar moves)
        Wb = {}
        mated = {n for n in sopts if 'mated' in sflag.get(n, '')}
        for n in mated: Ws[n] = 0
        T = 0
        while True:
            T += 1
            changed = False
            for n, succ in bopts.items():
                if n in Wb: continue
                if bflag[n] or any(c in Ws and Ws[c] <= T - 1 for c in succ):
                    Wb[n] = T; changed = True
            for n, succ in sopts.items():
                if n in Ws: continue
                if 'spromo' in sflag.get(n, ''): continue
                if all(c in Wb and Wb[c] <= T for c in succ):
                    Ws[n] = T; changed = True
            if not changed: break
        root = ('S', k0, p0)
        Tmin = Ws.get(root)
        info = {"nodes": len(seen)}
        if Tmin is not None and want_l3:
            info["l3f"] = self.check_l3f(root, Tmin, Ws, Wb, sopts, bopts, bflag, sflag)
        return Tmin, info

    def check_l3f(self, root, T, Ws, Wb, sopts, bopts, bflag, sflag):
        """every s-node reached before the win, with s-bar playing only winning moves (given T): s has a legal Z-pawn move or
        a legal king move onto a square of FZ.  Returns (ok, number of s-nodes visited, first violation or None)."""
        cs = self.cs; b = self.b
        visited = set(); stack = [(root, T)]; viol = None; n_s = 0; stale = [0]
        while stack:
            node, t = stack.pop()
            if (node, t) in visited: continue
            visited.add((node, t))
            typ, k, p = node
            if typ == 'S':
                if 'mated' in sflag.get(node, ''): continue
                n_s += 1
                mv, pr = self.moves(k, p, cs)
                has = any((txt[0] == 'P') or (b.f(nk[cs]) in self.FZ) for nk, np_, txt in mv)
                if not has and viol is None: viol = (node, t)
                if not (mv or pr) and not self.in_check(k, p, cs): stale[0] += 1
                for c in sopts[node]: stack.append((c, t))
            else:
                for c in bopts[node]:
                    if c in Ws and Ws[c] <= t - 1: stack.append((c, t - 1))
        return (viol is None, n_s, viol, stale[0])

def build_qz(board, root, s_white, FZ, qc=True, reply_square=None, verbose=True):
    """For each legal non-promoting move m of s from `root` (a bare group with s to move) and the reply r = s-bar's king
    capturing on reply_square, solve the local game."""
    g = Game(board, s_white, FZ, qc)
    k, p = (lambda x: ((x[0], x[1]), (x[2], x[3])))(parse(board, root))
    cs, cb = g.cs, g.cb
    results = []
    mv, pr = g.moves(k, p, cs)
    for nk, np_, txt in mv:
        # reply: s-bar king captures on reply_square
        rep, rpro = g.moves(nk, np_, cb)
        rr = [(k2, p2, t2) for k2, p2, t2 in rep if t2.startswith("K") and t2.endswith(reply_square)]
        if not rr:
            results.append((txt, None, "reply not legal")); continue
        k2, p2, t2 = rr[0]
        T, info = g.solve(k2, p2)
        results.append((txt + " " + t2, T, info))
    return results

if __name__ == "__main__":
    pass
