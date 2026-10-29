#!/usr/bin/env python3
"""Referee's own check of Lemma D (K + Black pawn vs K, 8x8), from the text of PROOF.md section 4.1.
 (1) exact solve (own code): Black-win = Black promotion or mate of White, all pawn files, no White pawn.
 (2) S from the text: |S|, S subset of "not Black win" (Black to move).
 (3) closure of S under every Black move and rule rho (own implementation of rules 1-5).
usage: mykpk.py cyl|flat"""
import sys
from collections import Counter
cyl = sys.argv[1] == 'cyl'
W = H = 8
def sq(f, r): return r*W+f
def fr(s): return s % W, s//W
def mk(s):
    f, r = fr(s); out = []
    for df in (-1,0,1):
        for dr in (-1,0,1):
            if df == 0 and dr == 0: continue
            g = f+df; q = r+dr
            if not 0 <= q < H: continue
            if cyl: g %= W
            elif not 0 <= g < W: continue
            out.append(sq(g,q))
    return out
NB = [frozenset(mk(s)) for s in range(64)]
def pa(p):
    f, r = fr(p); o = set()
    for d in (-1,1):
        g = f+d
        if cyl: g %= W
        elif not 0 <= g < W: continue
        if r >= 1: o.add(sq(g,r-1))
    return o
PA = [pa(p) for p in range(64)]
def legal(stm, w, b, p):
    if w == b or w in NB[b] or p in (w, b): return False
    if stm == 1 and w in PA[p]: return False   # Black to move: white king may not be attacked
    return True
def check_on_white(w, p): return w in PA[p]
def wmoves(w, b, p):
    o = []
    for t in NB[w]:
        if t == b or t in NB[b] or t in PA[p]: continue
        o.append((t, p if t != p else None))
    return o
def bmoves(w, b, p):
    """list of (b', p', promo) """
    o = []
    for t in NB[b]:
        if t == w or t in NB[w] or t == p: continue
        o.append((t, p, False))
    f, r = fr(p); one = sq(f, r-1)
    if one != w and one != b:
        if r-1 == 0: o.append((b, None, True))
        else: o.append((b, one, False))
        if r == H-2:
            two = sq(f, r-2)
            if two != w and two != b: o.append((b, two, False))
    return o
# pawn ranks 1..6 (0-based), i.e. ranks 2..7
ST = [(w,b,sq(f,r)) for r in range(1,7) for f in range(W) for w in range(64) for b in range(64) if w != sq(f,r) and b != sq(f,r)]
def solve():
    """worklist retrograde analysis. Nodes: ('B',w,b,p) Black to move; ('W',w,b,p) White to move."""
    from collections import defaultdict, deque
    winB_b = set(); lostW_w = set()
    # successors
    preds = defaultdict(list)       # node -> list of predecessor nodes
    cnt = {}                        # W-node -> number of successors not yet Black-win
    queue = deque()
    for (w,b,p) in ST:
        if w != b and w not in NB[b]:
            ms = wmoves(w,b,p)
            if not ms:
                if check_on_white(w,p):
                    lostW_w.add((w,b,p)); queue.append(('W',w,b,p))
            else:
                cnt[(w,b,p)] = len(ms)
                for t,q in ms:
                    if q is None:
                        cnt[(w,b,p)] = 10**9      # White can capture the pawn: never lost (K v K draw)
                    else:
                        preds[('B',t,b,q)].append(('W',w,b,p))
        if legal(1,w,b,p):
            for t,q,pr in bmoves(w,b,p):
                if pr:
                    if (w,b,p) not in winB_b: winB_b.add((w,b,p)); queue.append(('B',w,b,p))
                else:
                    preds[('W',w,t,q)].append(('B',w,b,p))
    while queue:
        n = queue.popleft()
        for pr in preds.get(n, ()):
            kind,w,b,p = pr
            if kind == 'B':
                if (w,b,p) not in winB_b:
                    winB_b.add((w,b,p)); queue.append(pr)
            else:
                if (w,b,p) in lostW_w: continue
                cnt[(w,b,p)] -= 1
                if cnt[(w,b,p)] == 0:
                    lostW_w.add((w,b,p)); queue.append(pr)
    return winB_b, lostW_w
winB, lostW = solve()
print(sys.argv[1], 'exact: Black-to-move Black-wins', len(winB), 'White-to-move lost', len(lostW))

E = 4
def rel(s, p):
    dx = fr(s)[0]-fr(p)[0]
    if cyl: dx = (dx+4) % 8 - 4
    return (dx, fr(s)[1]-fr(p)[1])
def inS(w, b, p):
    f, r1 = fr(p); r = r1+1
    if f != E or not 2 <= r <= 7: return False
    W_, B_ = rel(w,p), rel(b,p)
    if r >= 4:
        if W_ in ((0,-1),(0,-2)): return True
        if W_ == (-1,-2): return not (B_[0] in (1,2) and -3 <= B_[1] <= 0)
        if W_ == (1,-2): return not (B_[0] in (-1,-2) and -3 <= B_[1] <= 0)
        return False
    d = lambda name: sq(ord(name[0])-97, int(name[1])-1)
    if r == 3:
        if w == d('e2'): return True
        if w == d('e1'): return b not in (d('d3'), d('f3'))
        if w == d('d1'): return b == d('d3')
        if w == d('f1'): return b == d('f3')
        return False
    if r == 2: return w == d('e1') and b in (d('d3'), d('f3'))
def at(p, x, y):
    f, r = fr(p); g = f+x; q = r+y
    if not 0 <= q < H: return None
    if cyl: g %= W
    elif not 0 <= g < W: return None
    return sq(g,q)
def rho(w, b, p):
    """white move per rules 1-5; returns (w', p') or None (no legal move) or raises"""
    ms = wmoves(w, b, p)
    if not ms: return None
    for t,q in ms:
        if q is None: return (t, None)        # rule 1
    legalt = {t for t,q in ms}
    x, y = rel(w, p)
    def go(sqr):
        return (sqr, p) if sqr is not None and sqr in legalt else None
    F, M = at(p,0,-1), at(p,0,-2)
    if (x,y) == (0,-1): r_ = go(M)
    elif (x,y) == (0,-2):
        r_ = go(F)
        if r_ is None:
            bx = rel(b,p)[0]
            assert bx in (-1,1), 'M rule'
            r_ = go(at(p,bx,-2))
    elif (x,y) in ((-1,-2),(1,-2)):
        r_ = go(M) or go(F)
    elif y == -1 and abs(x) == 1:
        r_ = go(F)
    else:
        raise AssertionError('undefined')
    assert r_ is not None, 'rule has no legal move'
    return r_
S = [(w,b,p) for (w,b,p) in ST if legal(1,w,b,p) and inS(w,b,p)]
print('|S| =', len(S), dict(sorted(Counter(fr(p)[1]+1 for _,_,p in S).items(), reverse=True)))
bad = [s for s in S if s in winB]
print('S positions that are Black wins in own exact solve:', len(bad))
pairs = 0; cap = stale = ins = 0; wpos = set()
for (w,b,p) in S:
    for t,q,pr in bmoves(w,b,p):
        pairs += 1
        assert not pr, 'promotion available'
        assert legal(0,w,t,q) or (w != t and w not in NB[t]), 'bad'
        wpos.add((w,t,q))
        r_ = rho(w,t,q)
        if r_ is None:
            assert not check_on_white(w,q), 'White mated'
            stale += 1
        elif r_[1] is None: cap += 1
        else:
            w2, p2 = r_
            assert legal(1,w2,t,p2) and inS(w2,t,p2), ('leaves S', w,b,p,t,q,r_)
            ins += 1
print('closure: pairs', pairs, 'capture', cap, 'stalemate', stale, 'in S', ins, 'distinct white positions', len(wpos))
# is there a Black-to-move S position with no Black move?
print('S positions where Black has no move:', sum(1 for (w,b,p) in S if not bmoves(w,b,p)))
# starts
d = lambda name: sq(ord(name[0])-97, int(name[1])-1)
for wk in ('e5','d5','f5'):
    w, b, p = d(wk), d('d7'), d('e7')
    r_ = rho(w,b,p); print('start', wk, '-> rho ->', r_, 'inS', inS(r_[0], b, r_[1]))
    # also: exact value
    print('   exact White-to-move lost?', (w,b,p) in lostW)
print('OK')
