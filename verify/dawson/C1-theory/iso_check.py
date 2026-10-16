"""Check that the 0.137 strip n and the 0.07 heap n+1 have identical game trees, by comparing
option sets recursively (multisets of nonzero heaps, 0.07 heap 1 = game 0), for n <= 300.
0.137: remove 1 token leaving no heap; remove 2 leaving 0 or 1 heap; remove 3 leaving 0, 1 or 2.
Run: .venv/bin/python verify/dawson/C1-theory/iso_check.py"""
def opts137(n):
    out = set()
    if n == 1: out.add(())                       # digit 1 (=1): remove 1, leave nothing
    if n == 2: out.add(())                       # digit 3 (=1+2): remove 2, leave nothing
    if n >= 3: out.add((n - 2,))                 #   ... or leave one heap
    if n == 3: out.add(())                       # digit 7 (=1+2+4): remove 3, leave nothing
    if n >= 4: out.add((n - 3,))                 #   ... or one heap
    for a in range(1, n - 3):                    #   ... or two heaps
        b = n - 3 - a
        if b >= 1: out.add(tuple(sorted((a, b))))
    return out
def opts07(m):
    out = set()
    if m == 2: out.add(())                       # digit 7: remove 2 leave nothing
    if m >= 3: out.add((m - 2,))                 # leave one heap
    for a in range(1, m - 2):
        b = m - 2 - a
        if b >= 1: out.add(tuple(sorted((a, b))))
    return out
def to137(t):   # 0.07 heaps -> 0.137 heaps (heap 1 of 0.07 is the game 0, dropped)
    return tuple(sorted(x - 1 for x in t if x >= 2))
bad = [n for n in range(1, 301) if {to137(t) for t in opts07(n + 1)} != opts137(n)]
print("0.137 strip n vs 0.07 heap n+1, n = 1..300: mismatches", bad, "; 0.07 heap 1 options:", opts07(1))
