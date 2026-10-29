"""Score the three draw treatments against the collected draws."""
import json, os
ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
syspath = os.path.join(ROOT)
import sys; sys.path.insert(0, syspath)
from cylcgt import pawns, cgt
from cylcgt.pawns import Pos, Board

board = Board(4, 8, False, True)
draws = json.load(open("draws.json"))

def outcome_of_component(comp):
    comp = comp.split("(")[0].strip()
    pos = Pos.parse(comp)
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()
    try:
        v = pawns.value(board, pos)
        return cgt.outcome(v), cgt.show(v)
    except Exception as e:
        return "ERR", str(e)

# real nodes
nodes = []
for n in draws["real_nodes"]:
    oc, sh = outcome_of_component(n["component"])
    nodes.append((n["component"], oc, sh, n["real_class"]))

# suite roots
suite = []
for x in draws["suite_draw_roots"]:
    oc, sh = outcome_of_component(x["component"])
    suite.append((x["id"], oc, sh))

# terminals: model value is a passer (BIG); represent as N (first-player win) in model
terminals = [("W: a4 / B: b7 c6", "N"), ("W: a5 / B: b7 c5", "N"), ("W: c4 / B: a6 d6", "N")]

# king moves: all components 0 (P) per computation
king = []
for r in draws["proven_king_moves"]:
    oc, sh = outcome_of_component(r["component"])
    king.append((r["component"], oc, sh))

def reproducibility(oc):
    # A treatment reproduces a real draw iff the resulting game is a draw (dud)
    # under that treatment. At component level:
    # (i) as 0: never a draw (0 is P, not D)
    # (ii) as dud: only when the pawn value is P (0), so 0+dud = dud (draw)
    # (iii) as {on|off}: never a draw ({on|off} is N)
    return {
        "draw_as_0": 0,
        "draw_as_dud": 1 if oc == "P" else 0,
        "draw_as_onoff": 0,
    }

totals = {k: 0 for k in ["draw_as_0", "draw_as_dud", "draw_as_onoff"]}
counts = {k: 0 for k in totals}
groups = {
    "real_nodes (13)": [(oc,) for (_, oc, _, _) in nodes],
    "terminals (3)": [(oc,) for (_, oc) in terminals],
    "king_moves (6)": [(oc,) for (_, oc, _) in king],
    "suite_roots (17)": [(oc,) for (_, oc, _) in suite],
}
# For terminals, pawn model outcome is N (passer) but real draw; treat as P? 
# Terminals are passers: model says first-player win (N). Under dud treatment terminal becomes dud -> draw.
for name, ocs in groups.items():
    pass

# Count manually per group
def count_group(items_outcomes):
    c = {k: 0 for k in totals}
    n = 0
    for oc in items_outcomes:
        oc = oc[0]
        n += 1
        # terminals: force reproducibility for dud
        r = reproducibility(oc)
        # terminals are passers -> model N; dud treatment still makes the terminal dud -> draw
        if oc == "N" and name_startswith_terminals:
            r["draw_as_dud"] = 1
        for k in totals:
            c[k] += r[k]
    return c, n

# We'll just compute with explicit handling:
summary = {}
# real nodes
c = {k:0 for k in totals}; n=0
for (_, oc, _, _) in nodes:
    n+=1
    r = reproducibility(oc)
    for k in totals: c[k]+=r[k]
summary["real_nodes"] = (c, n)

# terminals: all dud-reproducible
c = {k:0 for k in totals}; n=0
for (_, oc) in terminals:
    n+=1
    c["draw_as_0"] += 0
    c["draw_as_dud"] += 1
    c["draw_as_onoff"] += 0
summary["terminals"] = (c, n)

# king moves
c = {k:0 for k in totals}; n=0
for (_, oc, _) in king:
    n+=1
    r = reproducibility(oc)
    for k in totals: c[k]+=r[k]
summary["king_moves"] = (c, n)

# suite roots
c = {k:0 for k in totals}; n=0
for (_, oc, _) in suite:
    n+=1
    r = reproducibility(oc)
    for k in totals: c[k]+=r[k]
summary["suite_roots"] = (c, n)

grand = {k:0 for k in totals}; grandn=0
for (c,n) in summary.values():
    grandn += n
    for k in totals: grand[k]+=c[k]

print("group               n   as_0  as_dud  as_onoff")
for name,(c,n) in summary.items():
    print(f"{name:18s} {n:3d}  {c['draw_as_0']:3d}   {c['draw_as_dud']:3d}     {c['draw_as_onoff']:3d}")
print(f"{'TOTAL':18s} {grandn:3d}  {grand['draw_as_0']:3d}   {grand['draw_as_dud']:3d}     {grand['draw_as_onoff']:3d}")

with open("score_summary.json","w") as f:
    json.dump({"summary":{k:(v[0],v[1]) for k,v in summary.items()},
               "grand":(grand,grandn)}, f, indent=2)