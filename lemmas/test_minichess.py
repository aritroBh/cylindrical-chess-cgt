"""Sanity checks for lemmas/minichess.py against published perft counts
(chessprogramming.org "Perft Results"; positions without castling rights).

Run: PYTHONPATH=. .venv/bin/python lemmas/test_minichess.py
"""
import sys

from lemmas.minichess import from_fen, legal_moves


def perft(pos, depth):
    if depth == 0:
        return 1
    return sum(perft(ch, depth - 1) for _, ch in legal_moves(pos))


CASES = [
    # start position (castling cannot occur within 3 plies)
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1", [20, 400, 8902]),
    # CPW "position 3": e.p., checks, pins, no castling
    ("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1", [14, 191, 2812, 43238]),
    # promotion test position (all four promotion pieces, captures onto the last rank)
    ("n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1", [24, 496, 9483]),
]


def test_perft():
    for fen, counts in CASES:
        p = from_fen(fen)
        for d, n in enumerate(counts[:3], start=1):
            assert perft(p, d) == n, (fen, d)


if __name__ == "__main__":
    bad = 0
    for fen, counts in CASES:
        p = from_fen(fen)
        for d, n in enumerate(counts, start=1):
            got = perft(p, d)
            print(f"{fen}  depth {d}: {got} (expected {n})", "ok" if got == n else "MISMATCH", flush=True)
            bad += got != n
    print("FAILURES:", bad)
    sys.exit(1 if bad else 0)
