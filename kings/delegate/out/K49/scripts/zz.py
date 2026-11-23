"""K49: the Black zugzwangs Z: y_b in W_N with y_w not in P_L (so y_w in ON, by pass-closure), listed by geometry."""
import load
from collections import Counter
def cd(a, b, W): d = (a - b) % W; return min(d, W - d)
for W in (3, 5, 6, 7, 8):
    for H in (6, 8):
        t = load.load(W, H); c = Counter(); ex = {}
        for pos, k in t.items():
            if not pos.endswith('b') or k == 'DUD': continue
            kw = t.get(pos[:-1] + 'w')
            if kw != 'ON': continue
            wk, bk, p, s = pos.split()
            (wf, wr), (bf, br), (pf, pr) = map(load.sq, (wk, bk, p))
            sd = lambda f: ((f - pf + W // 2) % W) - W // 2
            key = (H - pr, sd(wf), wr - pr, sd(bf), br - pr)
            if sd(wf) < 0 or (sd(wf) == 0 and sd(bf) < 0): key = (H - pr, -sd(wf), wr - pr, -sd(bf), br - pr)
            c[(H - pr, k)] += 1
        print(W, H, sorted(c.items()))
