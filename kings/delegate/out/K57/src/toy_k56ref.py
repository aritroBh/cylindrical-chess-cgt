"""K56 referee: abstract sanity test of Lemma 4.13 (K56) on toy groups.

A toy group G is a finite D-game (Definition 1.1) with no checks and no e.p. rights; terminals are its
"promotions". Positions 0 = A and 1 = B are the roots (Black's shuttle A <-> B), the q's are the targets of
White's non-losing root moves. Alone (the analogue of P), a side with no option and no pass is
stalemated: a DRAW. In a D-sum (Definition 1.3) a side with no option in any component loses; a terminal
ends the whole play; infinite play is a draw. A pass of X: the position stays, the move goes to Y.

Checks, for random G: Definition 4.8 (over orientation), tempo-exactness (K56 Definition 1), pass-robust
exactness; then r(G (+) T) against r(over_D (+) T) for random finite D-games T (loopy, with terminals),
every position t, both sides to move, both roots and every q (q against T alone).
usage: python3 toy.py SEED NGROUPS NTESTS
"""
import random
import sys

INF = -1
WT, BT = "W", "B"  # terminals: White has won, Black has won


def solve(nodes, side, opts, nomove_draw):
    """Least fixed point. opts[v]: list of targets (node index or WT/BT). Returns 'W'/'L'/'D' per node
    (from White's view). nomove_draw[v]: a node without options is a draw instead of a loss."""
    n = len(nodes)
    val = [None] * n
    changed = True
    while changed:
        changed = False
        for v in range(n):
            if val[v] is not None:
                continue
            s = side[v]
            o = opts[v]
            if not o:
                if nomove_draw[v]:
                    continue
                val[v] = "L" if s == 0 else "W"
                changed = True
                continue
            res = []
            for t in o:
                if t == WT:
                    res.append("W")
                elif t == BT:
                    res.append("L")
                else:
                    res.append(val[t])
            good = "W" if s == 0 else "L"
            bad = "L" if s == 0 else "W"
            if good in res:
                val[v] = good
                changed = True
            elif all(r == bad for r in res):
                val[v] = bad
                changed = True
    return [x if x is not None else "D" for x in val]


def pass_game(G, X, k):
    """Values of G alone with X passing at most k times (k = INF: at will). Returns dict (g, s, l) -> value."""
    L, R = G
    n = len(L)
    layers = [0] if k == 0 else ([0, 1] if k == 1 else [INF])
    idx = {}
    nodes = []
    for l in layers:
        for g in range(n):
            for s in (0, 1):
                idx[(g, s, l)] = len(nodes)
                nodes.append((g, s, l))
    side, opts, nmd = [], [], []
    for (g, s, l) in nodes:
        o = []
        for t in (L[g] if s == 0 else R[g]):
            o.append(t if t in (WT, BT) else idx[(t, 1 - s, l)])
        if s == X and l != 0:
            o.append(idx[(g, 1 - s, l if l == INF else l - 1)])
        side.append(s)
        opts.append(o)
        nmd.append(True)
    val = solve(nodes, side, opts, nmd)
    return {nodes[i]: val[i] for i in range(len(nodes))}


def ywins(val, X):
    return "W" if X == 1 else "L"  # Y's win, White's view


def exact_over(G):
    """Definition 4.8, over orientation, on the toy. Returns list of q's or None."""
    L, R = G
    p0 = pass_game(G, 1, 0)  # values of G alone
    # (O1) shuttle legal; every other Black root move loses at once
    if 1 not in R[0] or 0 not in R[1]:
        return None
    for r, other in ((0, 1), (1, 0)):
        for y in R[r]:
            if y == other:
                continue
            if y == BT:
                return None
            if y != WT and p0[(y, 0, 0)] != "W":
                return None
    qs = set()
    for r in (0, 1):
        fr = []
        for y in L[r]:
            if y == WT:
                return None  # a "promotion" freeze: not exact
            if y == BT:
                continue
            if p0[(y, 1, 0)] != "L":
                fr.append(y)
        if not fr:
            return None  # (O2)
        qs.update(fr)
    for q in qs:  # (O3), (O4): mutual zugzwang, each side has a move and every move loses at once
        if not L[q] or not R[q] or p0[(q, 1, 0)] != "W" or p0[(q, 0, 0)] != "L":
            return None
        if q in (0, 1):
            return None
    return sorted(qs)


def tempo_exact(G, qs, usedV=None):
    usedV = usedV if usedV is not None else [False]
    L, R = G
    pB1 = pass_game(G, 1, 1)
    pWi = pass_game(G, 0, INF)
    p0 = pass_game(G, 0, 0)
    for r, other in ((0, 1), (1, 0)):
        for y in R[r]:
            if y == other or y == WT:
                continue
            n1 = pB1[(y, 0, 1)] == "W"
            v1 = pB1[(y, 1, 1)] == "W"
            if not (n1 or v1):
                return False
            if v1 and not n1:
                usedV[0] = True
        for y in L[r]:
            if y in qs or y == BT:
                continue
            ni = pWi[(y, 1, INF)] == "L"
            v0 = p0[(y, 0, 0)] == "L"
            if not (ni or v0):
                return False
            if v0 and not ni:
                usedV[0] = True
    return True


def pass_robust(G, qs):
    L, R = G
    pBi = pass_game(G, 1, INF)
    pWi = pass_game(G, 0, INF)
    for r, other in ((0, 1), (1, 0)):
        for y in R[r]:
            if y != other and y != WT and pBi[(y, 0, INF)] != "W":
                return False
        for y in L[r]:
            if y not in qs and y != BT and pWi[(y, 1, INF)] != "L":
                return False
    for q in qs:
        for y in R[q]:
            if y != WT and (y == BT or pBi[(y, 0, INF)] != "W"):
                return False
        for y in L[q]:
            if y != BT and (y == WT or pWi[(y, 1, INF)] != "L"):
                return False
    return True


def sum_values(G, T):
    """r(G (+) T) for all (g, t, s): Definition 1.3, no move in either component loses."""
    LG, RG = G
    LT, RT = T
    nodes = [(g, t, s) for g in range(len(LG)) for t in range(len(LT)) for s in (0, 1)]
    idx = {x: i for i, x in enumerate(nodes)}
    side, opts, nmd = [], [], []
    for (g, t, s) in nodes:
        o = []
        for y in (LG[g] if s == 0 else RG[g]):
            o.append(y if y in (WT, BT) else idx[(y, t, 1 - s)])
        for y in (LT[t] if s == 0 else RT[t]):
            o.append(y if y in (WT, BT) else idx[(g, y, 1 - s)])
        side.append(s)
        opts.append(o)
        nmd.append(False)
    val = solve(nodes, side, opts, nmd)
    return {nodes[i]: val[i] for i in range(len(nodes))}


OVER = ([[1], []], [[0], []])  # omega = 0: L = {0_D}, R = {omega}; 0_D = 1
OVER = ([[1], []], [[0], []])


def rand_game(rng, n, p, pterm):
    L, R = [], []
    for _ in range(n):
        for side in (L, R):
            o = [t for t in range(n) if rng.random() < p]
            if rng.random() < pterm:
                o.append(WT)
            if rng.random() < pterm:
                o.append(BT)
            side.append(o)
    return (L, R)


def rand_group(rng):
    n = rng.randint(4, 8)
    L, R = rand_game(rng, n, rng.choice([0.15, 0.25, 0.35]), 0.25)
    # roots: shuttle and at least one White move to a candidate q
    R[0] = [x for x in R[0] if x != 1] + [1]
    R[1] = [x for x in R[1] if x != 0] + [0]
    for r in (0, 1):
        if not any(isinstance(x, int) and x >= 2 for x in L[r]):
            L[r].append(rng.randint(2, n - 1))
    return (L, R)


def rand_group_repaired(rng):
    """Random game, then the root and q options are re-chosen (a few rounds) so that Definition 4.8 tends to hold:
    White's root moves = some mutual zugzwangs of G alone (the q's) + some moves that lose at once; Black's root
    moves = the shuttle + some moves that lose at once; q's moves stay as generated."""
    n = rng.randint(5, 9)
    G = rand_game(rng, n, rng.choice([0.15, 0.25, 0.35]), 0.3)
    L, R = G
    for _ in range(4):
        p0 = pass_game(G, 1, 0)
        zz = [y for y in range(2, n) if p0[(y, 1, 0)] == "W" and p0[(y, 0, 0)] == "L" and L[y] and R[y]]
        if not zz:
            return None
        wl = [y for y in range(n) if p0[(y, 1, 0)] == "L"] + [BT]
        bl = [y for y in range(n) if p0[(y, 0, 0)] == "W"] + [WT]
        for r, other in ((0, 1), (1, 0)):
            L[r] = sorted(set(rng.sample(zz, rng.randint(1, min(2, len(zz)))) +
                              rng.sample(wl, rng.randint(0, min(3, len(wl))))), key=str)
            R[r] = sorted(set([other] + [y for y in rng.sample(bl, rng.randint(0, min(3, len(bl)))) if y != other]), key=str)
    return G


def main():
    seed, ngroups, ntests = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    tests = []
    for _ in range(ntests):
        tests.append(rand_game(rng, rng.randint(1, 4), rng.choice([0.2, 0.35, 0.5]), rng.choice([0.0, 0.15, 0.3])))
    over_vals = [sum_values(OVER, T) for T in tests]
    stats = dict(tempo_via_V=0, tempo_not_robust=0, tried=0, exact=0, tempo=0, robust=0, robust_not_tempo=0, tempo_diff=0, robust_diff=0,
                 exact_other=0, other_diff_groups=0, results_tempo=0, results_other=0)
    seen = set()
    while stats["tempo"] < ngroups and stats["tried"] < 400 * ngroups:
        stats["tried"] += 1
        G = rand_group_repaired(rng) if rng.random() < 0.9 else rand_group(rng)
        if G is None:
            continue
        key = repr(G)
        if key in seen:
            continue
        seen.add(key)
        qs = exact_over(G)
        if qs is None:
            continue
        stats["exact"] += 1
        uv = [False]
        te = tempo_exact(G, qs, uv)
        stats["tempo_via_V"] += te and uv[0]
        stats["tempo_not_robust"] += te and not pass_robust(G, qs)
        pr = pass_robust(G, qs)
        stats["tempo"] += te
        stats["robust"] += pr
        stats["robust_not_tempo"] += pr and not te
        if not te and not pr and stats["exact_other"] >= 2 * ngroups:
            continue
        diff = 0
        nres = 0
        for T, ov in zip(tests, over_vals):
            sv = sum_values(G, T)
            for t in range(len(T[0])):
                for s in (0, 1):
                    for g in (0, 1):
                        nres += 1
                        diff += sv[(g, t, s)] != ov[(0, t, s)]
                    for q in qs:
                        nres += 1
                        diff += sv[(q, t, s)] != ov[(1, t, s)]
        if te:
            stats["results_tempo"] += nres
            stats["tempo_diff"] += diff
            if diff:
                print("COUNTEREXAMPLE (tempo-exact):", G, qs)
        if pr:
            stats["robust_diff"] += diff
            if diff:
                print("COUNTEREXAMPLE (pass-robust):", G, qs)
        if not te and not pr:
            stats["exact_other"] += 1
            stats["results_other"] += nres
            stats["other_diff_groups"] += diff > 0
    print(stats)


if __name__ == "__main__":
    main()
