"""Enumerate labelled DAGs. Compare direct attractors with Theorem 3.4."""
from itertools import product

WHITE, BLACK = 0, 1
PLUS, MINUS = -2, -1
RESERVOIRS = {"dud": (True, True), "on": (True, False), "off": (False, True)}


def subsets(items):
    return [tuple(x for i, x in enumerate(items) if mask >> i & 1)
            for mask in range(1 << len(items))]


def all_games(n):
    choices = [subsets([PLUS, MINUS, *range(i + 1, n)]) for i in range(n)]
    yield from product(*(opts for opts in choices for _ in (WHITE, BLACK)))


def tree_games(n):
    # Each vertex j > 0 chooses its parent, then which sides may use that edge.
    terminal_options = subsets([PLUS, MINUS])
    for parents in product(*(range(j) for j in range(1, n))):
        for owners in product((1, 2, 3), repeat=n - 1):
            graph = [[] for _ in range(2 * n)]
            for j, (parent, owner) in enumerate(zip(parents, owners), 1):
                for side in (WHITE, BLACK):
                    if owner & (1 << side):
                        graph[2 * parent + side].append(j)
            prefix = tuple(map(tuple, graph[:-2]))
            for exits in product(terminal_options, repeat=2):
                yield prefix + exits


def direct(game, passes):
    # State 2*x+s is (x, omega, s). Terminal vertices carry their own outcomes.
    moves = []
    for state, options in enumerate(game):
        other = 1 - state % 2
        successors = [2 * y + other if y >= 0 else y for y in options]
        if passes[state % 2]:
            successors.append(state ^ 1)
        moves.append(successors)

    result = ["D"] * len(moves)
    for side, terminal, label in ((WHITE, PLUS, "W"), (BLACK, MINUS, "L")):
        reached = {terminal}
        while True:
            added = set()
            for state, options in enumerate(moves):
                if state in reached:
                    continue
                if state % 2 == side:
                    wins = any(y in reached for y in options)
                else:
                    wins = all(y in reached for y in options)
                if wins:
                    added.add(state)
            if not added:
                break
            reached.update(added)
        for state in reached - {terminal}:
            assert result[state] == "D"
            result[state] = label
    return result


def theorem(game, mode):
    n = len(game) // 2

    def forced(side):
        win = [False] * (2 * n)
        favorable = (PLUS, MINUS)[side]
        for x in reversed(range(n)):
            own, opposing = 2 * x + side, 2 * x + 1 - side
            win[own] = any(y == favorable if y < 0 else win[2 * y + 1 - side]
                           for y in game[own])
            win[opposing] = win[own] and all(
                y == favorable if y < 0 else win[2 * y + side] for y in game[opposing])
        return win

    if mode == "on":
        return ["L" if v else "W" for v in forced(BLACK)]
    if mode == "off":
        return ["W" if v else "L" for v in forced(WHITE)]
    return ["W" if w else "L" if b else "D" for w, b in zip(forced(WHITE), forced(BLACK))]


def check(n, games):
    counts = {mode: dict.fromkeys("WLD", 0) for mode in RESERVOIRS}
    total = mismatches = 0
    for game in games:
        total += 1
        for mode, passes in RESERVOIRS.items():
            actual = direct(game, passes)
            predicted = theorem(game, mode)
            for state, (a, p) in enumerate(zip(actual, predicted)):
                counts[mode][a] += 1
                if a != p:
                    mismatches += 1
                    print("disagreement", game, mode, divmod(state, 2), a, p)
    print(n, total, total * 6 * n, mismatches, counts, flush=True)
    return mismatches


if __name__ == "__main__":
    errors = sum(check(n, all_games(n) if n <= 3 else tree_games(n)) for n in range(1, 7))
    raise SystemExit(bool(errors))
