# fortresses: x (+) on with Kxp scored as a Black win, result D; geometry of the kings relative to the pawn
import sys, subprocess
from collections import Counter
for b in sys.argv[1:]:
    W, H = map(int, b.split("x"))
    out = subprocess.run(["./vk", str(W), str(H), "t/on.t", "-k"], capture_output=True, text=True).stdout.split("\n")
    F = [l.split() for l in out if l and l.split()[4] == "D"]
    g = Counter()
    def fd(a, b): return min(abs(a - b), W - abs(a - b))
    for wk, p, bk, s, _ in F:
        fw, fp, fb = ord(wk[1]) - 97, ord(p[1]) - 97, ord(bk[1]) - 97
        back = (W - 1) // 2
        g[(s, fd(fw, fp) == back and fd(fb, fp) == back, "same" if fw == fb else "diff", abs(int(wk[2:]) - int(bk[2:])) >= 2)] += 1
    print(f"cyl:{b}: {len(F)} fortress positions; (side, both kings on back files, same/diff file, rank distance>=2): {dict(g)}", flush=True)
