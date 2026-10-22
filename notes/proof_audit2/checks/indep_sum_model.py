"""Independent (CGT-free) implementation of the paper's two models of a pawn position:
  W(X): whole-board game, the first passed pawn ends the game; e.p. rights are global (expire after one ply).
  S(X): sum model; a component that gets a passed pawn is frozen to +-BIG, play goes on in the others;
        e.p. rights live inside their component (the paper's Section V 'sum model').
Both are evaluated by plain alternating-play minimax (outcome only), written from the paper's rules.
It does not import cylcgt/ or lemmas/.   Positions: ((files,ranks,wrap,ep), white, black) with squares (file,rank), ranks from 1.
"""
import sys
from functools import lru_cache
sys.setrecursionlimit(1000000)

class Cfg:
    files = 8; ranks = 8; wrap = True; ep = True
    rule = "count"        # count | mover | opponent
    epaware = True        # e.p.-aware passed test
    BIG = 40

def nb(f, d):
    g = f + d
    if Cfg.wrap:
        return g % Cfg.files
    return g if 0 <= g < Cfg.files else None

def ep_capturable(W, B, ep, side, sqr):
    """is `side`'s pawn on sqr capturable e.p. by the opponent right now?"""
    if not (Cfg.epaware and ep and ep[1] == sqr and ep[2] != side):
        return False
    f, r = sqr
    theirs = B if side == 'W' else W
    return any((g, r) in theirs for g in (nb(f, -1), nb(f, 1)) if g is not None)

def passed(W, B, ep, side):
    mine, theirs = (W, B) if side == 'W' else (B, W)
    for (f, r) in mine:
        fl = {f}
        for d in (-1, 1):
            g = nb(f, d)
            if g is not None:
                fl.add(g)
        if side == 'W':
            blocked = any(g in fl and s > r for g, s in theirs)
        else:
            blocked = any(g in fl and s < r for g, s in theirs)
        if not blocked and not ep_capturable(W, B, ep, side, (f, r)):
            return True
    return False

def promo_dist(W, B, ep, side):
    mine = W if side == 'W' else B
    occ = W | B
    best = 10**6
    for (f, r) in mine:
        # a pawn counts only if it is passed (alone, textbook) and not e.p.-capturable
        fl = {f}
        for d in (-1, 1):
            g = nb(f, d)
            if g is not None:
                fl.add(g)
        theirs = B if side == 'W' else W
        if side == 'W':
            if any(g in fl and s > r for g, s in theirs): continue
        else:
            if any(g in fl and s < r for g, s in theirs): continue
        if ep_capturable(W, B, ep, side, (f, r)): continue
        if side == 'W':
            if any((f, s) in occ for s in range(r + 1, Cfg.ranks + 1)): continue
            d = Cfg.ranks - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)): continue
            d = r - 1 - (1 if r == Cfg.ranks - 1 else 0)
        best = min(best, d)
    return best

def pawn_moves(W, B, ep, side):
    """positions (W', B', ep') after one move of `side`; the right of the other side is ignored (expires)."""
    mine, theirs = (W, B) if side == 'W' else (B, W)
    occ = W | B
    d = 1 if side == 'W' else -1
    start = 2 if side == 'W' else Cfg.ranks - 1
    use_ep = ep if (ep and ep[2] == side) else None
    out = []
    def emit(nm, nt, e=None):
        out.append((frozenset(nm), frozenset(nt), e) if side == 'W' else (frozenset(nt), frozenset(nm), e))
    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if not (1 <= r1 <= Cfg.ranks):
            continue
        if (f, r1) not in occ:
            emit(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= Cfg.ranks and (f, r2) not in occ:
                e = ((f, r1), (f, r2), 'B' if side == 'W' else 'W') if Cfg.ep else None
                emit(rest | {(f, r2)}, theirs, e)
        for df in (-1, 1):
            g = nb(f, df)
            if g is None: continue
            t = (g, r1)
            if t in theirs:
                emit(rest | {t}, theirs - {t})
            elif use_ep and use_ep[0] == t:
                emit(rest | {t}, theirs - {use_ep[1]})
    return list(dict.fromkeys(out))

def race_winner(W, B, ep, mover):
    other = 'B' if mover == 'W' else 'W'
    if Cfg.rule == "mover": return mover
    if Cfg.rule == "opponent": return other
    return other if promo_dist(W, B, ep, other) <= promo_dist(W, B, ep, mover) else mover

def term(W, B, ep, mover):
    """None (non terminal), or 'W'/'B' = winner of the decided position (race rule applied)."""
    wp, bp = passed(W, B, ep, 'W'), passed(W, B, ep, 'B')
    if wp and bp: return race_winner(W, B, ep, mover)
    if wp: return 'W'
    if bp: return 'B'
    return None

# ---------------------------------------------------------------- W
@lru_cache(maxsize=None)
def W_win(W, B, ep, side):
    """True iff `side` to move wins the whole-board game (no terminal at the root)."""
    other = 'B' if side == 'W' else 'W'
    for (w2, b2, e2) in pawn_moves(W, B, ep, side):
        t = term(w2, b2, e2, side)
        res = t if t is not None else (other if W_win(w2, b2, e2, other) else side)
        # res is the winner of the position after the move
        if res == side:
            return True
    return False

def W_outcome(W, B, ep=None):
    t = term(W, B, ep, 'W')
    if t is not None: return 'L' if t == 'W' else 'R'
    wf, ws = W_win(W, B, ep, 'W'), not W_win(W, B, ep, 'B')   # White wins moving first / moving second
    return {(True, True): 'L', (False, False): 'R', (True, False): 'N', (False, True): 'P'}[(wf, ws)]

# ---------------------------------------------------------------- S
def comps(W, B, ep):
    occ = sorted({f for f, _ in W | B})
    if not occ: return []
    groups = []
    for f in occ:
        if groups and f == groups[-1][-1] + 1: groups[-1].append(f)
        else: groups.append([f])
    if Cfg.wrap and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == Cfg.files - 1:
        groups[0] = groups.pop() + groups[0]
    out = []
    for g in groups:
        fs = set(g)
        e = ep if (ep and ep[0][0] in fs) else None
        out.append((frozenset(p for p in W if p[0] in fs), frozenset(p for p in B if p[0] in fs), e))
    return out

def canon(cs):
    return tuple(sorted(cs, key=lambda c: (sorted(c[0]), sorted(c[1]), str(c[2]))))

@lru_cache(maxsize=None)
def S_win(cs, k, side):
    """cs: tuple of live components; k: net frozen integer (units of single moves; +BIG per white passer).
    True iff `side` to move wins (a side with no move loses)."""
    other = 'B' if side == 'W' else 'W'
    # moves in the integer summand
    if side == 'W' and k > 0:
        if not S_win(cs, k - 1, 'B'): return True
    if side == 'B' and k < 0:
        if not S_win(cs, k + 1, 'W'): return True
    for i, (W, B, ep) in enumerate(cs):
        rest = cs[:i] + cs[i + 1:]
        for (w2, b2, e2) in pawn_moves(W, B, ep, side):
            t = term(w2, b2, e2, side)
            if t is not None:
                nk = k + (Cfg.BIG if t == 'W' else -Cfg.BIG)
                nxt = rest
            else:
                nk = k
                nxt = canon(rest + tuple(comps(w2, b2, e2)))
            if not S_win(nxt, nk, other):
                return True
    return False

def S_outcome(W, B, ep=None):
    wp, bp = passed(W, B, ep, 'W'), passed(W, B, ep, 'B')
    if wp != bp: return 'L' if wp else 'R'
    if wp and bp: raise ValueError("race at root")
    cs = canon(tuple(comps(W, B, ep)))
    wf, ws = S_win(cs, 0, 'W'), not S_win(cs, 0, 'B')
    return {(True, True): 'L', (False, False): 'R', (True, False): 'N', (False, True): 'P'}[(wf, ws)]

def parse(text):
    w, b = text.split('/')
    sq = lambda s: ("abcdefghijklmnop".index(s[0]), int(s[1:]))
    W = frozenset(sq(t) for t in w.replace('W:', '').split())
    B = frozenset(sq(t) for t in b.replace('B:', '').split())
    return W, B

def configure(files, ranks, wrap, ep, rule="count", epaware=True, big=40):
    Cfg.files, Cfg.ranks, Cfg.wrap, Cfg.ep, Cfg.rule, Cfg.epaware, Cfg.BIG = files, ranks, wrap, ep, rule, epaware, big
    W_win.cache_clear(); S_win.cache_clear()
