#!/usr/bin/env python3
"""ringlib.py -- token rings for the whole-board pawn game on C_n (8 ranks): parse, legality, dihedral canon,
colour reversal, wall insertion.  Token syntax = rg tokens ("W4B7", "B6", "W23B5"), one per file."""
import re, sys, os

SINGLES = ["W%d" % r for r in range(2, 7)] + ["B%d" % r for r in range(3, 8)]   # W2..W6, B3..B7


def parse_tok(t):
    w = re.search(r"W(\d+)", t); b = re.search(r"B(\d+)", t)
    return (tuple(sorted(int(c) for c in w.group(1))) if w else (), tuple(sorted(int(c) for c in b.group(1))) if b else ())


def parse(ring):
    return [parse_tok(t) for t in ring.split()]


def passed_free(ring):
    """True iff no pawn is passed (root ring: no e.p. right exists).  White pawn (f,r) is passed iff no black pawn on
    files f-1,f,f+1 (mod n) has rank > r; black pawn (f,r) is passed iff no white pawn there has rank < r."""
    cfg = parse(ring)
    n = len(cfg)
    for f in range(n):
        w, b = cfg[f]
        nbr = (cfg[(f - 1) % n], cfg[f], cfg[(f + 1) % n])
        blk = [x for c in nbr for x in c[1]]     # black ranks on the three files
        wht = [x for c in nbr for x in c[0]]
        for r in w:
            if not any(s > r for s in blk):
                return False
        for r in b:
            if not any(s < r for s in wht):
                return False
    return True


def canon(ring):
    t = ring.split()
    n = len(t)
    imgs = []
    for s in range(n):
        imgs.append(tuple(t[(i + s) % n] for i in range(n)))
        imgs.append(tuple(t[(s - i) % n] for i in range(n)))
    return " ".join(min(imgs))


def mirror_tok(t):
    w, b = parse_tok(t)
    W = sorted(9 - r for r in b); B = sorted(9 - r for r in w)
    return ("W" + "".join(map(str, W)) if W else "") + ("B" + "".join(map(str, B)) if B else "")


def mirror(ring):
    return " ".join(mirror_tok(t) for t in ring.split())


def npawns(ring):
    return sum(len(w) + len(b) for w, b in parse(ring))


def insertions(ring, k):
    """all rings obtained by inserting k single-pawn files (ordered k-tuples of SINGLES) at one cut of the ring.
    cut c = between file c-1 and file c (c = 0..n-1; cut 0 = between the last and the first file)."""
    t = ring.split()
    n = len(t)
    out = []
    for c in range(n):
        if k == 1:
            for x in SINGLES:
                out.append((c, (x,), " ".join(t[:c] + [x] + t[c:])))
        else:
            for x in SINGLES:
                for y in SINGLES:
                    out.append((c, (x, y), " ".join(t[:c] + [x, y] + t[c:])))
    return out


def sigtype(sig):
    return {"NNPN": "*2", "NNNP": "*3", "PNNN": "0", "NPNN": "*1"}.get(sig, "other")
