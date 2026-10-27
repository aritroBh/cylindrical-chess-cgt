#!/usr/bin/env python3
"""
Independent check of the tables written by twist.c (-d DIR).

Geometry here is built a different way from twist.c: not from the cover plane, but by parallel
transport over the four edge neighbours.  A walker carries a frame (fx, fy) that records whether the
original file/rank axes have been reversed by the gluings crossed so far.  A diagonal step is a file
step and a rank step, a knight jump is three steps, in every order (all orders must agree), and a
slider ray repeats one step with the frame carried along.  Rules (legality, check, captures, stalemate)
are applied by brute force on an explicit board.  Then random positions (biased to board edges) are
checked against the Bellman equations using the stored child values:
    W = 1 + min over white moves of B(child);   B = max over black moves of W(child) (0 mated).

usage:  verify.py geom mat dumpdir [nsample] [seed]       (ray rule 0 = geodesic only)
        verify.py geom geometry geomfile                 (compare move tables with twist -G output)
"""
import sys, random
import numpy as np

TCH = "QRBN"
ILLEGAL, UNSET, MAXVAL = 255, 254, 250


class Geom:
    def __init__(self, name):
        self.name = name
        self.flipR_on_file = name in ("mobius", "klein", "rp2")
        self.file_wrap = name != "plane"
        self.rank_wrap = name in ("torus", "klein", "rp2")
        self.rank_flips_file = name == "rp2"
        self.build()

    # one orthogonal step in the ORIGINAL frame: axis 0 = file, 1 = rank, sign +-1
    def orth(self, st, axis, sign):
        f, r, fx, fy = st
        if axis == 0:
            ls = sign * fx
            nf = f + ls
            if 0 <= nf < 8:
                return (nf, r, fx, fy)
            if not self.file_wrap:
                return None
            nf %= 8
            if self.flipR_on_file:
                return (nf, 7 - r, fx, -fy)
            return (nf, r, fx, fy)
        ls = sign * fy
        nr = r + ls
        if 0 <= nr < 8:
            return (f, nr, fx, fy)
        if not self.rank_wrap:
            return None
        nr %= 8
        if self.rank_flips_file:
            return (7 - f, nr, -fx, fy)
        return (f, nr, fx, fy)

    def walk(self, st, steps):
        for axis, sign in steps:
            st = self.orth(st, axis, sign)
            if st is None:
                return None
        return st

    def multi(self, st, orders):
        """All step orders must agree (cell and frame); returns the common result or raises."""
        res = [self.walk(st, o) for o in orders]
        if any(x != res[0] for x in res):
            raise SystemExit("path-dependent move at %s: %s" % (st, res))
        return res[0]

    def build(self):
        DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.king = [[-1] * 8 for _ in range(64)]
        self.knight = [set() for _ in range(64)]
        self.rays = [[[] for _ in range(8)] for _ in range(64)]
        for s in range(64):
            st0 = (s & 7, s >> 3, 1, 1)
            for d, (a, b) in enumerate(DIRS):
                st = self.diag_or_orth(st0, a, b)
                if st is not None and st[0] + 8 * st[1] != s:
                    self.king[s][d] = st[0] + 8 * st[1]
                # ray
                seen = {s}
                cur = st0
                out = []
                while True:
                    nx = self.diag_or_orth(cur, a, b)
                    if nx is None:
                        break
                    t = nx[0] + 8 * nx[1]
                    if t in seen:
                        break
                    seen.add(t)
                    out.append(t)
                    cur = nx
                self.rays[s][d] = out
            for a, b in [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]:
                sa = 1 if a > 0 else -1
                sb = 1 if b > 0 else -1
                x = [(0, sa)] * abs(a)
                y = [(1, sb)] * abs(b)
                orders = []
                # all interleavings of the file steps and rank steps
                n = abs(a) + abs(b)
                import itertools
                for pos in itertools.combinations(range(n), abs(a)):
                    seq, xi, yi = [], 0, 0
                    for i in range(n):
                        if i in pos:
                            seq.append(x[xi]); xi += 1
                        else:
                            seq.append(y[yi]); yi += 1
                    orders.append(seq)
                st = self.multi(st0, orders)
                if st is not None and st[0] + 8 * st[1] != s:
                    self.knight[s].add(st[0] + 8 * st[1])

    def diag_or_orth(self, st, a, b):
        if a == 0:
            return self.orth(st, 1, b)
        if b == 0:
            return self.orth(st, 0, a)
        return self.multi(st, [[(0, a), (1, b)], [(1, b), (0, a)]])


def sqname(s):
    return "abcdefgh"[s & 7] + str(1 + (s >> 3))


class Verifier:
    def __init__(self, geom, dumpdir):
        self.g = Geom(geom)
        self.gname = geom
        self.dir = dumpdir
        self.cache = {}
        self.kadj = [set(x for x in self.g.king[s] if x >= 0) for s in range(64)]

    def table(self, mat):
        if mat not in self.cache:
            W = np.fromfile("%s/%s_%s.W" % (self.dir, self.gname, mat), dtype=np.uint8)
            B = np.fromfile("%s/%s_%s.B" % (self.dir, self.gname, mat), dtype=np.uint8)
            self.cache[mat] = (W, B)
        return self.cache[mat]

    # ---- rules -------------------------------------------------------------------------------
    def piece_moves(self, ty, sq, occ):
        """squares a piece can move to / attack; sliders stop at first occupied square (included)."""
        if ty == 3:
            return list(self.g.knight[sq])
        dirs = range(4, 8) if ty == 2 else (range(0, 4) if ty == 1 else range(0, 8))
        out = []
        for d in dirs:
            for t in self.g.rays[sq][d]:
                out.append(t)
                if t in occ:
                    break
        return out

    def attacked(self, sq, wk, pieces, bk):
        """is square sq attacked by the white men, with white men and a black king on bk as blockers"""
        occ = {wk, bk} | {p for _, p in pieces}
        if sq in self.kadj[wk]:
            return True
        for ty, p in pieces:
            if sq in self.piece_moves(ty, p, occ):
                return True
        return False

    def idx(self, np_, wk, ps, bk):
        i = wk
        for p in ps:
            i = i * 64 + p
        return i * 64 + bk

    def w_expect(self, mat, wk, pieces, bk):
        """expected (legal, value) of the white-to-move position; value None = no win"""
        sqs = [wk, bk] + [p for _, p in pieces]
        if len(set(sqs)) != len(sqs) or bk in self.kadj[wk]:
            return (False, None)
        occ = set(sqs)
        for ty, p in pieces:
            if bk in self.piece_moves(ty, p, occ):
                return (False, None)
        W, B = self.table(mat)
        best = None
        occ = set(sqs)
        # white king moves
        cands = []
        for t in self.g.king[wk]:
            if t >= 0 and t not in occ and t not in self.kadj[bk]:
                cands.append((t, pieces))
        for i, (ty, p) in enumerate(pieces):
            for t in self.piece_moves(ty, p, occ):
                if t in occ:
                    continue
                np_ = list(pieces)
                np_[i] = (ty, t)
                cands.append((None, np_, t))
        vals = []
        for c in cands:
            if len(c) == 2:
                nwk, np_ = c
                ps = [p for _, p in np_]
                v = B[self.idx(len(np_), nwk, ps, bk)]
            else:
                _, np_, t = c
                ps = [p for _, p in np_]
                v = B[self.idx(len(np_), wk, ps, bk)]
            vals.append(int(v))
        fin = [v for v in vals if v < MAXVAL]
        if fin:
            best = 1 + min(fin)
        return (True, best)

    def b_expect(self, mat, wk, pieces, bk):
        """expected (legal, value) of the black-to-move position; None value = not lost"""
        sqs = [wk, bk] + [p for _, p in pieces]
        if len(set(sqs)) != len(sqs) or bk in self.kadj[wk]:
            return (False, None)
        W, B = self.table(mat)
        incheck = any(bk in self.piece_moves(ty, p, set(sqs)) for ty, p in pieces)
        moves = []
        for s in self.g.king[bk]:
            if s < 0 or s == wk:
                continue
            rem = [(ty, p) for ty, p in pieces if p != s]
            if s in self.kadj[wk]:
                continue
            occ = {wk, s} | {p for _, p in rem}
            if any(s in self.piece_moves(ty, p, occ) for ty, p in rem):
                continue
            moves.append((s, rem))
        if not moves:
            return (True, 0 if incheck else None)
        vals = []
        for s, rem in moves:
            if len(rem) == len(pieces):
                v = W[self.idx(len(pieces), wk, [p for _, p in pieces], s)]
            elif len(rem) == 0:
                v = UNSET
            else:
                sub = "K" + TCH[rem[0][0]] + "K"
                Ws, _ = self.table(sub)
                v = Ws[self.idx(1, wk, [rem[0][1]], s)]
            vals.append(int(v))
        if any(v >= MAXVAL for v in vals):
            return (True, None)
        return (True, max(vals))


def stored(v):
    return None if v >= MAXVAL else int(v)


def verify_tables(geom, mat, dumpdir, nsample, seed):
    rnd = random.Random(seed)
    V = Verifier(geom, dumpdir)
    types = [TCH.index(c) for c in mat]
    name = "K" + mat + "K"
    W, B = V.table(name)
    edge = [s for s in range(64) if (s & 7) in (0, 7) or (s >> 3) in (0, 7)]

    def rsq():
        return rnd.choice(edge) if rnd.random() < 0.5 else rnd.randrange(64)

    bad = 0
    chk = 0
    cnt = {"Wlegal": 0, "Wwon": 0, "Blegal": 0, "Bfinite": 0, "Bmate": 0, "Bcapture": 0}
    for _ in range(nsample):
        wk = rsq(); bk = rsq()
        pieces = [(t, rsq()) for t in types]
        ps = [p for _, p in pieces]
        i = V.idx(len(types), wk, ps, bk)
        legal, val = V.w_expect(name, wk, pieces, bk)
        sw = int(W[i])
        cnt["Wlegal"] += legal
        cnt["Wwon"] += (val is not None)
        if (sw != ILLEGAL) != legal or (legal and stored(sw) != val):
            bad += 1
            print("W MISMATCH", name, wk, pieces, bk, "stored", sw, "expected", legal, val)
        legal, val = V.b_expect(name, wk, pieces, bk)
        sb = int(B[i])
        cnt["Blegal"] += legal
        cnt["Bfinite"] += (val is not None)
        cnt["Bmate"] += (val == 0)
        if (sb != ILLEGAL) != legal or (legal and stored(sb) != val):
            bad += 1
            print("B MISMATCH", name, wk, pieces, bk, "stored", sb, "expected", legal, val)
        chk += 1
        if bad > 20:
            break
    print("VERIFY geom=%s mat=%s sampled=%d mismatches=%d  (W legal %d, W won %d, B legal %d, B lost %d, B mated %d)" % (
        geom, name, chk, bad, cnt["Wlegal"], cnt["Wwon"], cnt["Blegal"], cnt["Bfinite"], cnt["Bmate"]))
    return bad


def compare_geometry(geom, path):
    g = Geom(geom)
    K, N, R = {}, {}, {}
    for line in open(path):
        p = line.split()
        if p[0] == "K":
            K[int(p[1])] = list(map(int, p[2:]))
        elif p[0] == "N":
            N[int(p[1])] = set(map(int, p[2:]))
        else:
            R[(int(p[1]), int(p[2]))] = list(map(int, p[3:]))
    bad = 0
    for s in range(64):
        if K[s] != g.king[s]:
            bad += 1; print("king", s, K[s], g.king[s])
        if N[s] != g.knight[s]:
            bad += 1; print("knight", s, N[s], g.knight[s])
        for d in range(8):
            if R[(s, d)] != g.rays[s][d]:
                bad += 1; print("ray", s, d, R[(s, d)], g.rays[s][d])
    print("GEOMETRY geom=%s differences=%d" % (geom, bad))
    return bad


if __name__ == "__main__":
    geom, mat = sys.argv[1], sys.argv[2]
    if mat == "geometry":
        sys.exit(1 if compare_geometry(geom, sys.argv[3]) else 0)
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    sys.exit(1 if verify_tables(geom, mat, sys.argv[3], n, seed) else 0)
