# Lemma 1 (reduction) on random small positions: full G+*h outcome vs reduced-game outcome, both movers, h=0..3
import sys, random, time
from eng import *
from red import build

def outcome_full(pos, ep, hs=(0, 1, 2, 3)):
    s = Solver(); out = []
    for h in hs:
        out.append((s.win(pos, ep, h, 'W'), s.win(pos, ep, h, 'B')))
    return out

def outcome_red(pos, ep, hs=(0, 1, 2, 3)):
    ids = {(pos, ep): 0}
    # reuse build with an arbitrary root
    from collections import deque
    order = [(pos, ep)]; info = {}; q = deque(order); seen = {(pos, ep)}
    while q:
        nd = q.popleft(); p, e = nd; rec = {}
        for side in 'WB':
            cl = classify_moves(p, e, side)
            T = {(a, b) for k, a, b in cl if k == 'T'}
            K = {(a, b) for k, a, b in cl if k == 'K'}
            rec[side] = (T, K, 0)
            for c in K:
                if c not in seen: seen.add(c); order.append(c); q.append(c)
        info[nd] = rec
    memo = {}
    def win(nd, h, mover):
        key = (nd, h, mover)
        if key in memo: return memo[key]
        T, K, _ = info[nd][mover]
        res = bool(T)
        y = other(mover)
        if not res:
            for c in K:
                if not win(c, h, y): res = True; break
        if not res:
            for h2 in range(h):
                if not win(nd, h2, y): res = True; break
        memo[key] = res; return res
    return [(win((pos, ep), h, 'W'), win((pos, ep), h, 'B')) for h in hs], len(order)

def rand_small(rng):
    n = rng.randint(5, 7)
    w = [0] * n; b = [0] * n
    k = rng.randint(3, 7)
    for _ in range(k):
        f = rng.randrange(n); r = rng.randint(2, 6) if rng.random() < .8 else rng.choice((2, 7))
        if rng.random() < .5: w[f] |= 1 << (r - 1)
        else: b[f] |= 1 << (r - 1)
    for f in range(n):
        x = w[f] & b[f]; w[f] &= ~x
    return tuple(zip(w, b))

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[2])); N = int(sys.argv[1])
    ok = bad = skip = 0; t0 = time.time(); redsz = 0
    while ok + bad < N:
        pos = rand_small(rng)
        if passed_ranks(pos, None, 'W') or passed_ranks(pos, None, 'B'): skip += 1; continue
        a = outcome_full(pos, None); b, sz = outcome_red(pos, None); redsz += sz
        if a == b: ok += 1
        else:
            bad += 1; print('MISMATCH', pos, a, b)
        if time.time() - t0 > 600: break
    print('lemma1 random: agree', ok, 'disagree', bad, 'skipped(passed)', skip, 'avg reduced nodes %.1f' % (redsz / max(1, ok + bad)))
