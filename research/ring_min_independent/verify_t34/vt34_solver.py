#!/usr/bin/env python3
"""Verifier's own solver for T34 (written from the brief only; not derived from ring.c / ring_check.py / cylcgt).

usage: vt34.py N MAXP [--textbook] [--noep] [--race count|mover|opp]

Board: string of 8*N chars, index f*8 + (rank-1); '.', 'W', 'B'.  ep = None or (file, colour) of the pawn that
just double-stepped and can really be taken e.p. on the opponent's next board move.
Outcome vector of a board S (ints): bit 2h  -> Left (White) to move wins S + *h ; bit 2h+1 -> Right to move wins.
S = *k  iff  neither player moving first wins S + *k.
"""
import sys, itertools, time
sys.setrecursionlimit(10000)
N = int(sys.argv[1]); MAXP = int(sys.argv[2])
TEXTBOOK = '--textbook' in sys.argv
NOEP = '--noep' in sys.argv
RACE = 'count'
if '--race' in sys.argv: RACE = sys.argv[sys.argv.index('--race') + 1]
HN = 3  # heaps *0,*1,*2


def at(f, r): return (f % N) * 8 + r - 1


def dist_w(r): return 5 if r == 2 else 8 - r
def dist_b(r): return 5 if r == 7 else r - 1


def passed_dists(b, ep):
    """(best White promotion distance among passed White pawns or 99, same for Black)"""
    maxB = [0] * N; minW = [99] * N
    for f in range(N):
        for r in range(1, 9):
            c = b[f * 8 + r - 1]
            if c == 'B' and r > maxB[f]: maxB[f] = r
            if c == 'W' and r < minW[f]: minW[f] = r
    dw = db = 99
    for f in range(N):
        nb = ((f - 1) % N, f, (f + 1) % N)
        topB = max(maxB[g] for g in nb)      # highest black pawn on the 3 files
        botW = min(minW[g] for g in nb)      # lowest white pawn on the 3 files
        for r in range(1, 9):
            c = b[f * 8 + r - 1]
            if c == 'W' and r >= topB:       # no black pawn strictly ahead
                if ep is not None and not TEXTBOOK and ep == (f, 'W') and r == 4: continue
                d = dist_w(r)
                if d < dw: dw = d
            elif c == 'B' and r <= botW:
                if ep is not None and not TEXTBOOK and ep == (f, 'B') and r == 5: continue
                d = dist_b(r)
                if d < db: db = d
    return dw, db


def verdict(b, ep, mover):
    dw, db = passed_dists(b, ep)
    if dw == 99 and db == 99: return None
    if db == 99: return 'W'
    if dw == 99: return 'B'
    other = 'B' if mover == 'W' else 'W'
    if RACE == 'mover': return mover
    if RACE == 'opp': return other
    dm, do = (dw, db) if mover == 'W' else (db, dw)
    return other if do <= dm else mover


def board_moves(b, ep, me):
    """yield (newboard, newep)"""
    d = 1 if me == 'W' else -1
    start = 2 if me == 'W' else 7
    foe = 'B' if me == 'W' else 'W'
    out = []
    for f in range(N):
        for r in range(2, 8):
            if b[f * 8 + r - 1] != me: continue
            i = f * 8 + r - 1
            j = at(f, r + d)
            if b[j] == '.':
                l = list(b); l[i] = '.'; l[j] = me
                out.append((''.join(l), None))
                if r == start:
                    k = at(f, r + 2 * d)
                    if b[k] == '.':
                        l = list(b); l[i] = '.'; l[k] = me
                        nb = ''.join(l)
                        e = None
                        if not NOEP and any(nb[at(g, r + 2 * d) % (8 * N)] == foe for g in (f - 1, f + 1)):
                            e = (f, me)
                        out.append((nb, e))
            for df in (-1, 1):
                g = (f + df) % N
                t = at(g, r + d)
                if b[t] == foe:
                    l = list(b); l[i] = '.'; l[t] = me
                    out.append((''.join(l), None))
    if ep is not None and ep[1] == foe and not NOEP:
        g = ep[0]
        er = 4 if foe == 'W' else 5
        for df in (-1, 1):
            f = (g + df) % N
            i = at(f, er)
            if b[i] == me:
                l = list(b); l[i] = '.'; l[at(g, er)] = '.'; l[at(g, er + d)] = me
                out.append((''.join(l), None))
    return out


memo = {}


def outcome(b, ep):
    key = (b, ep)
    v = memo.get(key)
    if v is not None: return v
    # kids[colour] = list of ('T', winner) or ('S', outcome-int)
    win = {}
    kids = {}
    for me in 'WB':
        ks = []
        for (nb, ne) in board_moves(b, ep, me):
            t = verdict(nb, ne, me)
            ks.append(('T', t) if t else ('S', outcome(nb, ne)))
        kids[me] = ks
    w = {('W', 0): None}
    res = {}
    for h in range(HN):
        for me in 'WB':
            foe = 'B' if me == 'W' else 'W'
            ok = False
            for (kind, x) in kids[me]:
                if kind == 'T':
                    if x == me: ok = True; break
                else:  # opponent now moves first in child + *h
                    bit = 2 * h + (1 if foe == 'B' else 0)
                    if not (x >> bit) & 1: ok = True; break
            if not ok:
                for hp in range(h):
                    if not res[(foe, hp)]: ok = True; break
            res[(me, h)] = ok
    v = 0
    for h in range(HN):
        if res[('W', h)]: v |= 1 << (2 * h)
        if res[('B', h)]: v |= 1 << (2 * h + 1)
    memo[key] = v
    return v


def klass(v):
    for h in range(HN):
        if not (v >> 2 * h) & 1 and not (v >> (2 * h + 1)) & 1: return h
    return None


# ---- enumeration: per-file configurations, then products ----
# a file configuration: tuple of (rank, colour) ; W allowed on 2..6, B on 3..7
def file_configs():
    res = []
    opts = {2: ['.', 'W'], 3: ['.', 'W', 'B'], 4: ['.', 'W', 'B'], 5: ['.', 'W', 'B'], 6: ['.', 'W', 'B'], 7: ['.', 'B']}
    for combo in itertools.product(*[opts[r] for r in range(2, 8)]):
        cfg = tuple((r, c) for r, c in zip(range(2, 8), combo) if c != '.')
        if cfg: res.append(cfg)
    return res


FC = file_configs()
info = []
for cfg in FC:
    ws = [r for r, c in cfg if c == 'W']; bs = [r for r, c in cfg if c == 'B']
    info.append((len(cfg), max(ws) if ws else 0, min(bs) if bs else 99, max(bs) if bs else 0, min(ws) if ws else 99))
IDX = list(range(len(FC)))
bysize = {}
for i, c in enumerate(FC): bysize.setdefault(len(c), []).append(i)


def canon_key(t):
    best = None
    for rot in range(N):
        for refl in (0, 1):
            u = [0] * N
            for f in range(N):
                u[(((-f) if refl else f) + rot) % N] = t[f]
            u = tuple(u)
            if best is None or u < best: best = u
    return best


def to_board(t):
    l = ['.'] * (8 * N)
    for f in range(N):
        for r, c in FC[t[f]]: l[f * 8 + r - 1] = c
    return ''.join(l)


def fmt(t):
    W = []; B = []
    for f in range(N):
        for r, c in FC[t[f]]:
            (W if c == 'W' else B).append('%s%d' % (chr(97 + f), r))
    return 'W: %s / B: %s' % (' '.join(W), ' '.join(B))


def ring_ok(t):
    """no passed pawn at the root, both colours present"""
    anyW = anyB = False
    for f in range(N):
        _, mW, mB, _, _ = info[t[f]]
        if mW: anyW = True
        if mB < 99: anyB = True
    if not (anyW and anyB): return False
    for f in range(N):
        nb = ((f - 1) % N, f, (f + 1) % N)
        topB = max(info[t[g]][3] for g in nb)
        botW = min(info[t[g]][4] for g in nb)
        maxW = info[t[f]][1]; minB = info[t[f]][2]
        if maxW and not maxW < topB: return False      # a white pawn with nothing strictly ahead
        if minB < 99 and not minB > botW: return False
    return True


DUMP = open(sys.argv[sys.argv.index('--dump') + 1], 'w') if '--dump' in sys.argv else None


def main():
    t0 = time.time()
    stats = {}
    star2 = {}
    def rec(f, cur, np):
        if f == N:
            if not ring_ok(cur): return
            st = stats.setdefault(np, [0, 0, [0] * (HN + 1), [0] * (HN + 1)])
            st[0] += 1
            tt = tuple(cur)
            if canon_key(tt) != tt: return
            # orbit size
            orb = set()
            for rot in range(N):
                for refl in (0, 1):
                    u = [0] * N
                    for g in range(N): u[(((-g) if refl else g) + rot) % N] = tt[g]
                    orb.add(tuple(u))
            st[1] += 1
            v = outcome(to_board(tt), None)
            k = klass(v)
            kk = HN if k is None else k
            st[2][kk] += 1; st[3][kk] += len(orb)
            if k == 2: star2.setdefault(np, []).append((fmt(tt), len(orb)))
            if DUMP: DUMP.write('%d\t%s\t%s\n' % (np, 'x' if k is None else k, fmt(tt)))
            return
        rest = N - f - 1
        for k in range(1, MAXP - np - rest + 1):
            for i in bysize.get(k, []):
                cur.append(i); rec(f + 1, cur, np + k); cur.pop()
    rec(0, [], 0)
    print('N=%d MAXP=%d textbook=%s noep=%s race=%s' % (N, MAXP, TEXTBOOK, NOEP, RACE))
    print('pawns | raw placements | classes | classes by value [0,*1,*2,other] | placements by value')
    for np in sorted(stats):
        s = stats[np]
        print(np, s[0], s[1], s[2], s[3])
    for np in sorted(star2):
        for x in star2[np]: print('STAR2', np, x)
    print('states', len(memo), '%.0fs' % (time.time() - t0))


main()
