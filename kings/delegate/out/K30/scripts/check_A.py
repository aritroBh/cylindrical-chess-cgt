#!/usr/bin/env python3
"""check_A.py -- K30 step 2b: (A) White cannot win from P7 w (P, chess, EPW, EPB), and (C) Kf7 loses in P.
usage: check_A.py cyl:8x8|flat:8x8"""
import sys, collections
sys.path.insert(0, '.')
from kpm import *
spec = sys.argv[1]
B = Board(spec)
X = parse(B, 'Ke6 Pd7 kd8 pe7 w -')
labs = {lab: t for lab, k, t in gen(B, X)}
print(spec, 'White legal moves at P7 w:', sorted(labs))
assert sorted(labs) == ['e6d5', 'e6e5', 'e6f5', 'e6f7'], 'move list differs from the proof'
# the three moves the proof calls illegal
for bad in ('e6d6', 'e6f6', 'e6e7x'):
    assert bad not in labs
print('  illegal: Kd6, Kf6 (attacked by the pawn e7), Kxe7 (protected by kd8): confirmed not generated')

# ---- (A) after each White move Black may play Kxd7; White then has a lone king ----
d7 = B.sq('d7')
after = []
for lab, t in sorted(labs.items()):
    cap = [(l, k, t2) for l, k, t2 in gen(B, t) if l == 'd8d7x']
    assert len(cap) == 1, lab
    t2 = cap[0][2]
    assert t2[3] == () and t2[0] == 0 and legal(B, t2)       # White has no pawn
    after.append((lab, t2))
    print('  %s : ...Kxd7 gives %s (White has no pawn)' % (lab, fmt(B, t2)))

# (A, EPW) Black's rule tau: never move the pawn, move the king to a free neighbour that is not a corner of a flat board
def corner(s):
    return (not B.cyl) and B.f(s) in (0, B.W - 1) and B.r(s) in (0, B.H - 1)

def tau_moves(pos):
    """all king moves allowed by tau"""
    out = []
    for lab, k, t in gen(B, pos):
        if k != 'n':
            continue
        if t[2] == pos[2]:           # a pawn move
            continue
        if corner(t[2]):
            continue
        out.append(t)
    return out

seenW, seenB = set(), set()
dq = collections.deque(t for lab, t in after)
for t in dq: seenW.add(t)
nterm_cap = 0
while dq:
    t = dq.popleft()                                   # White to move
    for lab, k, nt in gen(B, t):
        assert k == 'n'
        if nt[4] == ():                                # White captured the pawn: K v K, nothing can happen any more
            nterm_cap += 1
            continue
        assert not in_check(B, nt, 1)                  # a lone White king never gives check
        if nt in seenB:
            continue
        seenB.add(nt)
        mv = tau_moves(nt)
        assert mv, ('Black has no tau move', fmt(B, nt))
        for u in mv:
            assert u[4] == nt[4]                       # the pawn never moves, so no promotion
            if u not in seenW:
                seenW.add(u); dq.append(u)
print('  EPW/chess/P/EPB, rule tau: %d White-to-move and %d Black-to-move positions; White captures the pawn %d times; '
      'Black always has a tau move, never promotes, is never in check: White cannot win' % (len(seenW), len(seenB), nterm_cap))

# exact solves (own solver) for comparison: after each first move and ...Kxd7, White does not win in any model
for model in ('P', 'EPW', 'EPB'):
    idx, pl, val, mv = solve(B, model, [X])
    row = []
    for lab, t2 in after:
        row.append('%s:%s' % (lab, val[idx[t2]]))
    print('  exact (own solver) model %s: value of X = %s; value after Kxd7: %s' % (model, val[idx[X]], ' '.join(row)))
    for lab, t2 in after:
        assert val[idx[t2]] in ('D', 'L')

# ---- (C) Kf7 loses in P: Black plays e5 and runs the pawn with the king on d8 ----
f7 = labs['e6f7']
b1 = [t for l, k, t in gen(B, f7) if l == 'e7e5']
assert len(b1) == 1
start = b1[0]
levels = collections.Counter()
seen = set()
frontier = [start]            # White to move
depth = 0
promos = 0
while frontier:
    depth += 1
    nxt = []
    for t in frontier:
        assert t[0] == 0
        ms = gen(B, t)
        assert all(k == 'n' for l, k, x in ms)
        assert ms, 'White stalemated'
        for l, k, x in ms:
            assert x[4] != (), ('White captured the pawn', fmt(B, t), l)        # pawn never lost
            assert x[2] == B.sq('d8')                                            # Black king never moved
            # Black to move: pawn push
            bm = gen(B, x)
            push = [(l2, k2, y) for l2, k2, y in bm if l2[0] == 'e' and l2[2] == 'e' and l2[1] != l2[3]]
            assert len(push) == 1, ('no unique push', fmt(B, x), [m[0] for m in bm])
            l2, k2, y = push[0]
            assert not in_check(B, x, 1)
            if k2 == 'p':
                promos += 1
                levels[depth] += 1
            else:
                if y not in seen:
                    seen.add(y); nxt.append(y)
    frontier = nxt
print('Kf7 e5!: pawn pushes on every turn, king on d8: promotion reached in %s (Black move count after e5), %d White-to-move states, never stopped: check passed' % (dict(levels), len(seen)+1))
assert set(levels) == {4}
print('OK')
