"""w+b<=5: cylinder-only (non-W) sets under all six settings (independent model only),
intersections over race rules for fixed e.p., and over all six.
  cd verify/cylatlas/C4-refute && ../../../.venv/bin/python analyze_le5_all6.py
"""
import json
only = {}
for e in (1, 0):
    for r in ("count", "mover", "opponent"):
        d = json.load(open(f"out/le5_{r}_ep{e}.json"))
        F = set(d["flat_single"]) | set(d["flat_pair"])
        R = d["ring"]
        only[(r, e)] = {k: R[k] for k in R if k not in F and not R[k][2]}
        print(f"{r}/ep{'on' if e else 'off'}: cylinder-only non-W = {len(only[(r, e)])}")
for lab, keys in (("e.p. on, 3 rules", [(r, 1) for r in ("count", "mover", "opponent")]),
                  ("e.p. off, 3 rules", [(r, 0) for r in ("count", "mover", "opponent")]),
                  ("all six", list(only))):
    I = set.intersection(*(set(only[k]) for k in keys))
    print(f"\nunder all of [{lab}]: {len(I)}")
    for k in sorted(I):
        print("   ", only[keys[0]][k][3], "|", only[keys[0]][k][0])
