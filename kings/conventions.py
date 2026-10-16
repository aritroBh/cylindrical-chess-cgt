"""Re-score experiment files under both passed-pawn conventions of the pawn model.

  textbook: cylcgt as it is in the main checkout (a pawn is passed if no enemy
            pawn can stop it, ignoring a pending e.p. capture)
  ep-aware: a pawn that can still be taken en passant is not yet passed
            (the convention on the main session's ep-aware-passed branch; this is
            our own reimplementation, done by wrapping cylcgt.pawns.passed at
            run time; cylcgt itself is not edited)

Usage (from the project root):
  python3 kings/conventions.py kings/results/exp_cyl6x6_epon_Q.jsonl [...]
Writes <file>_conv.jsonl (each row gains convention_<rule>, predicted_<rule>,
verdict_<rule>) and prints the tallies per rule.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from cylcgt import cgt, pawns  # noqa: E402
from kings.experiment import PREDICT, layout  # noqa: E402

TEXTBOOK = pawns.passed


def passed_ep_aware(board, pos, side):
    """Like cylcgt's passed(), but a pawn the opponent may capture e.p. right now
    does not count as passed."""
    mine, theirs = (pos.white, pos.black) if side == "W" else (pos.black, pos.white)
    victim = pos.ep[1] if (pos.ep and pos.ep[2] != side) else None
    for f, r in mine:
        if (f, r) == victim:
            continue
        files = {f} | {g for g in (board.nb(f, -1), board.nb(f, 1)) if g is not None}
        if side == "W":
            blocked = any(g in files and s > r for g, s in theirs)
        else:
            blocked = any(g in files and s < r for g, s in theirs)
        if not blocked:
            return True
    return False


def set_rule(rule):
    pawns.passed = TEXTBOOK if rule == "textbook" else passed_ep_aware
    pawns._value.cache_clear()


def sq(t):
    return "abcdefgh".index(t[0]), int(t[1:])


def value_of(row_P, pfiles, H, ep):
    w = [sq(t) for t in row_P.split("/")[0].split(":")[1].split()]
    b = [sq(t) for t in row_P.split("/")[1].split(":")[1].split()]
    off = pfiles[0]
    board = pawns.Board(len(pfiles), H, False, ep)
    pos = pawns.Pos(frozenset((f - off, r) for f, r in w), frozenset((f - off, r) for f, r in b))
    try:
        g = pawns.value(board, pos)
    except pawns.RaceError:
        return None, "race"
    return cgt.show(g), cgt.outcome(g)


def main():
    for path in sys.argv[1:]:
        summary = json.load(open(path.replace(".jsonl", "_summary.json")))
        kind, size = summary["board"].split(":")
        W, H = map(int, size.split("x"))
        _, pfiles = layout(kind, W, H)
        ep = summary["ep"] == "on"
        rows = [json.loads(l) for l in open(path)]
        tallies = {}
        for rule in ("textbook", "ep-aware"):
            set_rule(rule)
            t = Counter()
            for row in rows:
                val, outc = value_of(row["P"], pfiles, H, ep)
                row[f"convention_{rule}"] = {"value": val, "outcome": outc}
                rw, rb = row["real"]["wtm"], row["real"]["btm"]
                if outc == "race":
                    v = "race-at-start"
                elif not (rw[0] == rw[1] and rb[0] == rb[1]):
                    v = "undetermined"
                else:
                    pred = PREDICT[outc]
                    row[f"predicted_{rule}"] = pred
                    v = "match" if (rw[0], rb[0]) == pred else "MISMATCH"
                row[f"verdict_{rule}"] = v
                t[v] += 1
            tallies[rule] = dict(t)
        set_rule("textbook")
        changed = [r["P"] for r in rows if r["verdict_textbook"] != r["verdict_ep-aware"]]
        with open(path.replace(".jsonl", "_conv.jsonl"), "w") as fh:
            for row in rows:
                fh.write(json.dumps(row) + "\n")
        print(json.dumps({"file": path, "tallies": tallies, "verdict_changes": changed}, indent=1))


if __name__ == "__main__":
    main()
