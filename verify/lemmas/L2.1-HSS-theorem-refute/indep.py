"""Independent re-implementation (adversarial verifier, claim L2.1-HSS-theorem).

Imports NOTHING from cylcgt/ or lemmas/. Stdlib only.

Models, written from the definitions in notes/lemmas.md section 0 and 2:
  * pawn moves M1-M4 (push, double step with e.p. right, capture, e.p.),
    flat board or cylinder, e.p. on/off;
  * passer / race / race rule (count, mover, opponent);
  * oW(X): alternating-play outcome of the whole-board convention game
    (first passer ends everything, race scored by rule, e.p. rights global);
  * oS(X): outcome of the sum-model game form F (live components, each with
    its own *local* e.p. right that survives moves elsewhere, plus one integer
    k = sum of frozen +-BIG scores). Left may play k -> k-1 when k >= 1, Right
    k -> k+1 when k <= -1. Outcome computed by plain minimax, no CGT;
  * tau(Z) threat sets, pairwise safety, HSS, condition (E).

BIG is a parameter so the move-count hypothesis BIG > max(M_W, M_B) can be
probed at its tightest value.
"""
from __future__ import annotations

import sys
from functools import lru_cache

sys.setrecursionlimit(100000)


class Board:
    __slots__ = ("n", "m", "wrap", "ep", "_adj")

    def __init__(self, n, m, wrap, ep):
        self.n, self.m, self.wrap, self.ep = n, m, wrap, ep
        adj = []
        for f in range(n):
            s = set()
            for d in (-1, 1):
                g = f + d
                if wrap:
                    g %= n
                if 0 <= g < n and g != f:
                    s.add(g)
            adj.append(frozenset(s))
        self._adj = tuple(adj)

    def adj(self, f):
        return self._adj[f]

    def key(self):
        return (self.n, self.m, self.wrap, self.ep)

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, o):
        return isinstance(o, Board) and self.key() == o.key()

    def __repr__(self):
        return f"{self.n}x{self.m} {'cyl' if self.wrap else 'flat'} ep={'on' if self.ep else 'off'}"


# A position is (W, B, e): W, B sorted tuples of (file, rank); e is None or
# (target_sq, captured_sq, side) with side in 'W','B'.

def mkpos(w, b, e=None):
    return (tuple(sorted(w)), tuple(sorted(b)), e)


FILES = "abcdefghijklmnop"


def parse(text):
    wp, bp = text.split("/")
    sq = lambda t: (FILES.index(t[0]), int(t[1:]))
    return mkpos([sq(t) for t in wp.split(":")[1].split()], [sq(t) for t in bp.split(":")[1].split()])


def show(pos):
    w, b, e = pos
    s = "W: " + " ".join(f"{FILES[f]}{r}" for f, r in w) + " / B: " + " ".join(f"{FILES[f]}{r}" for f, r in b)
    if e:
        s += f" (ep {FILES[e[0][0]]}{e[0][1]} for {e[2]})"
    return s


def gen_moves(bd: Board, pos, side):
    """All children after one move of `side`. The side may use an e.p. right
    only if the right names it. Children carry a right only after a double step."""
    w, b, e = pos
    mine, theirs = (w, b) if side == "W" else (b, w)
    mine_s, theirs_s = set(mine), set(theirs)
    occ = mine_s | theirs_s
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else bd.m - 1
    other = "B" if side == "W" else "W"
    out = set()

    def emit(nm, nt, ne=None):
        if side == "W":
            out.add(mkpos(nm, nt, ne))
        else:
            out.add(mkpos(nt, nm, ne))

    for (f, r) in mine:
        r1 = r + d
        if not (1 <= r1 <= bd.m):
            continue
        rest = mine_s - {(f, r)}
        if (f, r1) not in occ:
            emit(rest | {(f, r1)}, theirs_s)
            r2 = r + 2 * d
            if r == start and 1 <= r2 <= bd.m and (f, r2) not in occ:
                ne = ((f, r1), (f, r2), other) if bd.ep else None
                emit(rest | {(f, r2)}, theirs_s, ne)
        for g in bd.adj(f):
            t = (g, r1)
            if t in theirs_s:
                emit(rest | {t}, theirs_s - {t})
            elif e is not None and e[2] == side and e[0] == t:
                emit(rest | {t}, theirs_s - {e[1]})
    return out


def has_passer(bd: Board, pos, side):
    w, b, _ = pos
    mine, theirs = (w, b) if side == "W" else (b, w)
    for f, r in mine:
        files = bd.adj(f) | {f}
        if side == "W":
            if not any(g in files and s > r for g, s in theirs):
                return True
        else:
            if not any(g in files and s < r for g, s in theirs):
                return True
    return False


def status(bd, pos):
    return has_passer(bd, pos, "W"), has_passer(bd, pos, "B")


def prom_dist(bd: Board, pos, side):
    w, b, _ = pos
    mine, theirs = (w, b) if side == "W" else (b, w)
    allp = set(w) | set(b)
    best = 10 ** 6
    for f, r in mine:
        files = bd.adj(f) | {f}
        if side == "W":
            if any(g in files and s > r for g, s in theirs):
                continue
            if any((f, s) in allp for s in range(r + 1, bd.m + 1)):
                continue
            dd = bd.m - r - (1 if r == 2 else 0)
        else:
            if any(g in files and s < r for g, s in theirs):
                continue
            if any((f, s) in allp for s in range(1, r)):
                continue
            dd = r - 1 - (1 if r == bd.m - 1 else 0)
        best = min(best, dd)
    return best


def race_winner(bd, child, mover, rule):
    other = "B" if mover == "W" else "W"
    if rule == "mover":
        return mover
    if rule == "opponent":
        return other
    return other if prom_dist(bd, child, other) <= prom_dist(bd, child, mover) else mover


def components(bd: Board, pos):
    """Connected components of the occupied-file graph (generic BFS)."""
    w, b, e = pos
    occf = {f for f, _ in w} | {f for f, _ in b}
    comps = []
    seen = set()
    for f0 in sorted(occf):
        if f0 in seen:
            continue
        grp, stack = set(), [f0]
        seen.add(f0)
        while stack:
            f = stack.pop()
            grp.add(f)
            for g in bd.adj(f):
                if g in occf and g not in seen:
                    seen.add(g)
                    stack.append(g)
        ce = e if (e is not None and e[0][0] in grp) else None
        comps.append(mkpos([p for p in w if p[0] in grp], [p for p in b if p[0] in grp], ce))
    return comps


# ---------------------------------------------------------------------------
# W: whole-board alternating minimax
# ---------------------------------------------------------------------------

class RaceRoot(Exception):
    pass


def make_W(bd, rule):
    @lru_cache(maxsize=None)
    def win(pos, tm):  # winner with `tm` to move; pos has no passer
        other = "B" if tm == "W" else "W"
        for c in gen_moves(bd, pos, tm):
            wp, bp = status(bd, c)
            if wp and bp:
                r = race_winner(bd, c, tm, rule)
            elif wp:
                r = "W"
            elif bp:
                r = "B"
            else:
                r = win(c, other)
            if r == tm:
                return tm
        return other
    return win


def outcome_from(wfirst_wins_for_W, wsecond_wins_for_W):
    if wfirst_wins_for_W and wsecond_wins_for_W:
        return "L"
    if not wfirst_wins_for_W and not wsecond_wins_for_W:
        return "R"
    return "N" if wfirst_wins_for_W else "P"


def oW(bd, pos, rule, _cache={}):
    key = (bd, rule)
    if key not in _cache:
        _cache[key] = make_W(bd, rule)
    win = _cache[key]
    wp, bp = status(bd, pos)
    if wp or bp:
        raise RaceRoot(show(pos))
    return outcome_from(win(pos, "W") == "W", win(pos, "B") == "W")


# ---------------------------------------------------------------------------
# S: sum-model game form F, minimax on (live components, integer k)
# ---------------------------------------------------------------------------

def make_S(bd, rule, BIG):
    @lru_cache(maxsize=None)
    def comp_moves(z, side):
        """Options of one live component z for `side`, as (delta_k, new_comps tuple)."""
        res = []
        for c in gen_moves(bd, z, side):
            wp, bp = status(bd, c)
            if wp and bp:
                res.append((BIG if race_winner(bd, c, side, rule) == "W" else -BIG, ()))
            elif wp:
                res.append((BIG, ()))
            elif bp:
                res.append((-BIG, ()))
            else:
                parts = tuple(p for p in components(bd, c) if not dead(p))
                res.append((0, parts))
        return tuple(res)

    @lru_cache(maxsize=None)
    def dead(z):
        return not gen_moves(bd, z, "W") and not gen_moves(bd, z, "B")

    @lru_cache(maxsize=None)
    def win(comps, k, tm):
        """Winner of F(comps, k) with tm to move. comps is a sorted tuple."""
        other = "B" if tm == "W" else "W"
        # integer move first (speed only; the minimax is exhaustive)
        if tm == "W" and k >= 1:
            if win(comps, k - 1, other) == tm:
                return tm
        if tm == "B" and k <= -1:
            if win(comps, k + 1, other) == tm:
                return tm
        for i, z in enumerate(comps):
            rest = comps[:i] + comps[i + 1:]
            for dk, parts in comp_moves(z, tm):
                nc = tuple(sorted(rest + parts))
                if win(nc, k + dk, other) == tm:
                    return tm
        return other

    return win


def oS(bd, pos, rule, BIG=256, _cache={}):
    key = (bd, rule, BIG)
    if key not in _cache:
        _cache[key] = make_S(bd, rule, BIG)
    win = _cache[key]
    wp, bp = status(bd, pos)
    if wp or bp:
        raise RaceRoot(show(pos))
    comps = tuple(sorted(components(bd, pos)))
    return outcome_from(win(comps, 0, "W") == "W", win(comps, 0, "B") == "W")


def clear_caches():
    oW.__defaults__[0].clear()
    oS.__defaults__[1].clear()


# ---------------------------------------------------------------------------
# threats, HSS, condition (E)
# ---------------------------------------------------------------------------

def make_tau(bd):
    @lru_cache(maxsize=None)
    def tau(z):
        wp, bp = status(bd, z)
        if wp or bp:
            return frozenset(([1] if wp else []) + ([-1] if bp else []))
        out = set()
        for side in ("W", "B"):
            for c in gen_moves(bd, z, side):
                out |= tau(c)
        return frozenset(out)
    return tau


_tau_cache = {}


def tau_of(bd):
    if bd not in _tau_cache:
        _tau_cache[bd] = make_tau(bd)
    return _tau_cache[bd]


def reachable_nonterminal(bd, pos):
    """Whole-board positions reachable from pos by moves of either side in any
    order, through positions with no passer. Returns (nonterminal set, terminal set)."""
    seen = {pos}
    stack = [pos]
    nonterm, term = [], []
    while stack:
        y = stack.pop()
        wp, bp = status(bd, y)
        if wp or bp:
            term.append(y)
            continue
        nonterm.append(y)
        for side in ("W", "B"):
            for c in gen_moves(bd, y, side):
                if c not in seen:
                    seen.add(c)
                    stack.append(c)
    return nonterm, term


def pairwise_safe(bd, y):
    tau = tau_of(bd)
    ts = [tau(c) for c in components(bd, y)]
    for i, a in enumerate(ts):
        for j, bb in enumerate(ts):
            if i != j and 1 in a and -1 in bb:
                return False
    return True


def ep_usable(bd, y):
    w, b, e = y
    if e is None:
        return False
    side = e[2]
    mine = w if side == "W" else b
    d = 1 if side == "W" else -1
    t = e[0]
    for f, r in mine:
        if r + d == t[1] and t[0] in bd.adj(f):
            return True
    return False


def analyse(bd, pos):
    """Returns dict with HSS, E (over non-terminal), E_all (incl. terminal),
    split (some non-terminal reachable node has >=2 components),
    nontrivial (some non-terminal reachable node has >=2 components, one of
    which has a non-empty threat set while another component is not dead),
    bothsigns (tau(X) has both signs)."""
    tau = tau_of(bd)
    nonterm, term = reachable_nonterminal(bd, pos)
    hss, E, E_all, split, nontriv = True, True, True, False, False
    for y in nonterm:
        comps = components(bd, y)
        if len(comps) >= 2:
            split = True
            if not pairwise_safe(bd, y):
                hss = False
            if ep_usable(bd, y):
                E = False
                E_all = False
            ts = [tau(c) for c in comps]
            if any(ts) and sum(1 for c in comps if gen_moves(bd, c, "W") or gen_moves(bd, c, "B")) >= 2:
                nontriv = True
    for y in term:
        if len(components(bd, y)) >= 2 and ep_usable(bd, y):
            E_all = False
    t = tau(pos)
    return dict(HSS=hss, E=E, E_all=E_all, split=split, nontrivial=nontriv,
                bothsigns=(1 in t and -1 in t), nreach=len(nonterm))


def move_bound(bd, pos):
    w, b, _ = pos
    return sum(bd.m - r for _, r in w), sum(r - 1 for _, r in b)
