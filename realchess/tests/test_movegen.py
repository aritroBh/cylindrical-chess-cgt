"""Perft regression (published perft figures) and FEN handling.

The authoritative validation is realchess/validate_movegen.py (160 positions
against the Lichess move lists, results/movegen_validation.json)."""
import pytest

from realchess import movegen as mg

FAST = [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1", 3, 8902),
    ("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1", 4, 43238),
    ("8/8/2k5/5q2/5n2/8/5K2/8 b - - 0 1", 4, 23527),        # double check
    ("K1k5/8/P7/8/8/8/8/8 w - - 0 1", 6, 2217),               # self stalemate
    ("8/P1k5/K7/8/8/8/8/8 w - - 0 1", 5, None),
]
SLOW = [
    ("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1", 5, 674624),
    ("8/8/1k6/2b5/2pP4/8/5K2/8 b - d3 0 1", 6, 1440467),      # ep gives check
    ("8/5bk1/8/2Pp4/8/1K6/8/8 w - d6 0 1", 6, 824064),        # avoid illegal ep
    ("3k4/3p4/8/K1P4r/8/8/8/8 b - - 0 1", 6, 1134888),        # avoid illegal ep
    ("8/8/4k3/8/2p5/8/B2P2K1/8 w - - 0 1", 6, 1015133),
    ("8/8/8/8/k1p4R/8/3P4/3K4 w - - 0 1", 6, 1134888),
    ("2K2r2/4P3/8/8/8/8/8/3k4 w - - 0 1", 6, 3821001),        # promote out of check
    ("8/8/1P2K3/8/2n5/1q6/8/5k2 b - - 0 1", 5, 1004658),      # discovered check
    ("4k3/1P6/8/8/8/8/K7/8 w - - 0 1", 6, 217342),            # promote to give check
    ("8/P1k5/K7/8/8/8/8/8 w - - 0 1", 6, 92683),              # under-promote to check
    ("8/k1P5/8/1K6/8/8/8/8 w - - 0 1", 7, 567584),            # stalemate & mate
]


@pytest.mark.parametrize("fen,depth,n", [c for c in FAST if c[2]])
def test_perft_fast(fen, depth, n):
    assert mg.perft(mg.parse_fen(fen), depth) == n


@pytest.mark.slow
@pytest.mark.parametrize("fen,depth,n", SLOW)
def test_perft_slow(fen, depth, n):
    assert mg.perft(mg.parse_fen(fen), depth) == n


def test_fen_roundtrip_and_ep_modes():
    f = "8/8/8/KPp4r/8/8/8/7k w - c6 0 1"   # e.p. pseudo-legal but illegal (pin)
    p = mg.parse_fen(f)
    assert mg.ep_pseudo(p) and not mg.ep_legal(p)
    assert mg.to_fen(p, "pseudo") == f
    assert mg.to_fen(p, "legal") == "8/8/8/KPp4r/8/8/8/7k w - - 0 1"
    q = mg.parse_fen("8/8/8/2Pp4/4K3/8/8/k7 w - d6 0 1")
    assert "c5d6" in {m.uci() for m in mg.legal_moves(q)}
    r = mg.parse_fen("4k3/8/8/8/8/8/3P4/4K3 b - d3 0 1")  # no capturer: ep dropped
    assert mg.normal_fen(r) == "4k3/8/8/8/8/8/3P4/4K3 b - - 0 1"


def test_candidate_fen():
    f = "8/1p1p4/8/5Kp1/6Pk/8/P1P5/8 w - - 0 1"
    p = mg.parse_fen(f)
    assert mg.to_fen(p) == f and p.men() == 8
    ucis = {m.uci() for m in mg.legal_moves(p)}
    # f4 is attacked by g5 and e6 by d7, g4/g5 are blocked: four king moves
    assert {u for u in ucis if u.startswith("f5")} == {"f5e4", "f5e5", "f5f6", "f5g6"}
    assert {u for u in ucis if not u.startswith("f5")} == {"a2a3", "a2a4", "c2c3", "c2c4"}
    pb = mg.parse_fen(f.replace(" w ", " b "))
    ub = {m.uci() for m in mg.legal_moves(pb)}
    assert {u for u in ub if u.startswith("h4")} == {"h4g3", "h4h3"}


def test_stalemate_and_mate():
    assert mg.status(mg.parse_fen("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")) == "stalemate"
    assert mg.status(mg.parse_fen("8/8/8/8/8/4k3/8/r3K3 w - - 0 1")) == "checkmate"
