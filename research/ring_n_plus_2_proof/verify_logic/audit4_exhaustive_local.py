"""Exhaustive local test of Lemma 3 (insertion) with a pattern arc of exactly 10 files (c-4..c+5) and ALL contents from a
menu on the m outside files, so every outside file sits next to an arc end or next to another outside file.
Both wall phases (arc starts with W2, or with B4).  Positions with a passed pawn are skipped (hypothesis of the lemma).
Compared for each side: T-flag, and the set of K children (mapped by ins_c)."""
import sys, itertools, time
import engine
from engine import *

W2 = parse_file('W2'); B4 = parse_file('B4')

def menu(kind):
    toks = ['-'] + ['W%d' % r for r in range(2, 8)] + ['B%d' % r for r in range(2, 8)]
    if kind == 'big':
        toks += ['W%dB%d' % (r, s) for r in range(2, 8) for s in range(2, 8) if r != s]
        toks += ['W%d%d' % (a, b) for a in range(2, 8) for b in range(a + 1, 8)]
        toks += ['B%d%d' % (a, b) for a in range(2, 8) for b in range(a + 1, 8)]
    elif kind == 'mid':
        toks += ['W2B5', 'W3B5', 'W3B6', 'W4B6', 'W4B7', 'W5B7', 'W2B6', 'W2B7', 'W3B7', 'W6B3', 'W5B4', 'W7B2']
    return [parse_file(t) for t in toks]

def cls(pos):
    out = {}
    for side in 'WB':
        cl = classify(pos, None, side)
        out[side] = (any(c == 'T' for c, *_ in cl), frozenset((npos, nep) for c, npos, nep, *_ in cl if c == 'K'))
    return out

def run(m, kind, phase):
    M = menu(kind)
    arc = [(W2 if (j + phase) % 2 == 0 else B4) for j in range(10)]
    n = m + 10
    cidx = (1 + 4)            # outside files: first one (left of arc) ... we put 1 outside file left, m-1 right
    tested = skipped = bad = 0
    ex = None
    for combo in itertools.product(range(len(M)), repeat=m):
        outs = [M[i] for i in combo]
        pos = tuple([outs[0]] + arc + outs[1:])
        c = 1 + 4          # arc occupies indices 1..10, c-4 = 1
        if passed_list(pos, None, 'W') or passed_list(pos, None, 'B'):
            skipped += 1; continue
        ph = ins(pos, c)
        if passed_list(ph, None, 'W') or passed_list(ph, None, 'B'):
            bad += 1; ex = ex or ('phat has passed', pos); continue
        a = cls(pos); b = cls(ph)
        tested += 1
        if tested % 2000 == 0: engine._cache.clear()
        for s in 'WB':
            if a[s][0] != b[s][0] or {ins_nd(k, c) for k in a[s][1]} != set(b[s][1]):
                bad += 1; ex = ex or ('mismatch', fmt(pos), s); break
    return tested, skipped, bad, ex

if __name__ == '__main__':
    m = int(sys.argv[1]); kind = sys.argv[2]
    for phase in (0, 1):
        t0 = time.time()
        print('m', m, 'menu', kind, 'size', len(menu(kind)), 'phase', phase, run(m, kind, phase), '%.0fs' % (time.time() - t0), flush=True)
