"""Falsification tests for Lemma L4 (the race rules are not exact chess).

Run (from the project root):
    PYTHONPATH=. .venv/bin/python lemmas/test_L4_races.py

For each example position (flat 8x8, both sides have a passed pawn) we print
  * the winner predicted by each race rule of cylcgt.pawns ("count", "mover",
    "opponent"), applied as if the side NOT to move had just made the move
    that started the race, and
  * the result of an exact forced-win search in real chess (lemmas/minichess.py:
    legal moves incl. under-promotion, check, mate, stalemate; a line ends in
    checkmate or in a KQK leaf).
Example 4.6 is the other way round: the count rule is right and the
"mover" rule is wrong, so every one of the three rules fails on some example.
A "proved" verdict means the search found a forced win for that side within
the stated number of plies, so the other side has no forced win. Each check
asserts that the count rule's prediction is contradicted.

The last example (both sides queen) is only bounded evidence: a search finds no
forced win for either side within the stated depth; it does not prove a draw.
"""
from __future__ import annotations

import sys

from cylcgt import pawns
from cylcgt.pawns import Board, Pos

from cylcgt import cgt

from lemmas import minichess as mc
from lemmas.common import NBIG, PBIG, race_winner, reachable, split_ep, terminal

FAIL = []

EXAMPLES = [
    # (label, phenomenon, position, side to move, max plies for the search)
    ("4.1", "square rule: the defending king catches the passer",
     "W: Ke3 Pa5 / B: Kh7 Pd4", "B", 12),
    ("4.2", "square rule: the defending king captures the faster pawn",
     "W: Kh8 Pa6 / B: Kb6 Pd3", "W", 10),
    ("4.3", "king next to the promotion square: the new queen is taken",
     "W: Kh8 Pa7 / B: Kb7 Ph3", "W", 10),
    ("4.4", "promotion with check: a skewer wins the first queen",
     "W: Kd5 Pa7 / B: Kb6 Ph2", "W", 10),
    ("4.6", "the new queen stops the other pawn (count right, 'mover' wrong)",
     "W: Ka4 Pg7 / B: Ka6 Pg2", "W", 8),
]

BOUNDED = ("4.5", "both sides queen (Q vs Q); the count rule calls it a White win",
           "W: Ka3 Pc7 / B: Kh6 Pf2", "W", 6)


def pawn_only(text: str) -> Pos:
    w, b = text.split("/")
    wp = [t[1:] for t in w.split(":")[1].split() if t.startswith("P")]
    bp = [t[1:] for t in b.split(":")[1].split() if t.startswith("P")]
    return Pos.parse("W: " + " ".join(wp) + " / B: " + " ".join(bp))


def rule_predictions(text: str, stm: str):
    board = Board(8, 8, False, True)
    pos = pawn_only(text)
    assert pawns.passed(board, pos, "W") and pawns.passed(board, pos, "B"), text
    mover = "B" if stm == "W" else "W"  # the side that "just moved"
    return {r: race_winner(board, pos, mover, r) for r in ("count", "mover", "opponent")}, \
        (pawns.promote_distance(board, pos, "W"), pawns.promote_distance(board, pos, "B"))


def run(bounded: bool = True):
    rows = []
    for label, what, text, stm, depth in EXAMPLES:
        preds, dists = rule_predictions(text, stm)
        p = mc.make_pos(text, stm)
        res = {}
        for who in "WB":
            res[who] = mc.min_forced_win(p, who, depth)
        winner = [w for w in "WB" if res[w] is not None]
        line = mc.principal_line(p, winner[0], res[winner[0]]) if winner else []
        rows.append((label, what, text, stm, dists, preds, res, " ".join(line)))
        if len(winner) != 1:
            FAIL.append(f"{label}: expected exactly one forced winner, got {res}")
        elif label != "4.6" and preds["count"] == winner[0]:
            FAIL.append(f"{label}: count rule agrees with chess ({winner[0]})")
        elif label == "4.6" and (preds["mover"] == winner[0] or preds["count"] != winner[0]):
            FAIL.append(f"{label}: expected count right and mover wrong")
    if not bounded:
        return rows
    label, what, text, stm, depth = BOUNDED
    preds, dists = rule_predictions(text, stm)
    p = mc.make_pos(text, stm)
    res = {who: mc.forces_win(p, who, depth) for who in "WB"}
    rows.append((label, what, text, stm, dists, preds, res, "(bounded search only)"))
    return rows


# ---------------------------------------------------------------------------
# 4.7  sensitivity of the *2 candidate to individual race verdicts
# ---------------------------------------------------------------------------

def W_override(board, pos, rule, override, memo):
    """Whole-board convention game W, except that the race verdicts listed in
    `override` ({(child, mover): winner}) replace the race rule."""
    g = memo.get(pos)
    if g is not None:
        return g
    t = terminal(board, pos)
    if t == 1:
        g = PBIG
    elif t == -1:
        g = NBIG
    else:
        lpos, rpos = split_ep(pos)
        L = [_ov_child(board, c, "W", rule, override, memo) for c in pawns.moves(board, lpos, "W")]
        R = [_ov_child(board, c, "B", rule, override, memo) for c in pawns.moves(board, rpos, "B")]
        g = cgt.make(L, R)
    memo[pos] = g
    return g


def _ov_child(board, c, mover, rule, override, memo):
    if terminal(board, c) == 0:
        w = override.get((c, mover)) or race_winner(board, c, mover, rule)
        return PBIG if w == "W" else NBIG
    return W_override(board, c, rule, override, memo)


def race_nodes(board, x):
    races = set()
    for y in reachable(board, x):
        if terminal(board, y) is not None:
            continue
        lpos, rpos = split_ep(y)
        for side, src in (("W", lpos), ("B", rpos)):
            for c in pawns.moves(board, src, side):
                if terminal(board, c) == 0:
                    races.add((c, side))
    return races


def sensitivity(ep: bool, trials: int = 200, seed: int = 1):
    import random
    b = Board(4, 8, False, ep)
    x = Pos.parse("W: a2 c2 / B: b7 d7")
    races = race_nodes(b, x)
    base = W_override(b, x, "count", {}, {})
    critical = []
    for c, m in sorted(races, key=str):
        w = race_winner(b, c, m, "count")
        v = W_override(b, x, "count", {(c, m): ("B" if w == "W" else "W")}, {})
        if v is not base:
            critical.append((c, m, w, cgt.show(v)))
    crit = {(c, m) for c, m, _, _ in critical}
    other = lambda m: "B" if m == "W" else "W"
    mixed = {(c, m): (m if (c, m) in crit else other(m)) for c, m in races}
    v_mixed = W_override(b, x, "count", mixed, {})
    rng = random.Random(seed)
    hist = {}
    for _ in range(trials):
        ov = {(c, m): (m if (c, m) in crit else rng.choice("WB")) for c, m in races}
        v = cgt.show(W_override(b, x, "count", ov, {}))
        hist[v] = hist.get(v, 0) + 1
    return dict(ep=ep, base=cgt.show(base), n_races=len(races),
                count_equals_mover=sum(1 for c, m in races if race_winner(b, c, m, "count") == m),
                critical=[(str(c), m, w, v) for c, m, w, v in critical],
                critical_mover_rest_opponent=cgt.show(v_mixed), random_rest=hist)


def test_examples():
    FAIL.clear()
    run(bounded=False)
    assert not FAIL, FAIL


if __name__ == "__main__":
    for label, what, text, stm, dists, preds, res, line in run():
        print(f"Example {label}: {what}")
        print(f"   position {text}, {stm} to move; promotion distances (W, B) = {dists}")
        print(f"   race rules predict: {preds}")
        print(f"   chess: forced win found for W within {res['W']} plies, for B within {res['B']} plies"
              if label != BOUNDED[0] else
              f"   chess: forced win for W within {BOUNDED[4]} plies: {res['W']}; for B: {res['B']}")
        print(f"   line: {line}")
    for ep in (True, False):
        r = sensitivity(ep)
        print(f"4.7 *2 candidate, e.p. {'on' if ep else 'off'}: value under count = {r['base']}; "
              f"{r['n_races']} distinct race nodes (child, mover); count verdict = mover on {r['count_equals_mover']}")
        print("    single race verdicts whose flip changes the value (child, mover, count verdict, new value):")
        for t in r["critical"]:
            print("      ", t)
        print("    critical races won by the mover, all other races lost by the mover:",
              r["critical_mover_rest_opponent"])
        print("    critical races won by the mover, other races random (200 trials):", r["random_rest"])
        if r["base"] != "*2":
            FAIL.append("4.7 base value is not *2")
    print("FAILURES:", len(FAIL), FAIL)
    sys.exit(1 if FAIL else 0)
