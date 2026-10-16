"""Tests for kings/kpsolve against hand-checked positions (rules: kings/SPEC.md).

Run from the project root:  .venv/bin/python -m pytest -q kings/test_kpsolve.py
"""
import os
import subprocess
import sys

import tempfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# build a private copy, so the tests never overwrite a binary that a long run is using
BIN = os.path.join(tempfile.mkdtemp(prefix="kpsolve-test-"), "kpsolve")


@pytest.fixture(scope="session", autouse=True)
def build():
    subprocess.run(["cc", "-O2", "-o", BIN, os.path.join(ROOT, "kings", "kpsolve.c")], check=True)


def solve(board, lines, *opts):
    out = subprocess.run([BIN, "--board", board, *opts], input="\n".join(lines) + "\n",
                         capture_output=True, text=True, check=True).stdout.splitlines()
    return out


def value(board, line, *opts):
    a, b = solve(board, [line], *opts)[0].split("|")[1].split()
    return a, b


def moves(board, line, *opts):
    parts = solve(board, [line], "--moves", *opts)[0].split("|")
    return dict(tok.rsplit(":", 1) for tok in parts[2].split())


def test_illegal_when_side_not_to_move_is_in_check():
    assert value("flat:4x4", "Ka1 kc3 Pb2 w -") == ("X", "X")   # b2 attacks c3
    assert value("flat:8x8", "Ke1 ke2 b -") == ("X", "X")       # kings adjacent
    assert value("flat:8x8", "Ke1 ke8 Pa8 w -") == ("X", "X")   # pawn on the last rank


def test_checkmate_and_stalemate():
    assert value("flat:8x8", "Kb6 ka8 Qb7 b -") == ("W", "W")   # mated
    assert value("flat:8x8", "Kb6 ka8 Qc7 b -") == ("D", "D")   # stalemate
    assert value("flat:8x8", "Kb6 ka8 Qh7 b -") == ("W", "W")   # Kb8 Qb7#


def test_kpk_draw_by_stalemate_trick():
    assert value("flat:8x8", "Kc6 ka8 Pb6 w -") == ("D", "D")   # 1.b7+ Kb8 2.Kb6 stalemate


def test_cylinder_wraps_and_flat_does_not():
    mv = moves("cyl:4x4", "Kb1 kc4 Pa2 pd3 w -")
    assert "Pa2d3" in mv and "Pa2b3" not in mv                 # capture across the seam
    mv = moves("flat:4x4", "Kb1 kc4 Pa2 pd3 w -")
    assert "Pa2d3" not in mv
    mv = moves("cyl:5x5", "Ka3 kc3 Pc2 w -")
    assert "Ka3e4" in mv and "Ka3e2" in mv                     # king steps across the seam


def test_rook_ray_wraps_and_stops_at_home():
    mv = moves("cyl:5x4", "Ra1 Kc3 ke3 w -")
    rank1 = sorted(m for m in mv if m.startswith("Ra1") and m.endswith("1"))
    assert rank1 == ["Ra1b1", "Ra1c1", "Ra1d1", "Ra1e1"]       # each square once, no Ra1a1
    mv = moves("flat:5x4", "Ra1 Kc3 ke3 w -")
    assert sorted(m for m in mv if m.startswith("Ra1") and m.endswith("1")) == rank1


def test_en_passant_only_immediately_and_only_when_on():
    mv = moves("flat:5x5", "Ka1 ke5 Pb4 pc4 b b3")
    assert "Pc4b3" in mv                                       # c4xb3 e.p.
    mv = moves("flat:5x5", "Ka1 ke5 Pb4 pc4 b -")
    assert "Pc4b3" not in mv                                   # right expired
    mv = moves("flat:5x5", "Ka1 ke5 Pb4 pc4 b b3", "--ep", "off")
    assert "Pc4b3" not in mv
    assert value("flat:5x5", "Ka1 ke5 Pb4 pc4 b c3") == ("X", "X")  # no white pawn just passed c3


def test_double_step_creates_en_passant_right():
    # White b2-b4 next to a black pawn on c4: Black's e.p. reply must be considered.
    mv = moves("flat:5x5", "Ka1 ke5 Pb2 pc4 w -")
    assert "Pb2b4" in mv and "Pb2b3" in mv


def test_all_four_promotions_listed():
    mv = moves("flat:5x5", "Ka1 ke4 Pb4 w -")
    assert {"Pb4b5=Q", "Pb4b5=R", "Pb4b5=B", "Pb4b5=N"} <= set(mv)
    mv = moves("flat:5x5", "Ka1 ke4 Pb4 w -", "--promote", "Q")
    assert "Pb4b5=Q" in mv and "Pb4b5=N" not in mv


def test_frozen_mode_matches_cylcgt_on_single_file_components():
    sys.path.insert(0, ROOT)
    from kings import experiment
    z, pfiles = experiment.layout("cyl", 6, 6)
    for ws, bs in [(((3, 2),), ((3, 3),)), (((3, 2),), ((3, 4),)), (((3, 2), (3, 3)), ((3, 5),))]:
        _, outc, _ = experiment.convention(ws, bs, pfiles, 6, True)
        base = " ".join(z + [f"P{experiment.name(*s)}" for s in ws] + [f"p{experiment.name(*s)}" for s in bs])
        got = (value("cyl:6x6", base + " w -", "--frozen")[0], value("cyl:6x6", base + " b -", "--frozen")[0])
        assert got == experiment.PREDICT[outc], (ws, bs, outc, got)


def test_trebuchet_is_a_mutual_zugzwang_on_6x6_cylinder():
    z, _ = experiment_layout()
    assert value("cyl:6x6", " ".join(z) + " w -", "--promote", "Q") == ("L", "L")
    assert value("cyl:6x6", " ".join(z) + " b -", "--promote", "Q") == ("W", "W")


def experiment_layout():
    sys.path.insert(0, ROOT)
    from kings import experiment
    return experiment.layout("cyl", 6, 6)
