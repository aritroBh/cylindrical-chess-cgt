"""Hypothesis probe (NOT a proof): frozen-king game FG2 in which a promotion wins at once UNLESS the opponent can promote
on his very next move (then the result is a draw: two queens appear). Compared with the exact real-king results."""
import json, sys, collections
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms")
import pawngame as pg
R = "/Users/aritro/Downloads/Research/Chessendgames/kings/results/"
G = pg.Game(2, 6, True, 3)
memo = {}


def val(pos, side):
    """+1 White wins, 0 draw, -1 Black wins"""
    key = (pos, side)
    if key in memo: return memo[key]
    mv = G.moves(pos, side)
    if not mv:
        r = -1 if side == "W" else 1
    else:
        best = None
        for lab, p, promo in mv:
            if promo:
                opp = "B" if side == "W" else "W"
                if any(pr for _, _, pr in G.moves((p[0], p[1], None), opp)):
                    v = 0
                else:
                    v = 1 if side == "W" else -1
            else:
                v = val(p, "B" if side == "W" else "W")
            if best is None or (v > best if side == "W" else v < best):
                best = v
        r = best
    memo[key] = r
    return r


rows = [json.loads(l) for l in open(R + "exp_cyl7x6_epon_Q_conv.jsonl")]
sym = {1: "W", 0: "D", -1: "L"}
c = collections.Counter()
for r in rows:
    if not r["exact"]: continue
    pos = G.parse(r["P"])
    real = (r["real"]["wtm"][0], r["real"]["btm"][0])
    fz = (r["frozen"]["wtm"][0], r["frozen"]["btm"][0])
    f2 = (sym[val(pos, "W")], sym[val(pos, "B")])
    c["exact rows"] += 1
    c["FG matches real"] += fz == real
    c["FG2 matches real"] += f2 == real
    if fz != real:
        c["rows FG!=real"] += 1
        c["  of which FG2==real"] += f2 == real
    else:
        c["rows FG==real"] += 1
        c["  of which FG2 breaks it"] += f2 != real
print(dict(c))
