"""Independent second computation of o(S(X)) and o(W(X)) for pawn positions on a cylinder,
e.p. OFF, race rule 'count'. Written from the paper's rules; does not import cylcgt.
Pawns are (file, rank) with file 0..7 (a..h), rank 1..8. White moves up, Black down."""
import sys, time, threading
sys.setrecursionlimit(1000000)
NF, NR, BIG = 8, 8, 256

def passed_side(white, black, side):
    mine, theirs = (white, black) if side == 0 else (black, white)
    out = []
    for (f, r) in mine:
        ok = True
        for (g, s) in theirs:
            if (g - f) % NF in (0, 1, NF - 1) and ((s > r) if side == 0 else (s < r)):
                ok = False; break
        if ok: out.append((f, r))
    return out

def dist(p, side):
    f, r = p
    if side == 0: return NR - r - (1 if r == 2 else 0)
    return r - 1 - (1 if r == NR - 1 else 0)

def verdict(white, black, mover):
    """None if no passed pawn; else +1 (White wins) / -1 (Black wins). mover 0=W,1=B."""
    wp, bp = passed_side(white, black, 0), passed_side(white, black, 1)
    if not wp and not bp: return None
    if wp and not bp: return 1
    if bp and not wp: return -1
    dw = min(dist(p, 0) for p in wp); db = min(dist(p, 1) for p in bp)
    # opponent of the mover moves first in the race; tie goes to the side that did not move
    if mover == 0: return -1 if db <= dw else 1
    return 1 if dw <= db else -1

def moves(white, black, side):
    """all positions (white, black) after one move of side; no e.p."""
    mine, theirs = (white, black) if side == 0 else (black, white)
    occ = set(white) | set(black)
    d = 1 if side == 0 else -1
    start = 2 if side == 0 else NR - 1
    res = set()
    for p in mine:
        f, r = p
        r1 = r + d
        if not (1 <= r1 <= NR): continue
        rest = [q for q in mine if q != p]
        if (f, r1) not in occ:
            res.add((tuple(sorted(rest + [(f, r1)])), theirs))
            if r == start and (f, r + 2 * d) not in occ:
                res.add((tuple(sorted(rest + [(f, r + 2 * d)])), theirs))
        for df in (-1, 1):
            t = ((f + df) % NF, r1)
            if t in theirs:
                res.add((tuple(sorted(rest + [t])), tuple(q for q in theirs if q != t)))
    out = []
    for m, t in res:
        out.append((m, t) if side == 0 else (t, m))
    return out

def split(white, black):
    """components (list of (white,black) tuples), split along empty files; ring if none empty."""
    occ = {f for f, _ in white} | {f for f, _ in black}
    if not occ: return []
    if len(occ) == NF: return [(white, black)]
    # start after an empty file
    e = next(f for f in range(NF) if f not in occ)
    groups, cur = [], []
    for k in range(1, NF + 1):
        f = (e + k) % NF
        if f in occ: cur.append(f)
        elif cur: groups.append(set(cur)); cur = []
    if cur: groups.append(set(cur))
    return [(tuple(p for p in white if p[0] in g), tuple(p for p in black if p[0] in g)) for g in groups]

def after_move(white, black, mover):
    """sum-model image of a position just produced by 'mover' inside one component:
    returns ('int', +-BIG) or ('comps', [components])"""
    v = verdict(white, black, mover)
    if v is not None: return ('int', v * BIG)
    return ('comps', split(white, black))

# ---------------- sum model S ----------------
sys.setrecursionlimit(1000000)
memo = {}
stats = {'nodes': 0, 'splits': 0, 'maxcomps': 0}

def win(state, t, player):
    """True iff 'player' (0=Left/White,1=Right/Black) to move wins. state=sorted tuple of components."""
    key = (state, t, player)
    r = memo.get(key)
    if r is not None: return r
    stats['nodes'] += 1
    res = False
    if player == 0:
        if t > 0 and not win(state, t - 1, 1): res = True
        if not res:
            for i, (w, b) in enumerate(state):
                if i and state[i] == state[i - 1]: continue
                for (w2, b2) in moves(w, b, 0):
                    if apply_child(state, i, w2, b2, 0, t, 1): res = True; break
                if res: break
    else:
        if t < 0 and not win(state, t + 1, 0): res = True
        if not res:
            for i, (w, b) in enumerate(state):
                if i and state[i] == state[i - 1]: continue
                for (w2, b2) in moves(w, b, 1):
                    if apply_child(state, i, w2, b2, 1, t, 0): res = True; break
                if res: break
    memo[key] = res
    return res

def apply_child(state, i, w2, b2, mover, t, nxt):
    """True iff the mover's move leads to a position lost for the next player."""
    kind, val = after_move(w2, b2, mover)
    rest = state[:i] + state[i + 1:]
    if kind == 'int':
        ns, nt = rest, t + val
    else:
        if len(val) > 1: stats['splits'] += 1
        ns, nt = tuple(sorted(rest + tuple(val))), t
    stats['maxcomps'] = max(stats['maxcomps'], len(ns))
    return not win(ns, nt, nxt)

def S_outcome(white, black):
    white, black = tuple(sorted(white)), tuple(sorted(black))
    assert verdict(white, black, 0) is None
    st = tuple(sorted(split(white, black)))
    L = win(st, 0, 0); R = win(st, 0, 1)
    return {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(L, R)]

# ---------------- whole-board game W ----------------
wmemo = {}
wstats = {'nodes': 0}
def Wwin(white, black, player):
    key = (white, black, player)
    r = wmemo.get(key)
    if r is not None: return r
    wstats['nodes'] += 1
    res = False
    for (w2, b2) in moves(white, black, player):
        v = verdict(w2, b2, player)
        if v is not None:
            if (v == 1) == (player == 0): res = True; break
        elif not Wwin(w2, b2, 1 - player): res = True; break
    wmemo[key] = res
    return res

def W_outcome(white, black):
    white, black = tuple(sorted(white)), tuple(sorted(black))
    L, R = Wwin(white, black, 0), Wwin(white, black, 1)
    return {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(L, R)]

def parse(txt):
    w, b = txt.split('/')
    sq = lambda s: ('abcdefgh'.index(s[0]), int(s[1:]))
    return tuple(sorted(sq(s) for s in w.split())), tuple(sorted(sq(s) for s in b.split()))

def run_main():
    X = parse("b2 d4 g3 h5 / a7 c7 f7 g4")
    t0 = time.time()
    st = tuple(sorted(split(*X)))
    print("root components:", len(st), [(len(w), len(b)) for w, b in st])
    L = win(st, 0, 0); R = win(st, 0, 1)
    print("S(X): White-to-move wins:", L, " Black-to-move wins:", R)
    print("S(X) outcome:", {(True,True):'N',(True,False):'L',(False,True):'R',(False,False):'P'}[(L,R)])
    print("S nodes", stats, "memo", len(memo), "time %.1fs" % (time.time() - t0))
    t0 = time.time()
    print("W(X) outcome:", W_outcome(*X), "W nodes", wstats, "time %.1fs" % (time.time() - t0))

if __name__ == '__main__':
    threading.stack_size(512 * 1024 * 1024)
    th = threading.Thread(target=run_main); th.start(); th.join()
