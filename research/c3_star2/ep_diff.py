"""T33 item 3: which en passant capture makes the C3 root worth *2 (e.p. on) rather than 0 (e.p. off).

Breadth-first over the e.p.-on game (plies <= MAXPLY, no promotion). At every position where the side to
move has an e.p. capture available, compare the e.p.-on value with the value of the same pawns on the
e.p.-off board. The first ply with a difference names the capture that matters. Run from the project root:
    PYTHONPATH=. .venv/bin/python research/c3_star2/ep_diff.py
"""
import sys
from collections import deque
from cylcgt import pawns, cgt
from research.c3_star2.walk import setup
from research.c3_star2.reach import label

MAXPLY = int(sys.argv[1]) if len(sys.argv) > 1 else 4
FILES = 3


def ep_capture_moves(pos, side):
    """Children of pos for `side` that capture en passant right now."""
    out = []
    if not (pos.ep and pos.ep[2] == side):
        return out
    for ch in pawns.moves(B_ON, pos, side):
        own_p, own_c = (pos.white, ch.white) if side == "W" else (pos.black, ch.black)
        op_p, op_c = (pos.black, ch.black) if side == "W" else (pos.white, ch.white)
        if pos.ep[1] in op_p and pos.ep[1] not in op_c and pos.ep[0] in own_c and pos.ep[0] not in own_p:
            out.append(ch)
    return out


def main():
    global B_ON
    B_ON = pawns.Board(FILES, 8, True, True)
    B_OFF = pawns.Board(FILES, 8, True, False)
    setup("count", True)
    root = pawns.Pos.parse("W: a2 a3 b2 / B: b7 c6 c7")
    print("root on:", cgt.show(pawns.value(B_ON, root)), " root off:", cgt.show(pawns.value(B_OFF, root)))
    key0 = (root.white, root.black, root.ep, "W")
    frontier = [key0]
    seen = {key0}
    found = []
    for ply in range(1, MAXPLY + 1):
        nxt = []
        for key in frontier:
            w, b, ep, side = key
            pos = pawns.Pos(w, b, ep)
            caps = ep_capture_moves(pos, side)
            if caps:
                plain = pawns.Pos(w, b, None)
                von = pawns.value(B_ON, pos)
                voff = pawns.value(B_OFF, plain)
                line = f"ply {ply}: {pos} side {side}; e.p. capture(s) {[label(pos, c, side) for c in caps]}; on {cgt.show(von)} vs off {cgt.show(voff)}"
                print(line, flush=True)
                if von is not voff:
                    found.append(line)
            for ch in pawns.moves(B_ON, pos, side):
                if any(r == B_ON.ranks for f, r in ch.white) or any(r == 1 for f, r in ch.black):
                    continue
                other = "B" if side == "W" else "W"
                ck = (ch.white, ch.black, ch.ep, other)
                if ck not in seen:
                    seen.add(ck)
                    nxt.append(ck)
        frontier = nxt
        print(f"-- ply {ply} done, frontier {len(frontier)}", flush=True)
    print("first differences:", found[:3] if found else "none up to ply", MAXPLY)


if __name__ == "__main__":
    main()
