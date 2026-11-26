"""Independent finite-game check. Run from the repository root, see REPORT.md."""
from functools import cache
from math import inf
from sys import argv

WHITE, BLACK = 0, 1
BIG = 256
# A reference game indexes its white and black options. -1/8 = {-1/4 | 0}.
REF = {
    "0": ((), ()), "*": (("0",), ("0",)), "*2": (("0", "*"), ("0", "*")),
    "-1": ((), ("0",)), "-1/2": (("-1",), ("0",)),
    "-1/4": (("-1/2",), ("0",)), "-1/8": (("-1/4",), ("0",)),
}
ROOTS = {
    "A": ("a4 b3 d2 d3", "a7 b7 c5"), "B": ("b4 c2 d2", "a6 a7 c6 d5"),
    "eighth": ("a2 b2 b3", "a5 a6 b6"), "X": ("b2 d4 g3 h5", "a7 c7 f7 g4"),
}


def square(s):
    return (int(s[1]) - 1) * 8 + ord(s[0]) - ord("a")


def name(q):
    return chr(ord("a") + q % 8) + str(q // 8 + 1)


def position(w, b):
    return tuple(sorted(map(square, w.split()))), tuple(sorted(map(square, b.split()))), -1


def thresholds(white_options, black_options):
    # Smallest integer k for White to win G+k, for each starting player.
    u = min(white_options, default=inf)
    v = max(black_options, default=-inf)
    return min(u, 1 + max(0, v)), max(v, min(0, u - 1))


def run(label, ep, race, model):
    wrapped = label == "X"
    def adjacent(a, b):
        gap = abs(a % 8 - b % 8)
        return gap == 1 or (wrapped and gap == 7)

    def steps(pos, side):
        own, enemy, flag = pos[side], pos[1-side], pos[2]
        step = (-8 if side else 8)
        occupied = set(own + enemy)
        for src in own:
            one = src + step
            if not 0 <= one < 64:
                continue
            moves = []
            if one not in occupied:
                moves.append((one, -1, -1))
                if src // 8 == (6 if side else 1) and one + step not in occupied:
                    usable = ep != "off" and any(
                        p // 8 == (one + step) // 8 and adjacent(p, src) for p in enemy)
                    moves.append((one + step, -1, one + step if usable else -1))
            for victim in enemy:
                if adjacent(victim, src):
                    if victim // 8 == one // 8:
                        moves.append((victim, victim, -1))
                    if victim == flag and victim // 8 == src // 8 and victim + step not in occupied:
                        moves.append((victim + step, victim, -1))
            for dst, victim, newflag in moves:
                mine = tuple(sorted((set(own) - {src}) | {dst}))
                theirs = tuple(q for q in enemy if q != victim)
                yield name(src) + "-" + name(dst), ((theirs, mine, newflag) if side else (mine, theirs, newflag))

    def passers(pos, side):
        direction = -1 if side else 1
        for q in pos[side]:
            if any((p // 8 - q // 8) * direction > 0 and
                   (p % 8 == q % 8 or adjacent(p, q)) for p in pos[1-side]):
                continue
            if ep == "aware" and q == pos[2] and any(
                    p // 8 == q // 8 and adjacent(p, q) for p in pos[1-side]):
                continue
            yield q

    def split(pos):
        if model == "W":
            return (pos,)
        unseen = {q % 8 for q in pos[0] + pos[1]}
        parts = []
        while unseen:
            files = {unseen.pop()}
            while more := {f for f in unseen if any(adjacent(f, g) for g in files)}:
                files.update(more)
                unseen -= more
            parts.append(tuple(tuple(q for q in pieces if q % 8 in files) for pieces in pos[:2])
                         + (pos[2] if pos[2] >= 0 and pos[2] % 8 in files else -1,))
        return tuple(sorted(parts))

    races = set()
    @cache
    def options(pos, side):
        found = []
        for move, child in steps(pos, side):
            w, b = (list(passers(child, s)) for s in (WHITE, BLACK))
            if not (w or b):
                found.append((move, split(child), 0))
                continue
            if w and b:
                races.add((child, side))
                if race == "count":
                    wd = min(7 - q // 8 - (q // 8 == 1) for q in w)
                    bd = min(q // 8 - (q // 8 == 6) for q in b)
                    winner = (1-side if wd == bd else int(bd < wd))
                else:
                    winner = {"mover": side, "opponent": 1-side, "white": WHITE, "black": BLACK}[race]
            else:
                winner = WHITE if w else BLACK
            found.append((move, (), BIG if winner == WHITE else -BIG))
        return found

    @cache
    def solve(parts, ref):
        choices = [[], []]
        for side in (WHITE, BLACK):
            for newref in REF[ref][side]:
                choices[side].append(solve(parts, newref)[1-side])
            for i, part in enumerate(parts):
                rest = parts[:i] + parts[i+1:]
                for _, newparts, shift in options(part, side):
                    need = solve(tuple(sorted(rest + newparts)), ref)[1-side]
                    choices[side].append(need - shift)
        return thresholds(*choices)

    root = position(*ROOTS[label])
    ref = {"A": "*2", "B": "*2", "eighth": "-1/8", "X": "0"}[label]
    initial = split(root)
    assert not any(list(passers(root, s)) for s in (WHITE, BLACK))
    a, b = solve(initial, ref)
    outcome = ("L" if b <= 0 else "N") if a <= 0 else ("P" if b <= 0 else "R")
    print(label, model, ep, race, ref, (a, b), outcome, flush=True)
    if label == "eighth" and (model, race) == ("S", "count"):
        # solve above visits both colours and every child. Check all assignments
        # simultaneously, with one bit per assignment and no integer-shift logic.
        keys = sorted(races)
        n = 2 ** len(keys)
        full = (1 << n) - 1
        white_wins_race = {
            key: sum(1 << j for j in range(n) if (j >> i) & 1)
            for i, key in enumerate(keys)
        }

        @cache
        def white_wins(pos, tree, side):
            masks = [white_wins(pos, t, 1-side) for t in REF[tree][side]]
            for _, child in steps(pos, side):
                w, b = (bool(list(passers(child, s))) for s in (WHITE, BLACK))
                if w and b:
                    masks.append(white_wins_race[child, side])
                elif w or b:
                    # Sole pawn component has ended; BIG exceeds reference height.
                    masks.append(full if w else 0)
                else:
                    assert split(child) == (child,)
                    masks.append(white_wins(child, tree, 1-side))
            result = full if side == BLACK else 0
            for mask in masks:
                result = (result & mask) if side == BLACK else (result | mask)
            return result

        white_start = white_wins(root, ref, WHITE)
        black_start = white_wins(root, ref, BLACK)
        previous_wins = (full ^ white_start) & black_start
        print("assignments", ep, "keys", len(keys), "tested", n, "P", previous_wins.bit_count())
        assert previous_wins == full
        white_wins.cache_clear()
    if label == "X" and model == "S":
        # Replay the witness found by breadth-first search; either side may move.
        def follow(pos, line):
            for move in line:
                assert not any(list(passers(pos, s)) for s in (WHITE, BLACK))
                [pos] = [child for s in (WHITE, BLACK) for m, child in steps(pos, s) if m == move]
            return pos

        prefix = ["h5-h6", "a7-h6"]
        left, right = ["d4-d5", "c7-c5"], ["h6-h5", "h5-h4", "g3-h4"]
        branch = follow(root, prefix)
        assert not any(list(passers(branch, s)) for s in (WHITE, BLACK))
        parts = split(branch)
        assert len(initial) == 1 and len(parts) == 2
        for side, line in enumerate((left, right)):
            part = next(p for p in parts if square(line[0][:2]) in p[0] + p[1])
            assert list(passers(follow(part, line), side))
            parts = tuple(p for p in parts if p != part)
        print("HSS witness", prefix, "white", left, "black", right, "root components", len(initial))
    options.cache_clear()
    solve.cache_clear()
    return outcome


def main():
    assert thresholds([], []) == (1, 0)
    assert thresholds([0], [1]) == (0, 1)  # star
    assert thresholds([0], []) == (0, -1)  # +1
    for label in argv[1:] or ROOTS:
        for model in ("W", "S"):
            if label == "X":
                assert run(label, "off", "count", model) == ("R" if model == "S" else "N")
                continue
            for ep in ("aware", "off", "textbook"):
                for race in (("count", "mover", "opponent", "white", "black") if label == "eighth"
                             else ("count", "mover", "opponent")):
                    result = run(label, ep, race, model)
                    assert (result == "P") == (label == "eighth" or (ep != "off" and race != "opponent"))


if __name__ == "__main__":
    main()
