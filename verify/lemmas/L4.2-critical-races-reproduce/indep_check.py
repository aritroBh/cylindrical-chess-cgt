"""Independent re-check of claim L4.2-critical-races (verifier scratch).

Uses NO project code (no cylcgt, no lemmas): own pawn move generator, own
passer test, own count rule, and a CGT-free test of game equality:
    G = H  <=>  G + (-H) is a second-player win (P-position).
G is the whole-board convention game W of the 4-file flat 8-rank strip from
W: a2 c2 / B: b7 d7 (exactly one passer -> +-BIG, which dominates the small
comparison game; both passers -> race verdict). The small comparison games
0, *, *2, up, down are explicit trees. All play is alternating minimax on the
SUM of W and the small game, so the e.p. right stays in W's state while the
other summand is played (that is the CGT semantics of W).

ep_mode: "always" = a double step always leaves a right (as cylcgt.pawns does),
         "usable" = only if an enemy pawn stands next to the landing square,
         "off"    = no e.p.
"""
import sys, random, itertools
from functools import lru_cache
sys.setrecursionlimit(100000)

FILES, RANKS = 4, 8
FN = "abcdefgh"

def nm(s): return f"{FN[s[0]]}{s[1]}"
def show(st):
    w, b, ep = st
    s = f"W: {' '.join(sorted(map(nm, w)))} / B: {' '.join(sorted(map(nm, b)))}"
    return s + (f" (ep {nm(ep[0])})" if ep else "")

def parse(t):
    a, c = t.split("/")
    f = lambda part: frozenset((FN.index(x[0]), int(x[1:])) for x in part.split(":")[1].split())
    return (f(a), f(c), None)

def is_passer(st, side):
    w, b, _ = st
    mine, theirs = (w, b) if side == "W" else (b, w)
    for f, r in mine:
        ok = True
        for g, s in theirs:
            if abs(g - f) <= 1 and ((s > r) if side == "W" else (s < r)):
                ok = False; break
        if ok:
            return True
    return False

def dist(st, side):
    """moves to promote for the best passer that is the front pawn of its file."""
    w, b, _ = st
    mine, theirs = (w, b) if side == "W" else (b, w)
    occ = w | b
    best = 10**6
    for f, r in mine:
        if any(abs(g - f) <= 1 and ((s > r) if side == "W" else (s < r)) for g, s in theirs):
            continue
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, RANKS + 1)): continue
            d = (RANKS - r) - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)): continue
            d = (r - 1) - (1 if r == RANKS - 1 else 0)
        best = min(best, d)
    return best

def count_winner(st, mover):
    other = "B" if mover == "W" else "W"
    return other if dist(st, other) <= dist(st, mover) else mover

def term(st):
    a, c = is_passer(st, "W"), is_passer(st, "B")
    if a and c: return 0
    if a: return 1
    if c: return -1
    return None

def gen(st, side, ep_mode):
    w, b, ep = st
    mine, theirs = (w, b) if side == "W" else (b, w)
    occ = w | b
    d = 1 if side == "W" else -1
    home = 2 if side == "W" else RANKS - 1
    myep = ep if (ep and ep[2] == side) else None
    out = []
    def put(nm_, nt, e=None):
        st2 = (frozenset(nm_), frozenset(nt), e) if side == "W" else (frozenset(nt), frozenset(nm_), e)
        if st2 not in out: out.append(st2)
    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if not 1 <= r1 <= RANKS: continue
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == home and (f, r2) not in occ:
                e = None
                opp = "B" if side == "W" else "W"
                if ep_mode == "always" or (ep_mode == "usable" and any((f + k, r2) in theirs for k in (-1, 1))):
                    e = ((f, r1), (f, r2), opp)
                put(rest | {(f, r2)}, theirs, e)
        for k in (-1, 1):
            g = f + k
            if not 0 <= g < FILES: continue
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif myep and myep[0] == t:
                put(rest | {t}, theirs - {myep[1]})
    return out

# small comparison games: name -> (Left options, Right options)
SMALL = {"0": ([], []), "*": (["0"], ["0"]), "*2": (["0", "*"], ["0", "*"]),
         "up": (["0"], ["*"]), "down": (["*"], ["0"])}

def make_solver(ep_mode, override):
    @lru_cache(maxsize=None)
    def win(st, h, mover):
        other = "B" if mover == "W" else "W"
        for c in gen(st, mover, ep_mode):
            t = term(c)
            if t == 0:
                v = override.get((c, mover)) or count_winner(c, mover)
                if v == mover: return True
                continue
            if t is not None:
                if (t == 1) == (mover == "W"): return True
                continue
            if not win(c, h, other): return True
        for h2 in SMALL[h][0 if mover == "W" else 1]:
            if not win(st, h2, other): return True
        return False
    return win

def value_name(win, root):
    """Which of the small games equals W? (negatives: -*2=*2, -up=down)."""
    neg = {"0": "0", "*": "*", "*2": "*2", "up": "down", "down": "up"}
    hits = [g for g in SMALL if not win(root, neg[g], "W") and not win(root, neg[g], "B")]
    return hits[0] if hits else "other"

def race_nodes(root, ep_mode):
    seen, stack, races = {root}, [root], set()
    while stack:
        x = stack.pop()
        if term(x) is not None: continue
        for side in "WB":
            for c in gen(x, side, ep_mode):
                if term(c) == 0: races.add((c, side))
                if c not in seen:
                    seen.add(c); stack.append(c)
    return races, len(seen)

if __name__ == "__main__":
    root = parse("W: a2 c2 / B: b7 d7")
    flip = lambda w: "B" if w == "W" else "W"
    for ep_mode in ("always", "off", "usable"):
        races, nreach = race_nodes(root, ep_mode)
        base = value_name(make_solver(ep_mode, {}), root)
        crit = []
        for c, m in sorted(races, key=lambda k: (show(k[0]), k[1])):
            v = value_name(make_solver(ep_mode, {(c, m): flip(count_winner(c, m))}), root)
            if v != base:
                crit.append((show(c), m, count_winner(c, m), v))
        cset = {(c, m) for c, m in races if any(show(c) == s and m == mm for s, mm, _, _ in crit)}
        mixed = {(c, m): (m if (c, m) in cset else flip(m)) for c, m in races}
        v_mixed = value_name(make_solver(ep_mode, mixed), root)
        lost4 = {(c, m): flip(m) for c, m in cset}
        v_lost4 = value_name(make_solver(ep_mode, lost4), root)
        print(f"ep_mode={ep_mode}: reachable={nreach} race nodes={len(races)} base={base}")
        for t in crit: print("   critical", t)
        print("   critical won by mover, rest lost by mover:", v_mixed)
        print("   critical lost by mover, rest count:", v_lost4)
        for rule in ("mover", "opponent"):
            ov = {(c, m): (m if rule == "mover" else flip(m)) for c, m in races}
            print(f"   whole rule {rule}:", value_name(make_solver(ep_mode, ov), root))
        # random trials with a deterministic (sorted) order, several seeds
        order = sorted(races, key=lambda k: (show(k[0]), k[1]))
        for seed in (1, 2, 3):
            rng = random.Random(seed); hist = {}
            for _ in range(200):
                ov = {(c, m): (m if (c, m) in cset else rng.choice("WB")) for c, m in order}
                v = value_name(make_solver(ep_mode, ov), root)
                hist[v] = hist.get(v, 0) + 1
            print(f"   random rest, seed {seed} (sorted order):", sorted(hist.items()), flush=True)
