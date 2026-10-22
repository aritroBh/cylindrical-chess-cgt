"""Helpers for the ring-family study (T41). Run from project root with PYTHONPATH=."""
import sys, time, itertools
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos, sq, name, FILES

RANKS = 8

def parse(text):
    return Pos.parse(text)

def to_sets(pos):
    return set(pos.white), set(pos.black)

def fmt(white, black):
    w = " ".join(sorted((name(s) for s in white)))
    b = " ".join(sorted((name(s) for s in black)))
    return f"W: {w} / B: {b}"

def canon_key(white, black, n):
    """canonical form under rotation, reflection, colour reversal"""
    best = None
    for colour in (0, 1):
        W, B = (white, black) if colour == 0 else (
            {(f, RANKS + 1 - r) for f, r in black}, {(f, RANKS + 1 - r) for f, r in white})
        for refl in (0, 1):
            for rot in range(n):
                def tr(s):
                    f, r = s
                    if refl: f = (n - 1 - f)
                    return ((f + rot) % n, r)
                w2 = tuple(sorted(tr(s) for s in W)); b2 = tuple(sorted(tr(s) for s in B))
                k = (w2, b2)
                if best is None or k < best[0]:
                    best = (k, (colour, refl, rot))
    return best

def canon_pos(text, n):
    p = parse(text)
    (w, b), _ = canon_key(set(p.white), set(p.black), n)
    return fmt(set(w), set(b))

def orbit(text, n):
    p = parse(text); out = set()
    for colour in (0, 1):
        W, B = (set(p.white), set(p.black)) if colour == 0 else (
            {(f, RANKS + 1 - r) for f, r in p.black}, {(f, RANKS + 1 - r) for f, r in p.white})
        for refl in (0, 1):
            for rot in range(n):
                def tr(s):
                    f, r = s
                    if refl: f = (n - 1 - f)
                    return ((f + rot) % n, r)
                out.add(fmt({tr(s) for s in W}, {tr(s) for s in B}))
    return out

def files_table(text, n):
    """per file: (white ranks, black ranks)"""
    p = parse(text)
    rows = []
    for f in range(n):
        ws = sorted(r for g, r in p.white if g == f)
        bs = sorted(r for g, r in p.black if g == f)
        rows.append((ws, bs))
    return rows

def show_table(text, n):
    rows = files_table(text, n)
    return " | ".join(f"{FILES[f]}:W{''.join(map(str,ws)) or '-'}/B{''.join(map(str,bs)) or '-'}" for f, (ws, bs) in enumerate(rows))

def val(text, n, whole=True, ep=True, race="count", respects=True):
    pawns.RACE_RULE = race
    pawns.PASSED_RESPECTS_EP = respects
    pawns._value.cache_clear()
    if whole:
        old = pawns.components
        pawns.components = lambda b, p: [p]
    try:
        g = pawns.value(Board(n, RANKS, True, ep), parse(text))
    finally:
        if whole:
            pawns.components = old
    return g

def sh(g):
    return cgt.show(g)
