#!/usr/bin/env python3
"""Second, independently structured implementation (pure Python, stdlib only) of the T34 ring check.

Differences from ring.c on purpose: pawns are sets of (file, rank) pairs, adjacency of files is
circular distance, e.p. is stored with the landing rank and tested dynamically, the race is decided by
"mover wins iff strictly closer", outcomes are computed by the plain definition of who wins S + *h.

usage: ring_check.py N MAXPAWNS [compare_file_from_ring.c --all] [--sample K]
"""
import sys, itertools, time, random

N = int(sys.argv[1]); MAXP = int(sys.argv[2])
CMP = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else None
SAMPLE = None
if '--sample' in sys.argv: SAMPLE = int(sys.argv[sys.argv.index('--sample') + 1])
HMAX = 4
OFF = N * 8


def circ(a, b):
    d = abs(a - b)
    return min(d, N - d)


def dist(col, r):                       # promotion distance, double step allowed from the start rank
    return 8 - r - (1 if r == 2 else 0) if col == 'W' else r - 1 - (1 if r == 7 else 0)


def capturable(W, B, ep):               # ep = (colour, file, rank) of the pawn that just double-stepped
    if ep is None: return False
    col, f, r = ep
    enemy = B if col == 'W' else W
    return any((g, r) in enemy and circ(g, f) == 1 for g in range(N))


def passed_dists(W, B, ep):
    """(min promotion distance of passed White pawns or None, same for Black)"""
    dw = db = None
    live = ep if capturable(W, B, ep) else None
    for (f, r) in W:
        if live and live == ('W', f, r): continue
        if all(not (circ(f, g) <= 1 and q > r) for (g, q) in B):
            d = dist('W', r); dw = d if dw is None or d < dw else dw
    for (f, r) in B:
        if live and live == ('B', f, r): continue
        if all(not (circ(f, g) <= 1 and q < r) for (g, q) in W):
            d = dist('B', r); db = d if db is None or d < db else db
    return dw, db


def verdict(W, B, ep, mover):           # None = play on, 'W' / 'B' = that side wins
    dw, db = passed_dists(W, B, ep)
    if dw is None and db is None: return None
    if db is None: return 'W'
    if dw is None: return 'B'
    dm, dn = (dw, db) if mover == 'W' else (db, dw)
    return mover if dm < dn else ('B' if mover == 'W' else 'W')


def moves(W, B, ep, col):
    """list of (W', B', ep') after a move by col"""
    mine, theirs = (W, B) if col == 'W' else (B, W)
    d = 1 if col == 'W' else -1
    start = 2 if col == 'W' else 7
    out = []

    def emit(m2, t2, e2):
        out.append((m2, t2, e2) if col == 'W' else (t2, m2, e2))
    occupied = W | B
    for (f, r) in mine:
        if (f, r + d) not in occupied:
            emit((mine - {(f, r)}) | {(f, r + d)}, theirs, None)
            if r == start and (f, r + 2 * d) not in occupied:
                m2 = (mine - {(f, r)}) | {(f, r + 2 * d)}
                e2 = (col, f, r + 2 * d)
                Wn, Bn = (m2, theirs) if col == 'W' else (theirs, m2)
                emit(m2, theirs, e2 if capturable(Wn, Bn, e2) else None)
        for g in {(f + 1) % N, (f - 1) % N}:
            if (g, r + d) in theirs:
                emit((mine - {(f, r)}) | {(g, r + d)}, theirs - {(g, r + d)}, None)
    if ep is not None and ep[0] != col:
        _, g, er = ep
        for (f, r) in mine:
            if r == er and circ(f, g) == 1:
                emit((mine - {(f, r)}) | {(g, er + d)}, theirs - {(g, er)}, None)
    return out


def key(W, B, ep):
    k = 0
    for (f, r) in W: k |= 1 << (f * 8 + r - 1)
    for (f, r) in B: k |= 1 << (OFF + f * 8 + r - 1)
    if ep is not None: k |= (1 + ep[1] + (4 if ep[0] == 'B' else 0)) << (2 * OFF)
    return k


memo = {}


def outcome(W, B, ep):
    """int with bit 2h: Left (White) to move wins S+*h ; bit 2h+1: Right (Black) to move wins S+*h"""
    k = key(W, B, ep)
    v = memo.get(k)
    if v is not None: return v
    kids = {'W': [], 'B': []}
    for col in 'WB':
        for (W2, B2, e2) in moves(W, B, ep, col):
            t = verdict(W2, B2, e2, col)
            kids[col].append(t if t is not None else outcome(W2, B2, e2))
    res = {}                                    # res[(player, h)] -> bool
    for h in range(HMAX):
        for col in 'WB':
            other = 'B' if col == 'W' else 'W'
            win = False
            for kd in kids[col]:
                if isinstance(kd, str):
                    if kd == col: win = True; break
                else:                           # kid is an outcome int: opponent moves next in kid + *h
                    bit = 2 * h + (1 if other == 'B' else 0)
                    if not (kd >> bit) & 1: win = True; break
            if not win:
                for hp in range(h):             # reduce the heap
                    if not res[(other, hp)]: win = True; break
            res[(col, h)] = win
    v = 0
    for h in range(HMAX):
        v |= (1 << (2 * h)) if res[('W', h)] else 0
        v |= (1 << (2 * h + 1)) if res[('B', h)] else 0
    memo[k] = v
    return v


# ---------- independent enumeration of rings ----------
def file_configs():
    """all contents of one file: tuple of (rank, colour) with White on 2..6 and Black on 3..7 (others are passed)"""
    cells = [(2, 'W')] + [(r, c) for r in range(3, 7) for c in 'WB'] + [(7, 'B')]
    by_rank = {}
    for (r, c) in cells: by_rank.setdefault(r, []).append(c)
    ranks = sorted(by_rank)
    res = []
    def go(i, cur):
        if i == len(ranks):
            res.append(tuple(cur)); return
        go(i + 1, cur)
        for c in by_rank[ranks[i]]:
            cur.append((ranks[i], c)); go(i + 1, cur); cur.pop()
    go(0, [])
    return [c for c in res if c]               # every file occupied


def canon(cfg):                                 # cfg = tuple of per-file configs
    best = None
    for rot in range(N):
        for refl in (0, 1):
            t = [None] * N
            for f in range(N):
                g = ((-f if refl else f) + rot) % N
                t[g] = cfg[f]
            t = tuple(t)
            if best is None or t < best: best = t
    return best


def to_sets(cfg):
    W = frozenset((f, r) for f in range(N) for (r, c) in cfg[f] if c == 'W')
    B = frozenset((f, r) for f in range(N) for (r, c) in cfg[f] if c == 'B')
    return W, B


def fmt(cfg):
    W, B = to_sets(cfg)
    s = lambda S: ' '.join('%s%d' % (chr(97 + f), r) for (f, r) in sorted(S))
    return 'W: %s / B: %s' % (s(W), s(B))


def parse(s):
    cfg = [[] for _ in range(N)]
    col = None
    for tok in s.replace('/', ' ').split():
        if tok == 'W:': col = 'W'
        elif tok == 'B:': col = 'B'
        else: cfg[ord(tok[0]) - 97].append((int(tok[1:]), col))
    return tuple(tuple(sorted(c)) for c in cfg)


def main():
    t0 = time.time()
    fc = file_configs()
    bysize = {}
    for c in fc: bysize.setdefault(len(c), []).append(c)
    raw = {}; classes = {}
    def rec(f, cur, np):
        if f == N:
            W, B = to_sets(cur)
            if not W or not B: return
            dw, db = passed_dists(W, B, None)
            if dw is not None or db is not None: return
            raw[np] = raw.get(np, 0) + 1
            if canon(cur) == tuple(cur): classes.setdefault(np, []).append(tuple(cur))
            return
        for k in range(1, MAXP - np - (N - f - 1) + 1):
            for c in bysize.get(k, []):
                cur.append(c); rec(f + 1, cur, np + k); cur.pop()
    rec(0, [], 0)
    print('enumerated in %.1fs' % (time.time() - t0), flush=True)
    cmp = {}
    if CMP:
        for line in open(CMP):
            np_, v, s = line.rstrip('\n').split('\t')
            cmp[fmt(canon(parse(s)))] = int(v)
    stats = {}
    bad = 0; checked = 0
    rnd = random.Random(12345)
    for np in sorted(classes):
        lst = classes[np]
        if SAMPLE and len(lst) > SAMPLE and np == max(classes): lst = rnd.sample(lst, SAMPLE)
        st = {'cls': len(classes[np]), 'raw': raw[np], 'val': [0] * (HMAX + 1)}
        # (value counts only over the solved ones)
        for cfg in lst:
            W, B = to_sets(cfg)
            v = outcome(W, B, None)
            cl = HMAX
            for h in range(HMAX):
                if not (v >> 2 * h) & 1 and not (v >> (2 * h + 1)) & 1: cl = h
            st['val'][cl] += 1
            if cl == 2: print('STAR2', np, fmt(cfg), flush=True)
            if cmp:
                s = fmt(cfg); checked += 1
                if s not in cmp or cmp[s] != v:
                    bad += 1
                    if bad < 10: print('MISMATCH', s, v, cmp.get(s))
        st['solved'] = len(lst)
        stats[np] = st
        print('pawns', np, st, 'states so far', len(memo), '%.0fs' % (time.time() - t0), flush=True)
    print('compared', checked, 'mismatches', bad)


main()
