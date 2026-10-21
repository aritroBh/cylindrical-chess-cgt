import sys; sys.path.insert(0, sys.argv[1])
from indep_tree import parse, make_solver, outcome, tree_check
for w, t in ((4, "W: a2 c2 / B: b7 d7"), (3, "W: a2 c2 / B: a3 b5"), (3, "W: a2 c2 / B: a3 b6"), (2, "W: a6 b3 / B: a7 c7".replace("c7","b7"))):
    root = parse(t)
    row = []
    for aware in (False, True):
        for rule in ("count", "mover", "opponent"):
            for ep in (True, False):
                a, tm = make_solver(w, ep, aware, rule)
                row.append(f"{'aw' if aware else 'tb'}/{rule[:3]}/{'on' if ep else 'off'}={outcome(tm(root,'W'), tm(root,'B'))}")
    print(w, t, "tree identical:", tree_check(w, root)[0]); print("   ", " ".join(row))
