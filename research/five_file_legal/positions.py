"""The 21 five-file *2 positions of the flat 5-file board (count rule, e.p.-aware test).

Source of truth: the C/aware rows of research/star2_width5/hits.tsv (T21's flat
width-5, 8-pawn scan; 14,680,983 roots, 9 settings).  Every position there is of
value *2 under the count rule with the e.p.-aware passed test.

Files a..e are the five files of the scanned board; the trébuchet is added later
on files f..h (W Kf5 Pg4, B Kh4 Pg5).
"""
from __future__ import annotations

import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HITS = os.path.join(ROOT, "research", "star2_width5", "hits.tsv")

FILES = "abcdefgh"


def parse_pos(text):
    """'W: a2 b2 c2 d2 / B: a5 b4 d7 e4' -> (white set, black set) of (file, rank)."""
    wpart, bpart = text.split("/")
    out = []
    for part in (wpart, bpart):
        body = part.split(":")[1]
        out.append(frozenset((FILES.index(sq[0]), int(sq[1])) for sq in body.split()))
    return out[0], out[1]


def fmt_pos(white, black):
    w = " ".join(f"{FILES[f]}{r}" for f, r in sorted(white, key=lambda q: (q[1], q[0])))
    b = " ".join(f"{FILES[f]}{r}" for f, r in sorted(black, key=lambda q: (q[1], q[0])))
    return f"W: {w} / B: {b}"


def load_positions(path=HITS):
    """The 21 positions of the hits file whose settings include C/aware."""
    out = []
    with open(path) as fh:
        header = fh.readline()
        assert header.startswith("k\tsettings\tposition"), header
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            k, settings, position = line.split("\t")
            if "C/aware" not in settings.split(","):
                continue
            white, black = parse_pos(position)
            out.append({"k": int(k), "settings": settings.split(","), "position": position,
                        "white": white, "black": black})
    return out


if __name__ == "__main__":
    pos = load_positions()
    print(len(pos), "positions")
    for p in pos:
        print(p["position"])
