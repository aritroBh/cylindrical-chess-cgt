"""V1 verifier scratch: does any game tree behind the V1 claim contain a node where a
double step creates a 'passed' pawn (per pawns.passed) that the opponent could
immediately capture en passant?  pawns.passed() ignores e.p. rights, so at such a node
the solver ends the game (or calls the race rule) although the e.p. capture exists.

Also recomputes every V1 value with an e.p.-aware passed() (the double-stepped pawn is
not counted as passed while the opponent holds a usable e.p. capture of it), by
monkeypatching pawns.passed at runtime.  cylcgt itself is not edited.

Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     PYTHONPATH=. .venv/bin/python verify/diagrams/V1-reproduce/ep_passer_check.py
"""
import sys
from dataclasses import replace

from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos, moves

sys.setrecursionlimit(100000)
ORIG_PASSED = pawns.passed
CYL = Board(8, 8, True, True)

POSITIONS = {
    "2.1": "W: e4 / B: e5",
    "2.2": "W: a2 h1 / B: a3 h4",
    "3.1": "W: a3 h1 / B: a4 h5",
    "3.2": "W: a4 h1 / B: a5 h6",
    "4.1": "W: e4 / B: e6",
    "4.2": "W: e3 / B: e6",
    "4.3": "W: a4 h2 h4 / B: a5 a6 a7 h3",
    "7.1c": "W: c2 c3 / B: c5 c6",
    "7.1f": "W: f3 f4 / B: f7",
    "7.1ah": "W: a4 a5 h2 h3 / B: a7 h6",
    "7.2abh": "W: a2 b2 h3 / B: a6 b7 h7",
    "7.3": "W: a1 a5 c1 c3 d3 f7 g1 h1 / B: c2 d4 d5 d6 g3 g7 h4",
    "7.3cd": "W: c1 c3 d3 / B: c2 d4 d5 d6",
    "KEY *2 (4-file flat)": "W: a2 c2 / B: b7 d7",
}


def ep_capturable(board, pos):
    """True if pos carries an e.p. right that the entitled side can actually use."""
    if not pos.ep:
        return False
    target, victim, side = pos.ep
    capt = pos.black if side == "B" else pos.white
    f, r = victim
    return any(board.nb(f, df) is not None and (board.nb(f, df), r) in capt for df in (-1, 1))


def passed_ep_aware(board, pos, side):
    if pos.ep and ep_capturable(board, pos) and pos.ep[2] != side:
        victim = pos.ep[1]
        mine = (pos.white if side == "W" else pos.black) - {victim}
        p2 = Pos(mine, pos.black, None) if side == "W" else Pos(pos.white, mine, None)
        return ORIG_PASSED(board, p2, side)
    return ORIG_PASSED(board, pos, side)


def flag_tree(board, root):
    seen, stack, flagged = set(), [root], []
    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        wp, bp = ORIG_PASSED(board, p, "W"), ORIG_PASSED(board, p, "B")
        if p.ep and ep_capturable(board, p):
            if (wp, bp) != (passed_ep_aware(board, p, "W"), passed_ep_aware(board, p, "B")):
                flagged.append(p)
        if wp or bp:
            continue  # terminal for the solver
        plain = Pos(p.white, p.black, None)
        lpos = plain if (p.ep and p.ep[2] != "W") else p
        rpos = plain if (p.ep and p.ep[2] != "B") else p
        stack.extend(moves(board, lpos, "W"))
        stack.extend(moves(board, rpos, "B"))
    return len(seen), flagged


def values(board, pos):
    out = {}
    for rule in ("count", "mover", "opponent"):
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        out[rule] = cgt.show(pawns.value(board, pos))
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()
    return out


for label, text in POSITIONS.items():
    pos = Pos.parse(text)
    board = Board(4, 8, False, True) if label.startswith("KEY") else CYL
    n, fl = flag_tree(board, pos)
    print(f"{label:22s} {text:55s} nodes {n:6d}  e.p.-capturable-passer nodes {len(fl)}")
    for p in fl[:4]:
        print(f"      e.g. {p}")
    if fl:
        std = values(board, pos)
        pawns.passed = passed_ep_aware
        try:
            alt = values(board, pos)
        finally:
            pawns.passed = ORIG_PASSED
            pawns._value.cache_clear()
        out_std = {k: cgt.outcome(None) if False else k for k in std}
        print(f"      standard passed():  {std}")
        print(f"      e.p.-aware passed(): {alt}")
        # outcome classes
        for tag, fn in (("std", ORIG_PASSED), ("ep-aware", passed_ep_aware)):
            pawns.passed = fn
            oc = {}
            for rule in ("count", "mover", "opponent"):
                pawns.RACE_RULE = rule
                pawns._value.cache_clear()
                oc[rule] = cgt.outcome(pawns.value(board, pos))
            pawns.passed = ORIG_PASSED
            pawns.RACE_RULE = "count"
            pawns._value.cache_clear()
            print(f"      outcome ({tag}): {oc}")
