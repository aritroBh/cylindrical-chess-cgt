"""T32, covering model: push-only histories for the positions with a zero-shift assignment.

Covering model (the brief's test): the men that are not in the target (the doomed men) are
removed by enemy pieces outside the pawn history, so the pawn history only has to bring the
surviving pawns to their target squares.  If every target pawn of a colour sits on its own
file, each target can be matched to the start pawn on that file (zero file shift, so zero
pawn captures), and a same-file White pawn must end below the Black pawn on that file, the
pawns can reach their targets by pushes alone.

For each such position this script builds the push history (White first, then Black) from the
reduced start (only the surviving pawns on their home squares) and checks it with the
independent replay checker.  Positions with a file shift are reported as not handled here.

PYTHONPATH=. .venv/bin/python -I research/five_file_legal/covering_push.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pawnhist as ph            # noqa: E402
import replay_check as rc       # noqa: E402
from positions import load_positions  # noqa: E402


def push_history(W, B):
    """Return (moves, reduced_start_W, reduced_start_B) or (None, reason)."""
    wf = [f for f, _ in W]
    bf = [f for f, _ in B]
    if len(set(wf)) != len(wf) or len(set(bf)) != len(bf):
        return None, "a file shift is needed (two pawns of one colour on a file)"
    wd = dict(W)
    bd = dict(B)
    for f in set(wd) & set(bd):
        if not wd[f] < bd[f]:
            return None, "same-file White pawn above Black pawn"
    moves = []
    # White pawns: start on rank 2, push up to the target rank
    for f, s in sorted(W, key=lambda q: q[1]):
        r = 2
        if s >= 4:
            moves.append(("double", "W", (f, 2), (f, 4)))
            r = 4
        while r < s:
            moves.append(("push", "W", (f, r), (f, r + 1)))
            r += 1
    # Black pawns: start on rank 7, push down to the target rank
    for f, t in sorted(B, key=lambda q: -q[1]):
        r = 7
        if t <= 5:
            moves.append(("double", "B", (f, 7), (f, 5)))
            r = 5
        while r > t:
            moves.append(("push", "B", (f, r), (f, r - 1)))
            r -= 1
    start_w = frozenset((f, 2) for f in wf)
    start_b = frozenset((f, 7) for f in bf)
    return moves, (start_w, start_b)


def main():
    out = []
    for i, p in enumerate(load_positions(), 1):
        W = frozenset(p["white"])
        B = frozenset(p["black"])
        moves, info = push_history(W, B)
        if moves is None:
            out.append((i, p["position"], "not push-only: " + info, None))
            continue
        start_w, start_b = info
        ok, msg = rc.replay(moves, W, B, start=(start_w, start_b))
        out.append((i, p["position"], "push-only history, replay " + ("OK" if ok else "FAILED: " + msg),
                    " ".join(ph.format_history(moves))))
        print(i, p["position"], "|", "replay", "OK" if ok else "FAILED", "|",
              " ".join(ph.format_history(moves)) if ok else msg, flush=True)
    n_ok = sum(1 for _, _, s, _ in out if s.endswith("OK"))
    print(f"push-only histories verified: {n_ok} of {len(out)}")
    for i, pos, status, hist in out:
        if hist is None:
            print(i, pos, "::", status)


if __name__ == "__main__":
    main()
