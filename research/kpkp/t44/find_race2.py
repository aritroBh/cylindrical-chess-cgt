#!/usr/bin/env python3
"""List cylinder-vs-flat REVERSALS (W<->L) in which the two pawns are on files h/a (or a/h) and both kings are on files d-e, i.e.
the kings are at least two files from the seam and the pawns are the only pieces that can interact across it.
Streams the tables, keeps two small bytearrays.  Run from the project root:
    .venv/bin/python -I research/kpkp/t44/find_race2.py > research/kpkp/t44/find_race2.out
"""
import os
import subprocess
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SQ = {'abcdefgh'[f] + str(r + 1): r * 8 + f for r in range(8) for f in range(8)}
RES = {'L': 0, 'D': 1, 'W': 2}


def stream(board):
    for i in range(4):
        p = subprocess.Popen(['zstdcat', os.path.join(HERE, 'kpkp_%s_%d.out.zst' % (board, i))],
                             stdout=subprocess.PIPE, text=True, bufsize=1 << 20)
        for line in p.stdout:
            yield line
        p.wait()


def key(t):
    wk, wp, bk, bp = SQ[t[0][1:]], SQ[t[1][1:]], SQ[t[2][1:]], SQ[t[3][1:]]
    return (((wk * 64 + bk) * 48 + wp - 8) * 48 + bp - 8) * 2 + (t[4] == 'b')


flat = bytearray(64 * 64 * 48 * 48 * 2)
for line in stream('flat'):
    t = line.split()
    flat[key(t)] = 1 + RES[t[7]] * 3 + RES[t[8]]
cnt = Counter()
ex = {}
for line in stream('cyl'):
    t = line.split()
    wf, bf = t[1][1], t[3][1]
    if (wf, bf) not in (('h', 'a'), ('a', 'h')):
        continue
    if t[7] != t[8] or t[0][1] not in 'de' or t[2][1] not in 'de':
        continue
    f = flat[key(t)]
    fh, fl = divmod(f - 1, 3)
    if fh != fl or abs(fh - RES[t[7]]) != 2:
        continue
    k = (wf + bf, t[4], t[1][2] + t[3][2], 'LDW'[fh] + '>' + t[7])
    cnt[k] += 1
    ex.setdefault(k, []).append(line.strip())
for k, v in sorted(cnt.items()):
    print(k, v, ex[k][len(ex[k]) // 2])
