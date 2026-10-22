"""Independent checker for pawn-only histories (T32).

Written separately from the bitboard search in pawnhist.py: it uses Python sets of
(file, rank) squares and its own move rules.  Used two ways:
  * replay(history, target_w, target_b): validate a history move by move from the
    standard start and check it ends on the target;
  * reachable_states(start_w, start_b): brute-force forward BFS with the set-based
    generator, to cross-check pawnhist's move generator on small starts.
"""
from __future__ import annotations

from collections import deque


def _start(files=range(8)):
    W = frozenset((f, 2) for f in files)
    B = frozenset((f, 7) for f in files)
    return W, B


def legal_moves(W, B, last):
    """Set-based generator.  last = (side, kind, frm, to) of the previous move or None."""
    occ = set(W) | set(B)
    out = []
    for (f, r) in W:
        # forward one
        if r + 1 <= 7 and (f, r + 1) not in occ:
            out.append(("push", "W", (f, r), (f, r + 1)))
            # forward two from the home rank
            if r == 2 and (f, 3) not in occ and (f, 4) not in occ:
                out.append(("double", "W", (f, r), (f, 4)))
        # diagonal captures of enemy pawns
        if r + 1 <= 7:
            for g in (f - 1, f + 1):
                if 0 <= g <= 7 and (g, r + 1) in B:
                    out.append(("capture", "W", (f, r), (g, r + 1)))
        # en passant: previous move was a black double step passing next to us
        if last is not None and last[0] == "B" and last[1] == "double" and r == 5:
            bto = last[3]                       # black double step ended here
            if bto[1] == 5 and abs(bto[0] - f) == 1:
                out.append(("ep", "W", (f, r), (bto[0], 6)))
    for (f, r) in B:
        if r - 1 >= 2 and (f, r - 1) not in occ:
            out.append(("push", "B", (f, r), (f, r - 1)))
            if r == 7 and (f, 6) not in occ and (f, 5) not in occ:
                out.append(("double", "B", (f, r), (f, 5)))
        if r - 1 >= 2:
            for g in (f - 1, f + 1):
                if 0 <= g <= 7 and (g, r - 1) in W:
                    out.append(("capture", "B", (f, r), (g, r - 1)))
        if last is not None and last[0] == "W" and last[1] == "double" and r == 4:
            bfrm, bto = last[2], last[3]
            if bto[1] == 4 and abs(bto[0] - f) == 1:
                out.append(("ep", "B", (f, r), (bto[0], 3)))
    return out


def apply_move(W, B, mv):
    kind, side, frm, to = mv
    W, B = set(W), set(B)
    mover = W if side == "W" else B
    other = B if side == "W" else W
    mover.discard(frm)
    if kind == "ep":
        other.discard((to[0], frm[1]))
    elif kind == "capture":
        other.discard(to)
    mover.add(to)
    return frozenset(W), frozenset(B), (side, kind, frm, to)


def replay(history, target_w, target_b, start=None):
    """Validate `history` (list of (kind, side, from, to)) from the start position.

    Each move is checked against the explicit rules: the mover stands on `from`; a push
    needs an empty square ahead and no promotion; a double step needs two empty squares
    from the home rank; a capture needs an enemy pawn on the diagonal square; an e.p.
    capture needs the enemy pawn to have just double-stepped beside it.
    Returns (ok, message).
    """
    if start is None:
        W, B = _start()
    else:
        W, B = start
    last = None
    for i, (kind, side, frm, to) in enumerate(history):
        mover = W if side == "W" else B
        other = B if side == "W" else W
        d = 1 if side == "W" else -1
        f, r = frm
        tf, tr = to
        if frm not in mover:
            return False, f"move {i}: no {side} pawn on {frm}"
        if tr < 2 or tr > 7:
            return False, f"move {i}: pawn would leave ranks 2..7 ({to})"
        if kind == "push":
            if tf != f or tr != r + d or to in mover or to in other:
                return False, f"move {i}: illegal push {frm}->{to}"
        elif kind == "double":
            home = 2 if side == "W" else 7
            mid = (f, r + d)
            if r != home or tf != f or tr != r + 2 * d or mid in mover or mid in other or to in mover or to in other:
                return False, f"move {i}: illegal double step {frm}->{to}"
        elif kind == "capture":
            if abs(tf - f) != 1 or tr != r + d or to not in other:
                return False, f"move {i}: illegal capture {frm}x{to}"
        elif kind == "ep":
            if last is None or last[0] == side or last[1] != "double":
                return False, f"move {i}: e.p. not right after a double step"
            (lside, _, lfrm, lto) = last
            if lto != (tf, r) or abs(tf - f) != 1 or tr != r + d or to in mover or to in other:
                return False, f"move {i}: illegal e.p. {frm}x{to}"
            if (tf, r) not in other:
                return False, f"move {i}: e.p. victim missing"
        else:
            return False, f"move {i}: unknown kind {kind}"
        W, B, last = apply_move(W, B, (kind, side, frm, to))
        last = (side, kind, frm, to)
    if W != frozenset(target_w) or B != frozenset(target_b):
        return False, "final position differs from target"
    return True, f"valid, {len(history)} moves"


def reachable_states(start_w, start_b, cap=5_000_000):
    """Brute-force forward BFS with the set-based generator.  Returns the set of states."""
    s0 = (frozenset(start_w), frozenset(start_b), None)
    seen = {s0}
    dq = deque([s0])
    while dq:
        W, B, last = dq.popleft()
        for mv in legal_moves(W, B, last):
            W2, B2, l2 = apply_move(W, B, mv)
            st = (W2, B2, l2)
            if st not in seen:
                seen.add(st)
                if len(seen) > cap:
                    raise RuntimeError("cap")
                dq.append(st)
    return {(W, B) for (W, B, _) in seen}
