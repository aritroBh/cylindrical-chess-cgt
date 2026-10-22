"""T33 item 6: can the two positions arise in a game from pawns on ranks 2 and 7?

Breadth-first search over legal pawn-only moves (single and double steps, diagonal captures, en passant,
cylinder wrap), starting from the full ranks-2-and-7 setting, with no promotion. A pawn count below the
target's is pruned (pawns are never created, so captures cannot be undone). Two variants:
  unrestricted: any legal history (real chess);
  model: positions in which a side already has a passed pawn (under the e.p.-aware test) are not expanded,
         since the CGT model ends the game there.
Prints a reachability verdict, a shortest history with its capture list, and the number of states searched.

Run: PYTHONPATH=. .venv/bin/python research/c3_star2/reach.py
"""
import sys
from collections import deque
from cylcgt import pawns


def label(parent, child, mover):
    """Chess-like label of the move taking parent to child (mover = side that moved)."""
    own_p, own_c = (parent.white, child.white) if mover == "W" else (parent.black, child.black)
    op_p, op_c = (parent.black, child.black) if mover == "W" else (parent.white, child.white)
    moved_from = sorted(own_p - own_c)[0]
    moved_to = sorted(own_c - own_p)[0]
    captured = sorted(op_p - op_c)
    sep = "x" if captured else "-"
    s = f"{mover}:{pawns.name(moved_from)}{sep}{pawns.name(moved_to)}"
    if captured:
        s += f"({pawns.name(captured[0])})"
    return s


def legal_child(board, child, mover):
    # no promotion: a pawn may not reach the last rank, and no pawn may be on rank 8 (W) or 1 (B)
    for f, r in child.white:
        if r == board.ranks:
            return False
    for f, r in child.black:
        if r == 1:
            return False
    return True


def search(files, start, target, prune_passed=False, cap=5_000_000):
    board = pawns.Board(files, 8, True, True)
    tw, tb = target.white, target.black
    tcount = len(tw) + len(tb)
    key0 = (start.white, start.black, start.ep, "W")
    parent = {key0: None}
    queue = deque([key0])
    hits = []
    while queue:
        key = queue.popleft()
        w, b, ep, side = key
        pos = pawns.Pos(w, b, ep)
        if (w, b) == (tw, tb):
            hits.append(key)
            continue
        if len(parent) > cap:
            raise RuntimeError("cap reached")
        if prune_passed and (pawns.passed(board, pos, "W") or pawns.passed(board, pos, "B")):
            continue
        for child in pawns.moves(board, pos, side):
            if not legal_child(board, child, side):
                continue
            if len(child.white) + len(child.black) < tcount:
                continue
            nxt = "B" if side == "W" else "W"
            ck = (child.white, child.black, child.ep, nxt)
            if ck in parent:
                continue
            parent[ck] = (key, label(pos, child, side))
            queue.append(ck)
    return parent, hits


def path_to(parent, key):
    moves = []
    while parent[key] is not None:
        prev, lab = parent[key]
        moves.append(lab)
        key = prev
    return list(reversed(moves))


def run(files, start_text, target_text, prune_passed):
    start = pawns.Pos.parse(start_text)
    target = pawns.Pos.parse(target_text)
    parent, hits = search(files, start, target, prune_passed)
    name = "model (no expansion past a passed pawn)" if prune_passed else "unrestricted"
    print(f"C{files} target {target_text} | {name}: states searched {len(parent)}, "
          f"target reached: {'YES' if hits else 'NO'}")
    if hits:
        best = min(hits, key=lambda k: len(path_to(parent, k)))
        p = path_to(parent, best)
        caps = [m for m in p if "x" in m]
        print(f"  shortest history ({len(p)} plies): " + " ".join(p))
        print(f"  captures in that history: {caps}")
        print(f"  number of target keys reached: {len(hits)}")
    return bool(hits)


if __name__ == "__main__":
    print("== start: ranks 2 and 7 full (C3: 6 pawns; C4: 8 pawns)")
    run(3, "W: a2 b2 c2 / B: a7 b7 c7", "W: a2 a3 b2 / B: b7 c6 c7", False)
    run(3, "W: a2 b2 c2 / B: a7 b7 c7", "W: a2 a3 b2 / B: b7 c6 c7", True)
    run(4, "W: a2 b2 c2 d2 / B: a7 b7 c7 d7", "W: a4 b2 c2 / B: b6 c5 d6 d7", False)
    run(4, "W: a2 b2 c2 d2 / B: a7 b7 c7 d7", "W: a4 b2 c2 / B: b6 c5 d6 d7", True)
