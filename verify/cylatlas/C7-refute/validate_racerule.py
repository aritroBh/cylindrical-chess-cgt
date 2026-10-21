"""Control for the own solver in freeze_indep.py: the pure model (no king
interactions) must give W a2 c2 / B b7 d7 = *2 under the count and mover rules
and 0 under the opponent rule (the KEY FACT).  G = *k iff G + *k is a
second-player win; G = 0 iff G alone is a second-player win.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     .venv/bin/python -I verify/cylatlas/C7-refute/validate_racerule.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from freeze_indep import Geo, place, make_solver
for wrap in (False, True):
    geo = Geo(wrap, -1, 4)       # the proposed FEN's trebuchet: WK f5, BK h4
    for ep in (True, False):
        geo.ep = ep
        W0, B0 = place(0, False)
        for race in ("count", "mover", "opponent"):
            win, st = make_solver(geo, checks_win=False, real_ep=True, race=race)
            res = {h: (win(W0, B0, None, h, True), win(W0, B0, None, h, False)) for h in (0, 1, 2, 3)}
            val = [f"*{h}" if h else "0" for h in res if res[h] == (False, False)]
            print(f"{'cyl8' if wrap else 'flat8'} ep={ep} race={race}: G+*h second-player win for h in {val}; races={st['races']}")
        win, st = make_solver(geo, checks_win=True, real_ep=True)
        res = {h: (win(W0, B0, None, h, True), win(W0, B0, None, h, False)) for h in (0, 1, 2, 3)}
        print(f"   with checks scored as wins: (WhiteFirstWins, BlackFirstWins) by heap {res}")
