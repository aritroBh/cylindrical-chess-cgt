"""ringtools.py -- small, self-contained ring utilities written fresh for verify_hits (does not import
enum_rings / merge.py / ringlib).  A ring is a list of per-file (white_ranks, black_ranks) tuples; the text form is
the rg token syntax, one token per file ("W2B5", "W35", "B6", "W2").  Board: n files (cylinder), 8 ranks.
"""
import re

RANKS = 8


def parse(text):
    ring = []
    for tok in text.split():
        w, b, mode = [], [], None
        if tok == "-":
            ring.append(((), ()))
            continue
        for ch in tok:
            if ch == "W":
                mode = "W"
            elif ch == "B":
                mode = "B"
            elif ch.isdigit():
                (w if mode == "W" else b).append(int(ch))
            else:
                raise ValueError("bad token %r" % tok)
        ring.append((tuple(sorted(w)), tuple(sorted(b))))
    return tuple(ring)


def fmt(ring):
    out = []
    for w, b in ring:
        s = ""
        if w:
            s += "W" + "".join(map(str, w))
        if b:
            s += "B" + "".join(map(str, b))
        out.append(s or "-")
    return " ".join(out)


def colour_reverse(ring):
    """swap colours, rank r -> 9 - r"""
    return tuple((tuple(sorted(RANKS + 1 - r for r in b)), tuple(sorted(RANKS + 1 - r for r in w))) for w, b in ring)


def dihedral_images(ring):
    n = len(ring)
    for base in (ring, tuple(reversed(ring))):
        for s in range(n):
            yield base[s:] + base[:s]


def canon_dihedral(ring):
    return min(dihedral_images(ring))


def canon_full(ring):
    """canonical form under rotation, reflection AND colour reversal"""
    return min(canon_dihedral(ring), canon_dihedral(colour_reverse(ring)))


def legality(ring, n=None, npawns=None):
    """Own legality test of a root ring.  Returns a list of violated conditions (empty list = legal)."""
    errs = []
    n = n or len(ring)
    if len(ring) != n:
        errs.append("wrong number of files %d" % len(ring))
    total = sum(len(w) + len(b) for w, b in ring)
    if npawns is not None and total != npawns:
        errs.append("pawn count %d != %d" % (total, npawns))
    for f, (w, b) in enumerate(ring):
        if not (w or b):
            errs.append("file %d empty" % f)
        if len(set(w)) != len(w) or len(set(b)) != len(b):
            errs.append("file %d repeated rank within a colour" % f)
        if set(w) & set(b):
            errs.append("file %d: two pawns on one square %s" % (f, sorted(set(w) & set(b))))
        for r in w:
            if not (2 <= r <= 6):
                errs.append("file %d: white pawn on rank %d outside 2..6" % (f, r))
        for r in b:
            if not (3 <= r <= 7):
                errs.append("file %d: black pawn on rank %d outside 3..7" % (f, r))
    # passed pawns at the root (no e.p. right exists at the root)
    for f, (w, b) in enumerate(ring):
        nbrs = [ring[(f - 1) % n], ring[f], ring[(f + 1) % n]]
        for r in w:
            if not any(rb > r for (_, bb) in nbrs for rb in bb):
                errs.append("white pawn on file %d rank %d is passed" % (f, r))
        for r in b:
            if not any(rw < r for (ww, _) in nbrs for rw in ww):
                errs.append("black pawn on file %d rank %d is passed" % (f, r))
    return errs


def to_pos_text(ring):
    """cylcgt text form 'W: a2 b3 / B: a7 ...'"""
    FILES = "abcdefghijklmnopqrstuvwxyz"
    ws, bs = [], []
    for f, (w, b) in enumerate(ring):
        ws += ["%s%d" % (FILES[f], r) for r in w]
        bs += ["%s%d" % (FILES[f], r) for r in b]
    return "W: " + " ".join(ws) + " / B: " + " ".join(bs)


def split_of(ring):
    return (sum(len(w) for w, _ in ring), sum(len(b) for _, b in ring))
