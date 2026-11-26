#!/usr/bin/env python3
# Independent re-implementation of the pawn game from dist/tog/sections/02_rules.tex
# and 05_sums.tex. Written from the paper text only. No repo solver imported.
# Model: W(X) whole-board (first passed pawn ends); S(X) sum model (components + BIG).
# Value test: X has value v iff the player to move loses in X + (-v), for both players.
import sys
from functools import lru_cache
sys.setrecursionlimit(1000000)

# ---- Board / settings ----
FLAT, CYL = 'flat', 'cyl'
BIG = 256

def beside(n, topo, f, right):
    if right:
        if f + 1 < n: return (f + 1,)
        return (0,) if topo == CYL else None
    else:
        if f > 0: return (f - 1,)
        return (n - 1,) if topo == CYL else None

def ahead(up, r): return r + 1 if up else r - 1
def onBoard(ranks, r): return 1 <= r <= ranks
def homeRank(ranks, up): return 2 if up else ranks - 1

# Pawn = (file, rank, up)  up True=white
def capture_targets(n, topo, ranks, p):
    f, r, up = p
    out = []
    for right in (True, False):
        b = beside(n, topo, f, right)
        if b is None: continue
        g = b[0]
        rr = ahead(up, r)
        if onBoard(ranks, rr): out.append((g, rr, up))
    return out

def occupied(white, black, sq):
    return any((p[0], p[1]) == sq for p in (white | black))

def ep_captures(n, topo, ranks, white, black, owner, v):
    # owner: color of pawn v; capturers are the other color
    skipped = (v[0], ahead(not v[2], v[1]))
    capturers = white if owner == 'black' else black
    res = []
    for q in capturers:
        for t in capture_targets(n, topo, ranks, q):
            if (t[0], t[1]) == skipped:
                res.append((q, t))
    return res

def gen_moves(s, b, white, black, ep, c):
    # s = settings dict {ep: off/textbook/aware, race: count/mover/opponent}
    # b = (n, ranks, topo). Returns list of (white,black,ep).
    n, ranks, topo = b
    mine = white if c == 'white' else black
    theirs = black if c == 'white' else white
    out = []
    for p in mine:
        f, r, up = p
        # single step
        r1 = ahead(up, r)
        if onBoard(ranks, r1) and not occupied(white, black, (f, r1)):
            nmine = (mine - {p}) | {(f, r1, up)}
            w, bl = (nmine, theirs) if c == 'white' else (theirs, nmine)
            out.append((w, bl, None))
        # double step
        r2 = ahead(up, r1)
        if r == homeRank(ranks, up) and onBoard(ranks, r1) and onBoard(ranks, r2) \
           and not occupied(white, black, (f, r1)) and not occupied(white, black, (f, r2)):
            p2 = (f, r2, up)
            nmine = (mine - {p}) | {p2}
            w, bl = (nmine, theirs) if c == 'white' else (theirs, nmine)
            newep = None
            if s['ep'] != 'off' and ep_captures(n, topo, ranks, w, bl, c, p2):
                newep = (f, r2)
            out.append((w, bl, newep))
        # capture
        for t in capture_targets(n, topo, ranks, p):
            tsq = (t[0], t[1])
            q = None
            for qq in theirs:
                if (qq[0], qq[1]) == tsq: q = qq; break
            if q is not None:
                nmine = (mine - {p}) | {t}
                ntheirs = theirs - {q}
                w, bl = (nmine, ntheirs) if c == 'white' else (ntheirs, nmine)
                out.append((w, bl, None))
        # en passant
        if ep is not None:
            e = ep
            v = None
            for qq in theirs:
                if (qq[0], qq[1]) == e: v = qq; break
            if v is not None and s['ep'] != 'off':
                owner = 'black' if c == 'white' else 'white'
                for (q, t) in ep_captures(n, topo, ranks, white, black, owner, v):
                    if q == p:
                        nmine = (mine - {p}) | {t}
                        ntheirs = theirs - {v}
                        w, bl = (nmine, ntheirs) if c == 'white' else (ntheirs, nmine)
                        out.append((w, bl, None))
    # dedup
    seen = set(); res = []
    for st in out:
        key = (frozenset(st[0]), frozenset(st[1]), st[2])
        if key not in seen: seen.add(key); res.append(st)
    return res

# ---- passed pawns ----
def is_ahead(up, r, s): return r < s if up else s < r

def blocks(n, topo, ranks, p, q):
    f, r, up = p
    if q[0] == f and is_ahead(up, r, q[1]): return True
    for right in (True, False):
        bb = beside(n, topo, f, right)
        if bb is not None and q[0] == bb[0] and is_ahead(up, r, q[1]): return True
    return False

def textbook_passed(n, topo, ranks, white, black, c, p):
    theirs = black if c == 'white' else white
    return all(not blocks(n, topo, ranks, p, q) for q in theirs)

def ep_capturable(n, topo, ranks, white, black, ep, c, p):
    if ep is None or (p[0], p[1]) != ep: return False
    return len(ep_captures(n, topo, ranks, white, black, c, p)) > 0

def passed(s, b, white, black, ep, c, p):
    n, ranks, topo = b
    tp = textbook_passed(n, topo, ranks, white, black, c, p)
    if not tp: return False
    if s['ep'] == 'aware' and ep_capturable(n, topo, ranks, white, black, ep, c, p):
        return False
    return True

def has_passed(s, b, white, black, ep, c):
    mine = white if c == 'white' else black
    return any(passed(s, b, white, black, ep, c, p) for p in mine)

def distance(ranks, p):
    f, r, up = p
    d = (ranks - r) if up else (r - 1)
    if r == homeRank(ranks, up) and 2 <= d: return d - 1
    return d

def is_front(white, black, p):
    f, r, up = p
    for q in (white | black):
        if q[0] == f and is_ahead(up, r, q[1]): return False
    return True

def race_distance(s, b, white, black, ep, c):
    n, ranks, topo = b
    mine = white if c == 'white' else black
    ds = [distance(ranks, p) for p in mine if passed(s, b, white, black, ep, c, p) and is_front(white, black, p)]
    return min(ds) if ds else None

def le_inf(x, y):  # x <= y, None = infinity
    if y is None: return True
    if x is None: return False
    return x <= y

def race_winner(s, b, white, black, ep, mover):
    if s.get('force') in ('white', 'black'): return s['force']
    if s['race'] == 'mover': return mover
    if s['race'] == 'opponent': return 'black' if mover == 'white' else 'white'
    # count
    other = 'black' if mover == 'white' else 'white'
    if le_inf(race_distance(s, b, white, black, ep, other), race_distance(s, b, white, black, ep, mover)):
        return other
    return mover

def classify(s, b, white, black, ep, mover):
    hw = has_passed(s, b, white, black, ep, 'white')
    hb = has_passed(s, b, white, black, ep, 'black')
    if not hw and not hb: return ('open',)
    if hw and not hb: return ('won', 'white')
    if hb and not hw: return ('won', 'black')
    return ('race', race_winner(s, b, white, black, ep, mover))

# ---- components ----
def components(b, white, black, ep):
    n, ranks, topo = b
    occ = sorted({p[0] for p in (white | black)})
    if not occ: return []
    # runs of consecutive files
    runs = []
    cur = [occ[0]]
    for f in occ[1:]:
        if f == cur[-1] + 1: cur.append(f)
        else: runs.append(cur); cur = [f]
    runs.append(cur)
    # merge across seam for cyl
    if topo != FLAT and len(runs) >= 2 and runs[0][0] == 0 and runs[-1][-1] == n - 1:
        merged = runs[-1] + runs[0]
        runs = [merged] + runs[1:-1]
    comps = []
    for run in runs:
        fs = set(run)
        w = frozenset(p for p in white if p[0] in fs)
        bl = frozenset(p for p in black if p[0] in fs)
        e = ep if (ep is not None and ep[0] in fs) else None
        comps.append((w, bl, e))
    return comps

# ---- W: whole board ----
from functools import lru_cache
def make_W(s, b):
    n, ranks, topo = b
    @lru_cache(maxsize=None)
    def W(white, black, ep, c):
        for q in gen_moves(s, b, white, black, ep, c):
            v = classify(s, b, q[0], q[1], q[2], c)
            if v[0] == 'open':
                if not W(q[0], q[1], q[2], 'black' if c=='white' else 'white'): return True
            elif v[0] == 'won':
                if v[1] == c: return True
            else:
                if v[1] == c: return True
        return False
    return W

# ---- sum model S + value test ----
# component: ('P', white, black, ep) | ('N', n) | ('T', tree)
# tree: (left_tuple, right_tuple)
def tree_neg(t):
    l, r = t
    return (tuple(tree_neg(x) for x in r), tuple(tree_neg(x) for x in l))

def make_sum_solver(s, b):
    n, ranks, topo = b
    # options of one component for color c -> list of (list of components)
    def comp_options(comp, c):
        if comp[0] == 'N':
            k = comp[1]
            if c == 'white' and k > 0: return [[('N', k - 1)]]
            if c == 'black' and k < 0: return [[('N', k + 1)]]
            return []
        if comp[0] == 'T':
            l, r = comp[1]
            kids = l if c == 'white' else r
            return [[('T', t)] for t in kids]
        # pawns
        _, white, black, ep = comp
        res = []
        for q in gen_moves(s, b, white, black, ep, c):
            v = classify(s, b, q[0], q[1], q[2], c)
            if v[0] == 'open':
                res.append([('P', w, bl, e) for (w, bl, e) in components(b, q[0], q[1], q[2])])
            elif v[0] == 'won':
                res.append([('N', BIG if v[1] == 'white' else -BIG)])
            else:
                res.append([('N', BIG if v[1] == 'white' else -BIG)])
        return res
    from functools import lru_cache
    def canon(cs):
        # sort components for memo; keep integer sum separate handled by caller? keep simple: sort repr
        return tuple(sorted(cs, key=repr))
    @lru_cache(maxsize=None)
    def win(cs, c):
        # cs: tuple of components
        any_move = False
        for i, comp in enumerate(cs):
            for opt in comp_options(comp, c):
                any_move = True
                ncs = cs[:i] + tuple(opt) + cs[i+1:]
                ncs = tuple(sorted(ncs, key=repr))
                if not win(ncs, 'black' if c == 'white' else 'white'):
                    return True
        return False
    return win

def of_position(b, white, black, ep):
    return tuple(sorted([('P', w, bl, e) for (w, bl, e) in components(b, white, black, ep)], key=repr))

def is_value(s, b, white, black, ep, v):
    # root must have no passed pawn
    if has_passed(s, b, white, black, ep, 'white') or has_passed(s, b, white, black, ep, 'black'):
        return None
    win = make_sum_solver(s, b)
    base = list(of_position(b, white, black, ep)) + [('T', tree_neg(v))]
    base = tuple(sorted(base, key=repr))
    return (win(base, 'white') == False) and (win(base, 'black') == False)

# ---- trees ----  zero = {|} = ((), ())
ZERO = ((), ())
def star(k):
    if k == 0: return ZERO
    def stars_list(k):
        if k == 0: return ()
        return stars_list(k - 1) + (star(k - 1),)
    sl = stars_list(k)
    return (sl, sl)
def dy(k):
    if k == 0: return ((ZERO,), ())          # {0|}
    return ((ZERO,), (dy(k - 1),))            # {0 | 1/2^k}
EIGHTH = dy(3)

def P(sq):
    f = ord(sq[0]) - ord('a'); r = int(sq[1:]); return (f, r)

def pos_of(wlist, blist):
    white = frozenset((P(x)[0], P(x)[1], True) for x in wlist)
    black = frozenset((P(x)[0], P(x)[1], False) for x in blist)
    return white, black, None

SETTINGS = []
for ep in ('aware', 'textbook', 'off'):
    for race in ('count', 'mover', 'opponent'):
        SETTINGS.append({'ep': ep, 'race': race})
DEFAULT = {'ep': 'aware', 'race': 'count'}

def run_claims():
    print("=== L4: star2 (Theorem thm:star2seven) ===")
    A = pos_of(['a4','b3','d2','d3'], ['a7','b7','c5'])
    B = pos_of(['b4','c2','d2'], ['a6','a7','c6','d5'])
    flat8 = (8, 8, FLAT)
    for name, pos in (('A', A), ('B', B)):
        v = is_value(DEFAULT, flat8, *pos, star(2))
        print(f"  {name} default value==*2: {v}")
        for r in ('count','mover','opponent'):
            vv = is_value({'ep':'off','race':r}, flat8, *pos, star(2))
            print(f"  {name} ep-off race={r} value==*2: {vv}")
        for ep in ('aware','textbook','off'):
            vv = is_value({'ep':ep,'race':'opponent'}, flat8, *pos, star(2))
            print(f"  {name} opponent ep={ep} value==*2: {vv}")

    print("=== L5: eighth (Theorem thm:eighth) ===")
    G = pos_of(['a2','b2','b3'], ['a5','a6','b6'])
    for s in SETTINGS:
        v = is_value(s, flat8, *G, EIGHTH)
        print(f"  ep={s['ep']:8s} race={s['race']:8s} value==1/8: {v}")

    print("=== L6: sumcounter (Proposition prop:sumcounter) ===")
    X = pos_of(['b2','d4','g3','h5'], ['a7','c7','f7','g4'])
    cyl8 = (8, 8, CYL)
    sx = {'ep':'off','race':'count'}
    W = make_W(sx, cyl8)
    print(f"  X single component: {len(components(cyl8, *X))==1}")
    print(f"  W(X) white to move wins: {W(*X, 'white')}")
    print(f"  W(X) black to move wins: {W(*X, 'black')}")
    win = make_sum_solver(sx, cyl8)
    base = of_position(cyl8, *X)
    print(f"  S(X) white to move wins: {win(base, 'white')}")
    print(f"  S(X) black to move wins: {win(base, 'black')}")

if __name__ == '__main__':
    run_claims()