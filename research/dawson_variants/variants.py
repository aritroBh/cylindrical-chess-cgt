"""Independent Python solver for Dawson's chess on new surfaces and wider boards.

This is a second implementation, written independently of research/dawson_variants/variants.c,
used to cross-check the C results (CHECKED-2).  It deliberately uses a different
representation (immutable nested tuples of piece codes + a dict memo) from the C program
(bit masks + open-addressed hash table).

Piece codes: 0 empty, 1 White up, 2 White down, 3 Black up, 4 Black down.
A "direction" of +1 means the pawn moves toward higher ranks.

Surfaces
--------
flat     n x R, files do not wrap
cyl      n x R, files wrap
torus    n x R, files wrap and ranks wrap
mobiusM  files wrap, the seam is twisted.  Convention M: a pawn that crosses the seam
          steps to rank r+d and its direction reverses afterwards ("a pawn crossing the
          seam becomes the other colour's direction").
mobiusT  files wrap, the seam is twisted.  Convention T: the board is the quotient of the
          rectangle by (0,r) ~ (n-1,R-1-r); a pawn carries a frame bit (encoded in its
          direction) and the seam target row is R-2-r rather than r+d.

Run:  python -m research.dawson_variants.variants            # run the cross-check suite
      python -m research.dawson_variants.variants cyl 8 3     # one configuration
"""

import sys
from functools import lru_cache

E, WUP, WDN, BUP, BDN = 0, 1, 2, 3, 4

WHITE = 0
BLACK = 1


class Geometry:
    """Move generation on one surface."""

    name = "?"

    def __init__(self, files, ranks):
        self.files = files
        self.ranks = ranks

    # --- file adjacency -------------------------------------------------
    def file_neighbours(self, f):
        out = []
        for d in (-1, 1):
            g = f + d
            if self.wraps_files():
                g %= self.files
            if 0 <= g < self.files and g not in out:
                out.append(g)
        return out

    def wraps_files(self):
        return False

    def wraps_ranks(self):
        return False

    def twisted(self):
        return False

    def crosses_seam(self, f, g):
        if not self.twisted():
            return False
        return (f == 0 and g == self.files - 1) or (f == self.files - 1 and g == 0)

    # --- the start position ---------------------------------------------
    def start(self):
        rows = []
        for _ in range(self.files):
            col = [E] * self.ranks
            col[0] = WUP
            col[self.ranks - 1] = BDN
            rows.append(tuple(col))
        return tuple(rows)

    # --- move generation ------------------------------------------------
    def moves(self, pos, side):
        """Return (successors, is_capture).  Captures are compulsory."""
        caps, pushes = [], []
        for f in range(self.files):
            col = pos[f]
            for r in range(self.ranks):
                piece = col[r]
                if piece == E:
                    continue
                if side == WHITE and piece not in (WUP, WDN):
                    continue
                if side == BLACK and piece not in (BUP, BDN):
                    continue
                for (g, rr, np, is_capture) in self._targets(pos, f, r, piece, side):
                    occupied = pos[g][rr]
                    if is_capture:
                        if side == WHITE:
                            ok = occupied in (BUP, BDN)
                        else:
                            ok = occupied in (WUP, WDN)
                        if ok:
                            caps.append(self._apply(pos, f, r, g, rr, np))
                    elif occupied == E:
                        pushes.append(self._apply(pos, f, r, g, rr, np))
        if caps:
            return list(dict.fromkeys(caps)), True
        return list(dict.fromkeys(pushes)), False

    def _targets(self, pos, f, r, piece, side):
        """Yield (file, rank, new_piece_code, is_capture)."""
        up = piece in (WUP, BUP)
        if side == WHITE:
            local = +1 if piece in (WUP, WDN) else -1
        else:
            local = -1 if piece in (BDN, BUP) else +1
        direction = +1 if up else -1

        if self.twisted():
            # frame 0: local rank == r ; frame 1: local rank == R-1-r
            frame = 0 if piece in (WUP, BDN) else 1
            lam = r if frame == 0 else self.ranks - 1 - r
            lam2 = lam + local
            if lam2 < 0 or lam2 >= self.ranks:
                return
            # push (same file, no seam)
            rr = lam2 if frame == 0 else self.ranks - 1 - lam2
            yield (f, rr, self._code(side, frame), False)
            for g in self.file_neighbours(f):
                nframe = frame ^ (1 if self.crosses_seam(f, g) else 0)
                rr = lam2 if nframe == 0 else self.ranks - 1 - lam2
                yield (g, rr, self._code(side, nframe), True)
            return

        # straight push (same file)
        rr = r + direction
        if self.wraps_ranks():
            rr %= self.ranks
        elif not 0 <= rr < self.ranks:
            rr = None
        if rr is not None:
            yield (f, rr, self._code_from_direction(side, direction), False)

        # diagonal captures
        for g in self.file_neighbours(f):
            rr = r + direction
            if self.wraps_ranks():
                rr %= self.ranks
            elif not 0 <= rr < self.ranks:
                continue
            nd = direction
            if self.crosses_seam(f, g):
                nd = -direction
            yield (g, rr, self._code_from_direction(side, nd), True)

    def _code(self, side, frame):
        """Piece code for `side` in the given frame (twisted surfaces)."""
        if side == WHITE:
            return WUP if frame == 0 else WDN
        return BDN if frame == 0 else BUP

    @staticmethod
    def _code_from_direction(side, direction):
        if side == WHITE:
            return WUP if direction == +1 else WDN
        return BUP if direction == +1 else BDN

    @staticmethod
    def _apply(pos, f, r, g, rr, new_piece):
        cols = [list(c) for c in pos]
        cols[f][r] = E
        cols[g][rr] = new_piece
        return tuple(tuple(c) for c in cols)


class Flat(Geometry):
    name = "flat"


class Cylinder(Geometry):
    name = "cyl"

    def wraps_files(self):
        return True


class Torus(Geometry):
    name = "torus"

    def wraps_files(self):
        return True

    def wraps_ranks(self):
        return True


class MobiusM(Geometry):
    """Twisted seam; a crossing pawn's direction reverses (convention M)."""

    name = "mobiusM"

    def wraps_files(self):
        return True

    def twisted(self):
        return True

    def _targets(self, pos, f, r, piece, side):
        # identical to the cylinder except that a crossing capture flips the direction
        up = piece in (WUP, BUP)
        direction = +1 if up else -1
        rr = r + direction
        if not 0 <= rr < self.ranks:
            rr = None
        if rr is not None:
            yield (f, rr, self._code_from_direction(side, direction), False)
        for g in self.file_neighbours(f):
            rr = r + direction
            if not 0 <= rr < self.ranks:
                continue
            nd = -direction if self.crosses_seam(f, g) else direction
            yield (g, rr, self._code_from_direction(side, nd), True)


class MobiusT(Geometry):
    """Twisted seam with the quotient geometry (convention T)."""

    name = "mobiusT"

    def wraps_files(self):
        return True

    def twisted(self):
        return True


SURFACES = {
    "flat": Flat,
    "cyl": Cylinder,
    "torus": Torus,
    "mobiusM": MobiusM,
    "mobiusT": MobiusT,
}


def solve(geom, limit=8_000_000):
    """Return (normal_W, normal_B, misere_W, misere_B, positions)."""
    sys.setrecursionlimit(1_000_000)
    memo = {}
    count = [0]

    def rec(pos, side):
        key = (pos, side)
        hit = memo.get(key)
        if hit is not None:
            return hit
        count[0] += 1
        if count[0] > limit:
            raise RuntimeError("limit exceeded")
        succ, _ = geom.moves(pos, side)
        if not succ:
            res = (False, True)      # normal: lose ; misere: win
        else:
            n_win = m_win = False
            for q in succ:
                n_sub, m_sub = rec(q, 1 - side)
                if not n_sub:
                    n_win = True
                if not m_sub:
                    m_win = True
                if n_win and m_win:
                    break
            res = (n_win, m_win)
        memo[key] = res
        return res

    start = geom.start()
    n_w, m_w = rec(start, WHITE)
    n_b, m_b = rec(start, BLACK)
    return n_w, n_b, m_w, m_b, count[0]


def main():
    if len(sys.argv) >= 3:
        name = sys.argv[1]
        files, ranks = int(sys.argv[2]), int(sys.argv[3])
        geom = SURFACES[name](files, ranks)
        n_w, n_b, m_w, m_b, cnt = solve(geom)
        print(f"{name:8s} {files:3d} {ranks:3d}  {int(n_w)} {int(n_b)}  "
              f"{int(m_w)} {int(m_b)}  {cnt}")
        return

    # cross-check suite
    print("surface files ranks  normW normB  misW misB  positions")
    suite = []
    for n in range(3, 13):
        suite.append(("flat", n, 3))
        suite.append(("cyl", n, 3))
        suite.append(("torus", n, 3))
        suite.append(("mobiusM", n, 3))
        suite.append(("mobiusT", n, 3))
    for n in range(3, 9):
        suite.append(("flat", n, 4))
        suite.append(("cyl", n, 4))
    for n in range(3, 7):
        suite.append(("flat", n, 5))
        suite.append(("cyl", n, 5))
    for n in range(3, 8):
        suite.append(("cyl", n, 2))
    for name, n, r in suite:
        geom = SURFACES[name](n, r)
        n_w, n_b, m_w, m_b, cnt = solve(geom)
        print(f"{name:8s} {n:3d} {r:3d}  {int(n_w)} {int(n_b)}  "
              f"{int(m_w)} {int(m_b)}  {cnt}")


if __name__ == "__main__":
    main()
