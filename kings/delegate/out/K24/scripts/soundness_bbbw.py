"""Soundness test of the transfer lemma (bb, bw) against kpsolve's exact chess values.
bb: all promotions win for White.  If bb(X) != W (White cannot force a win there) then White cannot win chess: kpsolve's
lower bound must not be W.  bw: all promotions win for Black.  If bw(X) != L then kpsolve's upper bound must not be L.
usage: soundness_bbbw.py BOARD N SEED   (run from K24)"""
import subprocess, sys, re
board, N, seed = sys.argv[1], sys.argv[2], sys.argv[3]
W, H = map(int, board.split(":")[1].split("x"))
PY = "/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python"
pos = subprocess.run([PY, "scripts/gen_random.py", str(W), str(H), N, seed], capture_output=True, text=True, check=True).stdout
def mine(model):
    out = subprocess.run(["nice", "-n", "15", "./mine", "--board", board, "--model", model], input=pos, capture_output=True, text=True, check=True).stdout
    return [l.rsplit(" | ", 1)[1] for l in out.strip().splitlines()]
bb, bw, pm = mine("bb"), mine("bw"), mine("p")
kp = subprocess.run(["/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh", "./kp", "--board", board, "--ep", "on", "--promote", "QRBN", "--cap", "1"],
                    input=pos, capture_output=True, text=True, check=True).stdout.strip().splitlines()
lines = pos.strip().splitlines()
n = viol1 = viol2 = tight1 = tight2 = legal = 0
for p, a, b, m, k in zip(lines, bb, bw, pm, kp):
    if a == "X": continue
    legal += 1
    lo, hi = k.rsplit(" | ", 1)[1].split()
    if a != "W" and lo == "W": viol1 += 1; print("VIOLATION bb", p, a, k)
    if b != "L" and hi == "L": viol2 += 1; print("VIOLATION bw", p, b, k)
    if a != "W" and lo != "W": tight1 += 1   # bb says "White cannot win"
    if b != "L" and hi != "L": tight2 += 1
print(f"{board} seed {seed}: {legal} legal positions; violations bb {viol1}, bw {viol2}; "
      f"bb gives 'White cannot win' on {tight1} positions, bw gives 'Black cannot win' on {tight2}; "
      f"kpsolve exact (lo==hi) on {sum(1 for k in kp if '|' in k and k.rsplit(' | ',1)[1].split()[0:1]==k.rsplit(' | ',1)[1].split()[1:2])}")
