"""K60: test D-games and toy-group generators (own code)."""
import random
from k60lib import WT, BT, Group, dsum, exact_over, group_alone, OVER, UNDER


def chainW(n):   # integer n >= 0: White has n moves
    return ([[i + 1] for i in range(n)] + [[]], [[] for _ in range(n + 1)])


def chainB(n):   # integer -n
    return ([[] for _ in range(n + 1)], [[i + 1] for i in range(n)] + [[]])


ZERO = ([[]], [[]])
STAR = ([[1], []], [[1], []])
UP = ([[1], [], [1]], [[2], [], [1]])          # 0: up = {0 | *}; 1: 0; 2: *
DOWN = ([[2], [], [1]], [[1], [], [1]])        # 0: down = {* | 0}
ON = ([[0]], [[]])
OFF = ([[]], [[0]])
DUD = ([[0]], [[0]])
STAR2 = ([[1, 2], [], [1]], [[1, 2], [], [1]])  # *2 = {0, * | 0, *}; 2 = *


def pm(n):  # {n | -n}: 0 root; 1..n+1 White chain (value n at 1); n+2..2n+2 Black chain (value -n at n+2)
    a = list(range(1, n + 2))
    b = list(range(n + 2, 2 * n + 3))
    L = [[] for _ in range(2 * n + 3)]
    R = [[] for _ in range(2 * n + 3)]
    L[0], R[0] = [a[0]], [b[0]]
    for i in range(n):
        L[a[i]].append(a[i + 1])
        R[b[i]].append(b[i + 1])
    return (L, R)


def tiny(x):  # {0 || 0 | -x}: positions 0 root, 1 = 0, 2 = {0 | -x}, then -x chain
    m = chainB(x)
    off = 3
    L = [[1], [], [1]] + [[] for _ in m[0]]
    R = [[2], [], [off]] + [[y + off for y in o] for o in m[1]]
    return (L, R)


def neg(T):
    L, R = T
    sw = {WT: BT, BT: WT}
    return ([[sw.get(y, y) for y in o] for o in R], [[sw.get(y, y) for y in o] for o in L])


NAMED = {
    "0": ZERO, "1": chainW(1), "2": chainW(2), "3": chainW(3), "-1": chainB(1), "-2": chainB(2), "-3": chainB(3),
    "*": STAR, "*2": STAR2, "up": UP, "down": DOWN, "on": ON, "off": OFF, "dud": DUD,
    "over": OVER, "under": UNDER, "pm1": pm(1), "pm2": pm(2),
    "tiny1": tiny(1), "tiny2": tiny(2), "miny1": neg(tiny(1)), "miny2": neg(tiny(2)),
    "hot": ([[WT]], [[BT]]),
    "Wthr": ([[1], [WT]], [[], []]), "Bthr": ([[], []], [[1], [BT]]),
    "Wthr_ans": ([[1], [WT], []], [[], [2], []]), "Bthr_ans": ([[], [2], []], [[1], [BT], []]),
    "onB": ([[0]], [[BT]]), "offW": ([[WT]], [[0]]),
    "Bslow": ([[], [], [], []], [[1], [2], [3], [BT]]), "Wslow": ([[1], [2], [3], [WT]], [[], [], [], []]),
    "Wspare_Bthr": ([[0, 1], [], []], [[2], [], [BT]]), "Bspare_Wthr": ([[2], [], [WT]], [[0, 1], [], []]),
    "hotW": ([[1], [WT]], [[BT], []]),  # White threatens to threaten; Black wins by moving first
}


def named_battery():
    out = list(NAMED.items())
    base = ["*", "up", "down", "-1", "1", "over", "under", "tiny1", "miny1", "pm1", "off", "on", "*2"]
    for i, a in enumerate(base):
        for b in base[i:]:
            out.append((a + "+" + b, dsum(NAMED[a], NAMED[b])))
    for a in ["down", "*", "under", "-1"]:
        out.append((a + "x3", dsum(dsum(NAMED[a], NAMED[a]), NAMED[a])))
    out.append(("down+down+*", dsum(dsum(DOWN, DOWN), STAR)))
    out.append(("under+over+over", dsum(dsum(UNDER, OVER), OVER)))
    return out


def rand_T(rng, kmax=5):
    k = rng.randint(1, kmax)
    p = rng.choice([0.15, 0.3, 0.45])
    pt = rng.choice([0.0, 0.1, 0.25])
    L, R = [], []
    for _ in range(k):
        for side in (L, R):
            o = [t for t in range(k) if rng.random() < p]
            if rng.random() < pt:
                o.append(WT)
            if rng.random() < pt:
                o.append(BT)
            side.append(o)
    return (L, R)


# ---------------- toy groups ----------------
def _rmoves(rng, n, p, pterm, pd):
    o = [(y, 1 if rng.random() < pd else 0) for y in range(2, n) if rng.random() < p]
    if rng.random() < p / 2:
        o.append((rng.randint(0, 1), 0))   # back to a root
    if rng.random() < pterm:
        o.append((WT, 0))
    if rng.random() < pterm:
        o.append((BT, 0))
    return o


def random_group(rng):
    n = rng.randint(5, 10)
    p = rng.choice([0.15, 0.25, 0.35])
    pterm = rng.choice([0.1, 0.25, 0.4])
    pd = rng.choice([0.0, 0.0, 0.25])
    pc = rng.choice([0.0, 0.0, 0.15, 0.3])
    pe = rng.choice([0.0, 0.0, 0.3])
    chk = [[(g >= 2 and rng.random() < pc) for s in (0, 1)] for g in range(n)]
    mv = [[_rmoves(rng, n, p, pterm, pd) for s in (0, 1)] for g in range(n)]
    ep = [[(_rmoves(rng, n, p / 2, pterm / 2, 0.0) if rng.random() < pe else []) for s in (0, 1)] for g in range(n)]
    G = Group(n, mv, ep, chk)
    for _ in range(5):
        pv = group_alone(G)
        zz = [(q, d) for q in range(2, n) for d in (0, 1) if not chk[q][0] and not chk[q][1]
              and pv[(q, d, 1, 0)] == "W" and pv[(q, 0, 1, 0)] == "W" and pv[(q, 0, 0, 0)] == "L"
              and G.moves(q, d, 1) and G.mv[q][1] and G.mv[q][0]]
        if not zz:
            return None
        wl = [(y, d) for y in range(2, n) for d in (0, 1) if not chk[y][0] and pv[(y, d, 1, 0)] == "L"]
        bl = [(y, d) for y in range(2, n) for d in (0, 1) if not chk[y][1] and pv[(y, d, 0, 0)] == "W"]
        for r, o in ((0, 1), (1, 0)):
            mv[r][0] = rng.sample(zz, rng.randint(1, min(2, len(zz)))) + rng.sample(wl, rng.randint(0, min(3, len(wl))))
            mv[r][1] = [(o, 0)] + rng.sample(bl, rng.randint(0, min(4, len(bl))))
            ep[r] = [[], []]
        G = Group(n, mv, ep, chk)
        if exact_over(G) is not None:
            return G
    return None


def tempo_group(rng):
    """Adversarial family aimed at (B1): each bad Black root move enters a small 'race' gadget where Black is saved by a
    token used at the right moment, with White counter-resources (own spare moves, mutual zugzwangs, checks)."""
    mv, ep, chk = [], [], []

    def new(c0=False, c1=False):
        mv.append([[], []])
        ep.append([[], []])
        chk.append([c0, c1])
        return len(mv) - 1
    A, B = new(), new()
    mv[A][1].append((B, 0))
    mv[B][1].append((A, 0))
    q = new()
    zb, zw = new(), new()
    mv[zb][0].append((WT, 0))
    mv[zb][1].append((zb, 0) if rng.random() < 0.5 else (BT, 0) if False else (zb, 0))
    mv[zw][1].append((BT, 0))
    mv[zw][0].append((zw, 0))
    mv[q][1].append((zb, 0))
    mv[q][0].append((zw, 0))
    mv[A][0].append((q, 0))
    mv[B][0].append((q, rng.randint(0, 1)))
    # random gadget region
    k = rng.randint(3, 8)
    base = len(mv)
    nodes = [new(rng.random() < 0.15, rng.random() < 0.15) for _ in range(k)]
    for g in nodes:
        for s in (0, 1):
            for _ in range(rng.randint(0, 3)):
                c = rng.random()
                if c < 0.12:
                    mv[g][s].append((WT if s == 0 else BT, 0))
                elif c < 0.17:
                    mv[g][s].append((BT if s == 0 else WT, 0))
                elif c < 0.22:
                    mv[g][s].append((rng.choice([A, B, q]), 0))
                else:
                    mv[g][s].append((rng.choice(nodes), 1 if rng.random() < 0.15 else 0))
            if rng.random() < 0.1:
                ep[g][s].append((rng.choice(nodes + [WT if s == 0 else BT]), 0))
    for r in (A, B):
        for _ in range(rng.randint(1, 3)):
            mv[r][1].append((rng.choice(nodes), 1 if rng.random() < 0.2 else 0))
        if rng.random() < 0.4:
            mv[r][0].append((rng.choice(nodes), 0))
    G = Group(len(mv), mv, ep, chk)
    return G if exact_over(G) is not None else None


def T_N(N):
    """The counter game T_N: positions u_0..u_N and 0 (index N+1).  White: u_i -> u_{i+1} (i < N), u_N -> WT.
    Black: u_i -> 0 for every i.  (A finite 'under' whose White passes run out into a White threat.)"""
    z = N + 1
    L = [[i + 1] for i in range(N)] + [[WT], []]
    R = [[z] for i in range(N + 1)] + [[]]
    return (L, R)


def k_down(k):
    T = DOWN
    for _ in range(k - 1):
        T = dsum(T, DOWN)
    return T


def example_nob1():
    """Hand example (PROOF.md section 5): exact, fails (B1), has the results of omega.
    Boards: 0 A, 1 B, 2 q, 3 qb, 4 qw, 5 x, 6 y, 7 z, 8 y2, 9 x2."""
    n = 10
    mv = [[[], []] for _ in range(n)]
    W_, B_ = 0, 1
    mv[0][W_] = [(2, 0)]; mv[1][W_] = [(2, 0)]
    mv[0][B_] = [(1, 0), (5, 0)]; mv[1][B_] = [(0, 0), (5, 0)]
    mv[2][W_] = [(4, 0)]; mv[2][B_] = [(3, 0)]
    mv[3][W_] = [(WT, 0)]
    mv[4][B_] = [(BT, 0)]
    mv[5][W_] = [(6, 0)]; mv[5][B_] = [(9, 0)]
    mv[6][W_] = [(8, 0)]; mv[6][B_] = [(7, 0)]
    mv[7][W_] = [(WT, 0)]
    mv[8][B_] = [(BT, 0)]
    mv[9][W_] = [(WT, 0)]
    ep = [[[], []] for _ in range(n)]
    chk = [[False, False] for _ in range(n)]
    return Group(n, mv, ep, chk)


def example_cw():
    """Hand example: exact, satisfies (B1) (so it has the results of omega by Lemma 4.15), but the White-to-move
    comparison (C_W) fails beside hotW.  Boards: 0 A, 1 B, 2 q, 3 qb, 4 qw, 5 x, 6 w, 7 w2."""
    n = 8
    mv = [[[], []] for _ in range(n)]
    mv[0][0] = [(2, 0)]; mv[1][0] = [(2, 0)]
    mv[0][1] = [(1, 0), (5, 0)]; mv[1][1] = [(0, 0)]
    mv[2][0] = [(4, 0)]; mv[2][1] = [(3, 0)]
    mv[3][0] = [(WT, 0)]
    mv[4][1] = [(BT, 0)]
    mv[5][0] = [(6, 0)]; mv[5][1] = [(BT, 0)]
    mv[6][0] = [(WT, 0)]; mv[6][1] = [(7, 0)]
    mv[7][0] = [(WT, 0)]
    ep = [[[], []] for _ in range(n)]
    chk = [[False, False] for _ in range(n)]
    return Group(n, mv, ep, chk)


def example_k58():
    """K58's abstract witness (K58/PROOF.md section 6(a)): r0, r1, q, x, p = 0..4."""
    n = 5
    mv = [[[], []] for _ in range(n)]
    mv[0][0] = [(2, 0)]; mv[1][0] = [(2, 0)]
    mv[0][1] = [(1, 0), (3, 0)]; mv[1][1] = [(0, 0), (3, 0)]
    mv[2][0] = [(3, 0)]; mv[2][1] = [(4, 0)]
    mv[3][0] = [(2, 0)]; mv[3][1] = [(BT, 0)]
    mv[4][0] = [(WT, 0)]; mv[4][1] = [(BT, 0)]
    ep = [[[], []] for _ in range(n)]
    chk = [[False, False] for _ in range(n)]
    return Group(n, mv, ep, chk)
