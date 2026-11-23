"""K52, run from the repository root. One labeled placement/flag is one root."""
import argparse
from collections import Counter
from functools import cache
from itertools import combinations, product
from resource import RUSAGE_SELF, getrusage

from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas import common


def flags(board, pos):
    """All flags possible after a single double step, including inert flags."""
    yield pos
    occupied = pos.white | pos.black
    for side, army, rank, step in (("B", pos.white, 4, 1),
                                   ("W", pos.black, board.ranks - 3, -1)):
        for f, r in army:
            target = (f, r - step)
            if r == rank and target not in occupied and (f, r - 2*step) not in occupied:
                yield Pos(pos.white, pos.black, (target, (f, r), side))


def usable(board, pos):
    return bool(pos.ep and pawns.ep_capturable(board, pos,
                "W" if pos.ep[2] == "B" else "B", pos.ep[1]))


@cache
def conditions(board, pos):
    if common.terminal(board, pos) is not None:
        return True, True
    safe = common.pairwise_safe(board, pos)
    ep_ok = not (usable(board, pos) and len(pawns.components(board, pos)) > 1)
    for side in ("W", "B"):
        for child in pawns.moves(board, pos, side):
            child_safe, child_ep = conditions(board, child)
            safe &= child_safe
            ep_ok &= child_ep
    return safe, ep_ok


def sweep(board):
    squares = tuple(product(range(board.files), range(2, board.ranks)))
    rows = Counter()
    for nw, nb in product(range(3), repeat=2):
        for w in combinations(squares, nw):
            white = frozenset(w)
            for b in combinations([s for s in squares if s not in white], nb):
                for pos in flags(board, Pos(white, frozenset(b))):
                    if common.terminal(board, pos) is not None:
                        continue
                    hss, ep_ok = conditions(board, pos)
                    flag = ("usable" if usable(board, pos) else "inert") if pos.ep else "none"
                    rows[flag, "free"] += 1
                    if not hss:
                        continue
                    group = "E" if ep_ok else "failE"
                    rows[flag, group] += 1
                    got = cgt.outcome(pawns.value(board, pos))
                    expected = common.alt_outcome(board, pos, pawns.RACE_RULE)
                    if got != expected:
                        rows[flag, group + "_diff"] += 1
                        print("DIFF", board, pos, pos.ep, group, got, expected, flush=True)
    for flag in ("none", "inert", "usable"):
        print("cyl" if board.wrap else "flat", board.files, board.ranks, flag,
              *(rows[flag, c] for c in ("free", "E", "failE", "E_diff", "failE_diff")))
    print("peak_RSS_bytes_macOS", getrusage(RUSAGE_SELF).ru_maxrss)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("shape", choices=("flat", "cyl"))
    parser.add_argument("files", type=int, choices=(3, 4))
    parser.add_argument("ranks", type=int, choices=(4, 5, 6))
    parser.add_argument("--rule", choices=common.RULES, default="count")
    args = parser.parse_args()
    assert pawns.PASSED_RESPECTS_EP and pawns.BIG == 256
    pawns.RACE_RULE = args.rule
    pawns._value.cache_clear()
    # Memoize the engine's pure integer constructor; its result is already interned.
    cgt.integer = cache(cgt.integer)
    sweep(Board(args.files, args.ranks, args.shape == "cyl", True))
