"""Mechanism check (indep2 only): at the claimed mechanism node, with Left to
move, W says Left wins and S says Left loses. For every Left move that wins in
W, follow S's game form: show Right's winning reply in S and the frozen
integer k, then continue the line with both sides playing S-winning moves
(the side that wins in S picks a winning move; the loser picks its first move).

Run from the project root:
  .venv/bin/python -I verify/lemmas/L2.2-sum_safe-counterexample-refute/run2/pv.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep2 as I  # noqa: E402

B = I.Board(8, 8, True, False)
RULE = "count"
ab = I.make_S(B, RULE)
wwin = I.make_W(B, RULE)


def s_wins(w, k, eps, n, side):
    a, b = ab(w, k, eps)
    left_wins = (n >= a) if side == "W" else (n >= b)
    return left_wins if side == "W" else not left_wins


def options(w, k, eps, n, side):
    out = []
    if side == "W" and n >= 1:
        out.append(("tempo", w, k, eps, n - 1))
    if side == "B" and n <= -1:
        out.append(("tempo", w, k, eps, n + 1))
    for w2, k2, e2, dl in I.s_children(B, w, k, eps, side, RULE, False):
        tag = "freeze %+d" % dl if dl else "move"
        out.append((tag, w2, k2, e2, n + dl))
    return out


w0, k0 = I.parse("W: b5 d4 g3 / B: c6 f6 g4 h6")
print("node", I.fmt(w0, k0), "W says Left-to-move wins:", wwin(w0, k0, None, "W"),
      "| S says Left-to-move wins:", s_wins(w0, k0, frozenset(), 0, "W"))
for w1, k1, _ in I.gen(B, w0, k0, "W", None):
    pw, pb = I.has_passer(B, w1, k1, "W"), I.has_passer(B, w1, k1, "B")
    if pw or pb:
        wres = (I.race_winner(B, w1, k1, "W", RULE) == "W") if (pw and pb) else pw
    else:
        wres = not wwin(w1, k1, None, "B")
    if not wres:
        continue
    print(f"\nLeft's W-winning move -> {I.fmt(w1, k1)}  (passers W={pw} B={pb})")
    # now replay in S
    if pw or pb:
        dl = I.BIG if ((pw and pb and I.race_winner(B, w1, k1, 'W', RULE) == 'W') or (pw and not pb)) else -I.BIG
        # component containing the move freezes; recompute live state via s_children
    state = None
    for tag, w2, k2, e2, n2 in options(w0, k0, frozenset(), 0, "W"):
        if tag != "tempo" and (w2 | {p for p in w1 if p not in w2}) and True:
            pass
    # pick the S child that corresponds to this move: the one whose live pawns are a subset of (w1,k1)
    cands = [o for o in options(w0, k0, frozenset(), 0, "W")
             if o[0] != "tempo" and o[1] <= w1 and o[2] <= k1 and
             (o[0] == "move") == (not (pw or pb))]
    tag, w, k, eps, n = cands[0]
    side = "B"
    line = [f"W:{tag} k={n}"]
    for ply in range(60):
        opts = options(w, k, eps, n, side)
        if not opts:
            line.append(f"{side} has no move -> {side} loses")
            break
        other = "B" if side == "W" else "W"
        win = [o for o in opts if not s_wins(o[1], o[2], o[3], o[4], other)]
        tag, w, k, eps, n = (win or opts)[0]
        line.append(f"{side}:{tag} k={n} [{I.fmt(w, k) if (w or k) else 'no live pawns'}]")
        side = other
    print("   S line (k = frozen integer):")
    for s in line:
        print("     ", s)
