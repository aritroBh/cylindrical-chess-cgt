"""Census of the candidate's race nodes: number of a-d pawns (=> men count in the
8x8 embedding = pawns + 4), alternating reachability, count verdict = mover?
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/lemmas/L4.2-critical-races-theory/race_census.py
"""
from collections import Counter
from cylcgt import pawns
from cylcgt.pawns import Board, Pos
from lemmas.common import race_winner, terminal, split_ep
from lemmas.test_L4_races import race_nodes
other = lambda m: "B" if m == "W" else "W"

def alt_race_nodes(b, x):
    out, seen, stack = set(), set(), [(x, "W"), (x, "B")]
    while stack:
        y, tm = stack.pop()
        if (y, tm) in seen:
            continue
        seen.add((y, tm))
        if terminal(b, y) is not None:
            continue
        lpos, rpos = split_ep(y)
        for c in pawns.moves(b, lpos if tm == "W" else rpos, tm):
            t = terminal(b, c)
            if t == 0:
                out.add((c, tm))
            elif t is None:
                stack.append((c, other(tm)))
    return out

for ep in (True, False):
    b = Board(4, 8, False, ep)
    x = Pos.parse("W: a2 c2 / B: b7 d7")
    R = race_nodes(b, x)
    A = alt_race_nodes(b, x)
    men = Counter(len(c.white) + len(c.black) + 4 for c, m in R)
    men_alt = Counter(len(c.white) + len(c.black) + 4 for c, m in A)
    # distinct chess positions: drop ep field (model creates an ep right on every double step)
    chessR = {(c.white, c.black, other(m)) for c, m in R}
    chessA = {(c.white, c.black, other(m)) for c, m in A}
    cm = sum(1 for c, m in R if race_winner(b, c, m, "count") == m)
    print(f"e.p. {'on' if ep else 'off'}: race nodes {len(R)} (distinct ignoring ep field: {len(chessR)}); "
          f"alternating-reachable {len(A)} (distinct ignoring ep: {len(chessA)}); count=mover on {cm}")
    print(f"   men in 8x8 embedding, all race nodes: {dict(sorted(men.items()))}; alternating-reachable: {dict(sorted(men_alt.items()))}")
