"""mgame.py -- an engine for the whole-board pawn game on the Moebius strip, written for this proof.

Conventions (research/mobius_rings/REPORT.md, "Rules as implemented"):
  * n files 0..n-1, ranks 1..8.  The seam joins file n-1 to file 0 with ranks reversed: seen across the seam,
    a square (f, r) appears at rank 9-r and a pawn's direction appears reversed.
  * A pawn carries a direction d (+1 up, -1 down); White starts +1, Black -1.  Home rank, double step and
    distance follow d.  A capture across the seam lands on the mirrored rank and flips d.
  * Passed: no enemy pawn (any direction) strictly ahead in the pawn's direction on its file or the two
    neighbouring files (neighbours across the seam read with ranks mirrored); a pawn that the opponent can
    capture e.p. right now is not passed.  The game ends at the first passed pawn; if both sides have one,
    race rule "count": the side with the smaller distance wins, ties to the side that did NOT just move;
    distance = min over passed pawns that are the front pawn of their file (no pawn of either colour ahead
    on the same file), d = 8-r-[r=2] (up) or r-1-[r=7] (down).
  * e.p.: after a double step the opponent may, on the next move only, capture onto the skipped square
    with any pawn whose diagonal capture square is that square; the flag is stored only if such a capture
    exists (canonical convention); a flag nobody can use is dropped.
A position is (cells, ep): cells = tuple over files of tuples over ranks 1..8 with codes
0 empty, 1 white up, 2 white down, 3 black up, 4 black down; ep = None or (f, r_landing, r_skipped, holder).
Colour 0 = white, 1 = black.
"""
WU, WD, BU, BD = 1, 2, 3, 4

def col(c): return 0 if c <= 2 else 1
def dirn(c): return 1 if c in (1, 3) else -1
def code(colour, d): return (1 if d > 0 else 2) + 2 * colour
def flip(c): return code(col(c), -dirn(c))

class Board:
    def __init__(self, n, twist=True):
        self.n = n; self.twist = twist

    # ---- geometry -------------------------------------------------------
    def wrap(self, f, r):
        """chart square of the cover square (f, r) with f in -1..n; returns (f', r', crossed)."""
        n = self.n
        if 0 <= f < n: return f, r, False
        if not self.twist: return f % n, r, False      # plain cylinder (control)
        return f % n, 9 - r, True

    def at(self, cells, f, r):
        """code seen at cover square (f, r) (direction as seen from the chart side of the viewer)."""
        if r < 1 or r > 8: return 0
        g, s, x = self.wrap(f, r)
        c = cells[g][s - 1]
        return flip(c) if (x and c) else c

    # ---- passed / race --------------------------------------------------
    def blocked(self, cells, f, r):
        c = cells[f][r - 1]; me, d = col(c), dirn(c)
        for df in (-1, 0, 1):
            rr = r + d
            while 1 <= rr <= 8:
                e = self.at(cells, f + df, rr)
                if e and col(e) != me: return True
                rr += d
        return False

    def ep_victims(self, pos):
        """set of squares of pawns that can be captured e.p. now (0 or 1 element)."""
        cells, ep = pos
        return {(ep[0], ep[1])} if ep else set()

    def passers(self, pos, side):
        cells, ep = pos; out = []
        prot = self.ep_victims(pos)
        for f in range(self.n):
            for r in range(1, 9):
                c = cells[f][r - 1]
                if c and col(c) == side and (f, r) not in prot and not self.blocked(cells, f, r):
                    out.append((f, r))
        return out

    def dist(self, cells, sq):
        f, r = sq; d = dirn(cells[f][r - 1])
        rr = r + d
        while 1 <= rr <= 8:
            if cells[f][rr - 1]: return None          # not the front pawn of its file
            rr += d
        return (8 - r - (r == 2)) if d > 0 else (r - 1 - (r == 7))

    def classify(self, pos, mover):
        """0 non-terminal, +1 terminal won by mover, -1 terminal lost by mover."""
        pw, pb = self.passers(pos, 0), self.passers(pos, 1)
        if not pw and not pb: return 0
        if pw and pb:
            cells = pos[0]; INF = 10 ** 6
            def best(lst):
                v = [self.dist(cells, s) for s in lst]; v = [x for x in v if x is not None]
                return min(v) if v else INF
            dm = best(pw if mover == 0 else pb); do = best(pb if mover == 0 else pw)
            return -1 if do <= dm else 1
        return 1 if (pw if mover == 0 else pb) else -1

    # ---- moves ----------------------------------------------------------
    def _setc(self, cells, f, r, v):
        row = list(cells[f]); row[r - 1] = v; cells[f] = tuple(row)

    def capture_target(self, f, r, d, df):
        """chart square and new direction of a pawn at (f, r) with direction d capturing towards df."""
        g, s, x = self.wrap(f + df, r + d)
        return g, s, (-d if x else d), x

    def ep_possible(self, cells, f, sk, holder):
        """can a pawn of `holder` capture onto chart square (f, sk) ?"""
        for g in range(self.n):
            for r in range(1, 9):
                c = cells[g][r - 1]
                if not c or col(c) != holder: continue
                d = dirn(c)
                if not (1 <= r + d <= 8): continue
                for df in (-1, 1):
                    t = self.capture_target(g, r, d, df)
                    if (t[0], t[1]) == (f, sk): return True
        return False

    def moves(self, pos, side):
        """list of (description, child).  description = (file_from, rank_from, kind, file_to, rank_to)."""
        cells, ep = pos; n = self.n; out = []
        for f in range(n):
            for r in range(1, 9):
                c = cells[f][r - 1]
                if not c or col(c) != side: continue
                d = dirn(c); r1 = r + d
                if not (1 <= r1 <= 8): continue
                if not cells[f][r1 - 1]:
                    nc = list(cells); self._setc(nc, f, r, 0); self._setc(nc, f, r1, c)
                    out.append(((f, r, 's', f, r1), (tuple(nc), None)))
                    home = 2 if d > 0 else 7; r2 = r + 2 * d
                    if r == home and not cells[f][r2 - 1]:
                        nc = list(cells); self._setc(nc, f, r, 0); self._setc(nc, f, r2, c); nc = tuple(nc)
                        e = (f, r2, r1, 1 - side) if self.ep_possible(nc, f, r1, 1 - side) else None
                        out.append(((f, r, 'd', f, r2), (nc, e)))
                for df in (-1, 1):
                    g, s, nd, x = self.capture_target(f, r, d, df)
                    t = cells[g][s - 1]
                    if t and col(t) != side:
                        nc = list(cells); self._setc(nc, f, r, 0); self._setc(nc, g, s, code(side, nd))
                        out.append(((f, r, 'x', g, s), (tuple(nc), None)))
                    elif not t and ep and ep[3] == side and (g, s) == (ep[0], ep[2]):
                        nc = list(cells); self._setc(nc, f, r, 0); self._setc(nc, ep[0], ep[1], 0)
                        self._setc(nc, g, s, code(side, nd))
                        out.append(((f, r, 'e', g, s), (tuple(nc), None)))
        return out

def parse_ring(s):
    """ring notation: one token per file, e.g. 'B4 W2 W6B7' (default directions)."""
    cells = []
    for tok in s.split():
        row = [0] * 8; cur = None
        for ch in tok:
            if ch == 'W': cur = WU
            elif ch == 'B': cur = BD
            elif ch == '-': pass
            else: row[int(ch) - 1] = cur
        cells.append(tuple(row))
    return (tuple(cells), None)

def fmt(pos):
    cells, ep = pos; toks = []
    for row in cells:
        t = ''
        for colour, lw, lu in ((0, 'W', 'w'), (1, 'B', 'b')):
            for r in range(1, 9):
                c = row[r - 1]
                if c and col(c) == colour:
                    default = (dirn(c) == (1 if colour == 0 else -1))
                    t += (lw if default else lu) + str(r)
        toks.append(t or '-')
    s = ' '.join(toks)
    if ep: s += ' ep%d.%d' % (ep[0], ep[1])
    return s
