"""Sanity test for the k1_refute.py move generator (flat board): known perft counts.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && python3 verify/diagrams/K1-refute/perft_sanity.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k1_refute import parse, legal

def perft(pcs, side, d, ep=None):
    if d == 0:
        return 1
    ms = legal(pcs, side, False, ep)
    if d == 1:
        return len(ms)
    o = "B" if side == "W" else "W"
    return sum(perft(m[3], o, d - 1, m[4]) for m in ms)

# chessprogramming.org "Position 3" (no castling rights; has ep, checks, pins)
p3 = parse("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8")
for d, want in [(1, 14), (2, 191), (3, 2812), (4, 43238)]:
    got = perft(p3, "W", d)
    print("pos3 perft", d, got, want, "OK" if got == want else "MISMATCH")
start = parse("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
for d, want in [(1, 20), (2, 400), (3, 8902)]:
    got = perft(start, "W", d)
    print("start perft", d, got, want, "OK" if got == want else "MISMATCH")
