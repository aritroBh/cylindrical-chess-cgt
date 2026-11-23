#!/usr/bin/env python3
"""Validation 1: tw (C) vs cylcgt (whole-board model, components=[p]) on random positions.
usage (project root): PYTHONPATH=. .venv/bin/python research/tall_boards/validate.py R NPOS SEED [maxp] [tlim] outprefix
Writes outprefix.eval (C input) and outprefix.py (python signatures); the shell step runs tw and diffs."""
import sys, random, signal, time
from cylcgt import pawns, cgt
sys.setrecursionlimit(1000000)
pawns.components = lambda bd, p: [p]
R = int(sys.argv[1]); N = int(sys.argv[2]); seed = int(sys.argv[3]); maxp = int(sys.argv[4]); tlim = int(sys.argv[5]); out = sys.argv[6]
rnd = random.Random(seed * 1000 + R)
names = lambda L: " ".join(f"{chr(97+f)}{r}" for f, r in sorted(L, key=lambda x: (x[1], x[0])))
def passed(F, wrap, W, B):
    def nb(f):
        return [(f + d) % F if wrap else f + d for d in (-1, 0, 1) if wrap or 0 <= f + d < F]
    for f, r in W:
        if not any(g in nb(f) and s > r for g, s in B): return True
    for f, r in B:
        if not any(g in nb(f) and s < r for g, s in W): return True
    return False
def gen():
    while True:
        F = rnd.choice([3, 3, 4, 5]); wrap = rnd.random() < .5
        if F * R > 64: continue
        p = rnd.randint(3, maxp)
        nw = rnd.randint(1, p - 1); nb = p - nw
        sw = [(f, r) for f in range(F) for r in range(2, R - 1)]; sb = [(f, r) for f in range(F) for r in range(3, R)]
        W = rnd.sample(sw, min(nw, len(sw))); B = rnd.sample(sb, min(nb, len(sb)))
        if set(W) & set(B): continue
        if passed(F, wrap, W, B): continue
        return F, wrap, W, B
class TO(Exception): pass
def alarm(*a): raise TO()
signal.signal(signal.SIGALRM, alarm)
ev = open(out + ".eval", "w"); py = open(out + ".py", "w")
done = to = 0; t0 = time.time()
while done < N:
    F, wrap, W, B = gen()
    text = f"W: {names(W)} / B: {names(B)}"
    b = pawns.Board(F, R, wrap, True)
    pos = pawns.Pos.parse(text)
    signal.alarm(tlim)
    try:
        g = pawns.value(b, pos)
        sig = "".join(cgt.outcome(cgt.add(g, cgt.nimber(h))) for h in range(8))
    except TO:
        to += 1; continue
    finally:
        signal.alarm(0)
    if len(pawns._value.cache_info().__repr__()) and pawns._value.cache_info().currsize > 400000: pawns._value.cache_clear()
    ev.write(f"{F} {int(wrap)} {R} | {text}\n"); py.write(f"{sig}\t{F}\t{int(wrap)}\t{R}\t{text}\n"); done += 1
    if done % 200 == 0: ev.flush(); py.flush(); print(done, to, round(time.time() - t0), flush=True)
print("done", done, "timeouts", to, round(time.time() - t0), "s")
