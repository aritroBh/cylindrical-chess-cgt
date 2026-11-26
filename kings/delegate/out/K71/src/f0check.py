# f0check.py -- K71: independent solver for the promotion game P with a lone White king against
# a Black king and a b-pawn and/or a c-pawn (no White pawns). Written from the rules of P only
# (promotion wins, checkmate loses, stalemate and infinite play draw), retrograde with counters.
# It shares no code with r68.cpp / k71.cpp. Usage: python3 -I f0check.py [dump.txt]
#   prints the value of every position "Black Kb6, b7, c6, White to move" (Lemma F0) and, if a
#   dump file of k71 values is given (lines "FEN value"), compares every position of the family.
import sys
from collections import deque

def sq(f, r): return r * 8 + f
def fr(s): return s % 8, s // 8
def name(s): return "abcdefgh"[s % 8] + str(s // 8 + 1)
NB = []
for s in range(64):
    f, r = fr(s); L = []
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0: continue
            g, t = f + df, r + dr
            if 0 <= g < 8 and 0 <= t < 8: L.append(sq(g, t))
    NB.append(L)
def dist(a, b):
    fa, ra = fr(a); fb, rb = fr(b); return max(abs(fa - fb), abs(ra - rb))
# pawn config: (b, c) with b in {None, 1..6} = rank index (0-based) of the b-pawn, c likewise for the c-pawn
def pawnsq(cfg):
    b, c = cfg; S = []
    if b is not None: S.append(sq(1, b))
    if c is not None: S.append(sq(2, c))
    return S
def attacked_by_black_pawns(cfg):
    A = set()
    for s in pawnsq(cfg):
        f, r = fr(s)
        for df in (-1, 1):
            if 0 <= f + df < 8 and r - 1 >= 0: A.add(sq(f + df, r - 1))
    return A
CFGS = []
for b in [None, 1, 2, 3, 4, 5, 6]:
    for c in [None, 1, 2, 3, 4, 5, 6]:
        if b is None and c is None: continue
        CFGS.append((b, c))
def legal(cfg, wk, bk, stm):
    P = set(pawnsq(cfg))
    if wk == bk or dist(wk, bk) < 2 or wk in P or bk in P: return False
    if stm == 1 and wk in attacked_by_black_pawns(cfg): return False   # White (not to move) in check
    return True
def moves(cfg, wk, bk, stm):
    """list of (kind, newcfg, wk, bk) ; kind 'promo' for a Black promotion"""
    out = []; P = set(pawnsq(cfg)); A = attacked_by_black_pawns(cfg)
    if stm == 0:
        for t in NB[wk]:
            if dist(t, bk) < 2 or t in A: continue
            ncfg = cfg
            if t in P:                       # capture a Black pawn
                b, c = cfg
                ncfg = (None if (b is not None and sq(1, b) == t) else b, None if (c is not None and sq(2, c) == t) else c)
                if ncfg == (None, None): ncfg = None   # bare kings: draw
            out.append(('k', ncfg, t, bk))
    else:
        for t in NB[bk]:
            if dist(t, wk) < 2 or t in P: continue
            out.append(('k', cfg, wk, t))
        b, c = cfg
        for idx, (f, r) in enumerate([(1, b), (2, c)]):
            if r is None: continue
            s1 = sq(f, r - 1)
            if s1 in (wk, bk) or s1 in P: continue
            if r - 1 == 0: out.append(('promo', None, wk, bk)); continue
            n = list(cfg); n[idx] = r - 1; out.append(('k', tuple(n), wk, bk))
            if r == 6:
                s2 = sq(f, 4)
                if s2 not in (wk, bk) and s2 not in P:
                    n2 = list(cfg); n2[idx] = 4; out.append(('k', tuple(n2), wk, bk))
    return out
# retrograde over all states: value from Black's point of view: 'B' Black wins, else draw/unknown
states = []
for cfg in CFGS:
    for wk in range(64):
        for bk in range(64):
            for stm in (0, 1):
                if legal(cfg, wk, bk, stm): states.append((cfg, wk, bk, stm))
idx = {s: i for i, s in enumerate(states)}
N = len(states)
win = [False] * N   # Black wins
cnt = [0] * N       # White to move: number of moves not yet known to lose for White
pred = [[] for _ in range(N)]
Q = deque()
for i, (cfg, wk, bk, stm) in enumerate(states):
    mv = moves(cfg, wk, bk, stm)
    if stm == 1:
        for kind, ncfg, w2, b2 in mv:
            if kind == 'promo':
                if not win[i]: win[i] = True; Q.append(i)
                continue
            j = idx.get((ncfg, w2, b2, 0))
            if j is not None: pred[j].append(i)
    else:
        real = [m for m in mv]
        incheck = wk in attacked_by_black_pawns(cfg)
        if not real:
            if incheck and not win[i]: win[i] = True; Q.append(i)   # checkmate
            continue
        c = 0
        for kind, ncfg, w2, b2 in real:
            if ncfg is None: c += 1; continue          # bare kings: never a Black win
            j = idx.get((ncfg, w2, b2, 1))
            if j is None: raise SystemExit("missing successor")
            pred[j].append(i); c += 1
        # moves to bare kings can never become losses: keep them counted (cnt never reaches 0 then)
        cnt[i] = c
while Q:
    j = Q.popleft()
    for i in pred[j]:
        if win[i]: continue
        if states[i][3] == 1:
            win[i] = True; Q.append(i)
        else:
            cnt[i] -= 1
            if cnt[i] == 0: win[i] = True; Q.append(i)
def fen(cfg, wk, bk, stm):
    P = {s: 'p' for s in pawnsq(cfg)}; P[wk] = 'K'; P[bk] = 'k'; rows = []
    for r in range(7, -1, -1):
        e = 0; row = ''
        for f in range(8):
            ch = P.get(sq(f, r))
            if ch is None: e += 1; continue
            if e: row += str(e); e = 0
            row += ch
        if e: row += str(e)
        rows.append(row)
    return '/'.join(rows) + (' b' if stm else ' w')
F0 = [(i, s) for i, s in enumerate(states) if s[0] == (6, 5) and s[2] == sq(1, 5) and s[3] == 0]
nw = sum(1 for i, s in F0 if win[i])
print("F0 (Black Kb6, b7, c6, White to move): positions %d, Black wins %d" % (len(F0), nw))
print("all states %d, Black wins %d" % (N, sum(win)))
if len(sys.argv) > 2 and sys.argv[1] == '--list':
    byfen = {fen(*st): win[i] for i, st in enumerate(states)}
    n = bad = miss = 0
    for line in open(sys.argv[2]):
        f = line.strip()
        if not f: continue
        n += 1
        if f not in byfen: miss += 1; print("NOT IN DOMAIN", f); continue
        if not byfen[f]: bad += 1; print("NOT A BLACK WIN", f)
    print("list %s: %d positions, not Black wins %d, outside domain %d" % (sys.argv[2], n, bad, miss))
elif len(sys.argv) > 1:
    other = {}
    for line in open(sys.argv[1]):
        a = line.split()
        if len(a) >= 3: other[a[0] + ' ' + a[1]] = a[2]
    dis = 0; seen = 0
    for i, s in enumerate(states):
        f = fen(*s)
        if f in other:
            seen += 1
            ov = other[f] == 'B'
            if ov != win[i]: dis += 1; print("DISAGREE", f, other[f], win[i])
    print("compared %d positions, disagreements %d" % (seen, dis))
