"""cyl_children.py "<cstr>" [depth] : print the move tree of a ring with cylcgt values (default setting)."""
import sys
sys.path.insert(0, "research/ring_family")
from ringlib import *
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos, name
ring = from_cstr(sys.argv[1]); n = len(ring)
depth = int(sys.argv[2]) if len(sys.argv) > 2 else 1
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True; pawns._value.cache_clear()
board = Board(n, 8, True, True)
def desc(pos, child, side):
    a = (pos.white - child.white) if side == "W" else (pos.black - child.black)
    b = (child.white - pos.white) if side == "W" else (child.black - pos.black)
    cap = (pos.black - child.black) if side == "W" else (pos.white - child.white)
    s = f"{name(next(iter(a)))}->{name(next(iter(b)))}"
    if cap: s += "x" + name(next(iter(cap)))
    return s
def show_pos(p): return str(p)
def rec(pos, d, indent):
    plain = Pos(pos.white, pos.black, None)
    for side in ("W", "B"):
        lpos = plain if (pos.ep and pos.ep[2] != side) else pos
        for ch in pawns.moves(board, lpos, side):
            v = pawns._child(board, ch, side)
            print("  " * indent + f"{side} {desc(pos, ch, side)} -> {cgt.show(v)}   [{ch}]")
            if d > 1 and abs(v.num or 0) < 100 if v.num is not None else d > 1:
                rec(ch, d - 1, indent + 1)
pos = Pos.parse(to_text(ring))
print("root", pos, "=", cgt.show(pawns.value(board, pos)))
rec(pos, depth, 1)
