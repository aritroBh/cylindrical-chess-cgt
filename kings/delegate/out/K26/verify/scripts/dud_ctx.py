#!/usr/bin/env python3
"""Referee's own dud_D prediction (Theorem 3.4(a)) for a pawn-only context G with e.p. flag, compared with the P value
(ref3m) of G + Z at all 8 roots.
usage: dud_ctx.py GROUP BOARD FILES MAXP [i/n] [sampleN seed]"""
import sys, itertools, subprocess, random, json
from functools import lru_cache
sys.setrecursionlimit(100000)
GROUP, board, files, maxp = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
shard = sys.argv[5] if len(sys.argv) > 5 else "0/1"
si, sn = map(int, shard.split("/"))
sample = int(sys.argv[6]) if len(sys.argv) > 6 else 0
seed = int(sys.argv[7]) if len(sys.argv) > 7 else 1
cyl = board.startswith("cyl"); W, H = map(int, board.split(":")[1].split("x"))
GROUPS = {"ZB": (["b2","c3"],["a4","b5"],"Pa3 Pb4 pb3 pc4"), "ZC": (["c2","c3"],["a4","a5"],"Pa2 Pc4 pa3 pc5")}
ZW, ZB_, ZP = GROUPS[GROUP]
def fnorm(f):
    if cyl: return f % W
    return f if 0 <= f < W else None
def wmoves(wp, bp, ep):
    out = []; occ = wp | bp
    for (f, r) in wp:
        if (f, r + 1) not in occ:
            if r + 1 == H - 1: out.append('W')
            else:
                out.append((wp - {(f, r)} | {(f, r + 1)}, bp, None))
                if r == 1 and (f, r + 2) not in occ:
                    out.append((wp - {(f, r)} | {(f, r + 2)}, bp, (f, r + 1)))
        for df in (-1, 1):
            g = fnorm(f + df)
            if g is None: continue
            t = (g, r + 1)
            if t in bp:
                if r + 1 == H - 1: out.append('W')
                else: out.append(((wp - {(f, r)}) | {t}, bp - {t}, None))
            elif ep == t and (g, r) in bp:
                out.append(((wp - {(f, r)}) | {t}, bp - {(g, r)}, None))
    return out
def bmoves(wp, bp, ep):
    out = []; occ = wp | bp
    for (f, r) in bp:
        if (f, r - 1) not in occ:
            if r - 1 == 0: out.append('B')
            else:
                out.append((wp, bp - {(f, r)} | {(f, r - 1)}, None))
                if r == H - 2 and (f, r - 2) not in occ:
                    out.append((wp, bp - {(f, r)} | {(f, r - 2)}, (f, r - 1)))
        for df in (-1, 1):
            g = fnorm(f + df)
            if g is None: continue
            t = (g, r - 1)
            if t in wp:
                if r - 1 == 0: out.append('B')
                else: out.append((wp - {t}, (bp - {(f, r)}) | {t}, None))
            elif ep == t and (g, r) in wp:
                out.append((wp - {(g, r)}, (bp - {(f, r)}) | {t}, None))
    return out
# Theorem 3.4(a): Lambda_L (White to move wins), Lambda_R (Black to move, White wins); Rho_R (Black to move wins), Rho_L (White to move, Black wins)
@lru_cache(maxsize=None)
def LamL(x):
    for o in wmoves(*x):
        if o == 'W': return True
        if o != 'B' and LamR(o): return True
    return False
@lru_cache(maxsize=None)
def LamR(x):
    if not LamL(x): return False
    for o in bmoves(*x):
        if o == 'B': return False
        if o != 'W' and not LamL(o): return False
    return True
@lru_cache(maxsize=None)
def RhoR(x):
    for o in bmoves(*x):
        if o == 'B': return True
        if o != 'W' and RhoL(o): return True
    return False
@lru_cache(maxsize=None)
def RhoL(x):
    if not RhoR(x): return False
    for o in wmoves(*x):
        if o == 'W': return False
        if o != 'B' and not RhoR(o): return False
    return True
def pred(wp, bp):
    x = (frozenset(wp), frozenset(bp), None)
    def v(stm):
        if stm == 0: return 'W' if LamL(x) else ('L' if RhoL(x) else 'D')
        return 'W' if LamR(x) else ('L' if RhoR(x) else 'D')
    return v(0) + v(1)
fl = [ord(c) - 97 for c in files]
sqs = [(f, r) for f in fl for r in range(1, H - 1)]
def contexts():
    yield (), ()
    for k in range(1, maxp + 1):
        for cells in itertools.combinations(sqs, k):
            for cols in itertools.product((0, 1), repeat=k):
                yield tuple(c for c, o in zip(cells, cols) if o == 0), tuple(c for c, o in zip(cells, cols) if o == 1)
allc = list(contexts())
if sample:
    random.Random(seed).shuffle(allc); allc = allc[:sample]
allc = allc[si::sn]
def nm(s): return chr(97 + s[0]) + str(s[1] + 1)
lines = []; meta = []
for wp, bp in allc:
    ps = ZP + "".join(" P" + nm(s) for s in wp) + "".join(" p" + nm(s) for s in bp)
    for w in ZW:
        for b in ZB_:
            for stm in "wb":
                lines.append(f"K{w} k{b} {ps} {stm} -")
    meta.append((wp, bp))
bd = board if cyl else board.replace(":", "")
CH = 800  # roots per ref3m process
res = []
for i in range(0, len(lines), CH):
    o = subprocess.run(["bin/ref3m", "--board", bd, "--moves" if False else "--board", bd], input="\n".join(lines[i:i + CH]) + "\n", capture_output=True, text=True).stdout.splitlines()
    res += [l for l in o if " | " in l]
assert len(res) == len(lines)
bad = []; nroots = 0; ndiff = 0; byk = {}
for ci, (wp, bp) in enumerate(meta):
    vals = [res[8 * ci + j].rsplit("| ", 1)[1].strip() for j in range(8)]
    p = pred(wp, bp)  # White-to-move value, Black-to-move value
    exp = [p[0] if j % 2 == 0 else p[1] for j in range(8)]   # roots ordered (w,b,stm): stm alternates w,b
    nroots += 8
    d = sum(1 for a, b in zip(vals, exp) if a != b)
    if d:
        ndiff += d; bad.append(("W" + ",".join(map(nm, wp)), "B" + ",".join(map(nm, bp)), "".join(vals), "".join(exp)))
        k = len(wp) + len(bp); byk[k] = byk.get(k, 0) + 1
print(GROUP, board, files, "<=%dp" % maxp, "shard", shard, "contexts", len(meta), "roots", nroots, "roots differing", ndiff, "contexts differing", len(bad), "by #pawns", byk)
for b in bad[:12]: print("  ", b)
json.dump({"ctx": len(meta), "bad": bad}, open(f"logs/ctx_{GROUP}_{board.replace(':','')}_{files}_{maxp}_{si}of{sn}_{sample}.json", "w"))
