#!/usr/bin/env python3
"""Internal consistency of the tables: the rules are invariant under (flip ranks, swap colours, swap side to move),
which sends a White-view bound pair (A, B) to (neg B, neg A).  Checks every position of each board against its mirror.
This is a consistency check of one program (COMPUTED-1), not an independent one.  From the project root:
    .venv/bin/python -I research/kpkp/t44/symmetry_check.py
"""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SQ = {'abcdefgh'[f] + str(r + 1): r * 8 + f for r in range(8) for f in range(8)}
RES = {'L': 0, 'D': 1, 'W': 2}
flip = [(7 - s // 8) * 8 + s % 8 for s in range(64)]
for board in ('cyl', 'flat'):
    code = bytearray(64 * 64 * 48 * 48 * 2)
    for i in range(4):
        p = subprocess.Popen(['zstdcat', os.path.join(HERE, 'kpkp_%s_%d.out.zst' % (board, i))],
                             stdout=subprocess.PIPE, text=True, bufsize=1 << 20)
        for line in p.stdout:
            t = line.split()
            wk, wp, bk, bp = SQ[t[0][1:]], SQ[t[1][1:]], SQ[t[2][1:]], SQ[t[3][1:]]
            code[((((wk * 64 + bk) * 48 + wp - 8) * 48 + bp - 8) << 1) + (t[4] == 'b')] = 1 + RES[t[7]] * 3 + RES[t[8]]
        p.wait()
    n = bad = missing = 0
    for idx in range(len(code)):
        c = code[idx]
        if not c:
            continue
        n += 1
        stm = idx & 1
        k = idx >> 1
        bp = k % 48 + 8
        k //= 48
        wp = k % 48 + 8
        k //= 48
        bk = k % 64
        wk = k // 64
        m = ((((flip[bk] * 64 + flip[wk]) * 48 + flip[bp] - 8) * 48 + flip[wp] - 8) << 1) + (1 - stm)
        hi, lo = divmod(c - 1, 3)
        want = 1 + (2 - lo) * 3 + (2 - hi)
        if code[m] == 0:
            missing += 1
        elif code[m] != want:
            bad += 1
    print(board, 'positions', n, 'mirror missing', missing, 'mirror differs', bad)
