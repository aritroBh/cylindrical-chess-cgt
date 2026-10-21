"""Quick test of the claim's untested aside: on a 9-file cylinder the 4-file *2
fits beside a trebuchet with an empty buffer file on each side.
Trebuchet pawns on file 7, kings on files 6 and 8; component on files o..o+3.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     .venv/bin/python -I verify/cylatlas/C7-refute/cyl9_check.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import freeze_indep as F
F.N = 9
F.X = 7
F.FL = "abcdefghi"
for o in (0, 1, 2):
    for mirror in (False, True):
        ok = 0
        for s in (1, -1):
            for r in range(2, 7):
                geo = F.Geo(True, s, r)
                W0, B0 = F.place(o, mirror)
                dist, notes = F.reach(geo, W0, B0)
                bad = any(F.interactions(geo, n[0], n[1]) for n in dist)
                ok += not bad
        print(f"9-file cylinder, component on files {o}..{o+3}, mirror={mirror}: {ok}/10 trebuchet placements pass")
