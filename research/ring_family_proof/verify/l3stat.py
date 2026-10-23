import random, sys
from lem import *
from eng import *
from pump import cls, ins, insn
def run(kind, trials, seed):
    rng = random.Random(seed); acc = nk = nT = nPL = nmoves = nbad = 0
    for t in range(trials):
        n = rng.randint(16, 22); c = rng.randint(5, n - 7)
        pos = make(rng, kind, n, c, rng.randint(1, 4), 5)
        if passed_ranks(pos, None, 'W') or passed_ranks(pos, None, 'B'): continue
        ph = ins(pos, c); a = cls(pos, None); b = cls(ph, None); acc += 1
        for s in 'WB':
            nk += len(a[s][1]); nT += a[s][0]; nPL += sum(1 for k in a[s][2] if k in 'LP'); nmoves += len(a[s][2])
            if a[s][0] != b[s][0] or {insn((q, qe), c) for q, qe in a[s][1]} != set(b[s][1]): nbad += 1
    print(kind, 'accepted', acc, 'K-children compared', nk, 'T-flags', nT, 'L/P moves', nPL, 'all moves', nmoves, 'bad', nbad)
for k in 'OE': run(k, 20000, 7)
