"""Feed identical random race-verdict assignments to the worker's W_override
(cylcgt.cgt canonical forms) and to the independent CGT-free solver, and
compare the resulting values. Also count pawns.race_hits for the candidate."""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_check as ic
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas.test_L4_races import W_override

NAME = {"*2": "*2", "↑": "up", "↓": "down", "0": "0", "*": "*"}
root_ic = ic.parse("W: a2 c2 / B: b7 d7")
x = Pos.parse("W: a2 c2 / B: b7 d7")
for ep, mode in ((True, "always"), (False, "off")):
    b = Board(4, 8, False, ep)
    races, _ = ic.race_nodes(root_ic, mode)
    order = sorted(races, key=lambda k: (ic.show(k[0]), k[1]))
    rng = random.Random(12345)
    agree = disagree = 0
    for t in range(60):
        p = rng.random()
        ov_ic = {k: ("W" if rng.random() < p else "B") for k in order}
        ov_w = {(Pos(c[0], c[1], c[2]), m): v for (c, m), v in ov_ic.items()}
        v1 = cgt.show(W_override(b, x, "count", ov_w, {}))
        v2 = ic.value_name(ic.make_solver(mode, ov_ic), root_ic)
        if NAME.get(v1, "other") == v2: agree += 1
        else:
            disagree += 1; print("DISAGREE", ep, t, v1, v2)
    print(f"ep={ep}: {agree} agree, {disagree} disagree over 60 random full assignments")
    pawns.RACE_RULE = "count"; pawns._value.cache_clear(); pawns.race_hits.clear()
    print("   pawns.value =", cgt.show(pawns.value(b, x)), "race_hits =", len(pawns.race_hits),
          "distinct =", len(set(pawns.race_hits)))
