"""List the distinct race nodes (both sides have a passer after a move) reachable in the game
tree of W a2 c2 / B b7 d7 (4 files, flat), and compare the 'count' verdict with 'mover'.
Uses cylcgt's own move generator / passer test (read-only import)."""
from collections import Counter
from cylcgt import pawns

POS = "W: a2 c2 / B: b7 d7"
for ep in (False, True):
    b = pawns.Board(4, 8, False, ep)
    start = pawns.Pos.parse(POS)
    seen, stack, races = set(), [start], {}
    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        wp, bp = pawns.passed(b, p, "W"), pawns.passed(b, p, "B")
        if wp or bp:
            continue
        plain = pawns.Pos(p.white, p.black, None)
        for side in ("W", "B"):
            src = plain if (p.ep and p.ep[2] != side) else p
            for c in pawns.moves(b, src, side):
                cw, cb = pawns.passed(b, c, "W"), pawns.passed(b, c, "B")
                if cw and cb:
                    other = "B" if side == "W" else "W"
                    dm = pawns.promote_distance(b, c, side)
                    do = pawns.promote_distance(b, c, other)
                    win = other if do <= dm else side
                    races[(str(c), side)] = (dm, do, win)
                elif not (cw or cb):
                    stack.append(c)
                    # also the e.p.-cleared variant is reached when the other side moves elsewhere
                    if c.ep:
                        stack.append(pawns.Pos(c.white, c.black, None))
    cnt = Counter("mover" if v[2] == k[1] else "opponent" for k, v in races.items())
    print(f"ep={ep}: distinct (race position, mover) pairs = {len(races)}; count verdict: {dict(cnt)}")
    dist = Counter((v[0], v[1]) for v in races.values())
    print("   (mover distance, opponent distance) histogram:", dict(sorted(dist.items())))
