"""Sample comparison of ring.c's value class (0,*1,*2,*3,other) with cylcgt.value, after the counts were done.
usage: cmp_cylcgt_sample.py  c3_all.txt c4_all.txt [MULT]  (files written by ring.c --all; MULT scales the sample)"""
import sys, random, time
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos, value
rnd = random.Random(2026)
MULT = int(sys.argv[3]) if len(sys.argv) > 3 else 1
NAMES = {0: "0", 1: "*", 2: "*2", 3: "*3"}
def cls(v):
    for h in range(4):
        if not (v >> 2 * h) & 1 and not (v >> (2 * h + 1)) & 1: return NAMES[h]
    return None
def load(fn):
    rows = []
    for line in open(fn):
        np_, v, s = line.rstrip("\n").split("\t"); rows.append((int(np_), int(v), s))
    return rows
bad = tot = 0; t0 = time.time()
for fn, n, plan in [(sys.argv[1], 3, {4: 8, 5: 10, 6: 30}), (sys.argv[2], 4, {4: 8, 5: 10, 6: 14, 7: 16})]:
    rows = load(fn)
    for np_, k in plan.items():
        grp = [r for r in rows if r[0] == np_]
        pick = []
        for want in ["0", "*", "*2", None]:      # stratified: each value class of mine
            g = [r for r in grp if cls(r[1]) == want]
            pick += rnd.sample(g, min(len(g), max(1, k * MULT // 4)))
        for _, v, s in pick:
            g = value(Board(n, 8, True, True), Pos.parse(s)); sh = cgt.show(g)
            mine = cls(v); tot += 1
            ok = (mine == sh) if mine else (sh not in NAMES.values())
            if not ok:
                bad += 1; print("DISAGREE", n, s, "mine", mine, "cylcgt", sh, flush=True)
        print("n=%d pawns=%d compared %d, running disagreements %d, %.0fs" % (n, np_, len(pick), bad, time.time() - t0), flush=True)
print("TOTAL compared", tot, "disagreements", bad)
