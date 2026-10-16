"""Where does the S/W disagreement of the headline position actually arise in
ALTERNATING play?  (indep.py only.)

Before any component gets a passer, S-play and W-play visit the same pawn
positions (S's frozen integer N stays 0, W has not ended). So enumerate the
non-terminal positions reachable from X by alternating play (either side
first), each with its side to move, and list those where
    s_win(pos, tomove) != w_win(pos, tomove)
and every non-terminal child (one move later) agrees: the 'frontier' nodes,
which are where the two models genuinely diverge.

Also: is the worker's illustrative node W: b5 d4 g3 / B: c6 f6 g4 h6
reachable by alternating play, and with which side to move?
"""
import indep as I
from indep import Bd, parse, fmt, comps, gen, has_passer, s_win, w_win

X = "W: b2 d4 g3 h5 / B: a7 c7 f7 g4"
RULE = "count"
B = Bd(8, 8, True, False)


def term(w, k):
    return has_passer(B, w, k, "W") or has_passer(B, w, k, "B")


def threats(w, k, memo={}):
    key = (w, k)
    if key in memo:
        return memo[key]
    out = set()
    if has_passer(B, w, k, "W"):
        out.add("+")
    if has_passer(B, w, k, "B"):
        out.add("-")
    if not out:
        for side in "WB":
            for w2, k2, _ in gen(B, w, k, side, None):
                out |= threats(w2, k2)
    memo[key] = frozenset(out)
    return memo[key]


w0, k0 = parse(X)
states = set()
stack = [(w0, k0, "W"), (w0, k0, "B")]
while stack:
    st = stack.pop()
    if st in states:
        continue
    states.add(st)
    w, k, t = st
    o = "B" if t == "W" else "W"
    for w2, k2, _ in gen(B, w, k, t, None):
        if not term(w2, k2):
            stack.append((w2, k2, o))

dis = {}
for (w, k, t) in states:
    sv = s_win(B, w, k, frozenset(), 0, t, RULE)
    wv = w_win(B, w, k, None, t, RULE)
    if sv != wv:
        dis[(w, k, t)] = (sv, wv)
print(f"alternating-reachable non-terminal (pos, side-to-move) states: {len(states)}; "
      f"S/W disagree on {len(dis)}")

front = []
for (w, k, t), (sv, wv) in dis.items():
    o = "B" if t == "W" else "W"
    kids = [(w2, k2) for w2, k2, _ in gen(B, w, k, t, None) if not term(w2, k2)]
    if all((w2, k2, o) not in dis for w2, k2 in kids):
        front.append((w, k, t, sv, wv))
print(f"frontier disagreement states (all non-terminal children agree): {len(front)}")
n_multi = sum(1 for f in front if len(comps(B, f[0], f[1])) >= 2)
print(f"  of which with >= 2 components: {n_multi}")
for w, k, t, sv, wv in sorted(front, key=lambda f: -len(f[0] | f[1]))[:8]:
    cs = comps(B, w, k)
    parts = []
    for cf in cs:
        zw = frozenset(p for p in w if p[0] in cf)
        zk = frozenset(p for p in k if p[0] in cf)
        parts.append(f"[{fmt(zw, zk)} threats {''.join(sorted(threats(zw, zk)))}]")
    print(f"  {fmt(w, k)} {t} to move: S says mover {'wins' if sv else 'loses'}, "
          f"W says mover {'wins' if wv else 'loses'}; components: {' '.join(parts)}")

Y = parse("W: b5 d4 g3 / B: c6 f6 g4 h6")
for t in "WB":
    print(f"worker's node W: b5 d4 g3 / B: c6 f6 g4 h6 with {t} to move alternating-reachable: "
          f"{(Y[0], Y[1], t) in states}")
