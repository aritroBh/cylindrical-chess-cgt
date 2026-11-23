"""Bounded targeted sample with a double-step motif on three files."""
import random
from functools import cache
from itertools import combinations
from pawns_check import board, args, pawns, cgt, assess, wins, passers, conditions

cgt.integer = cache(cgt.integer)
rng = random.Random(5401)
contexts = []
for n in range(2,board.ranks-1):
    for occupied in combinations([(4,r) for r in range(2,board.ranks)],n):
        for k in range(1,n):
            for w in combinations(occupied,k):
                g = pawns.Pos(frozenset(w),frozenset(occupied)-set(w))
                if not passers(g):
                    contexts.append(g)
tests = 0
for i in range(30000):
    a,b = rng.choice(((0,1),(1,0),(1,2),(2,1)))
    free = [(f,r) for f in range(3) for r in range(2,board.ranks)
            if (f,r) not in ((a,2),(a,3),(a,4),(b,4))]
    n = rng.randint(2, min(7,len(free)))
    k = rng.randrange(1,n)
    chosen = rng.sample(free,n)
    A = pawns.Pos(frozenset([(a,2),*chosen[:k]]),frozenset([(b,4),*chosen[k:]]))
    if passers(A) or len({f for f,r in A.white|A.black})!=3:
        continue
    if i%100==0:
        pawns._value.cache_clear()
        pawns.race_hits.clear()
    for g in rng.sample(contexts,min(4,len(contexts))):
        p = pawns.Pos(A.white|g.white,A.black|g.black)
        s = cgt.outcome(pawns.value(board,p))
        tests+=1
        if (wins(p,"W"),wins(p,"B")) != (s in ("L","N"),s in ("R","N")):
            kind, pair = assess(p)
            if kind == "late":
                print("witness",p,kind,pair,"candidate",i,"evaluations",tests,flush=True)
                raise SystemExit
print("finished",board.ranks,args.rule,tests)
