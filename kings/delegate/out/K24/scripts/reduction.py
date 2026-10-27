"""K24: chess (C) value of P6 and of the Black-to-move entry of P7 by REDUCTION to king-and-pawn versus king.

Method (every step is an enumeration):
  1. list every legal move of the side to move in the bare group (mine --moves; legal moves do not depend on the model);
  2. after each move check that the enemy king's capture of the group's pawn is legal (mine --moves on the new position);
  3. after that capture the mover has a bare king and the capturer has a king and one pawn: look the position up in the
     exact KQK + KPK tables (kpk2, queen promotion only; a table win is a chess win because the loser has no pawn).
Run from the K24 directory:  .venv/bin/python scripts/reduction.py
"""
import subprocess

def run(cmd, text):
    return subprocess.run(cmd, input=text, capture_output=True, text=True, check=True).stdout

def moves(board, pos):
    out = run(["./mine", "--board", board, "--model", "p", "--moves"], pos + "\n").strip().splitlines()[-1]
    rest = out.split(" | ", 2)
    return rest[1], [m.split(":")[0] for m in rest[2].split()]

TASKS = {
    "cyl:8x8": [("P6, White to move", "Kh5 Pa4 kb4 pa5 w -", "a4", "-", "a5"),
                ("P6, Black to move", "Kh5 Pa4 kb4 pa5 b -", "a5", "+", "a4"),
                ("P7, Black to move", "Ke6 Pd7 kd8 pe7 b -", "e7", "+", "d7")],
    "flat:8x8": [("P7, Black to move", "Ke6 Pd7 kd8 pe7 b -", "e7", "+", "d7")],
    "cyl:7x6": [("P5, Black to move (Z_72, 6 ranks)", "Kc4 Pb5 kb6 pc5 b -", "c5", "+", "b5")],
}
allok = True
for board, tasks in TASKS.items():
    W, Hh = map(int, board.split(":")[1].split("x")); wrap = 1 if board.startswith("cyl") else 0
    queries, meta = [], []
    for label, root, capsq, dirn, cpawn in tasks:
        toks = root.split(); white = toks[-2] == "w"
        res, mv = moves(board, root)
        print(f"--- {board} {label}: {root}   P-value {res}; legal moves {mv}")
        for name in mv:
            if not name.startswith("K") or "=" in name:
                print(f"    {name}: not a king move, reduction does not apply"); allok = False; continue
            dest = name[3:5]
            nt = [("K" if white else "k") + dest if t[0] == ("K" if white else "k") else t for t in toks[:-2]]
            newpos = " ".join(nt) + (" b -" if white else " w -")
            _, mv2 = moves(board, newpos)
            cap = [m for m in mv2 if m.startswith("K") and m.endswith(capsq)]
            if not cap:
                print(f"    {name}: capture on {capsq} NOT legal"); allok = False; continue
            queries.append(f"{dirn} {capsq} {dest} {cpawn} D"); meta.append((label, name, cap[0], queries[-1]))
    out = run(["./kpk2", str(W), str(Hh), str(wrap)], "\n".join(queries) + "\n").strip().splitlines()
    for (label, name, cap, q), line in zip(meta, out):
        r = line.rsplit(" | ", 1)[1]
        print(f"    [{label}] {name}, reply {cap}: KPK [{q}] -> {r}")
        if r != "W": allok = False
print("EVERY MOVE ANSWERED BY THE CAPTURE AND A WON KPK:", allok)
