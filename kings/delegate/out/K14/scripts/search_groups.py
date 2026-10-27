#!/usr/bin/env python3
"""K14 stage-1 search: both-sides-shuttle king groups on a flat or cylinder board.

A candidate is (white king squares z,z', black king squares w,w', white pawns, black pawns) with pawns and
kings on the files of F_Z only (default: the first FZ files), such that in ALL FOUR combined states (a,b),
a in {z,z'}, b in {w,w'}:
  * both kings are on non-pawn squares, not attacked by an enemy pawn, and the kings are not adjacent
    (so each shuttle move is legal in every state, with the other king on either of its two squares);
  * z,z' adjacent, w,w' adjacent.
For every state we count the other legal moves of each side ("O-moves": king moves other than the shuttle,
pawn moves incl. captures and promotions; e.p. is ignored at stage 1).  The score is the total O-count.
Output: candidates sorted by score, one per line (JSON).  Pure geometry; no claim about chess results.

usage: search_groups.py BOARD(flat:WxH|cyl:WxH) FZ NW NB MAXSCORE > out
"""
import sys, json, itertools

board, FZ, NW, NB, MAXS = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
kind, dims = board.split(':'); W, H = map(int, dims.split('x')); WRAP = kind == 'cyl'


def sq(f, r): return r * W + f
def fr(s): return s % W, s // W


def nb(s, df, dr):
    f, r = fr(s); f += df; r += dr
    if r < 0 or r >= H: return -1
    if WRAP: f %= W
    elif f < 0 or f >= W: return -1
    return sq(f, r)


KN = {s: sorted({t for df in (-1, 0, 1) for dr in (-1, 0, 1) if (df or dr) and (t := nb(s, df, dr)) >= 0 and t != s}) for s in range(W * H)}


def adj(a, b): return b in KN[a]


def pawn_att(color, s):  # squares attacked by a pawn of `color` on s (0 = white moves up)
    d = 1 if color == 0 else -1
    return [t for df in (-1, 1) if (t := nb(s, df, d)) >= 0]


zfiles = range(FZ)
zsquares = [sq(f, r) for f in zfiles for r in range(H)]
wps = [sq(f, r) for f in zfiles for r in range(1, H - 1)]      # pawn squares (ranks 2..H-1)


def pawn_moves(color, s, occ, enemy_sq):
    """legal pawn moves ignoring check (kings handled by the caller): list of target squares."""
    d = 1 if color == 0 else -1
    out = []
    t = nb(s, 0, d)
    if t >= 0 and t not in occ:
        out.append(t)
        start = 1 if color == 0 else H - 2
        if fr(s)[1] == start:
            t2 = nb(t, 0, d)
            if t2 >= 0 and t2 not in occ: out.append(t2)
    for t in pawn_att(color, s):
        if t in enemy_sq: out.append(t)
    return out


def configs(n):
    for k in range(n + 1):
        yield from itertools.combinations(wps, k)


def attacked_by_pawns(color, pawns):
    a = set()
    for p in pawns: a.update(pawn_att(color, p))
    return a


def omoves_white(kz, kb, wp, bp, shuttle_to):
    """count other legal white moves in state (kz = white king, kb = black king)."""
    occ = set(wp) | set(bp) | {kz, kb}
    batt = attacked_by_pawns(1, bp)
    n = 0
    for t in KN[kz]:
        if t == shuttle_to or t == kb: continue
        if t in wp: continue
        if t in batt or adj(t, kb): continue
        if t in bp and (t in attacked_by_pawns(1, bp) or adj(t, kb)): continue  # defended pawn (approx: pawn defends pawn / king defends)
        n += 1
    for p in wp:
        for t in pawn_moves(0, p, occ, set(bp)):
            n += 1
    return n


def omoves_black(kz, kb, wp, bp, shuttle_to):
    occ = set(wp) | set(bp) | {kz, kb}
    watt = attacked_by_pawns(0, wp)
    n = 0
    for t in KN[kb]:
        if t == shuttle_to or t == kz: continue
        if t in bp: continue
        if t in watt or adj(t, kz): continue
        n += 1
    for p in bp:
        for t in pawn_moves(1, p, occ, set(wp)):
            n += 1
    return n


out = 0
for wp in configs(NW):
    for bp in configs(NB):
        if set(wp) & set(bp): continue
        pawns = set(wp) | set(bp)
        # a pawn of colour c may not be on its own first/last rank: wps already excludes ranks 1 and H
        batt = attacked_by_pawns(1, bp)   # squares attacked by black pawns: unsafe for white king
        watt = attacked_by_pawns(0, wp)
        wsafe = [s for s in zsquares if s not in pawns and s not in batt]
        bsafe = [s for s in zsquares if s not in pawns and s not in watt]
        wpairs = [(a, b) for a in wsafe for b in wsafe if a < b and adj(a, b)]
        bpairs = [(a, b) for a in bsafe for b in bsafe if a < b and adj(a, b)]
        for (z, z2) in wpairs:
            for (w, w2) in bpairs:
                if any(adj(a, b) or a == b for a in (z, z2) for b in (w, w2)): continue
                sc = 0
                for a, ab in ((z, z2), (z2, z)):
                    for b, bb in ((w, w2), (w2, w)):
                        sc += omoves_white(a, b, wp, bp, ab) + omoves_black(a, b, wp, bp, bb)
                if sc <= MAXS:
                    out += 1
                    print(json.dumps({'score': sc, 'board': board, 'K': [z, z2], 'k': [w, w2], 'P': list(wp), 'p': list(bp)}))
sys.stderr.write('candidates: %d\n' % out)
