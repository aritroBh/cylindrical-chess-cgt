"""K68: compare the P values of two separately written solvers on every position the proof names.

  o68   (src/o68.cpp, written for K68)
  ax68q (src/ax68q.cpp = the K65 referee's ax65.cpp plus a query block; shares no code with o68)

Positions: the four roots and the two q's (both sides to move), the position after every legal move there,
and the whole family of Lemma B (White to move; Black Kb6, pb7, pc6; White pawn on c2, c3 or c4; White king on
every legal square), and the positions after Black's ...Kxc5 at every White king move from d4 (Lemma B reduction).
Usage: compare.py O68_BINARY AX68Q_BINARY OUTDIR
"""
import os
import subprocess
import sys

import chess

o68, ax, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
sq = chess.parse_square
FILES = "abcdefgh"


def sname(s):
    return chess.square_name(s)


def pos_line(b):
    wk, bk = sname(b.king(chess.WHITE)), sname(b.king(chess.BLACK))
    wp = ",".join(sorted(sname(s) for s in b.pieces(chess.PAWN, chess.WHITE))) or "-"
    bp = ",".join(sorted(sname(s) for s in b.pieces(chess.PAWN, chess.BLACK))) or "-"
    return "%s %s %s %s %s" % (wk, bk, wp, bp, "w" if b.turn else "b")


def make(wk, bk, wp, bp, white_to_move):
    b = chess.Board(None)
    b.set_piece_at(sq(wk), chess.Piece(chess.KING, chess.WHITE))
    b.set_piece_at(sq(bk), chess.Piece(chess.KING, chess.BLACK))
    for s in wp:
        b.set_piece_at(sq(s), chess.Piece(chess.PAWN, chess.WHITE))
    for s in bp:
        b.set_piece_at(sq(s), chess.Piece(chess.PAWN, chess.BLACK))
    b.turn = white_to_move
    return b


positions = []
named = [("root b4", "b4", ["b6", "c2", "c5"]), ("root b5", "b5", ["b6", "c2", "c5"]),
         ("q1", "b4", ["b6", "c4", "c5"]), ("q2", "b5", ["b6", "c3", "c5"])]
for name, bk, wp in named:
    for side in (True, False):
        b = make("d4", bk, wp, ["b7", "c6"], side)
        assert b.is_valid(), b.fen()
        positions.append(pos_line(b))
        for m in b.legal_moves:
            if m.promotion:
                continue
            c = b.copy()
            c.push(m)
            positions.append(pos_line(c))
            # Lemma B reduction: after a White king move from d4, Black takes on c5; then every White move
            if side and b.piece_type_at(m.from_square) == chess.KING:
                kx = chess.Move(sq(bk), sq("c5"))
                if kx in c.legal_moves:
                    d = c.copy()
                    d.push(kx)
                    positions.append(pos_line(d))
                    for m2 in d.legal_moves:
                        e = d.copy()
                        e.push(m2)
                        positions.append(pos_line(e))
                        k2 = chess.Move(sq("c5"), sq("b6"))
                        if k2 in e.legal_moves:
                            f = e.copy()
                            f.push(k2)
                            positions.append(pos_line(f))
# Lemma B family
for g in ["c2", "c3", "c4"]:
    for s in range(64):
        n = sname(s)
        if n in ("b6", "b7", "c6", g):
            continue
        b = make(n, "b6", [g], ["b7", "c6"], True)
        if b.is_valid():
            positions.append(pos_line(b))
positions = list(dict.fromkeys(positions))

os.makedirs(outdir, exist_ok=True)
qf = os.path.join(outdir, "compare_queries.txt")
with open(qf, "w") as f:
    f.write("\n".join(positions) + "\n")

# o68: one query per line, value for the side to move -> convert to White's point of view
r = subprocess.run([o68, "P"], input="\n".join(p + " - 0" for p in positions) + "\n", capture_output=True, text=True)
vo = {}
for line in r.stdout.splitlines():
    if "=>" not in line:
        continue
    left, right = line.split("=>")
    p = " ".join(left.split()[:5])
    v = right.split()[0][0]
    stm_white = p.split()[4] == "w"
    vo[p] = v if stm_white else {"W": "L", "L": "W", "D": "D"}[v]

env = dict(os.environ, AX68_QUERY=qf)
r2 = subprocess.run([ax, "flat:8x8", "Kd4 kb4 Pb6 Pc2 Pc5 pb7 pc6", "b4", "b5", "--noladder", "--noaux"],
                    capture_output=True, text=True, env=env)
va = {}
for line in r2.stdout.splitlines():
    if " : " in line:
        p, v = line.split(" : ")
        va[p.strip()] = v.strip()

diff = 0
with open(os.path.join(outdir, "compare_values.txt"), "w") as f:
    f.write("# position (WK BK Wpawns Bpawns side) : o68 value, ax68q value (White's point of view)\n")
    for p in positions:
        a, b = vo.get(p, "?"), va.get(p, "?")
        if a != b:
            diff += 1
        f.write("%s : %s %s%s\n" % (p, a, b, "" if a == b else "   DIFFERENT"))
print("positions compared: %d, disagreements: %d" % (len(positions), diff))
