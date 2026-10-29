#!/usr/bin/env python3
"""Referee's own re-enumeration of the K30 strategy trees (tau for EPW, Kf7 line, sigma for the three sorties),
on top of myx.py (own generator). usage: mysigma.py cyl|flat"""
import sys
from collections import deque
import myx
from myx import *
cylb = myx.cyl
def corner(s):
    f, r = fr(s); return (not cylb) and f in (0, 7) and r in (0, 7)
X = (0, P('e6'), P('d8'), D7, E7)
wm = [m for m in moves(X)]
print(sys.argv[1], 'White moves at X:', sorted(chr(97+m[1]%8)+str(m[1]//8+1) for m in wm), '(king destination)')
assert sorted(m[1] for m in wm) == sorted(P(x) for x in ('e5','d5','f5','f7'))
# (A): after each, ...Kxd7 legal
after = []
for m in wm:
    cs = [n for n in moves(m) if n[0] != 'promo' and n[2] == D7]
    assert len(cs) == 1 and cs[0][3] is None
    after.append(cs[0])
# tau
seenW = set(after); seenB = set(); dq = deque(after)
while dq:
    t = dq.popleft()
    for n in moves(t):
        assert n[0] != 'promo'
        if n[4] is None: continue      # pawn captured
        assert not inc(n)
        if n in seenB: continue
        seenB.add(n)
        tm = [u for u in moves(n) if u[0] != 'promo' and u[4] == n[4] and not corner(u[2])]
        assert tm, ('no tau move', n)
        for u in tm:
            if u not in seenW: seenW.add(u); dq.append(u)
print('tau: White-to-move', len(seenW), 'Black-to-move', len(seenB), '(claimed cyl 3348/3348, flat 3164/3164)')
# Kf7 line
f7 = [m for m in wm if m[1] == P('f7')][0]
start = [n for n in moves(f7) if n[0] != 'promo' and n[4] == P('e5')][0]
frontier = [start]; seen = {start}; depth = 0; promo_depths = set()
while frontier:
    depth += 1; nxt = []
    for t in frontier:
        wms = moves(t); assert wms
        for x in wms:
            assert x[0] != 'promo' and x[4] is not None and x[2] == P('d8')
            bm = moves(x)
            push = [n for n in bm if n[0] == 'promo' or (n[2] == x[2] and n[4] is not None and n[4] != x[4])]
            assert len(push) == 1
            if push[0][0] == 'promo': promo_depths.add(depth)
            elif push[0] not in seen: seen.add(push[0]); nxt.append(push[0])
    frontier = nxt
print('Kf7 e5 line: White-to-move states', len(seen), 'promotion depths', promo_depths, '(claimed 52 cyl / 47 flat)')
# sigma
def rel(s, p):
    dx = fr(s)[0]-fr(p)[0]
    if cylb: dx = (dx+4) % 8 - 4
    return (dx, fr(s)[1]-fr(p)[1])
def at(p, x, y):
    f, r = fr(p); g = f+x; q = r+y
    if not 0 <= q < 8: return None
    if cylb: g %= 8
    elif not 0 <= g < 8: return None
    return sq(g, q)
def rho(st):
    stm, w, b, wp, p = st
    ms = [m for m in moves(st)]
    assert all(m[0] != 'promo' for m in ms)
    for m in ms:
        if m[4] is None: return m
    byk = {m[1]: m for m in ms}
    x, y = rel(w, p); F, M = at(p,0,-1), at(p,0,-2)
    go = lambda s_: byk.get(s_) if s_ is not None else None
    if (x,y) == (0,-1): r_ = go(M)
    elif (x,y) == (0,-2):
        r_ = go(F)
        if r_ is None:
            bx = rel(b,p)[0]; assert bx in (-1,1); r_ = go(at(p,bx,-2))
    elif (x,y) in ((-1,-2),(1,-2)): r_ = go(M) or go(F)
    elif y == -1 and abs(x) == 1: r_ = go(F)
    else: raise AssertionError(('rho undefined', st))
    assert r_ is not None
    return r_
c7, e6, e5, d5, f5 = P('c7'), P('e6'), P('e5'), P('d5'), P('f5')
tot = {}
for sortie in (e5, d5, f5):
    W_ = {X}; B_ = set(); dq = deque([X]); free = 0
    while dq:
        st = dq.popleft()
        ms = moves(st)
        if not ms:
            assert not inc(st); continue
        if st[3] is None and st[4] is not None: opts = [rho(st)]
        elif st == X: opts = [m for m in ms if m[0] != 'promo' and m[1] == sortie]
        elif st[3] == D7 and st[4] == E7 and st[1] in (e5,d5,f5) and st[2] == c7: opts = [m for m in ms if m[0] != 'promo' and m[1] == e6]
        elif st[3] == D7 and st[4] == E7 and st[1] == e6 and st[2] not in (c7, D8):
            opts = [m for m in ms if m[0] != 'promo' and m[4] is None]
        elif st[3] == D7 and st[4] is not None and st[4] != E7:
            opts = [m for m in ms if m[0] != 'promo' and m[4] is None]
        elif st[3] == D7 and st[4] is None:
            opts = [m for m in ms if m[0] != 'promo']     # any king move, never the pawn
        else: raise AssertionError(('sigma undefined', st))
        assert len(opts) >= 1, ('no option', st)
        for t in opts:
            assert t[0] != 'promo'
            if t[3] is None and t[4] is None: continue
            if t in B_: continue
            B_.add(t)
            bms = moves(t)
            if not bms:
                assert not inc(t); continue
            for n in bms:
                assert n[0] != 'promo', ('Black promotes', t)
                if n[3] is None and n[4] is None: continue
                if n not in W_: W_.add(n); dq.append(n)
    tot[sortie] = (len(W_), len(B_))
print('sigma White-to-move / Black-to-move states for Ke5, Kd5, Kf5:', [tot[s] for s in (e5, d5, f5)],
      '(claimed White-to-move cyl 3694/3696/3696, flat 3738/3740/3740)')
