"""T78 exhaustive audit. Run from the project root with the project Python."""
from collections import Counter
from functools import cache
from itertools import product

LEFT, RIGHT, DRAW = 0, 1, 2
PLUS, MINUS = -1, -2
EVENT = (PLUS, MINUS)
LIMIT = 5                       # total unfolded option edges, across all K_i
OPTIONS = []


@cache
def node(left, right):
    OPTIONS.append((left, right))
    return len(OPTIONS) - 1


ZERO = node((), ())


def forms():
    """Generate option sets in increasing unfolded edge cost."""
    sizes = {ZERO: 0}
    for budget in range(1, LIMIT + 1):
        items = sorted((size + 1, side, target)
                       for target, size in [(PLUS, 0), (MINUS, 0), *sizes.items()]
                       for side in (LEFT, RIGHT))

        def choose(start, remaining, selection):
            if remaining == 0:
                l, r = (tuple(sorted(t for s, t in selection if s == side))
                        for side in (LEFT, RIGHT))
                g = node(l, r)
                assert g not in sizes
                sizes[g] = budget
                return
            for i in range(start, len(items)):
                cost, side, target = items[i]
                if cost > remaining:
                    break
                choose(i + 1, remaining - cost, selection + [(side, target)])

        choose(0, budget, [])
    return sizes


@cache
def integer(n):
    if n > 0:
        return node((integer(n - 1),), ())
    if n < 0:
        return node((), (integer(n + 1),))
    return ZERO


@cache
def translate(g, b):
    if g in EVENT:
        return integer(b if g == PLUS else -b)
    return node(*(tuple(sorted({translate(t, b) for t in opts})) for opts in OPTIONS[g]))


def pack(games):
    # Permuting coordinates and deleting an inert zero preserve all moves.
    return tuple(sorted(g for g in games if g != ZERO))


def moves(games, side, passes):
    if side in passes:
        yield games, 1 - side
    for i, g in enumerate(games):
        for t in OPTIONS[g][side]:
            if t in EVENT:
                yield t                           # ends the whole sum
            else:
                yield pack((*games[:i], t, *games[i + 1:])), 1 - side


class Graph:
    """Explicit turn graph. Unresolved states after win/loss propagation draw."""
    def __init__(self, passes):
        self.passes = passes
        self.result = {PLUS: LEFT, MINUS: RIGHT}

    def solve(self, games):
        start = [(pack(games), s) for s in (LEFT, RIGHT)]
        edges = {}
        stack = list(start)
        while stack:
            v = stack.pop()
            if v in self.result or v in edges:
                continue
            edges[v] = tuple(moves(*v, self.passes))
            stack.extend(edges[v])

        # ponytail: scan the small new subgraph per round; queue predecessors for larger games.
        while edges:
            finished = {}
            for v, children in edges.items():
                side = v[1]
                if any(self.result.get(w) == side for w in children):
                    finished[v] = side
                elif all(self.result.get(w) == 1 - side for w in children):
                    finished[v] = 1 - side        # includes the empty option set
            if not finished:
                self.result.update(dict.fromkeys(edges, DRAW))
                break
            self.result.update(finished)
            for v in finished:
                del edges[v]
        return tuple(self.result[v] for v in start)


PLAIN = Graph(())
RES = (Graph((LEFT,)), Graph((RIGHT,)))


@cache
def reach(g):
    return frozenset([g]).union(*(reach(t) for opts in OPTIONS[g] for t in opts if t >= 0))


@cache
def events(g):
    return frozenset(t for opts in OPTIONS[g] for t in opts if t in EVENT)


@cache
def threats(g):
    return frozenset().union(*(events(t) for t in reach(g)))


@cache
def tempo(g, side):
    return max((int(s == side) + (tempo(t, side) if t >= 0 else 0)
                for s, opts in enumerate(OPTIONS[g]) for t in opts), default=0)


@cache
def playable(games, side, passer):
    found = set()
    for child in moves(games, side, (passer,)):
        if child in EVENT:
            found.add(child)
        else:
            found.update(playable(*child, passer))
    return frozenset(found)


@cache
def clipped_reserve(g, side, b, passer=None):
    graph = PLAIN if passer is None else RES[passer]
    for c in range(b):
        token = integer(c if side == LEFT else -c)
        if graph.solve((g, token))[1 - side] == side:
            return c
    return b                 # every value >= b violates an allowance of b - 1


@cache
def maximum_reserve(g, side, b):
    return max(clipped_reserve(translate(t, b), side, b) for t in reach(g))


def criterion(games, passer, b):
    for j, g in enumerate(games):
        for sign in threats(g):
            side = EVENT.index(sign)
            rest = clipped_reserve(ZERO, side, b, passer)
            rest += sum(maximum_reserve(h, side, b) for i, h in enumerate(games) if i != j)
            if rest >= b:
                return False
    return True


@cache
def at_tuple(games, passer, b):
    graph = RES[passer]
    tr = tuple(translate(g, b) for g in games)
    agree = graph.solve(games) == graph.solve(tr)
    dominant = True
    for j, g in enumerate(games):
        for sign in events(g):
            frontier = (*tr[:j], translate(sign, b), *tr[j + 1:])
            side = EVENT.index(sign)
            if graph.solve(frontier) != (side, side):
                dominant = False
    return agree, dominant


def notation(g):
    if g == ZERO:
        return '0'
    if g in EVENT:
        return '⊕' if g == PLUS else '⊖'
    l, r = (','.join(map(notation, opts)) for opts in OPTIONS[g])
    return '{' + l + '|' + r + '}'


def main():
    sizes = forms()
    catalog = sorted(sizes, key=lambda g: (sizes[g], g))
    print('component forms by edge count', sorted(Counter(sizes.values()).items()))
    counts, rows, examples = Counter(), Counter(), {}
    assert Graph((LEFT, RIGHT)).solve(()) == (DRAW, DRAW)
    assert PLAIN.solve((integer(1), integer(-1))) == (RIGHT, LEFT)

    def audit(games, budget):
        k = len(games)
        m = tuple(sum(tempo(g, side) for g in games) for side in (LEFT, RIGHT))
        b = 1 + max(m)
        safe = all(not (PLUS in threats(g) and MINUS in threats(h))
                   for i, g in enumerate(games) for j, h in enumerate(games) if i != j)
        followers = list(product(*(reach(g) for g in games)))
        for p in (LEFT, RIGHT):
            bad = EVENT[1 - p]
            global_ok = all(bad not in threats(g) for g in games)
            root_ok = all(bad not in events(g) for g in games)
            play_ok = all(bad not in playable(pack(games), s, p) for s in (LEFT, RIGHT))
            assert (not global_ok or play_ok) and (not play_ok or root_ok)
            beneficiary_ok = all(bad not in OPTIONS[t][1 - p] for g in games for t in reach(g))
            flags = {'global': global_ok, 'root': safe and root_ok, 'play': safe and play_ok,
                     'beneficiary': safe and beneficiary_ok}
            counts[p, k, 'total'] += 1
            root_equal = at_tuple(games, p, b)[0]
            checks = [at_tuple(t, p, b) for t in followers]
            all_equal = all(a for a, d in checks)
            dominant = all(d for a, d in checks)
            cert = criterion(games, p, b)
            assert not cert or dominant
            assert not dominant or all_equal
            assert not all_equal or root_equal
            for reading, ok in flags.items():
                if ok:
                    counts[p, k, reading] += 1
                    for label, fails in [('accepted', True), ('criterion fails', not cert),
                                         ('dominance fails', not dominant),
                                         ('root mismatch', not root_equal),
                                         ('some tuple mismatch', not all_equal)]:
                        if fails:
                            rows[p, reading, label] += 1
                    if not root_equal or not all_equal:
                        kind = 'root' if not root_equal else 'descendant only'
                        key = (p, reading, kind)
                        order = (budget, k, games)
                        if key not in examples or order < examples[key][0]:
                            t = next(t for t, (a, _) in zip(followers, checks) if not a)
                            examples[key] = (order, t, b)
            if global_ok:
                assert safe and cert and dominant and all_equal
                counts[p, k, 'nonvacuous'] += any(threats(g) for g in games)
                for n in {1, 1 + m[1 - p]}:
                    for t in followers:
                        a, d = at_tuple(t, p, n)
                        assert a and d
                    c = criterion(games, p, n)
                    if n == 1 + m[1 - p]:
                        assert c
                    if n == 1 and not c:
                        rows[p, 'global', 'B=1 criterion fails'] += 1

    def visit(start, games, budget):
        if games:
            audit(games, budget)
        if len(games) == 3:
            return
        for i in range(start, len(catalog)):
            g = catalog[i]
            if budget + sizes[g] > LIMIT:
                break
            visit(i, (*games, g), budget + sizes[g])

    visit(0, (), 0)
    for p in (LEFT, RIGHT):
        print(('on', 'off')[p])
        for k in (1, 2, 3):
            print('k', k, *(counts[p, k, col] for col in
                            ('total', 'global', 'nonvacuous', 'root', 'play')))
        for reading in ('global', 'root', 'play', 'beneficiary'):
            print(reading, {label: count for (s, r, label), count in rows.items()
                            if s == p and r == reading})
        for (s, reading, kind), ((cost, k, games), t, b) in sorted(examples.items()):
            if s == p:
                def results(v):
                    return RES[p].solve(v), RES[p].solve(tuple(translate(g, b) for g in v))
                print(reading, kind, 'edges', cost, 'K', list(map(notation, games)),
                      'B', b, 'root', results(games), 'differing tuple', list(map(notation, t)), results(t))
    print('total reservoir/multiset pairs', sum(counts[p, k, 'total']
                                                for p in (LEFT, RIGHT) for k in (1, 2, 3)))
    print('global hypothesis pairs', sum(counts[p, k, 'global']
                                         for p in (LEFT, RIGHT) for k in (1, 2, 3)))
    for p in (LEFT, RIGHT):
        suicide = node((MINUS,), ()) if p == LEFT else node((), (PLUS,))
        favored = node((PLUS,), ()) if p == LEFT else node((), (MINUS,))
        assert not criterion((suicide,), p, 2)
        assert at_tuple((suicide,), p, 2) == (True, False)
        for n in range(1, LIMIT + 1):
            chain = integer(-n if p == LEFT else n)
            assert not criterion((favored, chain), p, n)
            assert criterion((favored, chain), p, n + 1)
            assert at_tuple((favored, chain), p, 1) == (True, True)
    print('suicide and sharp tempo witnesses passed')
    assert all(counts[LEFT, k, col] == counts[RIGHT, k, col]
               for k in (1, 2, 3) for col in ('total', 'global', 'nonvacuous', 'root', 'play'))


if __name__ == '__main__':
    main()
