"""T33 walk-through checks: domination and reversal of every root option, one level deep, for both sides.

For each option X of the mover (a child position) it reports
  - dominated: another option Y of the same side with X <= Y (Left) or X >= Y (Right), value-wise;
  - reversible: a reply Z of the opponent to X with Z <= G (Left option) or Z >= G (Right option), and the
    replacement options (the mover's replies to Z) with their values.
All comparisons are exact (cgt.le on canonical values). Run from the project root:
    PYTHONPATH=. .venv/bin/python research/c3_star2/chains.py [c3|c4]
"""
import sys
from cylcgt import pawns, cgt
from research.c3_star2.walk import setup, val

ROOTS = {
    "c3": (3, "W: a2 a3 b2 / B: b7 c6 c7"),
    "c4": (4, "W: a4 b2 c2 / B: b6 c5 d6 d7"),
}


def name_of(p):
    return str(p)


def analyse(B, P, G, side):
    other = "B" if side == "W" else "W"
    opts = pawns.moves(B, P, side)
    vals = [val(B, c, side) for c in opts]
    lines = []
    for i, c in enumerate(opts):
        vi = vals[i]
        doms = []
        for j, vj in enumerate(vals):
            if j == i:
                continue
            if side == "W":
                if cgt.le(vi, vj) and (not cgt.le(vj, vi) or j < i):
                    doms.append(j)
            else:
                if cgt.le(vj, vi) and (not cgt.le(vi, vj) or j < i):
                    doms.append(j)
        tag = []
        if doms:
            tag.append("dominated by " + ", ".join(f"{side}{k+1:02d}" for k in doms))
        for d in pawns.moves(B, c, other):
            w = val(B, d, other)
            if (side == "W" and cgt.le(w, G)) or (side == "B" and cgt.le(G, w)):
                repl = [(z, val(B, z, side)) for z in pawns.moves(B, d, side)]
                tag.append(f"reversible via {other} {d} (value {cgt.show(w)})")
                for z, zv in repl:
                    tag.append(f"    -> {side} {z} value {cgt.show(zv)} [{cgt.outcome(zv)}]")
        lines.append(f"  {side}{i+1:02d} {c} value {cgt.show(vi)} [{cgt.outcome(vi)}]"
                     + ((" | " + "; ".join(tag)) if tag else ""))
    return lines


def main(key):
    files, text = ROOTS[key]
    B = pawns.Board(files, 8, True, True)
    P = pawns.Pos.parse(text)
    setup("count", True)
    G = pawns.value(B, P)
    print(f"== {key} default setting: root {P} value {cgt.show(G)}; equals *2? {G is cgt.make([cgt.ZERO, cgt.STAR],[cgt.ZERO, cgt.STAR])}")
    for side in ("W", "B"):
        print(f"-- {side} to move:")
        for ln in analyse(B, P, G, side):
            print(ln)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "c3")
