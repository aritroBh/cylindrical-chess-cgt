"""List each move's resulting value for selected sub-games (cylinder 8x8, e.p. on and off, race rule 'count').
Run: PYTHONPATH=. .venv/bin/python verify/diagrams/options.py
"""
from dataclasses import replace
from cylcgt import cgt, pawns
from cylcgt.pawns import CYL8, Pos, moves, value

def diff(a, b):
    gone_w = sorted(pawns.name(s) for s in a.white - b.white); new_w = sorted(pawns.name(s) for s in b.white - a.white)
    gone_b = sorted(pawns.name(s) for s in a.black - b.black); new_b = sorted(pawns.name(s) for s in b.black - a.black)
    return f"W{gone_w}->{new_w} B{gone_b}->{new_b}"

def show_opts(board, text, depth=1):
    p = Pos.parse(text)
    pawns._value.cache_clear()
    print(f"{text}  [{'ep on' if board.ep else 'ep off'}] value {cgt.show(value(board, p))}")
    for side in ("W", "B"):
        for q in moves(board, p, side):
            v = pawns._child(board, q, side)
            print(f"   {side}: {diff(p, q):40s} -> {cgt.show(v)}")

for b in (CYL8, replace(CYL8, ep=False)):
    show_opts(b, "W: a4 a5 h2 h3 / B: a7 h6")          # 7.1 a/h sub-game
    show_opts(b, "W: c1 c3 d3 / B: c2 d4 d5 d6")       # 7.3 {c,d} sub-game
    show_opts(b, "W: c1 d3 / B: c2 c3 d5 d6")          # 7.3 {c,d} after ...dxc3
