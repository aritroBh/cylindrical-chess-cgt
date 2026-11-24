"""Evaluate the abstract witness in PROOF.md. Run from the project root."""

from itertools import product

# Every pair lists White options first, Black options second. W and L end the sum.
group = {
    "r0": (("q",), ("r1", "x")),
    "r1": (("q",), ("r0", "x")),
    "q": (("x",), ("p",)),
    "x": (("q",), ("L",)),
    "p": (("W",), ("L",)),
}
over = {"omega": (("zero",), ("omega",)), "zero": ((), ())}
context = {"empty": ((), ()), "star": (("empty",), ("empty",)),
           "minus1": ((), ("empty",))}


def outcomes(board, outside):
    moves = {}
    for a, t, side in product(board, outside, (0, 1)):
        options = [v if v in ("W", "L") else (v, t, 1 - side)
                   for v in board[a][side]]
        options.extend(v if v in ("W", "L") else (a, v, 1 - side)
                       for v in outside[t][side])
        moves[a, t, side] = options

    known = {"W": "W", "L": "L"}
    while True:
        new = {}
        for state, options in moves.items():
            if state in known:
                continue
            own, enemy = ("W", "L") if state[2] == 0 else ("L", "W")
            if any(known.get(v) == own for v in options):
                new[state] = own
            elif all(known.get(v) == enemy for v in options):
                new[state] = enemy
        if not new:
            return {state: known.get(state, "D") for state in moves}
        known.update(new)


if __name__ == "__main__":
    for board, entries in (
        (group, [("q", "empty", "LW"), ("x", "empty", "WL"),
                 ("x", "minus1", "LL"), ("r0", "star", "WL"),
                 ("r1", "star", "WL"), ("q", "star", "WL")]),
        (over, [("omega", "star", "WW"), ("zero", "star", "WL")]),
    ):
        result = outcomes(board, context)
        for a, t, expected in entries:
            pair = "".join(result[a, t, side] for side in (0, 1))
            assert pair == expected, (a, t, pair, expected)
            print(a, t, pair)
