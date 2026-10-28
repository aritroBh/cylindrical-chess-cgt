"""K21: abstract D-games, sums with decisive events, retrograde analysis (Python implementation 1).

A component is a Comp(L, R, root): L[x], R[x] are lists of options; an option is a node index or PLUS (-1)
(the terminal "White has won") or MINUS (-2) ("Black has won").

Sum semantics (LOOPY.md Def 1.3): a move in one coordinate; a move to PLUS/MINUS ends the whole play;
a player with no option in any coordinate loses; infinite play is a draw.
Results are from White's (Left's) point of view: 'W', 'L', 'D'.  mover 0 = Left, 1 = Right.

The CGT translation (Def 1.4) replaces PLUS by the integer chain +B and MINUS by -B; the translated
components contain no terminals, and the sum is the plain loopy normal-play disjunctive sum.
"""
from __future__ import annotations

import random
from collections import deque

PLUS, MINUS = -1, -2


class Comp:
    __slots__ = ("L", "R", "root")

    def __init__(self, L, R, root=0):
        self.L = [list(x) for x in L]
        self.R = [list(x) for x in R]
        self.root = root

    @property
    def n(self):
        return len(self.L)

    def reach(self):
        """nodes reachable from the root without passing a terminal (any player's moves)"""
        seen = {self.root}
        st = [self.root]
        while st:
            x = st.pop()
            for o in self.L[x] + self.R[x]:
                if o >= 0 and o not in seen:
                    seen.add(o)
                    st.append(o)
        return sorted(seen)

    def events(self):
        """set of signs sigma in {+1,-1} with some reachable node having an option to the terminal"""
        ev = set()
        for x in self.reach():
            for o in self.L[x] + self.R[x]:
                if o == PLUS:
                    ev.add(1)
                elif o == MINUS:
                    ev.add(-1)
        return ev

    def is_stopper(self):
        """no infinite alternating play from the root (either player first): the graph on
        (node, mover) with edges (x,L)->(x^L,R), (x,R)->(x^R,L) is acyclic on the reachable part."""
        nodes = self.reach()
        color = {}

        def dfs(s):
            color[s] = 1
            x, m = s
            for o in (self.L[x] if m == 0 else self.R[x]):
                if o < 0:
                    continue
                t = (o, 1 - m)
                c = color.get(t, 0)
                if c == 1:
                    return False
                if c == 0 and not dfs(t):
                    return False
            color[s] = 2
            return True

        for x in nodes:
            for m in (0, 1):
                if color.get((x, m), 0) == 0 and not dfs((x, m)):
                    return False
        return True

    def is_short(self):
        nodes = self.reach()
        color = {}

        def dfs(x):
            color[x] = 1
            for o in self.L[x] + self.R[x]:
                if o < 0:
                    continue
                c = color.get(o, 0)
                if c == 1:
                    return False
                if c == 0 and not dfs(o):
                    return False
            color[x] = 2
            return True

        return all(color.get(x, 0) != 0 or dfs(x) for x in nodes)

    def terminal_free(self):
        return all(o >= 0 for x in self.reach() for o in self.L[x] + self.R[x])

    def prune(self):
        """renumber to the reachable part, root = 0"""
        nodes = self.reach()
        idx = {x: i for i, x in enumerate(nodes)}

        def f(o):
            return o if o < 0 else idx[o]

        return Comp([[f(o) for o in self.L[x]] for x in nodes], [[f(o) for o in self.R[x]] for x in nodes], idx[self.root])

    def key(self):
        c = self.prune()
        return (tuple(tuple(x) for x in c.L), tuple(tuple(x) for x in c.R))


def mk_on():
    return Comp([[0]], [[]])


def mk_off():
    return Comp([[]], [[0]])


def mk_dud():
    return Comp([[0]], [[0]])


def mk_over():  # over = {0 | over}
    return Comp([[1], []], [[0], []])


def mk_under():  # under = {under | 0}
    return Comp([[0], []], [[1], []])


def mk_int(c):
    """the integer c >= 0 as a chain of c Left moves; root = c"""
    return Comp([[] if i == 0 else [i - 1] for i in range(c + 1)], [[] for _ in range(c + 1)], c)


def mk_negint(c):
    return Comp([[] for _ in range(c + 1)], [[] if i == 0 else [i - 1] for i in range(c + 1)], c)


def translate(comp, B):
    """y -> y^B : PLUS -> integer +B, MINUS -> integer -B (as chains appended to the node list)."""
    n = comp.n
    useP = any(o == PLUS for x in range(n) for o in comp.L[x] + comp.R[x])
    useM = any(o == MINUS for x in range(n) for o in comp.L[x] + comp.R[x])
    L = [list(x) for x in comp.L]
    R = [list(x) for x in comp.R]
    pbase = mbase = None
    if useP:
        pbase = len(L)  # node pbase+i is the integer i
        for i in range(B + 1):
            L.append([] if i == 0 else [pbase + i - 1])
            R.append([])
    if useM:
        mbase = len(L)
        for i in range(B + 1):
            L.append([])
            R.append([] if i == 0 else [mbase + i - 1])

    def f(o):
        if o == PLUS:
            return pbase + B
        if o == MINUS:
            return mbase + B
        return o

    for x in range(n):
        L[x] = [f(o) for o in L[x]]
        R[x] = [f(o) for o in R[x]]
    return Comp(L, R, comp.root), pbase, mbase


class SumGraph:
    """explicit product graph reachable from the given root tuples (both movers)."""

    def __init__(self, comps, roots):
        self.comps = comps
        self.k = len(comps)
        self.idx = {}
        self.state = []
        self.children = []   # list of child indices (unique)
        self.term = []       # bitmask: 1 = option to PLUS, 2 = option to MINUS  (any option, any coordinate)
        self.nopt = []       # total number of options (to detect "no option")
        self.roots = roots
        for t in roots:
            for m in (0, 1):
                self._add(t, m)
        i = 0
        while i < len(self.state):
            self._expand(i)
            i += 1

    def _add(self, t, m):
        key = (t, m)
        j = self.idx.get(key)
        if j is None:
            j = len(self.state)
            self.idx[key] = j
            self.state.append(key)
            self.children.append(None)
            self.term.append(0)
            self.nopt.append(0)
        return j

    def _expand(self, i):
        t, m = self.state[i]
        ch = set()
        tm = 0
        no = 0
        for c, comp in enumerate(self.comps):
            opts = comp.L[t[c]] if m == 0 else comp.R[t[c]]
            for o in opts:
                no += 1
                if o == PLUS:
                    tm |= 1
                elif o == MINUS:
                    tm |= 2
                else:
                    t2 = t[:c] + (o,) + t[c + 1:]
                    ch.add(self._add(t2, 1 - m))
        self.children[i] = sorted(ch)
        self.term[i] = tm
        self.nopt[i] = no

    def win_set(self, sigma):
        """least fixed point: forced win in finitely many moves for player sigma (0 = Left, 1 = Right)."""
        N = len(self.state)
        mine = 1 if sigma == 0 else 2   # terminal bit that sigma wants
        theirs = 2 if sigma == 0 else 1
        parents = [[] for _ in range(N)]
        for i in range(N):
            for c in self.children[i]:
                parents[c].append(i)
        win = [False] * N
        rem = [len(self.children[i]) for i in range(N)]
        q = deque()
        for i in range(N):
            m = self.state[i][1]
            if m == sigma:
                if self.term[i] & mine:
                    win[i] = True
                    q.append(i)
            else:
                if self.nopt[i] == 0 or (not (self.term[i] & theirs) and rem[i] == 0):
                    win[i] = True
                    q.append(i)
        while q:
            c = q.popleft()
            for p in parents[c]:
                if win[p]:
                    continue
                if self.state[p][1] == sigma:
                    win[p] = True
                    q.append(p)
                else:
                    rem[p] -= 1
                    if rem[p] == 0 and not (self.term[p] & theirs):
                        win[p] = True
                        q.append(p)
        return win

    def results(self):
        wl = self.win_set(0)
        wr = self.win_set(1)
        out = []
        for i in range(len(self.state)):
            assert not (wl[i] and wr[i])
            out.append("W" if wl[i] else ("L" if wr[i] else "D"))
        return out

    def result_map(self):
        r = self.results()
        return {self.state[i]: r[i] for i in range(len(self.state))}


def solve(comps, roots):
    """dict (tuple, mover) -> 'W'/'D'/'L' for every state reachable from the roots (both movers)."""
    return SumGraph(comps, roots).result_map()


def product_nodes(comps):
    import itertools
    return list(itertools.product(*[c.reach() for c in comps]))


def d_results(comps):
    """D-result at every reachable tuple, both movers"""
    return solve(comps, product_nodes(comps))


def cgt_results(comps, B):
    """outcome of sum of y^B at every reachable tuple (translated positions), both movers"""
    tcomps = [translate(c, B)[0] for c in comps]
    return solve(tcomps, product_nodes(comps))


def dominance(comps, B):
    """first-event dominance for B (LOOPY Def 1.10) in the loopy CGT sense, over all reachable tuples.
    returns (holds, list of failing frontiers)."""
    tr = [translate(c, B) for c in comps]
    tcomps = [t[0] for t in tr]
    roots = []
    frontier = []  # (tuple, j, sigma, frontier tuple)
    prod = product_nodes(comps)
    reach = [c.reach() for c in comps]
    for t in prod:
        for j, c in enumerate(comps):
            for sgn, term in ((1, PLUS), (-1, MINUS)):
                has = any(o == term for o in c.L[t[j]] + c.R[t[j]])
                if has:
                    base = tr[j][1] if sgn == 1 else tr[j][2]
                    ft = t[:j] + (base + B,) + t[j + 1:]
                    # coordinates i != j stay at original nodes of translated comps
                    frontier.append((t, j, sgn, ft))
                    roots.append(ft)
    if not roots:
        return True, []
    res = solve(tcomps, sorted(set(roots)))
    bad = []
    for (t, j, sgn, ft) in frontier:
        want = "W" if sgn == 1 else "L"
        if res[(ft, 0)] != want or res[(ft, 1)] != want:
            bad.append((t, j, sgn))
    return (not bad), bad


def reserves(comp, B, Cmax):
    """(lam, rho): per reachable node y, lam[y] = least C in 0..Cmax with Left winning y^B + C moving second,
    rho[y] = least C with Right winning y^B - C moving second; None for 'more than Cmax' (read as infinity)."""
    tc, _, _ = translate(comp, B)
    nodes = comp.reach()
    chainL = mk_int(Cmax)
    chainR = mk_negint(Cmax)
    lam, rho = {}, {}
    rootsL = [(y, c) for y in nodes for c in range(Cmax + 1)]
    resL = solve([tc, chainL], rootsL)
    resR = solve([tc, chainR], rootsL)
    for y in nodes:
        lam[y] = next((c for c in range(Cmax + 1) if resL[((y, c), 1)] == "W"), None)
        rho[y] = next((c for c in range(Cmax + 1) if resR[((y, c), 0)] == "L"), None)
    return lam, rho


INF = 10 ** 6


def reserve_criterion(comps, B, Cmax=None):
    """Theorem B criterion: for every j and sign with an event in component j,
    sum_{i != j} max_{reachable y of comp i} res_sign(y) <= B - 1.  Returns (holds, detail)."""
    if Cmax is None:
        Cmax = 2 * B + 3
    mx = []
    for c in comps:
        lam, rho = reserves(c, B, Cmax)
        mx.append((max(INF if v is None else v for v in lam.values()), max(INF if v is None else v for v in rho.values())))
    ev = [c.events() for c in comps]
    ok = True
    for j in range(len(comps)):
        if 1 in ev[j]:
            if sum(mx[i][0] for i in range(len(comps)) if i != j) > B - 1:
                ok = False
        if -1 in ev[j]:
            if sum(mx[i][1] for i in range(len(comps)) if i != j) > B - 1:
                ok = False
    return ok, mx


# ----------------------------------------------------------------------------------------------
# random generators
# ----------------------------------------------------------------------------------------------

def rand_short(rng, nmax=4, pplus=(0.2, 0.0), pminus=(0.0, 0.2), nopt=2, terms=True):
    """DAG; node 0 is the root; options of node i go to nodes j > i.
    pplus = (prob of a PLUS option for Left, for Right), pminus likewise (per option slot)."""
    n = rng.randint(1, nmax)
    L = [[] for _ in range(n)]
    R = [[] for _ in range(n)]
    for i in range(n):
        for side, lst in ((0, L), (1, R)):
            for _ in range(rng.randint(0, nopt)):
                u = rng.random()
                if terms and u < pplus[side]:
                    lst[i].append(PLUS)
                elif terms and u < pplus[side] + pminus[side]:
                    lst[i].append(MINUS)
                elif i + 1 < n:
                    lst[i].append(rng.randint(i + 1, n - 1))
            lst[i] = sorted(set(lst[i]))
    return Comp(L, R, 0).prune()


def rand_loopy(rng, nmax=3, pplus=(0.0, 0.0), pminus=(0.0, 0.0), nopt=2, terms=False):
    n = rng.randint(1, nmax)
    L = [[] for _ in range(n)]
    R = [[] for _ in range(n)]
    for i in range(n):
        for side, lst in ((0, L), (1, R)):
            for _ in range(rng.randint(0, nopt)):
                u = rng.random()
                if terms and u < pplus[side]:
                    lst[i].append(PLUS)
                elif terms and u < pplus[side] + pminus[side]:
                    lst[i].append(MINUS)
                else:
                    lst[i].append(rng.randint(0, n - 1))
            lst[i] = sorted(set(lst[i]))
    return Comp(L, R, 0).prune()


NAMED = {"on": mk_on, "off": mk_off, "dud": mk_dud, "over": mk_over, "under": mk_under}


def comp_str(c):
    c = c.prune()
    def f(o):
        return "+" if o == PLUS else ("-" if o == MINUS else str(o))
    return "|".join("%d:{%s/%s}" % (x, ",".join(f(o) for o in c.L[x]), ",".join(f(o) for o in c.R[x])) for x in range(c.n))
