"""Position-by-position comparison of replica and egt_prototype.c tables.

Usage: python3 compare_positions.py <replica.dump> <prototype.dump> <np>

replica dump: int16 white-to-move values then int16 black-to-move values, in
plies (-1 draw, -2 illegal). prototype dump (a copy of egt_prototype.c that
writes its arrays): int8 values in moves; white > 0 won in n moves, black >= 0
lost with white mating in n more moves, -1 or -3 (stalemate) draw, -2 illegal.
Both index positions as ((wk*64 + bk)*64 + p1)*64 + p2.
"""
import sys

import numpy as np

rep_path, pro_path, np_men = sys.argv[1], sys.argv[2], int(sys.argv[3])
n = 64 ** (np_men + 2)
rep = np.fromfile(rep_path, dtype=np.int16)
pro = np.fromfile(pro_path, dtype=np.int8).astype(np.int16)
assert rep.size == 2 * n and pro.size == 2 * n, (rep.size, pro.size, n)
rw, rb, pw, pb = rep[:n], rep[n:], pro[:n], pro[n:]

# replica in plies -> moves; draws and illegal kept as -1 / -2
rw_m = np.where(rw >= 0, (rw + 1) // 2, rw)
rb_m = np.where(rb >= 0, rb // 2, rb)
pb_m = np.where(pb == -3, -1, pb)  # stalemate is a draw

bad_w = np.flatnonzero(rw_m != pw)
bad_b = np.flatnonzero(rb_m != pb_m)
print(f"wtm positions {n}: {bad_w.size} differ; btm positions {n}: {bad_b.size} differ")


def show(i):
    p = []
    for _ in range(np_men):
        p.append(i % 64)
        i //= 64
    bk, wk = i % 64, i // 64
    sq = lambda s: "abcdefgh"[s % 8] + str(s // 8 + 1)
    return f"K{sq(wk)} " + " ".join(sq(s) for s in reversed(p)) + f" k{sq(bk)}"


for i in bad_w[:5]:
    print(f"  wtm {show(int(i))}: replica {rw_m[i]} prototype {pw[i]}")
for i in bad_b[:5]:
    print(f"  btm {show(int(i))}: replica {rb_m[i]} prototype {pb_m[i]}")
sys.exit(1 if bad_w.size or bad_b.size else 0)
