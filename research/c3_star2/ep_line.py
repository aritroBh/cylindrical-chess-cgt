"""Find the shortest line (<= 5 plies, e.p. on) that reaches the e.p. capture c5xb6 which changes the C3 root value."""
from collections import deque
from cylcgt import pawns
from research.c3_star2.reach import label
B = pawns.Board(3, 8, True, True)
root = pawns.Pos.parse("W: a2 a3 b2 / B: b7 c6 c7")
key0 = (root.white, root.black, root.ep, "W")
par = {key0: None}
q = deque([(key0, 0)])
targets = []
while q:
    key, d = q.popleft()
    w, b, ep, side = key
    pos = pawns.Pos(w, b, ep)
    if d == 5:
        continue
    for ch in pawns.moves(B, pos, side):
        other = "B" if side == "W" else "W"
        ck = (ch.white, ch.black, ch.ep, other)
        if ck in par:
            continue
        par[ck] = (key, label(pos, ch, side))
        q.append((ck, d + 1))
# the two e.p. positions found by ep_diff at ply 5
want = [pawns.Pos.parse("W: a2 a3 c5 / B: b5 c7"), pawns.Pos.parse("W: a2 b2 c5 / B: b5 c7")]
for wp in want:
    for k in par:
        if (k[0], k[1]) == (wp.white, wp.black) and k[2] is not None and k[2][2] == "W":
            path = []
            cur = k
            while par[cur] is not None:
                prev, lab = par[cur]
                path.append(lab)
                cur = prev
            print(str(wp), "reached via", " ".join(reversed(path)), "then W c5xb6 e.p.")
            break
