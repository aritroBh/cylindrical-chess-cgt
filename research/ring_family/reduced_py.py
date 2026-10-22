"""Independent (Python/cylcgt move generator) one-ply-poison reduced graph; compare with the C dump.
Edge format: (position-without-ep, side, move, child-without-ep | TERMINAL-WIN)."""
import sys, re
sys.path.insert(0, "research/ring_family")
from ringlib import *
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos, name
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
BIG = pawns.BIG

def terminal(board, pos, mover):
    """+1 mover wins at once, -1 mover loses at once, 0 non-terminal  (same convention as the C code)"""
    wp, bp = pawns.passed(board, pos, "W"), pawns.passed(board, pos, "B")
    if wp and bp:
        v = pawns._child(board, pos, mover)          # race rule
        return 1 if (v.num > 0) == (mover == "W") else -1
    if wp: return 1 if mover == "W" else -1
    if bp: return 1 if mover == "B" else -1
    return 0

def other(s): return "B" if s == "W" else "W"
def strip(p): return str(Pos(p.white, p.black, None))

def mv_desc(pos, ch, side):
    mine = pos.white if side == "W" else pos.black
    chm = ch.white if side == "W" else ch.black
    theirs = pos.black if side == "W" else pos.white
    cht = ch.black if side == "W" else ch.white
    src = next(iter(mine - chm)); dst = next(iter(chm - mine))
    cap = theirs - cht
    s = f"{name(src)}{'x' if cap else '-'}{name(dst)}"
    if cap and next(iter(cap)) != dst: s += " e.p."
    return s

def moves_of(board, pos, side):
    plain = Pos(pos.white, pos.black, None)
    lpos = plain if (pos.ep and pos.ep[2] != side) else pos
    return pawns.moves(board, lpos, side)

def poisoned(board, child, mover):
    opp = other(mover)
    for c2 in moves_of(board, child, opp):
        if terminal(board, c2, opp) == 1: return True
    return False

def reduced_edges(ring):
    n = len(ring); board = Board(n, 8, True, True)
    start = Pos.parse(to_text(ring))
    seen = {start}; stack = [start]; edges = set()
    while stack:
        pos = stack.pop()
        for side in ("W", "B"):
            for ch in moves_of(board, pos, side):
                t = terminal(board, ch, side)
                d = mv_desc(pos, ch, side)
                if t < 0: continue
                if t > 0:
                    edges.add((strip(pos), side, d, "TERMINAL-WIN")); continue
                if poisoned(board, ch, side): continue
                edges.add((strip(pos), side, d, strip(ch)))
                if ch not in seen: seen.add(ch); stack.append(ch)
    return edges

if __name__ == "__main__":
    from pump_check import fam
    for name_, k in (("odd", 2), ("odd", 3), ("even", 1), ("even", 2)):
        ring = fam(name_, k)
        pe = reduced_edges(ring)
        ce = set()
        for l in open(f"research/ring_family/dumps/{name_}_k{k}.tsv"):
            a, side, mv, b = l.rstrip("\n").split("\t")
            ce.add((a.split(" ep")[0], side, mv, b if b == "TERMINAL-WIN" else b.split(" ep")[0]))
        print(f"{name_} k={k} C{len(ring)}: python edges {len(pe)}, C edges {len(ce)}, equal: {pe == ce}", flush=True)
        if pe != ce:
            print("   only py:", list(pe - ce)[:3]); print("   only C:", list(ce - pe)[:3])
