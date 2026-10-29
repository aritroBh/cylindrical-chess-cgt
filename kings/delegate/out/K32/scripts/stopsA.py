"""K32 implementation A (Python, own code; does not import K21's dsum.py).

Games: finite terminal-free loopy games, graph form: nodes 0..n-1, L[x], R[x] option lists, root 0.
Sum with a short game X (number game or integer chain) is solved by retrograde analysis on the product graph:
normal play, a player with no move loses, infinite play is a draw (cannot happen for stopper + short).

Stops (Siegel, CGT 2013, ch. VI, stoppers; KNOWN, definition quoted from memory, see FINDINGS.md):
   LS(G) = G           if G equals a number,   else  max over Left options  G^L of RS(G^L)   (max of {} = -inf)
   RS(G) = G           if G equals a number,   else  min over Right options G^R of LS(G^R)   (min of {} = +inf)
The test "G equals a number" is semantic.  For a short number x:  G >= x  iff Left wins G - x moving second
(proved in FINDINGS.md section 4, step S0), G <= x iff Right wins G - x moving second; G = x iff both.
A node is a number iff it equals some dyadic x on the grid {j / 2^K : |x| <= M} (K, M chosen from N; checked).
"""
import sys
from fractions import Fraction
from functools import lru_cache
from itertools import permutations

INF = float("inf")


# ---------------------------------------------------------------- game graphs
def parse(line):
    L, R = [], []
    for tok in line.split():
        l, r = tok.split("/")
        l, r = int(l, 16), int(r, 16)
        n = len(line.split())
        L.append([y for y in range(n) if l >> y & 1])
        R.append([y for y in range(n) if r >> y & 1])
    return L, R


def reach_from(L, R, v):
    seen = {v}
    st = [v]
    while st:
        x = st.pop()
        for o in L[x] + R[x]:
            if o not in seen:
                seen.add(o)
                st.append(o)
    return seen


def quotient(L, R, root):
    """bisimulation quotient of the part reachable from root; returns canonical key (tuple of (Lset,Rset)) with root 0."""
    nodes = sorted(reach_from(L, R, root))
    blk = {x: 0 for x in nodes}
    nb = 1
    while True:
        sig = {x: (blk[x], frozenset(blk[o] for o in L[x]), frozenset(blk[o] for o in R[x])) for x in nodes}
        ids = {}
        for x in nodes:
            ids.setdefault(sig[x], len(ids))
        newblk = {x: ids[sig[x]] for x in nodes}
        if len(ids) == nb:
            blk = newblk
            break
        blk, nb = newblk, len(ids)
    qL = [set() for _ in range(nb)]
    qR = [set() for _ in range(nb)]
    for x in nodes:
        for o in L[x]:
            qL[blk[x]].add(blk[o])
        for o in R[x]:
            qR[blk[x]].add(blk[o])
    r = blk[root]
    best = None
    others = [b for b in range(nb) if b != r]
    for p in permutations(range(nb - 1)):
        lab = {r: 0}
        for b, k in zip(others, p):
            lab[b] = k + 1
        code = [None] * nb
        for b in range(nb):
            code[lab[b]] = (tuple(sorted(lab[o] for o in qL[b])), tuple(sorted(lab[o] for o in qR[b])))
        code = tuple(code)
        if best is None or code < best:
            best = code
    return best


def key_to_graph(key):
    return [list(c[0]) for c in key], [list(c[1]) for c in key]


def subkey(key, v):
    L, R = key_to_graph(key)
    return quotient(L, R, v)


def is_stopper(L, R):
    n = len(L)
    col = {}

    def dfs(s):
        col[s] = 1
        x, m = s
        for o in (L[x] if m == 0 else R[x]):
            t = (o, 1 - m)
            c = col.get(t, 0)
            if c == 1:
                return False
            if c == 0 and not dfs(t):
                return False
        col[s] = 2
        return True

    return all(col.get((x, m), 0) != 0 or dfs((x, m)) for x in range(n) for m in (0, 1))


# ---------------------------------------------------------------- short number games
@lru_cache(maxsize=None)
def numgame(val):
    """short game of the dyadic Fraction val, returned as (L, R) lists, root = last node"""
    nodes = {}
    L, R = [], []

    def build(v):
        if v in nodes:
            return nodes[v]
        if v.denominator == 1:
            n = int(v)
            if n == 0:
                lo, ro = [], []
            elif n > 0:
                lo, ro = [build(Fraction(n - 1))], []
            else:
                lo, ro = [], [build(Fraction(n + 1))]
        else:
            lo, ro = [build(v - Fraction(1, v.denominator))], [build(v + Fraction(1, v.denominator))]
        nodes[v] = len(L)
        L.append(lo)
        R.append(ro)
        return nodes[v]

    r = build(val)
    return tuple(map(tuple, L)), tuple(map(tuple, R)), r


def chain(c):
    """integer c (positive: Left tokens, negative: Right tokens), node i = integer sign*i"""
    n = abs(c)
    if c >= 0:
        return [[i - 1] if i else [] for i in range(n + 1)], [[] for _ in range(n + 1)], n
    return [[] for _ in range(n + 1)], [[i - 1] if i else [] for i in range(n + 1)], n


# ---------------------------------------------------------------- sum solver
def solve_sum(GL, GR, XL, XR):
    """Left-win sets of the sum of the games (g, x); returns (winL, winR): dicts (g,x,mover)->bool.
    mover 0 = Left to move, 1 = Right.  Asserts that there is no draw."""
    n, m = len(GL), len(XL)
    states = [(g, x, mv) for g in range(n) for x in range(m) for mv in (0, 1)]

    def opts(s):
        g, x, mv = s
        if mv == 0:
            return [(o, x, 1) for o in GL[g]] + [(g, o, 1) for o in XL[x]]
        return [(o, x, 0) for o in GR[g]] + [(g, o, 0) for o in XR[x]]

    ch = {s: opts(s) for s in states}
    par = {s: [] for s in states}
    for s in states:
        for t in ch[s]:
            par[t].append(s)

    def lfp(sigma):  # least fixed point for the player sigma (0 Left, 1 Right): forced win
        win = set()
        cnt = {s: len(ch[s]) for s in states}
        q = []
        for s in states:
            if s[2] != sigma and cnt[s] == 0:
                win.add(s)
                q.append(s)
        while q:
            t = q.pop()
            for s in par[t]:
                if s in win:
                    continue
                if s[2] == sigma:
                    win.add(s)
                    q.append(s)
                else:
                    cnt[s] -= 1
                    if cnt[s] == 0:
                        win.add(s)
                        q.append(s)
        return win

    wl, wr = lfp(0), lfp(1)
    assert not (wl & wr)
    assert len(wl) + len(wr) == len(states), "draw in stopper + short sum"
    return wl, wr


# ---------------------------------------------------------------- stops
class Stops:
    def __init__(self, K, M):
        self.K, self.M = K, M
        self.grid = [Fraction(j, 2 ** K) for j in range(-M * 2 ** K, M * 2 ** K + 1)]
        self.num_cache = {}
        self.ls_cache = {}
        self.rs_cache = {}

    def left_wins_second(self, key, y):  # G >= y
        GL, GR = key_to_graph(key)
        XL, XR, xr = numgame(-y)
        wl, _ = solve_sum(GL, GR, XL, XR)
        return (0, xr, 1) in wl

    def right_wins_second(self, key, y):  # G <= y
        GL, GR = key_to_graph(key)
        XL, XR, xr = numgame(-y)
        _, wr = solve_sum(GL, GR, XL, XR)
        return (0, xr, 0) in wr

    def number_value(self, key):
        """the dyadic x on the grid with G = x, or None"""
        if key in self.num_cache:
            return self.num_cache[key]
        lo, hi = 0, len(self.grid) - 1
        res = None
        if self.left_wins_second(key, self.grid[0]):
            # largest j with G >= grid[j] (monotone)
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if self.left_wins_second(key, self.grid[mid]):
                    lo = mid
                else:
                    hi = mid - 1
            if self.right_wins_second(key, self.grid[lo]):
                res = self.grid[lo]
        self.num_cache[key] = res
        return res

    def LS(self, key):
        if key in self.ls_cache:
            return self.ls_cache[key]
        x = self.number_value(key)
        if x is not None:
            v = x
        else:
            L, R = key_to_graph(key)
            v = max([self.RS(subkey(key, o)) for o in L[0]], default=-INF)
        self.ls_cache[key] = v
        return v

    def RS(self, key):
        if key in self.rs_cache:
            return self.rs_cache[key]
        x = self.number_value(key)
        if x is not None:
            v = x
        else:
            L, R = key_to_graph(key)
            v = min([self.LS(subkey(key, o)) for o in R[0]], default=INF)
        self.rs_cache[key] = v
        return v


def reserves(key, cmax):
    """(lam, rho) of the root: least C >= 0 with Left winning G + C moving second (Right moves first), resp. Right winning
    G - C moving second; INF if none up to cmax"""
    GL, GR = key_to_graph(key)
    XL, XR, _ = chain(cmax)
    wl, _ = solve_sum(GL, GR, XL, XR)
    lam = next((c for c in range(cmax + 1) if (0, c, 1) in wl), INF)
    XL, XR, _ = chain(-cmax)
    _, wr = solve_sum(GL, GR, XL, XR)
    rho = next((c for c in range(cmax + 1) if (0, c, 0) in wr), INF)
    return lam, rho


def fmt(v):
    if v == INF:
        return "inf"
    if v == -INF:
        return "-inf"
    return str(v)


def main():
    N = int(sys.argv[1])
    infile = sys.argv[2]
    K, M = max(N - 1, 1), N + 1
    st = Stops(K, M)
    cmax = 2 * N + 3
    memo = {}
    out = sys.stdout
    for line in open(infile):
        line = line.strip()
        if not line:
            continue
        L, R = parse(line)
        key = quotient(L, R, 0)
        r = memo.get(key)
        if r is None:
            assert is_stopper(*key_to_graph(key))
            r = (st.LS(key), st.RS(key)) + reserves(key, cmax)
            memo[key] = r
        out.write("%s %s %s %s %s\n" % (line.replace(" ", "_"), fmt(r[0]), fmt(r[1]), fmt(r[2]), fmt(r[3])))
    sys.stderr.write("distinct quotient games: %d\n" % len(memo))


if __name__ == "__main__":
    main()
