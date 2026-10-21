"""Part 3 of the independent C7 check: add king captures to the G' + *2 test.

Extended model (own code, imports only freeze_indep.py from this folder):
  * a component pawn move that gives check wins for the checker;
  * the side to move may also capture, with its king, an adjacent enemy
    component pawn that no enemy pawn protects.  The king thereby leaves the
    trebuchet and the enemy king takes its g-pawn, so the capture loses for
    the capturer unless the capture leaves the capturer a passed pawn; that
    race is scored with `race_cap` = "capturer" (capturer wins, the most
    favourable case for captures) or "opponent".
G' = *2 iff G' + *2 is a second-player win.

Run:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python -I verify/cylatlas/C7-refute/part3_captures.py
"""
import json
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from freeze_indep import Geo, gen, passed, place, race_count, nm  # noqa: E402


def solver(geo, race_cap, real_ep=True):
    st = {"cap_moves": 0, "cap_races": 0}

    def king_caps(W, B, white):
        k = geo.wk if white else geo.bk
        prey = B if white else W
        guards = (B | {geo.tb}) if white else (W | {geo.tw})
        other_k = geo.bk if white else geo.wk
        out = []
        for p in prey:
            if p not in geo.katt(k):
                continue
            if any(p in geo.patt(q, not white) for q in guards):
                continue
            if p in geo.katt(other_k):
                continue
            out.append(p)
        return out

    @lru_cache(maxsize=None)
    def win(W, B, ep, heap, wtm):
        anym = False
        for W2, B2, e2 in gen(geo, W, B, ep, wtm):
            anym = True
            wp, bp = passed(geo, W2, B2, True), passed(geo, W2, B2, False)
            chk = any(geo.bk in geo.patt(p, True) for p in W2) if wtm else \
                any(geo.wk in geo.patt(p, False) for p in B2)
            mine = (wp if wtm else bp) or chk
            opp = bp if wtm else wp
            if mine and opp:
                w = race_count(geo, W2, B2, wtm) if not chk else wtm
                if w == wtm:
                    return True
                continue
            if mine:
                return True
            if opp:
                continue
            if not win(W2, B2, e2, heap, not wtm):
                return True
        for h2 in range(heap):
            anym = True
            if not win(W, B, None if real_ep else ep, h2, not wtm):
                return True
        for p in king_caps(W, B, wtm):
            anym = True
            st["cap_moves"] += 1
            W2, B2 = (W, B - {p}) if wtm else (W - {p}, B)
            if passed(geo, W2, B2, wtm):
                st["cap_races"] += 1
                if race_cap == "capturer":
                    return True
        return False if anym else False
    return win, st


rows = []
for wrap in (False, True):
    for o in (0, 1):
        for mirror in (False, True):
            for s in (1, -1):
                for r in range(2, 7):
                    geo = Geo(wrap, s, r)
                    W0, B0 = place(o, mirror)
                    row = dict(board="cyl8" if wrap else "flat8", o=o, mirror=mirror, s=s, r=r,
                               wk=nm(geo.wk), bk=nm(geo.bk))
                    for rc in ("capturer", "opponent"):
                        for re_ in (True, False):
                            win, st = solver(geo, rc, re_)
                            res = {h: (win(W0, B0, None, h, True), win(W0, B0, None, h, False)) for h in (0, 1, 2)}
                            row[f"{rc}_{'realep' if re_ else 'modelep'}"] = dict(
                                g0=res[0], g_star=res[1], g_star2=res[2], star2=res[2] == (False, False),
                                fuzzy=res[0] == (True, True), **st)
                    rows.append(row)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "part3_captures.jsonl"), "w") as fh:
    for x in rows:
        fh.write(json.dumps(x) + "\n")
for b in ("flat8", "cyl8"):
    sub = [x for x in rows if x["board"] == b]
    for k in ("capturer_realep", "capturer_modelep", "opponent_realep", "opponent_modelep"):
        good = [x for x in sub if x[k]["star2"]]
        print(f"{b} {k}: G'=*2 in {len(good)}/{len(sub)}; capture races seen in "
              f"{sum(1 for x in sub if x[k]['cap_races'])} placements")
    for x in sub:
        if x["capturer_realep"]["star2"]:
            print(f"   {b} still *2 (checks win, captures w/ races to capturer): o={x['o']} mirror={x['mirror']} "
                  f"s={x['s']:+d} r={x['r']} WK {x['wk']} BK {x['bk']}")
