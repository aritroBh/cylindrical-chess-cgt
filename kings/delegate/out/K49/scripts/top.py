"""K49: classes of positions with the pawn d ranks below promotion (d = H - pawn rank), by relative king squares.
Usage: python top.py d"""
import load, sys
from collections import defaultdict
d = int(sys.argv[1])
def rel(f, pf, W): return ((f - pf + W // 2) % W) - W // 2
for W in (3, 5, 6, 7, 8):
    for H in (6, 8):
        t = load.load(W, H); g = defaultdict(set)
        for pos, k in t.items():
            wk, bk, p, s = pos.split()
            (wf, wr), (bf, br), (pf, pr) = map(load.sq, (wk, bk, p))
            if H - pr != d: continue
            g[(s, k)].add((rel(wf, pf, W), wr - pr, rel(bf, pf, W), br - pr))
        for (s, k), v in sorted(g.items()):
            if k != 'DEC': print(W, H, s, k, len(v), sorted(v) if len(v) < 40 else '')
