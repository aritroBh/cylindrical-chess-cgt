#!/usr/bin/env python3
"""Referee's own search for exact UNDER groups (U1)-(U4) of the proposed Definition 4.8 (no use of Lemma 4.9).
usage: ref_under.py BOARD nW nB NFILES [i/n]
White king shuttles on an adjacent pair z in F_Z; Black king on ONE square b0 (K1; K2 vs both z squares); <=nW White, <=nB Black pawns on F_Z ranks 2..H-1.
(U1) at both White-to-move roots: shuttle legal and every other White move loses at once (value L after it).
(U2) at both Black-to-move roots: some Black move does not lose at once (value after != W) = freeze.
     A freeze that is a promotion is recorded separately (decisive event, q undefined) and makes the placement NOT exact.
(U3) after every freeze: q (with e.p. flag if a double step), White to move: >=1 legal move, all White moves have value L.
(U4) same q, Black to move (no flag): q legal, >=1 legal move, every Black move has value W.
"""
import sys, itertools, subprocess, os, json
board, nW, nB, NF = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
shard = sys.argv[5] if len(sys.argv) > 5 else "0/1"
si, sn = map(int, shard.split("/"))
cyl = board.startswith("cyl"); W, H = map(int, board.split(":")[1].split("x"))
FILES = list(range(NF))
def fd(a, b):
    d = abs(a - b); return min(d, W - d) if cyl else d
def kdist(s, t): return max(fd(s[0], t[0]), abs(s[1] - t[1]))
def name(s): return chr(97 + s[0]) + str(s[1] + 1)
def unname(n): return (ord(n[0]) - 97, int(n[1:]) - 1)
kingsq = [(f, r) for f in FILES for r in range(H)]
pairs = [(s, t) for i, s in enumerate(kingsq) for t in kingsq[i + 1:] if kdist(s, t) == 1]
pawnsq = [(f, r) for f in FILES for r in range(1, H - 1)]
def subsets(n):
    for k in range(n + 1): yield from itertools.combinations(pawnsq, k)
def attacked_by(pawns, color, sq):
    d = 1 if color == 0 else -1
    return any(r + d == sq[1] and fd(f, sq[0]) == 1 for (f, r) in pawns)
def placements():
    for wp in subsets(nW):
        for bp in subsets(nB):
            if set(wp) & set(bp): continue
            occ = set(wp) | set(bp)
            wpairs = [p for p in pairs if not (set(p) & occ) and not any(attacked_by(bp, 1, s) for s in p)]
            bsqs = [s for s in kingsq if s not in occ and not attacked_by(wp, 0, s)]
            for wz in wpairs:
                for b0 in bsqs:
                    if all(kdist(s, b0) >= 2 for s in wz): yield wp, bp, wz, b0
def pstr(wp, bp, extra=()):
    return " ".join(["P" + name(s) for s in wp] + ["p" + name(s) for s in bp])
bd = board if cyl else board.replace(":", "")
def solve(lines):
    if not lines: return []
    o = subprocess.run(["bin/ref3m", "--board", bd, "--moves"], input="\n".join(lines) + "\n", capture_output=True, text=True).stdout.splitlines()
    o = [l for l in o if " | " in l]
    assert len(o) == len(lines)
    out = []
    for l in o:
        t = l.partition(" | ")[2].split()
        out.append((t[0], [x.rsplit(":", 1) for x in t[1:]]))
    return out

rows = list(placements())
rows = rows[si::sn]
cnt = {"placements": len(rows), "U1": 0, "on_strong": 0, "on_weak": 0}
exact = []
CH = 40000
for a in range(0, len(rows), CH):
    part = rows[a:a + CH]
    L1 = []
    for (wp, bp, wz, b0) in part:
        for zi in (0, 1):
            L1.append(f"K{name(wz[zi])} k{name(b0)} {pstr(wp,bp)} w -")
            L1.append(f"K{name(wz[zi])} k{name(b0)} {pstr(wp,bp)} b -")
    R = solve(L1)
    for k, (wp, bp, wz, b0) in enumerate(part):
        okw = True; okb = True
        for zi in (0, 1):
            rv, mv = R[4 * k + 2 * zi]
            shut = "K" + name(wz[zi]) + name(wz[1 - zi])
            if rv == "X" or [m for m, v in mv].count(shut) != 1 or any(v != "L" for m, v in mv if m != shut): okw = False
            rv, mv = R[4 * k + 2 * zi + 1]
            if rv == "X" or not mv or any(v != "W" for m, v in mv): okb = False
        if okw: cnt["U1"] += 1
        if okb: cnt["on_weak"] += 1
        if okw and okb:
            cnt["on_strong"] += 1; exact.append([list(map(name, wp)), list(map(name, bp)), list(map(name, wz)), name(b0)])
print(board, nW, nB, "files", NF, "shard", shard, json.dumps(cnt))
json.dump({"cnt": cnt, "exact": exact}, open(f"logs/on_{board.replace(':','')}_{nW}{nB}_f{NF}_{si}of{sn}.json", "w"))
