import sys, time
sys.path.insert(0, '.')
import mycgt as C, mypawns as P
tests = [
 (("flat",), "W: a2 c2 / B: b7 d7"),
 (("ring",4), "W: a2 c2 / B: b7 d7"),
 (("ring",3), "W: a2 b4 / B: b7 c6"),
 (("ring",3), "W: a2 b3 / B: a5 c7"),
 (("ring",3), "W: a2 b2 / B: c5 c6"),
 (("ring",3), "W: a2 a3 b2 / B: b6 c7"),
 (("flat",), "W: a2 / B: a5"),
 (("flat",), "W: a2 / B: a4"),
 (("flat",), "W: a2 b4 / B: a5 b7"),
]
for g,t in tests:
    t0=time.time()
    W,B = P.parse(t)
    v,re = P.start_value(g,W,B)
    print(g, t, C.key(v), C.has_big(v), re, f"{time.time()-t0:.2f}s")
