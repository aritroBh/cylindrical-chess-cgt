import sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/scripts')
import pyp
spec, posf, resf = sys.argv[1:4]
B = pyp.Board(spec)
n = bad = 0
from collections import Counter
c = Counter()
for lp, lr in zip(open(posf), open(resf)):
    lp = lp.strip(); r = lr.strip().split(" | ")
    A, Bv = r[1].split()
    mine = pyp.solve(B, pyp.parse(B, lp))
    n += 1
    c[mine] += 1
    if not (A == Bv == mine):
        bad += 1; print("MISMATCH", lp, "kpp", A, Bv, "pyp", mine)
print("xval", spec, "n", n, "mismatches", bad, dict(c))
