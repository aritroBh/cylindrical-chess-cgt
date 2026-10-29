#!/usr/bin/env python3
"""Referee's own solver (written from SPEC.md and PROOF.md text only; no K30 code) for the K30 material:
White king, White pawn on d7 (static until d8), Black king, Black pawn on the e-file.
Models: P (first promotion wins for promoter), EPW (any promotion = White win), EPB (any promotion = Black win).
usage: myx.py cyl|flat"""
import sys, itertools
cyl = sys.argv[1] == 'cyl'
W = H = 8
def sq(f, r): return r*W+f
def fr(s): return s % W, s//W
def nbrs(s):
    f, r = fr(s); out = []
    for df in (-1,0,1):
        for dr in (-1,0,1):
            if df==0 and dr==0: continue
            g = f+df; q = r+dr
            if not (0 <= q < H): continue
            if cyl: g %= W
            elif not (0 <= g < W): continue
            out.append(sq(g,q))
    return out
NB = [frozenset(nbrs(s)) for s in range(W*H)]
D7, D8, E7 = sq(3,6), sq(3,7), sq(4,6)
# Black pawn square attacks: black pawn at (f,r) attacks (f+-1, r-1)
def patt_b(p):
    f, r = fr(p); out = set()
    for df in (-1,1):
        g = f+df
        if cyl: g %= W
        elif not (0 <= g < W): continue
        if r-1 >= 0: out.add(sq(g, r-1))
    return out
PB = {p: patt_b(p) for p in range(W*H)}
# White pawn d7 attacks c8, e8
PW = {sq(2,7), sq(4,7)}

# state: (stm, wk, bk, wp, bp)  wp in (D7, None), bp in e-file squares or None
def attacked_by_white(s, wk, wp):
    return s in NB[wk] or (wp is not None and s in PW)
def attacked_by_black(s, bk, bp):
    return s in NB[bk] or (bp is not None and s in PB[bp])

def legal(st):
    stm, wk, bk, wp, bp = st
    if wk == bk or wk in NB[bk]: return False
    if wp is not None and wp in (wk, bk): return False
    if bp is not None and bp in (wk, bk): return False
    if wp is not None and bp is not None and wp == bp: return False
    if stm == 0 and attacked_by_white(bk, wk, wp): return False   # black king attacked, white to move: illegal
    if stm == 1 and (bp is not None and wk in PB[bp]): return False
    return True

def inc(st):
    stm, wk, bk, wp, bp = st
    if stm == 0: return bp is not None and wk in PB[bp]
    return attacked_by_white(bk, wk, wp)

PROMO = 'PROMO'
def moves(st):
    """list of successor states, or the token ('promo', side) for a promotion move"""
    stm, wk, bk, wp, bp = st
    out = []
    if stm == 0:
        for t in NB[wk]:
            if t == bk or t in NB[bk]: continue
            if bp is not None and t in PB[bp]: continue
            if wp is not None and t == wp: continue
            nbp = None if (bp is not None and t == bp) else bp
            out.append((1, t, bk, wp, nbp))
        if wp is not None:      # pawn d7: d8 push (promotion) if empty; captures c8/e8 need enemy piece (none capturable)
            if bk != D8 and wk != D8 and (bp is None or bp != D8):
                out.append(('promo', 0))
    else:
        for t in NB[bk]:
            if t == wk or t in NB[wk]: continue
            if t == bp: continue
            if wp is not None and t in PW: continue
            nwp = None if (wp is not None and t == wp) else wp
            out.append((0, wk, t, nwp, bp))
        if bp is not None:
            f, r = fr(bp)
            one = sq(f, r-1)
            occ = {wk, bk} | ({wp} if wp is not None else set())
            if one not in occ:
                if r-1 == 0: out.append(('promo', 1))
                else: out.append((0, wk, bk, wp, one))
                if r == H-2:
                    two = sq(f, r-2)
                    if two not in occ: out.append((0, wk, bk, wp, two))
    return out

def allstates():
    S = []
    bps = [None] + [sq(f,r) for f in range(W) for r in range(1,H-1)]
    wps = [None, D7]
    for stm in (0,1):
        for wk in range(64):
            for bk in range(64):
                for wp in wps:
                    for bp in bps:
                        st = (stm, wk, bk, wp, bp)
                        if legal(st): S.append(st)
    return S

def solve(model):
    from collections import defaultdict, deque
    states = allstates()
    succ = {st: moves(st) for st in states}
    def pval(s):
        if model == 'P': return +1 if s == 0 else -1
        if model == 'EPW': return +1
        return -1
    preds = defaultdict(list)
    for st in states:
        for m in succ[st]:
            if m[0] != 'promo': preds[m].append(st)
    win = {}
    for who in (+1, -1):
        Wn = set(); queue = deque(); cnt = {}
        for st in states:
            mover = +1 if st[0] == 0 else -1
            ms = succ[st]
            if not ms:
                if inc(st) and mover != who: Wn.add(st); queue.append(st)
                continue
            if mover == who:
                if any(m[0] == 'promo' and pval(m[1]) == who for m in ms): Wn.add(st); queue.append(st)
            else:
                # opponent to move: all successors must be wins for who; promotions count immediately
                if any(m[0] == 'promo' and pval(m[1]) != who for m in ms): cnt[st] = 10**9
                else: cnt[st] = sum(1 for m in ms if m[0] != 'promo')
                if cnt[st] == 0: Wn.add(st); queue.append(st)
        while queue:
            n = queue.popleft()
            for pr in preds.get(n, ()):
                if pr in Wn: continue
                mover = +1 if pr[0] == 0 else -1
                if mover == who:
                    Wn.add(pr); queue.append(pr)
                else:
                    cnt[pr] -= 1
                    if cnt[pr] == 0: Wn.add(pr); queue.append(pr)
        win[who] = Wn
    val = {}
    for st in states:
        assert not (st in win[+1] and st in win[-1])
        val[st] = 'W' if st in win[+1] else ('L' if st in win[-1] else 'D')
    return states, val, succ

def P(s):
    # parse like 'e6' -> square
    return sq(ord(s[0])-97, int(s[1])-1)
if __name__ == '__main__':
    X = (0, P('e6'), P('d8'), D7, E7)
    assert legal(X)
    res = {}
    for model in ('P','EPW','EPB'):
        states, val, succ = solve(model)
        print(sys.argv[1], model, 'states', len(states), 'X =', val[X])
        for m in succ[X]:
            print('   move ->', m, val[m] if m[0] != 'promo' else 'promo')
        from collections import Counter
        print('   value counts', Counter(val.values()))
