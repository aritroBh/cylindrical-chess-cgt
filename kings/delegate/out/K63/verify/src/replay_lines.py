"""K63 referee: replay lines of play from the investigator's logs/lines_h22.out move by move with
realchess.movegen (chess legality; in P the game ends at the first promotion), print the board after every
move, and write every position on the line (in pk's piece notation) for a value check by src/pk.cpp.
Usage (repository root):
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python kings/delegate/out/K63/verify/src/replay_lines.py gen N1 N2 ...
      (N = line numbers of logs/lines_h22.out, 1-based; writes verify/logs/replay_pk.in, prints the replay)
"""
import sys
from realchess import movegen as mg

V = "kings/delegate/out/K63/verify"
LINES = open("kings/delegate/out/K63/logs/lines_h22.out").read().split("\n")

def pieces_to_fen(pcs, stm):
    b = [["."] * 8 for _ in range(8)]
    for p in pcs.split():
        b[int(p[2]) - 1]["abcdefgh".index(p[1])] = p[0]
    rows = []
    for r in range(7, -1, -1):
        s, n = "", 0
        for c in b[r]:
            if c == ".": n += 1
            else:
                if n: s += str(n); n = 0
                s += c
        rows.append(s + (str(n) if n else ""))
    return "/".join(rows) + f" {stm} - - 0 1"

def fen_to_pieces(fen):
    rows = fen.split()[0].split("/")
    out = {"K": [], "k": [], "P": [], "p": []}
    for i, row in enumerate(rows):
        f = 0
        for ch in row:
            if ch.isdigit(): f += int(ch); continue
            out.setdefault(ch, []).append(f"{ch}{'abcdefgh'[f]}{8 - i}"); f += 1
    other = [x for k, v in out.items() if k not in "KkPp" for x in v]
    return " ".join(out["K"] + out["k"] + out["P"] + out["p"] + other), fen.split()[1]

def board(fen):
    rows = fen.split()[0].split("/")
    return "\n".join("    " + "".join("." * int(c) if c.isdigit() else c for c in row) for row in rows)

pk_in = []
for n in map(int, sys.argv[2:]):
    L = LINES[n - 1]
    head, rest = L.split(" | ", 1)
    toks = head.split()
    stm = toks[-2]
    pcs = " ".join(toks[:-2])
    mv = rest.split("line: ")[1].split()
    fen = pieces_to_fen(pcs, stm)
    pos = mg.parse_fen(fen)
    print(f"=== line {n}: {pcs} {'Black' if stm == 'b' else 'White'} to move; claimed value {rest.split()[0]}")
    print(board(fen))
    pk_in.append(f"{pcs} {stm} -")
    kh2 = False
    for i, m in enumerate(mv):
        u = m.lstrip(".").replace("x", "").replace("=promotes", "")
        u = u[1:5].lower()
        prom = m.endswith("=promotes")
        cand = [x for x in mg.legal_moves(pos) if x.uci()[:4] == u]
        if not cand:
            print(f"  ILLEGAL move {i + 1}: {m}"); break
        x = cand[0]
        if m.startswith("...k") and u[2:] == "h2" and "P" == pos.board[mg.sq("h2")]:
            kh2 = True
        mover = "Black" if pos.stm == "b" or getattr(pos, "stm", None) == mg.BLACK else "White"
        cap = mg.is_capture(pos, x)
        pos = mg.make(pos, x)
        f2 = mg.to_fen(pos, "pseudo", clocks=False)
        print(f"  {i + 1:2d}. {m:16s} legal{'  capture' if cap else ''}{'  PROMOTION: game over in P' if prom else ''}")
        if prom:
            assert len(x.uci()) == 5, "promotion flag but no promotion"
            break
        pc2, s2 = fen_to_pieces(f2 + " 0 1")
        pk_in.append(f"{pc2} {s2} -")
    print(board(mg.to_fen(pos, "pseudo", clocks=False)))
    print(f"  Black king captured a White pawn on h2 on this line: {kh2}\n")
    pk_in.append("")
open(f"{V}/logs/replay_pk.in", "w").write("\n".join(pk_in) + "\n")
