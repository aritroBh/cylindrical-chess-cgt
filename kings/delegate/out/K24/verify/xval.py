"""Referee cross-validation: psolve.py (mine) vs kp_p --pmodel (K7 build of kpsolve) on random positions.
usage: xval.py BOARD N SEED NW NB   -> writes xv_<tag>.txt, runs both, prints the number of differences"""
import random, sys, subprocess
board, N, seed, nw, nb = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
W, H = map(int, board.split(":")[1].split("x"))
random.seed(seed)
def sq(s): return "abcdefgh"[s % W] + str(s // W + 1)
out = []
while len(out) < N:
    squares = random.sample(range(W * H), 2 + nw + nb)
    wk, bk = squares[:2]; wp = squares[2:2+nw]; bp = squares[2+nw:]
    if any(s // W in (0, H - 1) for s in wp + bp): continue
    toks = [f"K{sq(wk)}", f"k{sq(bk)}"] + [f"P{sq(s)}" for s in wp] + [f"p{sq(s)}" for s in bp]
    out.append(" ".join(toks) + " " + random.choice("wb") + " -")
tag = board.replace(":", "_") + f"_{seed}"
open(f"xv_{tag}.txt", "w").write("\n".join(out) + "\n")
PY = "/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python"
a = subprocess.run(["./kp_p", "--pmodel", "--board", board, "--ep", "on", "--cap", "1"], stdin=open(f"xv_{tag}.txt"), capture_output=True, text=True).stdout.strip().splitlines()
b = subprocess.run([PY, "psolve.py", board, "p"], stdin=open(f"xv_{tag}.txt"), capture_output=True, text=True).stdout.strip().splitlines()
nd = 0; nill = 0
for x, y in zip(a, b):
    rx = x.split(" | ")[1].split()[0]; ry = y.split(" | ")[1].split()[0]
    if rx == "X": nill += 1
    if rx != ry:
        nd += 1; print("DIFF", x, "||", y)
print(f"{board} seed {seed} {nw}v{nb} pawns: {len(out)} positions ({len(out)-nill} legal), differences {nd}")
