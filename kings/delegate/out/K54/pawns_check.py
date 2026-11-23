"""From the project root, run with PYTHONPATH=. and python -B."""
import argparse
from collections import Counter
from functools import cache, lru_cache
from itertools import combinations

from cylcgt import cgt, pawns

parser = argparse.ArgumentParser()
parser.add_argument("ranks", type=int, choices=(6, 7))
parser.add_argument("rule", choices=("count", "mover", "opponent"))
parser.add_argument("--textbook", action="store_true")
args = parser.parse_args()
cgt.integer = cache(cgt.integer)  # Pure constructor returns already-interned games.
board = pawns.Board(5, args.ranks, False, True)
pawns.RACE_RULE = args.rule
pawns.PASSED_RESPECTS_EP = not args.textbook
pawns._value.cache_clear()


@lru_cache(8192)
def passers(pos):
    return frozenset(side for side in "WB" if pawns.passed(board, pos, side))


@lru_cache(8192)
def threats(pos):
    signs = passers(pos)
    if signs:
        return signs
    return frozenset(s for side in "WB" for child in pawns.moves(board, pos, side)
                     for s in threats(child))


@lru_cache(8192)
def conditions(pos):
    """Intersect HSS and E over the any-order whole-board pre-event tree."""
    if passers(pos):
        return True, True
    parts = pawns.components(board, pos)
    signs = [threats(c) for c in parts] if len(parts) > 1 else []
    safe = all(not ("W" in a and "B" in b)
               for i, a in enumerate(signs) for j, b in enumerate(signs) if i != j)
    usable = False
    if len(parts) > 1 and pos.ep:
        # Only an e.p. capture deletes the vulnerable pawn and lands on the target.
        target, victim, entitled = pos.ep
        usable = any(target in (q.white if entitled == "W" else q.black)
                     and victim not in (q.white | q.black)
                     for q in pawns.moves(board, pos, entitled))
    ep_ok = not usable
    for side in "WB":
        for child in pawns.moves(board, pos, side):
            h, e = conditions(child)
            safe, ep_ok = safe and h, ep_ok and e
    return safe, ep_ok


@lru_cache(8192)
def wins(pos, side):
    """Whole-board alternating minimax. On entry the previous mover is known."""
    other = "B" if side == "W" else "W"
    signs = passers(pos)
    if len(signs) == 2:
        if args.rule == "count":
            return pawns.promote_distance(board, pos, side) <= pawns.promote_distance(board, pos, other)
        return args.rule == "opponent"
    if signs:
        return side in signs
    return any(not wins(child, other) for child in pawns.moves(board, pos, side))


def assess(pos):
    parts = pawns.components(board, pos)
    if any("W" in threats(a) and "B" in threats(b) for a in parts for b in parts if a != b):
        return "unsafe", None
    safe, ep_ok = conditions(pos)
    if not safe:
        return "unsafe", None
    # Sum of remaining ranks bounds the sum of stopped counts after any split.
    assert max(sum(board.ranks-r for _, r in pos.white),
               sum(r-1 for _, r in pos.black)) < pawns.BIG
    s = cgt.outcome(pawns.value(board, pos))
    d = { (True, False): "L", (False, True): "R",
          (True, True): "N", (False, False): "P"}[wins(pos, "W"), wins(pos, "B")]
    return "E" if ep_ok else "late", (s, d)


def groups(files, nw, nb):
    cells = [(f, r) for f in files for r in range(2, board.ranks)]
    for occupied in combinations(cells, nw+nb):
        if len({f for f, r in occupied}) != len(files):
            continue
        for w in combinations(occupied, nw):
            p = pawns.Pos(frozenset(w), frozenset(occupied)-set(w))
            if not passers(p):
                yield p


if __name__ == "__main__":
    for left, right in (((0, 1), (4,)), ((0, 1, 2), (4,)), ((0, 1), (3, 4))):
        for material in ((3, 3), (3, 2), (2, 3)):
            counts = Counter()
            for nw in range(1, material[0]):
                for nb in range(1, material[1]):
                    others = list(groups(right, material[0]-nw, material[1]-nb))
                    for a in groups(left, nw, nb):
                        for b in others:
                            p = pawns.Pos(a.white | b.white, a.black | b.black)
                            stratum, pair = assess(p)
                            diff = bool(pair and pair[0] != pair[1])
                            if diff and counts[stratum, True] < 4:
                                print("mismatch", stratum, p, pair, flush=True)
                            counts[stratum, diff] += 1
            print("widths", (len(left), len(right)), "W/B", material,
                  "H", board.ranks, args.rule, "ep-aware", not args.textbook,
                  sorted(counts.items()), flush=True)
            assert not counts["E", True]
