#!/usr/bin/env python3
"""T27 step 4b: where does the e.p.-aware test (e.p. on) first differ from e.p. off, inside the
*2 gadget W a2 c2 / B b7 d7 (4 files, count rule)?  Finds the minimal differing positions: positions
whose value differs between the two settings although every child of the position has equal value
(so the difference is caused by that position's own passed-pawn test).

Run (project root): PYTHONPATH=. .venv/bin/python research/star27_textbook3/why_aware.py
"""
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos, moves, passed, value

pawns.RACE_RULE = "count"


def setting(ep_on, aware):
    pawns.PASSED_RESPECTS_EP = aware
    pawns._value.cache_clear()
    return Board(4, 8, False, ep_on)


def reachable(board, root):
    seen, stack = {root}, [root]
    while stack:
        p = stack.pop()
        if passed(board, p, "W") or passed(board, p, "B"):
            continue
        for side in ("W", "B"):
            for q in moves(board, p, side):
                q0 = Pos(q.white, q.black, None)  # plain position (e.p. right irrelevant to the key)
                if q0 not in seen:
                    seen.add(q0)
                    stack.append(q0)
    return seen


root = Pos.parse("W: a2 c2 / B: b7 d7")
B_off = setting(False, False)
plain = reachable(B_off, root)
vals = {}
for name, ep_on, aware in (("off", False, False), ("on/aware", True, True), ("on/textbook", True, False)):
    b = setting(ep_on, aware)
    vals[name] = {p: cgt.show(value(b, p)) for p in plain
                  if not (passed(b, p, "W") or passed(b, p, "B"))}
diff = [p for p in plain if p in vals["off"] and vals["off"][p] != vals["on/aware"].get(p)]
print(f"positions reachable (e.p. ignored): {len(plain)}; non-terminal: {len(vals['off'])}")
print(f"positions whose value differs, e.p. off vs on/aware: {len(diff)}")
print(f"positions whose value differs, e.p. off vs on/textbook: "
      f"{sum(vals['off'][p] != vals['on/textbook'][p] for p in vals['off'])}")
print()
# "local" differences: the position has a Left or Right option (a double step next to an enemy pawn)
# that is a new passed-pawn case.  Report positions with a single move that creates the divergence.
b_aw = setting(True, True)
for p in sorted(diff, key=lambda q: (len(str(q)), str(q)))[:12]:
    kids = []
    for side in ("W", "B"):
        for q in moves(b_aw, p, side):
            if q.ep is not None:
                kids.append((side, q))
    print(f"{p}:  off={vals['off'][p]}   on/aware={vals['on/aware'][p]}   "
          f"double steps with an e.p. right: {[(s, str(q)) for s, q in kids]}")

print()
print("Smallest illustration: White to move in W: a2 c2 / B: b4 d4, double step a2-a4 beside the b4 pawn.")
for name, ep_on, aware in (("e.p. off", False, False), ("e.p. on, textbook test", True, False),
                           ("e.p. on, e.p.-aware test", True, True)):
    b = setting(ep_on, aware)
    p0 = Pos.parse("W: a2 c2 / B: b4 d4")
    child = [q for q in moves(b, p0, "W") if (0, 4) in q.white][0]
    print(f"  {name:26s}: after a2-a4  passed(W a4)={passed(b, child, 'W')}   "
          f"value of whole position = {cgt.show(value(b, p0))}")
