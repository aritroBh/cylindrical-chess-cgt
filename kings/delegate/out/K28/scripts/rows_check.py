"""rows_check.py : with kchess.py (move generator written from SPEC.md; agrees with kpsolve's move lists, see cmp_moves.py) check
  (1) the five deviations: from the Z_B roots, the named move gives exactly the child position of the brief's table;
  (2) the reductions: row 1 child --Kxc3--> F_c3, row 2 child --Kxa4--> F_a4, and which side moves in each row;
  (3) the 26-move census at the roots is not needed here; only the 5 rows are checked."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import kchess
def kids(p): return dict(kchess.children(p))
rows = [
 (1, "Kb2 Pa3 Pb4 ka4 pb3 pc4 b -", "Pc4c3", "Kb2 Pa3 Pb4 ka4 pb3 pc3 w -"),
 (2, "Kc3 Pa3 Pb4 kb5 pb3 pc4 w -", "Pa3a4", "Kc3 Pa4 Pb4 kb5 pb3 pc4 b -"),
 (3, "Kc3 Pa3 Pb4 ka4 pb3 pc4 w -", "Kc3c4",  "Kc4 Pa3 Pb4 ka4 pb3 b -"),
 (4, "Kc3 Pa3 Pb4 ka4 pb3 pc4 b -", "Ka4a3",  "Kc3 Pb4 ka3 pb3 pc4 w -"),
 (5, "Kc3 Pa3 Pb4 kb5 pb3 pc4 w -", "Kc3d2",  "Kd2 Pa3 Pb4 kb5 pb3 pc4 b -"),
]
ok = True
for n, root, mv, want in rows:
    root = kchess.canon(root); want = kchess.canon(want)
    k = kids(root)
    got = k.get(mv)
    mover = 'White' if root.split()[-2] == 'w' else 'Black'
    print(f"row {n}: root {root} ({mover} to move) move {mv} -> {got}  {'OK' if got == want else 'MISMATCH, want ' + want}")
    ok &= (got == want)
red = [
 (1, "Kb2 Pa3 Pb4 ka4 pb3 pc3 w -", "Kb2c3", "Kc3 Pa3 Pb4 ka4 pb3 b -"),
 (2, "Kc3 Pa4 Pb4 kb5 pb3 pc4 b -", "Kb5a4", "Kc3 Pb4 ka4 pb3 pc4 w -"),
]
for n, pos, mv, want in red:
    pos = kchess.canon(pos); want = kchess.canon(want)
    got = kids(pos).get(mv)
    print(f"reduction row {n}: {pos} --{mv}--> {got}  {'OK' if got == want else 'MISMATCH, want ' + want}")
    ok &= (got == want)
print("ALL OK" if ok else "PROBLEM")
