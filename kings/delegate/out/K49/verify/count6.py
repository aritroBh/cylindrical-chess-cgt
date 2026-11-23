# number of legal positions (both sides to move) with the pawn on rank H-1; and whether rule B3 can ever give DUD
def fd(a, b, W): return min(abs(a - b), W - abs(a - b))
tot = 0; b3dud = 0; b3 = 0
for W in (3, 5, 6, 7, 8, 9):
    for H in (6, 7, 8):
        S = [(f, r) for r in range(H) for f in range(W)]
        kd = lambda a, b: max(fd(a[0], b[0], W), abs(a[1] - b[1]))
        for f in range(W):
            p = (f, H - 2); q = (f, H - 1); Pi = [((f + d) % W, H - 3) for d in (-1, 0, 1)]
            for wk in S:
                for bk in S:
                    if len({wk, bk, p}) < 3 or kd(wk, bk) <= 1: continue
                    chk = bk[1] == p[1] + 1 and fd(bk[0], p[0], W) == 1
                    tot += 1 + (0 if chk else 1)
                    # Black to move, B3 conditions
                    if kd(bk, p) == 1 and kd(wk, p) > 1: continue
                    if bk == q: continue
                    if kd(bk, q) == 1 and kd(wk, q) > 1 and wk != q:
                        b3 += 1
                        if min(kd(wk, x) for x in Pi) >= 1: b3dud += 1
print("positions with pawn on rank H-1, W in {3,5..9}, H in {6,7,8}:", tot)
print("B3 positions:", b3, " of which wk not in Pi (target not (on,L)):", b3dud)
