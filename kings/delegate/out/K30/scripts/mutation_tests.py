#!/usr/bin/env python3
"""mutation_tests.py -- K30: the closure check must FAIL when the invariant or the rule is damaged (sanity of the checker)."""
import sys
sys.path.insert(0, '.')
import k30lib
from k30lib import *
B = Board(sys.argv[1])
orig_inS, orig_rule = k30lib.inS, k30lib.white_rule

def try_(name):
    try:
        S = k30lib.all_S(B)
        k30lib.check_S_closure(B, S)
        print('MUTATION NOT DETECTED:', name)
        return False
    except AssertionError as e:
        print('detected (%s): %s' % (name, str(e)[:110]))
        return True

# mutation 1: smaller forbidden zone for L (y >= -2 only), r >= 4
def inS1(B, pos):
    ok = orig_inS(B, pos)
    if ok:
        stm, wk, bk, wp, bp, ep = pos
        p = bp[0]; r = B.r(p) + 1
        if r >= 4 and rel(B, wk, p) == (-1, -2):
            b = rel(B, bk, p)
            if b[0] in (1, 2) and b[1] == -3:
                return True
    else:
        stm, wk, bk, wp, bp, ep = pos
        if wp == () and len(bp) == 1 and B.f(bp[0]) == E:
            p = bp[0]; r = B.r(p) + 1
            if r >= 4 and rel(B, wk, p) == (-1, -2):
                b = rel(B, bk, p)
                if b[0] in (1, 2) and b[1] == -3:
                    return True
    return ok
k30lib.inS = inS1
r1 = try_('Z_L shrunk by one row')
k30lib.inS = orig_inS
# mutation 2: r=3 family M without the exclusion of d3, f3
def inS2(B, pos):
    stm, wk, bk, wp, bp, ep = pos
    if wp == () and len(bp) == 1 and B.f(bp[0]) == E and B.r(bp[0]) + 1 == 3 and rel(B, wk, bp[0]) == (0, -2):
        return True
    return orig_inS(B, pos)
k30lib.inS = inS2
r2 = try_('r=3, M without b not in {d3,f3}')
k30lib.inS = orig_inS
print('mutations detected:', r1, r2)
assert r1 and r2
