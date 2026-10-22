"""Shared helpers for the cylcgt-side checks (stdlib + cylcgt)."""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from cylcgt import cgt, pawns   # noqa: E402

# default setting: RACE_RULE="count", e.p. on, PASSED_RESPECTS_EP=True
pawns.RACE_RULE = "count"
pawns.PASSED_RESPECTS_EP = True

FILES = "abcdefghij"

def parse_pos(text):
    """'W: a2 b3 / B: c7' -> (set of (file,rank) white, set black); files 0-based."""
    wpart, bpart = text.split("/")
    sq = lambda t: (FILES.index(t[0]), int(t[1:]))
    return ([sq(t) for t in wpart.split(":")[1].split()], [sq(t) for t in bpart.split(":")[1].split()])

def pos_text(white, black):
    s = lambda L: " ".join(f"{FILES[f]}{r}" for f, r in sorted(L))
    return f"W: {s(white)} / B: {s(black)}"

def occupied_groups(white, black):
    """Maximal runs of consecutive occupied files -> list of (f0, f1)."""
    fs = sorted({f for f, _ in white} | {f for f, _ in black})
    groups = []
    for f in fs:
        if groups and f == groups[-1][1] + 1:
            groups[-1][1] = f
        else:
            groups.append([f, f])
    return [tuple(g) for g in groups]

def split_parts(white, black):
    """Parts of a position = pawn sets on maximal runs of occupied files; each normalised to start on file a.
    Returns list of (width, frozenset W, frozenset B)."""
    out = []
    for f0, f1 in occupied_groups(white, black):
        w = frozenset((f - f0, r) for f, r in white if f0 <= f <= f1)
        b = frozenset((f - f0, r) for f, r in black if f0 <= f <= f1)
        out.append((f1 - f0 + 1, w, b))
    return out

def mirror_part(width, w, b):
    return (width, frozenset((width - 1 - f, r) for f, r in w), frozenset((width - 1 - f, r) for f, r in b))

def part_key(width, w, b):
    """Canonical key of a part up to left-right reflection."""
    k1 = (width, tuple(sorted(w)), tuple(sorted(b)))
    m = mirror_part(width, w, b)
    k2 = (width, tuple(sorted(m[1])), tuple(sorted(m[2])))
    return min(k1, k2)

def value_of_part(width, w, b):
    """cylcgt value (default setting) of one part as a position on a flat board of exactly its width."""
    return pawns.value(pawns.Board(width, 8, False, True), pawns.Pos(frozenset(w), frozenset(b)))

def outcome_nim(g):
    return cgt.outcome(g), (g.nim if g.nim is not None else -1)
