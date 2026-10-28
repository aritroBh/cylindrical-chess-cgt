#!/usr/bin/env python3
"""Small exact fixed-point checks for K33; stdlib only."""

from itertools import product
import json
import random

WHITE, BLACK, DRAW = "+", "-", "D"


def gen_game(rng, n, terminals=True, restricted=False):
    """Each node/side/target edge is independently included with stated rates."""
    out = []
    for _ in range(n):
        sides = []
        for side in (0, 1):  # 0 = Left, 1 = Right
            options = [j for j in range(n) if rng.random() < 0.22]
            if terminals:
                allowed = (BLACK,) if restricted and side == 0 else (
                    (WHITE,) if restricted else (WHITE, BLACK)
                )
                options.extend(t for t in allowed if rng.random() < 0.14)
            sides.append(tuple(options))
        out.append(tuple(sides))
    return tuple(out)


def zero_game():
    return (((), ()),)


def reachable(g, root=0):
    seen, todo = set(), [root]
    while todo:
        x = todo.pop()
        if x in seen:
            continue
        seen.add(x)
        for side in (0, 1):
            todo.extend(o for o in g[x][side] if o not in (WHITE, BLACK))
    return tuple(sorted(seen))


def _attractors(states, edges, turn_of):
    """Least fixed points of finite White/Black wins; leftovers are draws."""
    ww, bw = set(), set()
    changed = True
    while changed:
        changed = False
        for s in states:
            opts = edges[s]
            turn = turn_of(s)
            if s not in ww:
                if turn == 0:
                    win = any(o == WHITE or (o not in (WHITE, BLACK) and o in ww) for o in opts)
                else:
                    win = not opts or all(
                        o == WHITE or (o not in (WHITE, BLACK) and o in ww) for o in opts
                    )
                if win:
                    ww.add(s)
                    changed = True
            if s not in bw:
                if turn == 1:
                    win = any(o == BLACK or (o not in (WHITE, BLACK) and o in bw) for o in opts)
                else:
                    win = not opts or all(
                        o == BLACK or (o not in (WHITE, BLACK) and o in bw) for o in opts
                    )
                if win:
                    bw.add(s)
                    changed = True
    return ww, bw


def d_sum_result(games, starts=None):
    """D-sum result, with an event ending the entire sum."""
    if starts is None:
        starts = tuple((nodes, turn) for nodes in product(*(range(len(g)) for g in games)) for turn in (0, 1))
    states = tuple(starts)
    edges = {}
    for nodes, turn in states:
        opts = []
        for i, g in enumerate(games):
            for o in g[nodes[i]][turn]:
                if o in (WHITE, BLACK):
                    opts.append(o)
                else:
                    nxt = list(nodes)
                    nxt[i] = o
                    opts.append((tuple(nxt), 1 - turn))
        edges[(nodes, turn)] = tuple(opts)
    ww, bw = _attractors(states, edges, lambda s: s[1])
    return ww, bw


def normal_result(games, start_nodes, integer, turn, B):
    """Outcome of the ordinary sum of translated games and one signed integer."""
    start = (tuple(start_nodes), integer, turn)
    states, seen, todo = [], set(), [start]
    edges = {}
    while todo:
        s = todo.pop()
        if s in seen:
            continue
        seen.add(s)
        states.append(s)
        nodes, value, mover = s
        opts = []
        for i, node in enumerate(nodes):
            if node is None:
                continue
            for o in games[i][node][mover]:
                ns = list(nodes)
                nv = value
                if o == WHITE:
                    ns[i] = None
                    nv += B
                elif o == BLACK:
                    ns[i] = None
                    nv -= B
                else:
                    ns[i] = o
                opts.append((tuple(ns), nv, 1 - mover))
        if mover == 0 and value > 0:
            opts.append((nodes, value - 1, 1))
        if mover == 1 and value < 0:
            opts.append((nodes, value + 1, 0))
        edges[s] = tuple(opts)
        todo.extend(opts)
    ww, bw = _attractors(states, edges, lambda s: s[2])
    if start in ww:
        return WHITE
    if start in bw:
        return BLACK
    return DRAW


def event_signs(g, node):
    return {o for side in (0, 1) for o in g[node][side] if o in (WHITE, BLACK)}


def first_event_dominant(games, B):
    reaches = [reachable(g) for g in games]
    frontier_checks = 0
    for nodes in product(*reaches):
        for i, node in enumerate(nodes):
            for sign in sorted(event_signs(games[i], node)):
                rest = tuple(None if j == i else n for j, n in enumerate(nodes))
                amount = B if sign == WHITE else -B
                for turn in (0, 1):
                    frontier_checks += 1
                    if normal_result(games, rest, amount, turn, B) != sign:
                        return False, frontier_checks
    return True, frontier_checks


def bridge_matches(games, B):
    reaches = [reachable(g) for g in games]
    states = tuple((nodes, turn) for nodes in product(*reaches) for turn in (0, 1))
    ww, bw = d_sum_result(games, states)
    checked = 0
    for nodes, turn in states:
        dvalue = WHITE if (nodes, turn) in ww else BLACK if (nodes, turn) in bw else DRAW
        cvalue = normal_result(games, nodes, 0, turn, B)
        checked += 1
        if dvalue != cvalue:
            return False, checked
    return True, checked


def reserve(g, node, B, side):
    """Return exact reserve through B-1, or B as a >B-1 sentinel."""
    # ponytail: cap at the criterion's B-1 ceiling; compute larger reserves only if those values matter.
    for c in range(B):
        if side == WHITE:
            got = normal_result((g,), (node,), c, 1, B) == WHITE
        else:
            got = normal_result((g,), (node,), -c, 0, B) == BLACK
        if got:
            return c
    return B


def reserve_condition(games, B):
    reaches = [reachable(g) for g in games]
    reserves = {
        (i, node, sign): reserve(games[i], node, B, sign)
        for i, nodes in enumerate(reaches)
        for node in nodes
        for sign in (WHITE, BLACK)
    }
    for j, nodes in enumerate(reaches):
        signs = set().union(*(event_signs(games[j], node) for node in nodes))
        for sign in signs:
            side = WHITE if sign == WHITE else BLACK
            total = sum(
                max(reserves[(i, node, side)] for node in reaches[i])
                for i in range(len(games)) if i != j
            )
            if total > B - 1:
                return False
    return True


def signal_case(rng, k):
    games = [gen_game(rng, rng.randint(1, 4))]
    # Ensure both event signs occur at a reachable node of the first component.
    g = [list(node) for node in games[0]]
    g[0][0] = tuple(dict.fromkeys((*g[0][0], WHITE)))
    g[0][1] = tuple(dict.fromkeys((*g[0][1], BLACK)))
    games[0] = tuple(tuple(side) for side in g)
    games.extend(zero_game() for _ in range(k - 1))
    return tuple(games)


def normal_game(rng, n):
    return tuple(
        tuple(tuple(j for j in range(n) if rng.random() < 0.22) for _ in (0, 1))
        for _ in range(n)
    )


def test_reserve_lemma(rng, trials=500):
    left_both = right_both = left_mono = right_mono = 0
    assertions = 0
    for _ in range(trials):
        g1 = normal_game(rng, rng.randint(1, 4))
        g2 = normal_game(rng, rng.randint(1, 4))
        n1, n2 = rng.randint(0, 4), rng.randint(0, 4)
        if (normal_result((g1,), (0,), n1, 1, 1) == WHITE and
                normal_result((g2,), (0,), n2, 1, 1) == WHITE):
            left_both += 1
            assert normal_result((g1, g2), (0, 0), n1 + n2, 1, 1) == WHITE
            assertions += 1
        if (normal_result((g1,), (0,), -n1, 0, 1) == BLACK and
                normal_result((g2,), (0,), -n2, 0, 1) == BLACK):
            right_both += 1
            assert normal_result((g1, g2), (0, 0), -(n1 + n2), 0, 1) == BLACK
            assertions += 1
        n = rng.randint(0, 4)
        m = rng.randint(n, 4)
        if normal_result((g1,), (0,), n, 1, 1) == WHITE:
            left_mono += 1
            assert normal_result((g1,), (0,), m, 1, 1) == WHITE
            assertions += 1
        if normal_result((g1,), (0,), -n, 0, 1) == BLACK:
            right_mono += 1
            assert normal_result((g1,), (0,), -m, 0, 1) == BLACK
            assertions += 1
    return {"generated_pairs": trials,
            "left_subadditivity_premises": left_both,
            "right_subadditivity_premises": right_both,
            "left_monotonicity_premises": left_mono,
            "right_monotonicity_premises": right_mono,
            "successful_implication_checks": assertions}


def test_bridge_and_criterion(rng, trials=180, signals=60):
    bridge = {"generated": 0, "dominant": 0, "positions": 0, "frontiers": 0}
    criterion = {"generated": 0, "holds": 0, "frontiers": 0, "positions": 0}
    for ix in range(trials + signals):
        k = rng.choice((2, 3))
        B = rng.randint(1, 4)
        games = signal_case(rng, k) if ix >= trials else tuple(
            gen_game(rng, rng.randint(1, 4)) for _ in range(k)
        )
        dom, checks = first_event_dominant(games, B)
        bridge["generated"] += 1
        bridge["frontiers"] += checks
        if dom:
            bridge["dominant"] += 1
            ok, positions = bridge_matches(games, B)
            assert ok
            bridge["positions"] += positions

        holds = reserve_condition(games, B)
        criterion["generated"] += 1
        if holds:
            criterion["holds"] += 1
            dom2, checks2 = first_event_dominant(games, B)
            assert dom2
            criterion["frontiers"] += checks2
            ok, positions = bridge_matches(games, B)
            assert ok
            criterion["positions"] += positions
    return {"bridge": bridge, "criterion": criterion}


def test_sandwich(rng, trials=300):
    on = (((0,), ()),)
    off = (((), (0,)),)
    dud = (((0,), (0,)),)
    positions = 0
    for _ in range(trials):
        k = gen_game(rng, rng.randint(1, 4))
        s = gen_game(rng, rng.randint(1, 4), restricted=True)
        for node in range(len(s)):
            assert WHITE not in s[node][0] and BLACK not in s[node][1]
        systems = [d_sum_result((k, q)) for q in (off, s, on, dud)]
        (wo, lo), (ws, ls), (wn, ln), (wd, ld) = systems
        for x in range(len(k)):
            for y in range(len(s)):
                for turn in (0, 1):
                    offq, sq, onq, dudq = (
                        ((x, 0), turn), ((x, y), turn), ((x, 0), turn), ((x, 0), turn)
                    )
                    if not ((offq not in wo or sq in ws) and (sq not in ws or onq in wn)):
                        raise AssertionError(("W-chain", k, s, x, y, turn,
                                              offq in wo, sq in ws, onq in wn))
                    if not ((onq not in ln or sq in ls) and (sq not in ls or offq in lo)):
                        raise AssertionError(("L-chain", k, s, x, y, turn,
                                              onq in ln, sq in ls, offq in lo))
                    if (offq in wo) != (dudq in wd):
                        raise AssertionError(("W-equality", k, s, x, y, turn,
                                              offq in wo, dudq in wd))
                    if (onq in ln) != (dudq in ld):
                        raise AssertionError(("L-equality", k, s, x, y, turn,
                                              onq in ln, dudq in ld))
                    positions += 1
    return {"generated_K_S_pairs": trials, "positions": positions,
            "assertions_per_position": 6}


def main():
    rng = random.Random(330027)
    print(json.dumps({
        "seed": 330027,
        "generator": "independent directed edges: node probability .22, allowed terminal probability .14; roots 0; n=1..4; B=1..4; seed 330027",
        "lemma_3_8a": test_reserve_lemma(rng),
        "theorems_3_7_3_8": test_bridge_and_criterion(rng),
        "theorem_3_11": test_sandwich(rng),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
