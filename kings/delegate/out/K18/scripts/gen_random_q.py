#!/usr/bin/env python3
"""random local-game positions Q (White = s to move, Black king on F_Z) for the cross-check of lg vs lg2."""
import random, sys
board, fz0, fzn, n, nep, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
random.seed(seed)
kind, dims = board.split(":"); CYL = kind == "cyl"; W, H = map(int, dims.split("x"))
fz = [(fz0 + i) % W for i in range(fzn)]
def nb(f, d):
    g = f + d
    return g % W if CYL else (g if 0 <= g < W else None)
def adjk(a, b):
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            g = nb(a[0], df)
            if g is not None and (g, a[1] + dr) == b: return True
    return False
def attacked_by_white(sq, wp):
    f, r = sq
    return any(nb(f, d) is not None and (nb(f, d), r - 1) in wp for d in (-1, 1))
def name(s): return "abcdefgh"[s[0]] + str(s[1] + 1)
sq_p = [(f, r) for f in fz for r in range(1, H - 1)]
out = []
tries = 0
while len(out) < n + nep:
    tries += 1
    isep = len(out) >= n
    nw, nbk = random.randint(0, 2), random.randint(0, 2)
    ws = set(random.sample(sq_p, nw)); bs = set(random.sample([s for s in sq_p if s not in ws], nbk))
    ep = None
    if isep:
        f = random.choice(fz); r = H - 4
        bs |= {(f, r)}; ep = (f, r + 1)
        side = random.choice((-1, 1)); g = nb(f, side)
        if g is None or g not in fz: continue
        ws |= {(g, r)}
        if (f, r + 1) in ws | bs or (f, r + 2) in ws | bs or (f, H-2) in ws|bs and False: continue
        if len(ws) > 2 or len(bs) > 2: continue
    allsq = [(f, r) for f in range(W) for r in range(H)]
    wk = random.choice([s for s in allsq if s not in ws | bs])
    bk = random.choice([s for s in [(f, r) for f in fz for r in range(H)] if s not in ws | bs and s != wk])
    if adjk(wk, bk): continue
    if attacked_by_white(bk, ws): continue
    if ep and (ep in (wk, bk)): continue
    # promotion squares sanity: no pawn on last/first rank by construction
    line = "K%s %s k%s %s w %s" % (name(wk), " ".join("P" + name(s) for s in sorted(ws)), name(bk), " ".join("p" + name(s) for s in sorted(bs)), name(ep) if ep else "-")
    out.append(" ".join(line.split()))
print("\n".join(out))
