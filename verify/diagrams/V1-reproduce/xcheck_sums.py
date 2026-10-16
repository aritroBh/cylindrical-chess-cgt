"""V1 verifier scratch: test the V1 values with the independent whole-board minimax
(crosscheck/minimax.py, race rule = "count" built in), via sum tests G + X.

G (a V1 position) is moved to a 16-file cylinder: files a-d keep their index, files e-h
move to 12-15, so h is still adjacent to a and no V1 component spans the d|e boundary.
X is a pawn group on files 6 and/or 8 (files 4,5,7,9,10,11 empty), so G and X are
independent summands.  Every X used never reaches a passed pawn (single-file rams or
own-pawn-blocked pawns), so whole-board play equals the disjunctive sum exactly.

Prediction = cgt.outcome(value8(G) + value(X)) from cylcgt on the ORIGINAL 8-file board.
Observed  = crosscheck.minimax.outcome_class on the 16-file board (whole board).

Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     PYTHONPATH=. .venv/bin/python verify/diagrams/V1-reproduce/xcheck_sums.py
"""
import sys
from dataclasses import replace

from cylcgt import cgt, pawns
from cylcgt.pawns import Board as PB, Pos
from crosscheck import minimax as mm

sys.setrecursionlimit(1000000)
FILES = "abcdefghijklmnopqrstuvwxyz"

G = {
    "2.1": "W: e4 / B: e5",
    "2.2": "W: a2 h1 / B: a3 h4",
    "3.1": "W: a3 h1 / B: a4 h5",
    "3.2": "W: a4 h1 / B: a5 h6",
    "4.1": "W: e4 / B: e6",
    "4.2": "W: e3 / B: e6",
    "4.3": "W: a4 h2 h4 / B: a5 a6 a7 h3",
    "7.1c": "W: c2 c3 / B: c5 c6",
    "7.1f": "W: f3 f4 / B: f7",
    "7.1ah": "W: a4 a5 h2 h3 / B: a7 h6",
    "7.1all": "W: a4 a5 c2 c3 f3 f4 h2 h3 / B: a7 c5 c6 f7 h6",
    "7.2abh": "W: a2 b2 h3 / B: a6 b7 h7",
    "7.3": "W: a1 a5 c1 c3 d3 f7 g1 h1 / B: c2 d4 d5 d6 g3 g7 h4",
}

# X components: (white squares, black squares) on file index 6 ('g' of the 16-file board) or 8 ('i')
X_ON_FILE = {
    "0": ([], []),
    "*": (["4"], ["6"]),          # W x4 / B x6
    "1": (["2", "4"], ["5"]),     # W x2 x4 / B x5
    "-1": (["4"], ["5", "7"]),    # W x4 / B x5 x7
    "-2": (["3"], ["4", "7"]),    # W x3 / B x4 x7
    "up": (["2"], ["5"]),         # W x2 / B x5
}
# down = colour-reversed up: W x4 / B x7
X_ON_FILE["down"] = (["4"], ["7"])
X_TESTS = ["0", "*", "1", "-1", "-2", "up", "down", "*+*", "-1+*", "-2+*", "1+*", "-1+-1", "down+*", "-1+up"]


def move16(sqs):
    out = []
    for s in sqs:
        f, r = pawns.sq(s)
        nf = f if f <= 3 else f + 8
        out.append(f"{FILES[nf]}{r}")
    return out


def xparts(spec):
    parts = spec.split("+") if spec != "0" else []
    # fix "-1+-1"
    w, b = [], []
    files = [6, 8]
    vals = []
    for i, p in enumerate(parts):
        fw, fb = X_ON_FILE[p]
        fl = FILES[files[i]]
        w += [fl + r for r in fw]
        b += [fl + r for r in fb]
        vals.append(p)
    return w, b, vals


def text(w, b):
    return f"W: {' '.join(w)} / B: {' '.join(b)}"


def main():
    for ep in (True, False):
        b8 = PB(8, 8, True, ep)
        b16 = PB(16, 8, True, ep)
        mb16 = mm.Board(16, 8, True, ep)
        print(f"\n===== en passant {'on' if ep else 'off'} =====")
        mism = 0
        total = 0
        for label, gtext in G.items():
            pawns.RACE_RULE = "count"
            pawns._value.cache_clear()
            g8 = pawns.value(b8, Pos.parse(gtext))
            gp = Pos.parse(gtext)
            gw = move16([pawns.name(s) for s in gp.white])
            gb = move16([pawns.name(s) for s in gp.black])
            # sanity: cylcgt value of the moved G on the 16-file board equals the 8-file value
            g16 = pawns.value(b16, Pos.parse(text(gw, gb)))
            same = cgt.eq(g8, g16) if hasattr(cgt, "eq") else (cgt.le(g8, g16) and cgt.le(g16, g8))
            row = []
            for xs in X_TESTS:
                xw, xb, _ = xparts(xs)
                xval = pawns.value(b16, Pos.parse(text(xw, xb))) if (xw or xb) else cgt.integer(0)
                pred = cgt.outcome(cgt.add(g8, xval))
                mm._winner.cache_clear()
                obs = mm.outcome_class(mb16, mm.parse_position(text(gw + xw, gb + xb)))
                total += 1
                if pred != obs:
                    mism += 1
                row.append(f"{xs}:{pred}{'' if pred == obs else '!=' + obs}")
            print(f"{label:7s} value8={cgt.show(g8)[:40]:40s} moved-same={same}  " + " ".join(row))
        print(f"mismatches: {mism}/{total}")


if __name__ == "__main__":
    main()
