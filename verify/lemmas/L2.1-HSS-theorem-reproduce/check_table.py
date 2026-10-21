"""Check indep_l21 against the counterexample table of notes/lemmas.md section 2 (o(S), o(W), HSS)."""
import sys, time
sys.path.insert(0, ".")
from indep_l21 import B, o_S, o_W, analyse, FILES

def parse(t):
    w, b = t.split("/")
    sq = lambda s: (FILES.index(s[0]), int(s[1:]))
    return (frozenset(map(sq, w.split(":")[1].split())), frozenset(map(sq, b.split(":")[1].split())), None)

rows = [
 ((8,8,True,False), "W: b2 d4 g3 h5 / B: a7 c7 f7 g4", "count", "R", "N"),
 ((8,8,True,False), "W: b3 f4 g5 / B: a5 b6 f5 h6", "count", "N", "L"),
 ((8,8,True,False), "W: b2 c5 d4 f3 / B: c7 d6 e7 g6", "count", "L", "N"),
 ((8,8,True,True),  "W: a2 c4 e4 h2 / B: a6 b5 d7 e7", "count", "R", "N"),
 ((8,8,True,True),  "W: a5 b6 d2 e2 / B: a7 c7 e7", "count", "L", "N"),
 ((8,7,True,False), "W: c2 g2 h4 / B: a5 b6 f5 g6", "count", "R", "N"),
 ((7,6,False,True), "W: b2 d3 f2 / B: c4 c5 e5 g5", "count", "N", "R"),
 ((8,8,True,True),  "W: a3 e2 e4 h6 / B: a4 a5 f5 g7", "opponent", "N", "L"),
 ((6,8,False,False),"W: b2 d4 f4 / B: b7 c5 e5 e7", "opponent", "R", "N"),
 ((4,5,False,False),"W: a2 c2 / B: a4 d4", "count", "N", "N"),
 ((4,8,False,True), "W: a2 c2 / B: b7 d7", "count", "N", "N"),
]
for bdt, t, rule, es, ew in rows:
    t0 = time.time()
    bd = B(*bdt); p = parse(t)
    s, w = o_S(bd, p, rule), o_W(bd, p, rule)
    h, E, nt = analyse(bd, p)
    print(f"{bd} {t} {rule}: o(S)={s} (table {es}) o(W)={w} (table {ew}) HSS={h} E={E} nontrivial={nt} "
          f"{'OK' if (s, w) == (es, ew) else 'MISMATCH'} [{time.time()-t0:.1f}s]", flush=True)
