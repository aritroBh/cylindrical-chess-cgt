"""Consistency tests for the EPD suite (offline; no network).

    cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python -m pytest -q engine/test_suite_files.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "suite"))

import run_suite as RS  # noqa: E402
import cgtpos as C  # noqa: E402
from cylcgt import cgt, pawns  # noqa: E402
from realchess import movegen as MG  # noqa: E402

EPDS = [os.path.join(HERE, "suite", f) for f in ("cgt_verified.epd", "cgt_disagree.epd")]


def lines(path):
    out = []
    for line in open(path, encoding="utf-8"):
        e = RS.parse_epd(line)
        if e:
            out.append(e)
    return out


def component_from_fen(fen4):
    b = RS.board_from_fen(fen4)
    w = frozenset((f, r) for (f, r), p in b.items() if p == "P" and f < 4)
    bl = frozenset((f, r) for (f, r), p in b.items() if p == "p" and f < 4)
    return pawns.Pos(w, bl)


def test_files_exist_and_parse():
    for p in EPDS:
        assert os.path.exists(p)
        assert lines(p), p


def test_san_matches_uci_and_moves_are_legal():
    for p in EPDS:
        for fen4, ops in lines(p):
            legal = MG.legal_uci(fen4 + " 0 1")
            uci = set(" ".join(ops["c2"]).split())
            assert uci <= legal, (fen4, uci - legal)
            assert {RS.san_to_uci_kp(fen4, m) for m in ops["bm"]} == uci, fen4
            pos = MG.parse_fen(fen4 + " 0 1")
            assert pos.men() <= 7 and not MG.validity_errors(pos), fen4


def test_verified_bm_equals_fresh_cgt_prediction():
    """Re-derive the CGT(count) winning set from cylcgt for every verified line."""
    C.set_rule("count")
    for fen4, ops in lines(EPDS[0]):
        comp = component_from_fen(fen4)
        stm = "W" if fen4.split()[1] == "w" else "B"
        wins = set()
        for uci, san, kind, child in C.labeled_moves(C.B4, comp, stm):
            if C.wins_for(stm, C.child_value(child, stm)):
                wins.add(uci)
        assert wins == set(" ".join(ops["c2"]).split()), fen4
        assert cgt.show(pawns.value(C.B4, comp))  # value is computable
