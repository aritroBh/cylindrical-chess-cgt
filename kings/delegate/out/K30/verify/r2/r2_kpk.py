"""r2_kpk.py -- referee 2: own exact K + black pawn vs K solver (all pawn files), and an own implementation of the
invariant S and the rule rho of Lemma D, written from the TEXT of PROOF.md section 4.1.  Own code only (r2_lib.Board).
usage: r2_kpk.py cyl|flat"""
import sys, collections
from r2_lib import Board, name, sqn
kind = sys.argv[1]
B = Board(kind)
sq = lambda f, r: f + 8 * (r - 1)          # r = rank number 1..8

# ---------------- exact solver of K + black pawn vs K : Black wins = promotion or mate of White ----------
# states: (side, wk, bk, p) ; side 0 = White to move, 1 = Black to move
def legal(side, wk, bk, p):
    if wk == bk or B.adj[wk][bk] or p in (wk, bk): return False
    if not (1 <= p // 8 <= 6): return False
    if side == 1 and wk in B.batt[p]: return False        # White would be in check with Black to move
    return True
def moves(side, wk, bk, p):
    """-> (list of successor states, has_capture, promotion_available, in_check_white)"""
    succ = []; cap = False; prom = False
    if side == 0:
        for n in B.nb[wk]:
            if n == bk or B.adj[n][bk]: continue
            if n == p: cap = True; continue
            if n in B.batt[p]: continue
            succ.append((1, n, bk, p))
        return succ, cap, False
    for n in B.nb[bk]:
        if n == p or n == wk or B.adj[n][wk]: continue
        succ.append((0, wk, n, p))
    f, r = p % 8, p // 8
    q = p - 8
    if q not in (wk, bk):
        if q // 8 == 0: prom = True
        else:
            succ.append((0, wk, bk, q))
            if r == 6 and (p - 16) not in (wk, bk):
                succ.append((0, wk, bk, p - 16))
    return succ, False, prom
allst = [(s, w, b, p) for s in (0, 1) for p in range(8, 56) for w in range(64) for b in range(64) if legal(s, w, b, p)]
idx = {s: i for i, s in enumerate(allst)}
n = len(allst)
succ = [None] * n; hascap = [False] * n; prom = [False] * n; win = [False] * n
pred = [[] for _ in range(n)]
for i, s in enumerate(allst):
    sl, cap, pr = moves(*s)
    succ[i] = [idx[x] for x in sl]       # KeyError would mean an illegal successor was generated
    hascap[i] = cap; prom[i] = pr
    for j in succ[i]: pred[j].append(i)
cnt = [0] * n; q = []
for i, s in enumerate(allst):
    if s[0] == 1:
        if prom[i]: win[i] = True; q.append(i)
    else:
        nm = len(succ[i]) + (1 if hascap[i] else 0)
        if hascap[i]: cnt[i] = -10**9; continue
        if nm == 0:
            if s[1] in B.batt[s[3]]: win[i] = True; q.append(i)      # mate of White
            continue                                                   # else stalemate: draw
        cnt[i] = len(succ[i])
while q:
    j = q.pop()
    for i in pred[j]:
        if win[i]: continue
        if allst[i][0] == 1: win[i] = True; q.append(i)
        else:
            cnt[i] -= 1
            if cnt[i] == 0: win[i] = True; q.append(i)
nB = sum(1 for i, s in enumerate(allst) if s[0] == 1 and win[i])
nW = sum(1 for i, s in enumerate(allst) if s[0] == 0 and win[i])
print(kind, 'KPk states', n, 'Black-to-move Black wins', nB, 'White-to-move Black wins', nW)
# sanity: a1 / d7 / e7 black to move is a Black win (White king far in the corner) ; and the three stated draws
def bw(side, w, b, p): return win[idx[(side, sqn(w), sqn(b), sqn(p))]]
print('sanity Ka1 kd7 pe7 Black to move: Black wins =', bw(1, 'a1', 'd7', 'e7'))
# ---------------- the invariant S and the rule rho, from the text ----------------
def rel(s, p):
    return (B.relx(s, p % 8), s // 8 - p // 8)
def Zset(p, sign):
    """Z_L (sign +1): files +1,+2 ; Z_R (sign -1): files -1,-2 ; ranks r-3..r"""
    r = p // 8 + 1
    out = set()
    for x in (1, 2):
        for rr in range(r - 3, r + 1):
            if 1 <= rr <= 8: out.add(sq(4 + sign * x, rr))
    return out
def all_S():
    S = set()
    for r in range(2, 8):
        p = sq(4, r)
        def add(w, bs):
            for b in bs:
                if legal(1, w, b, p): S.add((w, b, p))   # 'legal' = the stated 'all positions are legal'
        allb = range(64)
        if r >= 4:
            F, M, L, R = sq(4, r - 1), sq(4, r - 2), sq(3, r - 2), sq(5, r - 2)
            add(F, allb); add(M, allb)
            ZL, ZR = Zset(p, +1), Zset(p, -1)
            add(L, [b for b in allb if b not in ZL]); add(R, [b for b in allb if b not in ZR])
        elif r == 3:
            add(sq(4, 2), allb)
            add(sq(4, 1), [b for b in allb if b not in (sq(3, 3), sq(5, 3))])
            add(sq(3, 1), [sq(3, 3)]); add(sq(5, 1), [sq(5, 3)])
        else:   # r == 2
            add(sq(4, 1), [sq(3, 3), sq(5, 3)])
    return S
S = all_S()
perr = collections.Counter(p // 8 + 1 for (_, _, p) in S)
print('|S| =', len(S), 'by pawn rank', dict(sorted(perr.items())))
# every position of S: all are legal (by construction) and none is a Black win
badS = [x for x in S if win[idx[(1,) + x]]]
print('positions of S that are Black wins (Black to move):', len(badS))
def wlegal_target(w, t, b, p):
    """can the White king go from w to t (empty or the pawn square handled elsewhere)?"""
    return t is not None and B.adj[w][t] and t != b and not B.adj[t][b] and t != p and t not in B.batt[p]
def rho(w, b, p):
    """returns the target square (int) or None (rule undefined); the capture is 'cap'."""
    r = p // 8 + 1
    if B.adj[w][p] and not B.adj[p][b]:       # rule 1: capture, legal iff the pawn is unprotected
        return 'cap'
    x, y = rel(w, p)
    def Fsq(): return sq(4, r - 1) if r - 1 >= 1 else None
    def Msq(): return sq(4, r - 2) if r - 2 >= 1 else None
    F, M = Fsq(), Msq()
    if (x, y) == (0, -1):                      # rule 2
        return M
    if (x, y) == (0, -2):                      # rule 3
        if wlegal_target(w, F, b, p): return F
        bf = b % 8
        if bf == 3: return sq(3, r - 2)
        if bf == 5: return sq(5, r - 2)
        return None
    if (x, y) in ((-1, -2), (1, -2)):          # rule 4
        if wlegal_target(w, M, b, p): return M
        return F
    if (x, y) in ((-1, -1), (1, -1)):          # rule 5
        return F
    return None
def black_moves(w, b, p):
    """black legal moves from (w,b,p) with Black to move: list of (kind, b', p') ; kind 'k','s','d','prom'"""
    out = []
    for n_ in B.nb[b]:
        if n_ == p or n_ == w or B.adj[n_][w]: continue
        out.append(('k', n_, p))
    q_ = p - 8
    if q_ not in (w, b):
        if q_ // 8 == 0: out.append(('prom', b, None))
        else:
            out.append(('s', b, q_))
            if p // 8 == 6 and (p - 16) not in (w, b): out.append(('d', b, p - 16))
    return out
pairs = 0; capc = 0; stal = 0; inS = 0; fails = []
Wpos = set()
for (w, b, p) in sorted(S):
    for kind_, b2, p2 in black_moves(w, b, p):
        pairs += 1
        if kind_ == 'prom': fails.append(('promotion', w, b, p)); continue
        Wpos.add((w, b2, p2))
        # legal White-to-move position?  (kings not adjacent: ensured)
        t = rho(w, b2, p2)
        if t == 'cap':
            capc += 1; continue
        # does White have any legal move at all? (needed to classify the failure)
        anyw = [n_ for n_ in B.nb[w] if n_ != b2 and not B.adj[n_][b2] and (n_ == p2 or n_ not in B.batt[p2])]
        if t is None or not wlegal_target(w, t, b2, p2):
            if not anyw and w not in B.batt[p2]: stal += 1; continue      # stalemate: draw
            fails.append(('rho undefined/illegal', w, b2, p2, t)); continue
        if (t, b2, p2) in S: inS += 1
        else: fails.append(('left S', w, b2, p2, t))
print('closure: pairs', pairs, 'captures', capc, 'white stalemates', stal, 'reply in S', inS,
      'distinct White-to-move positions', len(Wpos), 'FAILURES', len(fails))
for f in fails[:10]: print('   ', [name(x) if isinstance(x, int) else x for x in f])
# no rho reply is a Black win, no White-to-move position of the closure is a Black win
badW = [x for x in Wpos if win[idx[(0,) + x]]]
print('White-to-move positions of the closure that are Black wins:', len(badW))
# the three starting positions: after a sortie and ...Kxd7 (White to move)
for w0 in ('e5', 'd5', 'f5'):
    w, b, p = sqn(w0), sqn('d7'), sqn('e7')
    t = rho(w, b, p)
    ok = t not in (None, 'cap') and wlegal_target(w, t, b, p) and (t, b, p) in S
    print('start Kx %s kd7 pe7 w: rho -> %s  in S: %s ; Black-win(White to move)=%s' % (w0, name(t), ok, win[idx[(0, w, b, p)]]))
# S compared with Black-win set: how many of the Black-to-move positions with the pawn on the e-file satisfy
# 'legal and not Black win' (S is a subset)
efile = [x for x in allst if x[0] == 1 and x[3] % 8 == 4]
print('e-file Black-to-move legal positions', len(efile), 'of which not Black wins', sum(1 for x in efile if not win[idx[x]]))
