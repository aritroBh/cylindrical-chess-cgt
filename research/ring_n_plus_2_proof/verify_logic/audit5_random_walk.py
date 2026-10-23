"""Lemma 3 on positions reached by random play (both sides, arbitrary move order = heap moves allow passing) from start_n.
A sampled position qualifies if it has no passed pawn, no flag, and a pattern arc c-4..c+5 (every file holds exactly the
wall pawn of its parity: W2 even / B4 odd).  For every admissible cut compare classify(p) with classify(ins_c p)."""
import sys, random, time
from engine import *

def pat(j):
    return parse_file('W2') if j % 2 == 0 else parse_file('B4')

def cls(pos, ep=None):
    out = {}
    for side in 'WB':
        cl = classify(pos, ep, side)
        out[side] = (any(c == 'T' for c, *_ in cl), frozenset((npos, nep) for c, npos, nep, *_ in cl if c == 'K'))
    return out

def main(n, samples, seed, maxlen):
    rng = random.Random(seed)
    start = parse(P_toks(n))
    tested = bad = 0
    ex = None
    seen = set()
    t0 = time.time()
    import collections
    byc = collections.Counter()
    while tested < samples and time.time() - t0 < 1500:
        pos, ep = start, None
        for step in range(rng.randint(1, maxlen)):
            mv = moves(pos, ep, 'W') + moves(pos, ep, 'B')
            # prefer moves of non-wall pawns to keep an arc alive, but allow everything
            core = [m for m in mv if m[2] <= 7 or rng.random() < 0.05]
            pool = core if core and rng.random() < 0.9 else mv
            npos, nep, src, kind = rng.choice(pool)
            if passed_list(npos, nep, 'W') or passed_list(npos, nep, 'B'):
                break
            pos, ep = npos, nep
        else:
            pass
        if ep is not None or (pos, ep) in seen:
            continue
        if passed_list(pos, ep, 'W') or passed_list(pos, ep, 'B'):
            continue
        seen.add((pos, ep))
        cuts = [c for c in range(4, n - 5) if all(pos[j] == pat(j) for j in range(c - 4, c + 6))]
        if not cuts:
            continue
        a = cls(pos)
        for c in cuts:
            ph = ins(pos, c)
            b = cls(ph)
            byc[c] += 1
            ok = all(a[s][0] == b[s][0] and {ins_nd(k, c) for k in a[s][1]} == set(b[s][1]) for s in 'WB')
            if not ok:
                bad += 1; ex = ex or (fmt(pos), c)
        tested += 1
    return tested, bad, ex, dict(byc), len(seen)

if __name__ == '__main__':
    n = int(sys.argv[1]); samples = int(sys.argv[2]); seed = int(sys.argv[3]); maxlen = int(sys.argv[4])
    t0 = time.time()
    print('n', n, 'samples', samples, 'seed', seed, main(n, samples, seed, maxlen), '%.0fs' % (time.time() - t0), flush=True)
