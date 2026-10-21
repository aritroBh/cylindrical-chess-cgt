import sys, time
sys.path.insert(0, '.')
import indep as I
cases = [
 (I.Board(8,8,True,False), "W: b2 d4 g3 h5 / B: a7 c7 f7 g4", "count", "R", "N"),
 (I.Board(8,8,True,True),  "W: a5 b6 d2 e2 / B: a7 c7 e7", "count", "L", "N"),
 (I.Board(8,8,True,False), "W: b3 f4 g5 / B: a5 b6 f5 h6", "count", "N", "L"),
 (I.Board(8,7,True,False), "W: c2 g2 h4 / B: a5 b6 f5 g6", "count", "R", "N"),
 (I.Board(4,5,False,False),"W: a2 c2 / B: a4 d4", "count", None, None),
 (I.Board(4,8,False,True), "W: a2 c2 / B: b7 d7", "count", "N", "N"),
 (I.Board(4,8,False,True), "W: a2 c2 / B: b7 d7", "opponent", "P", "P"),
]
for bd, t, rule, expS, expW in cases:
    t0=time.time(); x = I.parse(t)
    a = I.analyse(bd, x)
    s = I.oS(bd, x, rule); w = I.oW(bd, x, rule)
    print(bd, t, rule, "oS", s, "oW", w, "exp", expS, expW, {k:a[k] for k in ('HSS','E','split','nontrivial','bothsigns')}, f"{time.time()-t0:.1f}s")
