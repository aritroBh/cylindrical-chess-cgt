#!/usr/bin/env python3
"""
Independent verification of Dawson's chess on a cylinder (Part C).
Recomputes from the paper's rules without using any existing solver code.
"""

from functools import lru_cache
import sys

# Octal game 0.137 recurrence from the paper
def g_octal(n, memo={}):
    """Grundy values of octal game 0.137"""
    if n in memo:
        return memo[n]
    if n == 0:
        memo[n] = 0
        return 0
    if n == 1:
        memo[n] = 1
        return 1
    reachable = {g_octal(n - 2, memo)}
    for a in range(n - 2):
        b = n - 3 - a
        reachable.add(g_octal(a, memo) ^ g_octal(b, memo))
    m = 0
    while m in reachable:
        m += 1
    memo[n] = m
    return m

# Compute g values for n=0..60
g_values = [g_octal(i) for i in range(61)]
print("g(n) for n=0..60:")
for i, g in enumerate(g_values):
    print(f"  g({i}) = {g}")

# First player wins ordinary 3xn board iff g(n) != 0
print("\nFirst player wins ordinary 3xn board (g(n) != 0):")
wins_strip = [i for i in range(61) if g_values[i] != 0]
print(f"  n = {wins_strip}")

# Ring rule: first player wins 3xn cylinder iff g(n-3) == 0
print("\nFirst player wins 3xn cylinder (g(n-3) == 0):")
wins_cylinder = [n for n in range(3, 61) if g_values[n - 3] == 0]
print(f"  n = {wins_cylinder}")

# Paper claims: n = 3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57, ...
paper_claim = [3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57]
print(f"\nPaper claim (up to 60): {paper_claim}")
print(f"Match: {wins_cylinder[:len(paper_claim)] == paper_claim}")

# Cylinder Grundy value = mex{g(n-3)}
print("\nCylinder Grundy values (mex{g(n-3)}):")
for n in range(3, 21):
    cyl_g = 0 if g_values[n - 3] != 0 else 1  # mex of singleton {g(n-3)}
    print(f"  n={n}: cylinder Grundy = {cyl_g}, option Grundy = {g_values[n - 3]}")

print("\n=== Octal game verification complete ===")

# Now implement the actual pawn rules to verify the ring structure
# Board: 3 ranks (0,1,2 for ranks 1,2,3), n files (0..n-1)
# White pawns on rank 0, black on rank 2, rank 1 empty
# White moves up (rank+1), black moves down (rank-1)
# Captures are compulsory
# No double step, no promotion (pawn on last rank has no move)

Cell = {'E': 0, 'W': 1, 'B': 2}

def make_start(n):
    """Start position: list of 3*n cells, file by file, rank 0 first"""
    pos = []
    for f in range(n):
        pos.extend([Cell['W'], Cell['E'], Cell['B']])
    return tuple(pos)

def at(pos, n, f, r):
    """Get cell at file f, rank r"""
    return pos[3 * f + r]

def set_cell(pos, n, f, r, val):
    """Set cell at file f, rank r"""
    lst = list(pos)
    lst[3 * f + r] = val
    return tuple(lst)

def neighbors_cyl(n, f):
    """Neighboring files on cylinder"""
    return [(f + 1) % n, (f - 1) % n]

def neighbors_flat(n, f):
    """Neighboring files on flat board"""
    res = []
    if f + 1 < n:
        res.append(f + 1)
    if f - 1 >= 0:
        res.append(f - 1)
    return res

def captures(pos, n, side, wrap):
    """All captures for side (W or B)"""
    res = []
    pawn = Cell['W'] if side == 'W' else Cell['B']
    enemy = Cell['B'] if side == 'W' else Cell['W']
    fwd = 1 if side == 'W' else -1
    nbrs = neighbors_cyl if wrap else neighbors_flat
    for f in range(n):
        for r in range(3):
            if at(pos, n, f, r) == pawn:
                r2 = r + fwd
                if 0 <= r2 < 3:
                    for g in nbrs(n, f):
                        if at(pos, n, g, r2) == enemy:
                            new_pos = set_cell(pos, n, f, r, Cell['E'])
                            new_pos = set_cell(new_pos, n, g, r2, pawn)
                            res.append(new_pos)
    return res

def pushes(pos, n, side, wrap):
    """All pushes for side"""
    res = []
    pawn = Cell['W'] if side == 'W' else Cell['B']
    fwd = 1 if side == 'W' else -1
    for f in range(n):
        for r in range(3):
            if at(pos, n, f, r) == pawn:
                r2 = r + fwd
                if 0 <= r2 < 3 and at(pos, n, f, r2) == Cell['E']:
                    new_pos = set_cell(pos, n, f, r, Cell['E'])
                    new_pos = set_cell(new_pos, n, f, r2, pawn)
                    res.append(new_pos)
    return res

def moves(pos, n, side, wrap):
    """All legal moves for side (captures compulsory)"""
    caps = captures(pos, n, side, wrap)
    if caps:
        return caps
    return pushes(pos, n, side, wrap)

def other_side(side):
    return 'B' if side == 'W' else 'W'

# Test the ring structure claim: after a push on file i, forced captures leave
# file i blocked (W: [E,W,B], B: [W,B,E]), files i-1 and i+1 empty, others untouched
def after_ring_theory(n, i, side):
    """Theoretical position after push at i with forced captures"""
    pos = []
    for f in range(n):
        if f == i:
            if side == 'W':
                pos.extend([Cell['E'], Cell['W'], Cell['B']])
            else:
                pos.extend([Cell['W'], Cell['B'], Cell['E']])
        elif f == (i + 1) % n or f == (i - 1) % n:
            pos.extend([Cell['E'], Cell['E'], Cell['E']])
        else:
            pos.extend([Cell['W'], Cell['E'], Cell['B']])
    return tuple(pos)

def push_at(pos, n, i, side):
    """Position after side pushes on file i"""
    r = 0 if side == 'W' else 2
    new_pos = set_cell(pos, n, i, r, Cell['E'])
    new_pos = set_cell(new_pos, n, i, 1, Cell['W'] if side == 'W' else Cell['B'])
    return new_pos

# Settle forced captures: from a position, if side has captures, must capture
# Continue until side to move has no captures
def settle(pos, n, side, wrap, max_depth=50):
    """Play out forced captures until side has none. Returns list of (pos, side) outcomes."""
    if max_depth == 0:
        return None
    caps = captures(pos, n, side, wrap)
    if not caps:
        return [(pos, side)]
    results = []
    for next_pos in caps:
        res = settle(next_pos, n, other_side(side), wrap, max_depth - 1)
        if res is None:
            return None
        results.extend(res)
    return results

def after_push_full(n, i, side, wrap):
    """Position after push at i followed by all forced captures"""
    start = make_start(n)
    pushed = push_at(start, n, i, side)
    return settle(pushed, n, other_side(side), wrap, 50)

# Verify ring structure for n=3..10
print("\n=== Ring Structure Verification ===")
for n in range(3, 11):
    for side in ['W', 'B']:
        start = make_start(n)
        # Check no captures at start
        caps = captures(start, n, side, True)
        if caps:
            print(f"  n={n}, {side}: UNEXPECTED captures at start!")
        # Check pushes are exactly n files
        push_list = pushes(start, n, side, True)
        if len(push_list) != n:
            print(f"  n={n}, {side}: expected {n} pushes, got {len(push_list)}")
        # Check each push leads to after_ring_theory
        all_ok = True
        for i in range(n):
            pushed = push_at(start, n, i, side)
            settled = after_push_full(n, i, side, True)
            expected = after_ring_theory(n, i, side)
            if settled is None:
                print(f"  n={n}, {side}, i={i}: depth exhausted")
                all_ok = False
            elif len(settled) != 1 or settled[0] != (expected, other_side(side)):
                print(f"  n={n}, {side}, i={i}: mismatch!")
                print(f"    got: {settled}")
                print(f"    exp: {[(expected, other_side(side))]}")
                all_ok = False
        if all_ok:
            print(f"  n={n}, {side}: ring structure OK")

print("\n=== Ring structure verification complete ===")