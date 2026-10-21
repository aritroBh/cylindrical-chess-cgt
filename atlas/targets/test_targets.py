"""Regression tests for workstream A3-targets.

Run from the project root:
  PYTHONPATH=. .venv/bin/python -m pytest -q -p no:cacheprovider atlas/targets/test_targets.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C  # noqa: E402

PCGT = os.path.join(HERE, "pcgt")


def pcgt(lines):
    out = subprocess.run([PCGT, "--printlimit", "100000"], input="\n".join(lines) + "\n", capture_output=True,
                         text=True, check=True).stdout
    vals, rows = {}, {}
    for line in out.splitlines():
        q = line.split("\t")
        if q[0] == "#V":
            vals[int(q[1])] = q[4]
        else:
            rows[(q[0], q[3], int(q[4]), int(q[5]), int(q[2]))] = int(q[6])
    return {k: vals[g] for k, g in rows.items()}


def test_known_values():
    r = pcgt(["W: a2 c2 / B: b7 d7\t4\t0\tcount\t1\t0", "W: a2 c2 / B: b7 d7\t4\t0\tcount\t1\t1",
              "W: a2 c2 / B: b7 d7\t4\t0\topponent\t1\t0", "W: a2 c2 / B: b7 d7\t4\t1\tcount\t1\t0",
              "W: a2 / B: a5\t1\t0\tcount\t1\t0", "W: a2 a3 b2 / B: a6 b5 b6\t2\t0\tblack\t0\t0",
              "W: a4 b3 d2 d3 / B: a7 b7 c5\t4\t0\tcount\t1\t1", "W: a5 b2 b3 d2 / B: b7 c5 d7\t4\t0\twhite\t1\t1"])
    assert r[("W: a2 c2 / B: b7 d7", "count", 1, 0, 0)] == "*2"
    assert r[("W: a2 c2 / B: b7 d7", "count", 1, 1, 0)] == "{2±1 | -2±1}"
    assert r[("W: a2 c2 / B: b7 d7", "opponent", 1, 0, 0)] == "0"
    assert r[("W: a2 c2 / B: b7 d7", "count", 1, 0, 1)] == "{3/2±1/2 | -3/2±1/2}"
    assert r[("W: a2 / B: a5", "count", 1, 0, 0)] == "↑"
    assert r[("W: a2 a3 b2 / B: a6 b5 b6", "black", 0, 0, 0)] == "1/8"
    assert r[("W: a4 b3 d2 d3 / B: a7 b7 c5", "count", 1, 1, 0)] == "*2"
    assert r[("W: a5 b2 b3 d2 / B: b7 c5 d7", "white", 1, 1, 0)] == "1/16"


def test_parse_key_roundtrip_and_classes():
    g = C.parse_key("{*1,0|{*1|0}}")
    assert C.cgt.show(g) == "{0, * | ↓}"
    c = C.classify(g)
    assert c["cls"] == "upsecond-family" and c["ups"] == [0, 1, 0, 1]
    c = C.classify(C.parse_key("{1|{1|1/2}}"))
    assert c["cls"] == "tiny" and c["sub"] == "1/2" and c["shift"] == "1"
    c = C.classify(C.parse_key("{0|{0|{-1|-2}}}"))
    assert c["cls"] == "tiny" and c["sub"] == "3/2±1/2"


def test_colour_reversal_negates():
    r = pcgt(["W: a4 b3 d2 d3 / B: a7 b7 c5\t4\t0\tcount\t1\t1", "W: a2 b2 c4 / B: a5 b6 d6 d7\t4\t0\tcount\t1\t1",
              "W: a5 b2 b3 d2 / B: b7 c5 d7\t4\t0\tcount\t1\t1", "W: a2 b4 c2 / B: a7 c6 c7 d4\t4\t0\tcount\t1\t1"])
    assert C.colour_reverse("W: a4 b3 d2 d3 / B: a7 b7 c5") == "W: a2 b2 c4 / B: a5 b6 d6 d7"
    assert r[("W: a2 b2 c4 / B: a5 b6 d6 d7", "count", 1, 1, 0)] == "*2"
    assert r[("W: a5 b2 b3 d2 / B: b7 c5 d7", "count", 1, 1, 0)] == "1/16"
    assert r[("W: a2 b4 c2 / B: a7 c6 c7 d4", "count", 1, 1, 0)] == "-1/16"


def test_freeze_geometry():
    import freeze
    r = freeze.placements("W: a2 a3 b2 / B: a6 b5 b6", 2)
    assert r["n_freeze_ok"] == r["n_placements"] == 60  # width 2: 3 offsets x 2 mirrors x 10; no pawn meets a king
    assert freeze.placements("W: a2 b2 c2 d2 e2 f2 / B: a7 b7 c7 d7 e7 f7", 6)["fits"] is False
