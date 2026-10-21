#!/usr/bin/env python3
"""Cross-check the two perft programs and test the cylinder's symmetry invariants.

  1. Flat board: both programs against the published perft numbers of five standard positions.
  2. Cylinder: both programs on the start position, Kiwipete and hand-made seam positions.
  3. Symmetry: on random cylinder positions (random legal play from the start, castling rights dropped),
     perft must not change under the 8 file rotations and the file mirror. Checked with cylperft.c to
     depth 3, and the two programs must agree at depth 2 on every position.

Run from the project root (builds cylperft.c first if needed; about 2 minutes):
    .venv/bin/python engine/perft/check.py
Writes engine/perft/results.json.
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cylperft as PY  # noqa: E402

CBIN = HERE / "cylperft"

START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
KIWI = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
FLAT_REF = {  # published perft numbers (chessprogramming.org "Perft Results")
    START: [20, 400, 8902, 197281, 4865609],
    KIWI: [48, 2039, 97862, 4085603],
    "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1": [14, 191, 2812, 43238, 674624],
    "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1": [6, 264, 9467, 422333],
    "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8": [44, 1486, 62379, 2103487],
}
SEAM = {  # hand-made positions where the seam matters
    "rook on a rank, both routes": "7k/8/8/8/8/8/8/R3K3 w - - 0 1",
    "one bishop, double check along two helices": "8/8/8/4k3/8/8/8/B3K3 b - - 0 1",
    "e.p. across the seam (a5xh6)": "4k3/8/8/P6p/8/8/8/4K3 w - h6 0 1",
    "castling forbidden by an attack across the seam": "4k3/8/8/8/8/b7/8/4K2R w K - 0 1",
    "helix pin after 1.c3 (f7 pinned by Qd1)": "rnbqkbnr/pppppppp/8/8/8/2P5/PP1PPPPP/RNBQKBNR b KQkq - 0 1",
    "pawn capture across the seam, with promotion (h7xa8)": "r3k3/7P/8/8/8/8/8/4K3 w - - 0 1",
}


def cperft(topo, depth, fen):
    return int(subprocess.run([str(CBIN), topo, str(depth), fen], capture_output=True, text=True,
                              check=True).stdout.strip())


def to_fen(pos):
    rows = []
    for r in range(7, -1, -1):
        row, gap = "", 0
        for f in range(8):
            p = pos["board"].get((f, r))
            if p:
                row += (str(gap) if gap else "") + p
                gap = 0
            else:
                gap += 1
        rows.append(row + (str(gap) if gap else ""))
    ep = "-" if pos["ep"] is None else "abcdefgh"[pos["ep"][0]] + str(pos["ep"][1] + 1)
    return f"{'/'.join(rows)} {'w' if pos['white'] else 'b'} {pos['castle'] or '-'} {ep} 0 1"


def transform(pos, k, mirror):
    def t(sq):
        f = (7 - sq[0]) if mirror else sq[0]
        return ((f + k) % 8, sq[1])
    return {"board": {t(s): p for s, p in pos["board"].items()}, "white": pos["white"], "castle": "",
            "ep": None if pos["ep"] is None else t(pos["ep"])}


def main():
    if not CBIN.exists():
        subprocess.run(["cc", "-O2", "-o", str(CBIN), str(HERE / "cylperft.c")], check=True)
    out = {"flat": [], "cylinder": [], "seam": [], "symmetry": {}}
    flat_ok = True
    print("1. Flat board against published perft")
    B = PY.Board(False)
    for fen, ref in FLAT_REF.items():
        c = [cperft("flat", d, fen) for d in range(1, len(ref) + 1)]
        pyd = 3 if fen != KIWI else 2
        p = [B.perft(PY.parse_fen(fen), d) for d in range(1, pyd + 1)]
        ok = c == ref and p == ref[:pyd]
        flat_ok &= ok
        out["flat"].append({"fen": fen, "ref": ref, "c": c, "py": p, "ok": ok})
        print(f"   {'OK ' if ok else 'BAD'} {fen[:40]:40s} C {c}  Py(d<={pyd}) {p}")

    print("2. Cylinder")
    Bc = PY.Board(True)
    for label, fen, cd, pd in (("start", START, 6, 4), ("kiwipete", KIWI, 4, 3)):
        c = [cperft("cyl", d, fen) for d in range(1, cd + 1)]
        p = [Bc.perft(PY.parse_fen(fen), d) for d in range(1, pd + 1)]
        ok = c[:pd] == p
        out["cylinder"].append({"label": label, "fen": fen, "c": c, "py": p, "agree": ok})
        print(f"   {'agree' if ok else 'DISAGREE'} {label}: C {c}; Py {p}")
    for label, fen in SEAM.items():
        c = [cperft("cyl", d, fen) for d in range(1, 5)]
        f = [cperft("flat", d, fen) for d in range(1, 5)]
        p = [Bc.perft(PY.parse_fen(fen), d) for d in range(1, 4)]
        ok = c[:3] == p
        out["seam"].append({"label": label, "fen": fen, "cyl_c": c, "cyl_py": p, "flat_c": f, "agree": ok})
        print(f"   {'agree' if ok else 'DISAGREE'} {label}: cylinder C {c}, Py {p}; flat {f}")

    print("3. Symmetry on random cylinder positions")
    rng = random.Random(20261016)
    n_pos, bad_sym, bad_cross = 0, [], []
    while n_pos < 150:
        pos = PY.parse_fen(START)
        for _ in range(rng.randint(6, 40)):
            ms = Bc.legal(pos)
            if not ms:
                break
            pos = Bc.make(pos, rng.choice(sorted(ms)))
        if not Bc.legal(pos):
            continue
        pos["castle"] = ""
        n_pos += 1
        fen = to_fen(pos)
        base = cperft("cyl", 3, fen)
        for k in range(8):
            for mirror in (False, True):
                if k == 0 and not mirror:
                    continue
                v = cperft("cyl", 3, to_fen(transform(pos, k, mirror)))
                if v != base:
                    bad_sym.append((fen, k, mirror, base, v))
        if cperft("cyl", 2, fen) != Bc.perft(pos, 2):
            bad_cross.append(fen)
    out["symmetry"] = {"positions": n_pos, "transforms_each": 15, "depth": 3,
                       "violations": bad_sym, "c_vs_py_depth2_disagreements": bad_cross}
    print(f"   {n_pos} positions x 15 transforms at depth 3: {len(bad_sym)} violations; "
          f"C vs Py at depth 2: {len(bad_cross)} disagreements")
    (HERE / "results.json").write_text(json.dumps(out, indent=1))
    return 0 if flat_ok and not bad_sym and not bad_cross else 1


if __name__ == "__main__":
    sys.exit(main())
