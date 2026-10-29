"""r2_tree.py -- referee 2: own enumeration of (A) Black's never-promote rule tau in EPW, (C) the Kf7 ...e5 line,
(B) White's strategy sigma after Ke5 / Kd5 / Kf5 (Lemma D rule rho, Kc7 -> Ke6, captures, free mode).
Written from the text of PROOF.md; uses only r2_lib (own generator).   usage: r2_tree.py cyl|flat"""
import sys, collections
from r2_lib import *
kind = sys.argv[1]
B = Board(kind)
sq = lambda f, r: f + 8 * (r - 1)
corners = {0, 7, 56, 63}
X = parse(B, 'Ke6 Pd7 kd8 pe7 w -')
ids, states_all, succ_all, term_all, chk_all = build(B, [X])
WWe, BWe = solve(states_all, succ_all, term_all, chk_all, 'EPW')
WWb, BWb = solve(states_all, succ_all, term_all, chk_all, 'EPB')
WWp, BWp = solve(states_all, succ_all, term_all, chk_all, 'P')
def val(WW, BW, st): return value(WW, BW, ids[st])
def mv(st, lab):
    r = [n for l, k, n in gen(B, st) if l == lab]
    assert len(r) == 1, (lab, r)
    return r[0]
# ---------------- statement 0 ----------------
print('White moves at X:', sorted(l for l, k, n in gen(B, X)))
sorties = {'e5': mv(X, 'e6e5'), 'd5': mv(X, 'e6d5'), 'f5': mv(X, 'e6f5'), 'f7': mv(X, 'e6f7')}
# ---------------- part A: Kxd7 exists after each; tau in EPW ----------------
start = []
for s, st in sorties.items():
    labs = [l for l, k, n in gen(B, st)]
    assert 'd8d7x' in labs, s
    start.append(mv(st, 'd8d7x'))
    assert 'e7e6' in labs or True
def tau_moves(st):
    """Black to move: tau = move the king (never the pawn) to a legal neighbour that is not a flat corner."""
    wk, bk, wp, bp, side = st
    assert side == 1 and wp == -1
    out = []
    for l, k, n in gen(B, st):
        if k != 'n': raise AssertionError('Black has a promotion move under tau-states')
        if n[1] == bk: continue                      # a pawn move (king unchanged): excluded by tau
        if kind == 'flat' and n[1] in corners: continue
        out.append(n)
    return out
Wset = set(start); Bset = set(); fr = list(start)
while fr:
    w = fr.pop()
    assert not in_check(B, w)
    for l, k, nb in gen(B, w):
        assert k == 'n'          # White has no pawn: no promotion
        Bset.add(nb)
        t = tau_moves(nb)
        assert t, ('Black has no tau move', fmt(nb))
        assert not in_check(B, nb)
        for u in t:
            if u not in Wset: Wset.add(u); fr.append(u)
bad = [w for w in Wset if val(WWe, BWe, w) == 'W'] + [b for b in Bset if val(WWe, BWe, b) == 'W']
print('A. tau (EPW): White-to-move states', len(Wset), '(pawn still on e7: %d)' % sum(1 for w in Wset if w[3] >= 0), 'Black-to-move states', len(Bset), '(pawn on e7: %d)' % sum(1 for w in Bset if w[3] >= 0),
      'positions valued W in EPW:', len(bad), '; Black always has a tau move; Black never in check; White has no pawn')
# ---------------- part C: Kf7 e5 line ----------------
f7 = sorties['f7']
e5 = mv(f7, 'e7e5')
fr = {e5}; depth = 0; allW = set(); prom_at = set(); capt = 0
while fr:
    depth += 1
    nf = set()
    for w in fr:
        allW.add(w)
        assert not in_check(B, w)
        for l, k, nb in gen(B, w):
            assert k == 'n'                        # White has no promotion (d8 holds the Black king)
            if nb[3] == -1:
                capt += 1; continue                # White captured the pawn
            assert nb[1] == sqn('d8') and not in_check(B, nb)
            lab = name(nb[3]) + name(nb[3] - 8)
            cand = [(l2, k2, n2) for l2, k2, n2 in gen(B, nb) if l2 in (lab, lab + '=')]
            assert len(cand) == 1, (fmt(w), l)     # the push is always available
            l2, k2, n2 = cand[0]
            if k2 == 'BP': prom_at.add(depth)
            else: nf.add(n2)
    fr = nf
print('C. Kf7 e5 line: White-to-move states', len(allW), 'White moves that capture the pawn:', capt,
      'promotion at push number (after ...e5):', sorted(prom_at),
      '; every such White-to-move state is L in P:', all(val(WWp, BWp, w) == 'L' for w in allW))
# ---------------- part B: sigma ----------------
def rho(st):
    wk, bk, wp, bp, side = st
    assert wp == -1 and bp >= 0 and side == 0
    p = bp; w = wk; b = bk
    r = p // 8 + 1
    def legalt(t):
        return t is not None and B.adj[w][t] and t != b and not B.adj[t][b] and t != p and t not in B.batt[p]
    if B.adj[w][p] and not B.adj[p][b]: return [mv(st, name(w) + name(p) + 'x')]
    x, y = B.relx(w, p % 8), w // 8 - p // 8
    F = sq(4, r - 1) if r - 1 >= 1 else None
    M = sq(4, r - 2) if r - 2 >= 1 else None
    if (x, y) == (0, -1): t = M
    elif (x, y) == (0, -2):
        if legalt(F): t = F
        else: t = sq(3, r - 2) if b % 8 == 3 else (sq(5, r - 2) if b % 8 == 5 else None)
    elif (x, y) in ((-1, -2), (1, -2)): t = M if legalt(M) else F
    elif (x, y) in ((-1, -1), (1, -1)): t = F
    else: t = None
    if t is None or not legalt(t):
        anyw = gen(B, st)
        if not anyw and not in_check(B, st): return []         # stalemate
        raise AssertionError(('rho illegal', fmt(st), t))
    return [mv(st, name(w) + name(t))]
def sigma_reply(st, s):
    """list of White replies (one for strategy positions, all king moves in free mode); [] = no legal move."""
    wk, bk, wp, bp, side = st
    if wp >= 0 and bp < 0:                        # free mode: any king move, never the pawn
        return [n for l, k, n in gen(B, st) if k == 'n' and l.startswith(name(wk))]
    if wp < 0 and bp >= 0:
        return rho(st)
    if st == X: return [sorties[s]]
    if bp == sqn('e7') and wk == sqn('e6') and wp == sqn('d7') and bk in (sqn('b8'), sqn('b7'), sqn('b6'), sqn('c6')):
        return [mv(st, 'e6e7x')]          # the pawn is no longer protected
    if bp == sqn('e7') and bk == sqn('c7') and wp == sqn('d7'):
        return [mv(st, name(wk) + 'e6')]
    if bp in (sqn('e6'), sqn('e5')) and bk == sqn('d8') and wp == sqn('d7'):
        return [mv(st, name(wk) + name(bp) + 'x')]
    raise AssertionError(('sigma undefined', fmt(st)))
res = {}
for s in ('e5', 'd5', 'f5'):
    st0 = sorties[s]
    Wst = set(); Bst = set([st0]); dq = [st0]
    nomove = 0; freeW = 0; kvk = 0; drow = collections.Counter()
    promo = 0; mated = 0; bnomove = 0; bmated = 0
    while dq:
        b_ = dq.pop()
        mvs = gen(B, b_)
        if any(k != 'n' for l, k, n in mvs): promo += 1
        if not mvs:
            bnomove += 1
            if in_check(B, b_): bmated += 1
            continue
        for l, k, w in mvs:
            if k != 'n': continue
            if w[2] < 0 and w[3] < 0: kvk += 1; continue        # K against K: nothing more can happen
            if w in Wst: continue
            Wst.add(w)
            wm = gen(B, w)
            if not wm:
                if in_check(B, w): mated += 1
                nomove += 1
                continue
            r = sigma_reply(w, s)
            if not r:
                nomove += 1; continue
            for nb in r:
                if nb not in Bst: Bst.add(nb); dq.append(nb)
    free = sum(1 for w in Wst if w[2] >= 0 and w[3] < 0)
    res[s] = (len(Wst), free, len(Bst), promo, mated, nomove)
    # values: no state of the sigma tree is L in P or EPB or chess-model; check P and EPB
    badp = sum(1 for w in Wst if val(WWb, BWb, w) == 'L') + sum(1 for b in Bst if val(WWb, BWb, b) == 'L')
    badq = sum(1 for w in Wst if val(WWp, BWp, w) == 'L') + sum(1 for b in Bst if val(WWp, BWp, b) == 'L')
    print('B. sortie K%s: White-to-move states %d (free mode %d), Black-to-move %d; Black promotion moves seen %d; White mated %d; White stalemated %d; Black stalemated/mated-by-White %d/%d; states that are L in EPB %d, in P %d'
          % (s, len(Wst), free, len(Bst), promo, mated, nomove, bnomove - bmated, bmated, badp, badq))
