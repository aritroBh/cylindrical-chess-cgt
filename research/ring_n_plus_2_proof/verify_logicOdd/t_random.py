"""Adversarial stress tests of T50's Lemmas 2 and 3 in the setting of the ODD families (wall E-type, W2 at both ends, arc 2..11 at the cut c=6),
with engine D.  Positions are NOT restricted to the reduced game:

 mode l3mut : start position of R_n / Qo_n with 1-4 of the files OUTSIDE the arc (12..n-1, 0, 1) replaced by random contents
              (menu of tokens + random pawn sets); keep positions with no passed pawn and no e.p. flag (Lemma 3's hypotheses; the arc 2..11 is
              untouched, hence pattern files).  Compare K-children and the existence of a T-move of p (side W and B) with those of ins_6(p).
 mode l3walk: a reduced node of R_n/Qo_n followed by 1-2 arbitrary moves of either colour (any class), same hypotheses, same comparison.
 mode l2gar : Lemma 2 with GARBAGE outside the window: pick j in 3..10, the 5-file window (j-1..j+3 or j-3..j+1, as in the proof) is the
              exact pattern, every other file is random (menu), no passed pawn, no flag; for the wall pawn q on file j (its side X to move)
              check (a) X has no passed pawn after any move of q, (b) each move of q is L or P (never T or K).
 mode ctrl  : sensitivity control: l3mut with cut c=5 (arc 1..10 not guaranteed pattern) and c=7 at n=19 -- the conclusion may fail.
usage: t_random.py MODE FAM n N seed [c]"""
import sys, random, time
from collections import Counter
from common import *

MENU = ['-', '-', 'W2', 'W3', 'W4', 'W5', 'W6', 'B3', 'B4', 'B5', 'B6', 'B7', 'W2B4', 'W2B5', 'W3B6', 'W3B5', 'W2B6', 'W4B7', 'W5B7', 'W6B7', 'W23B4', 'W2B45', 'W3B67', 'W2B7', 'W4B5', 'W5B6', 'W3B4']

def rand_file(rng):
    if rng.random() < 0.6:
        return parse_file(rng.choice(MENU))
    w = tuple(sorted(rng.sample(range(2, 8), rng.choice([0, 1, 1, 2]))))
    b = tuple(sorted(rng.sample(range(2, 8), rng.choice([0, 1, 1, 2]))))
    if set(w) & set(b):
        b = tuple(x for x in b if x not in w)
    return (w, b)

def has_passer(pos, ep=None):
    return bool(passed_list(pos, ep, 'W') or passed_list(pos, ep, 'B'))

def l3_compare(p, c, stats, tag):
    """Lemma 3 comparison; p: no passer, no flag, files c-4..c+5 pattern.  Returns False on mismatch."""
    ph = ins(p, c)
    if has_passer(ph):
        stats['phat_passer'] += 1
        stats.setdefault('ex', ('phat has passer', fmt(p), c))
        return False
    a = cls(p); b = cls(ph)
    stats['tested'] += 1
    ok = True
    for s in 'WB':
        stats['K_children'] += len(a[s][1]); stats['sides_with_T'] += a[s][0]
        if a[s][0] != b[s][0] or {ins_nd(k, c) for k in a[s][1]} != set(b[s][1]):
            ok = False
    if not ok:
        stats['mismatch'] += 1
        stats.setdefault('ex', ('mismatch', fmt(p), c))
    return ok

def arc_ok(p, c, n):
    return all(p[j] == pat(j) for j in range(c - 4, c + 6))

def run_l3(mode, fam, n, N, seed, c):
    rng = random.Random(seed)
    stats = Counter()
    start = parse(TOKS[fam](n))
    c0 = 6 if mode == 'ctrl' else c       # ctrl: mutate outside the TRUE arc 2..11, but cut at c
    outside = [j for j in range(n) if not (c0 - 4 <= j <= c0 + 5)]
    if mode == 'l3walk':
        order, edges = build(start)
        nodes = [nd[0] for nd in order if nd[1] is None]
    t0 = time.time()
    tries = 0
    while stats['tested'] < N and tries < 40 * N:
        tries += 1
        if mode in ('l3mut', 'ctrl'):
            p = list(start)
            for j in rng.sample(outside, rng.randint(1, 4)):
                p[j] = rand_file(rng)
            p = tuple(p)
        else:
            p = rng.choice(nodes)
            for _ in range(rng.choice([1, 1, 2])):
                mv = moves(p, None, rng.choice('WB'))
                mv = [m for m in mv if m[1] is None]       # no flag (hypothesis)
                if not mv: break
                p = rng.choice(mv)[0]
        stats['tries'] += 1
        if has_passer(p): stats['rej_passer'] += 1; continue
        if mode != 'ctrl' and not arc_ok(p, c, n): stats['rej_arc'] += 1; continue
        l3_compare(p, c, stats, mode)
        if len(engineD._cache) > 400000: engineD._cache.clear()
    print(f'{mode} {fam} n={n} c={c} seed={seed}: ' + ' '.join(f'{k}={v}' for k, v in sorted(stats.items(), key=lambda kv: kv[0]) if k != 'ex'),
          ('EXAMPLE ' + str(stats['ex'])) if 'ex' in stats else '', f'({time.time()-t0:.0f}s)', flush=True)

def window_for(j, lo, hi):
    w = (j - 1, j + 3) if j + 3 <= hi else (j - 3, j + 1)
    return w

def run_l2(fam, n, N, seed):
    rng = random.Random(seed)
    stats = Counter()
    t0 = time.time()
    tries = 0
    while stats['positions'] < N and tries < 60 * N:
        tries += 1
        j = rng.randint(2, n - 3)
        # window as in the proof: right-looking if possible (j+3 <= j+3 always), else left-looking; test BOTH looking directions
        look = rng.choice(['R', 'L'])
        lo, hi = (j - 1, j + 3) if look == 'R' else (j - 3, j + 1)
        if lo < 0 or hi > n - 1: continue
        p = [None] * n
        for f in range(n):
            if lo <= f <= hi: p[f] = pat(f)
            else: p[f] = rand_file(rng)
        p = tuple(p)
        stats['tries'] += 1
        if has_passer(p): stats['rej_passer'] += 1; continue
        side = 'W' if j % 2 == 0 else 'B'
        y = other(side)
        stats['positions'] += 1
        stats['dir' + look] += 1
        for npos, nep, src, kind in moves(p, None, side):
            if src != j: continue
            # (a) X has no passed pawn afterwards
            if passed_list(npos, nep, side):
                stats['viol_a'] += 1; stats.setdefault('ex', ('a', fmt(p), j, look)); continue
            st = status(npos, nep, side)
            if st == side:
                stats['viol_b_T'] += 1; stats.setdefault('ex', ('bT', fmt(p), j, look)); continue
            if st == y:
                stats['L'] += 1; continue
            pr = any(status(p2, e2, y) == y for p2, e2, s2, k2 in moves(npos, nep, y))
            if pr: stats['P'] += 1
            else: stats['viol_b_K'] += 1; stats.setdefault('ex', ('bK', fmt(p), j, look, kind)); 
            stats['moves_' + kind] += 1
        if len(engineD._cache) > 400000: engineD._cache.clear()
    print(f'l2gar {fam} n={n} seed={seed}: ' + ' '.join(f'{k}={v}' for k, v in sorted(stats.items()) if k != 'ex'),
          ('EXAMPLE ' + str(stats['ex'])) if 'ex' in stats else '', f'({time.time()-t0:.0f}s)', flush=True)

if __name__ == '__main__':
    mode, fam, n, N, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    c = int(sys.argv[6]) if len(sys.argv) > 6 else 6
    if mode == 'l2gar': run_l2(fam, n, N, seed)
    else: run_l3(mode, fam, n, N, seed, c)
