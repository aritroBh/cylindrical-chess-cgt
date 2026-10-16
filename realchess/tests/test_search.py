"""The search on positions whose answer is forced, with a stub oracle."""
from realchess import movegen as mg
from realchess.search import Searcher, cat_interval


def test_cat_interval_modes():
    assert cat_interval("cursed-win", "pure") == (1, 1)
    assert cat_interval("cursed-win", "fifty") == (0, 0)
    assert cat_interval("blessed-loss", "fifty") == (0, 0)
    assert cat_interval("maybe-win", "fifty") == (0, 1)
    assert cat_interval(None, "pure") == (-1, 1)


def test_capture_children_come_from_one_probe():
    # 8 men; White to move can win the knight with a capture (stub says the
    # 7-man result after Rxd4 is a loss for Black) - one probe resolves it
    fen = "4k3/8/8/8/3n4/8/PPP4r/3RK3 w - - 0 1"
    seen = []

    def oracle(f):
        seen.append(f)
        pos = mg.parse_fen(f)
        moves = []
        for m in mg.legal_moves(pos):
            ch = mg.make(pos, m)
            cat = None
            if ch.men() <= 7:
                cat = "loss" if m.uci() == "d1d4" else "draw"
            moves.append({"uci": m.uci(), "category": cat})
        return {"status": 200, "data": {"category": "unknown", "moves": moves}}

    s = Searcher(oracle)
    pos = mg.parse_fen(fen)
    assert pos.men() == 8
    iv = s.search(pos, ext=1)
    assert iv == (1, 1)
    assert seen == [mg.normal_fen(pos)]
