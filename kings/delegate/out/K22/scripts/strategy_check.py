#!/usr/bin/env python3
"""Direct check of the proof of the repaired Lemma 2.9 (independent of any solver value):
s (Black) plays the strategy 'capture an attacked s-bar pawn with an s pawn if there is one, else pass'.
White (s-bar) plays every legal move.  The reachable game graph is explored exhaustively; the proof says that
(i) the strategy always has a legal move, (ii) White never has a promotion available, (iii) White never has a
pawn off file f, (iv) Black is never in check.  Roots: every root with at most one attacked s-bar pawn
(a random sample of SAMPLE of them).
usage: strategy_check.py BOARD W H FZLO FZHI F WMAX BMAX SAMPLE SEED [ep]"""
import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_py
kind, W, H, lo, hi, F, wmax, bmax, nsample, seed = sys.argv[1], *map(int, sys.argv[2:11])
withep = 'ep' in sys.argv[11:]
random.seed(seed)
wrap = kind == 'cyl'
def name(f, r): return chr(97 + f) + str(r + 1)
def fl(a, d):
    f = a + d
    return f % W if wrap else (f if 0 <= f < W else None)
wsq = [(F, r) for r in range(1, H - 1)]
bsq = [(f, r) for f in range(lo, hi + 1) for r in range(1, H - 1)]
roots = []
for nw in range(1, wmax + 1):
  for wp in itertools.combinations(wsq, nw):
    front = max(r for f, r in wp)
    for nb in range(0, bmax + 1):
      for bp in itertools.combinations(bsq, nb):
        if set(wp) & set(bp): continue
        att = sum(1 for (f, r) in wp if any((fl(f, d), r + 1) in bp for d in (-1, 1)))
        if (att >= 2) != bool(os.environ.get('CONTROL')): continue
        eps = [None]
        if withep and H >= 6 and (F, 3) in wp and (F, 1) not in wp and (F, 2) not in wp and not ((F,1) in bp or (F,2) in bp):
            if any((fl(F, d), 3) in bp for d in (-1, 1)): eps.append(((F, 2), 0))
        for ep in eps:
          for wk in [(f, r) for f in range(lo, hi + 1) for r in range(H)]:
            for bk in [(F, r) for r in range(front + 1, H)]:
                if wk == bk or wk in wp or wk in bp or bk in bp: continue
                if any(fl(wk[0], d) is not None and (fl(wk[0], d), wk[1] + 1) in bp for d in (-1, 1)): continue
                df = abs(wk[0] - bk[0]); df = min(df, W - df) if wrap else df
                if max(df, abs(wk[1] - bk[1])) <= 1: continue
                roots.append((frozenset(wp), frozenset(bp), wk, bk, 1, ep))
random.shuffle(roots)
roots = roots[:nsample]
solve = local_py.make(kind, W, H, lo, hi, False)
moves, hit = solve.moves, solve.hit
viol = 0; nstates = 0
for root in roots:
    seen = set(); stack = [root]; bad = None
    while stack and not bad:
        s = stack.pop()
        if s in seen: continue
        seen.add(s)
        wp, bp, wk, bk, stm, ep = s
        if any(p[0] != F for p in wp): bad = ('pawn off f', s); break
        ms = moves(s)
        if stm == 0:
            for k, ns in ms:
                if k != 'go': bad = ('white promotion available', s); break
                stack.append(ns)
        else:
            if hit(0, bk, wp): bad = ('black in check', s); break
            att = [p for p in wp if any((fl(p[0], d), p[1] + 1) in bp for d in (-1, 1))]
            if len(att) > 1 and s is not root: bad = ('two attacked pawns at a Black turn', s); break
            if att:
                strat = [ns for k, ns in ms if k == 'go' and len(ns[0]) < len(wp) and ns[3] == bk]
            else:
                strat = [ns for k, ns in ms if k == 'go' and ns[3] == bk and ns[0] == wp and ns[1] == bp and ns[2] == wk]
            if not strat: bad = ('strategy has no legal move', s); break
            for ns in strat: stack.append(ns)
    nstates += len(seen)
    if os.environ.get('CONTROL') and bad and bad[0].startswith('two'): bad = None; ctrl_two = globals().get('ctrl_two', 0) + 1
    if bad:
        viol += 1
        if viol <= 5: print('VIOLATION', bad[0], 'root', root[:4], '-> state', bad[1][:4])
print('%s:%dx%d FZ=%d..%d f=%d wmax=%d bmax=%d: %d roots with <=1 attacked pawn checked (of %d sampled), %d states, violations=%d' % (kind, W, H, lo, hi, F, wmax, bmax, len(roots), len(roots), nstates, viol))
