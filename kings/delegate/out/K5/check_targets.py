import os, sys, time, json
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
import cylcgt.pawns as P
import cylcgt.cgt as C
import canon
from fractions import Fraction

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
OUT = os.path.join(ROOT, "kings/delegate/out/K5")
canon.BIG_DISPLAY = P.BIG // 2


def convert(g):
    if getattr(g, "num", None) is not None:
        return canon.number(g.num)
    if getattr(g, "nim", None) is not None:
        return canon.nimber(g.nim)
    L = [convert(x) for x in g.L]
    R = [convert(x) for x in g.R]
    return canon.make(L, R)


TARGETS = [
    (1, 8, 8, False, "W: a2 a3 b2 / B: a6 b5 b6"),
    (2, 8, 8, False, "W: a2 b2 b3 / B: a5 a6 b6"),
    (3, 8, 8, False, "W: a2 b4 c4 / B: a7 b7 d6"),
    (4, 8, 8, False, "W: a2 b2 c3 / B: b5 b6 c7"),
    (5, 8, 8, False, "W: a2 b2 d4 / B: a7 c6 d7"),
    (6, 8, 8, False, "W: a2 b2 b6 / B: a6 b7 c5"),
    (7, 8, 8, False, "W: a2 b2 b6 / B: a6 b7 c6"),
    (8, 8, 8, False, "W: a2 c2 / B: b7 d7"),
    (9, 3, 8, True,  "W: a2 a3 b2 / B: b7 c6 c7"),
]


def claim(t, ep, race):
    if t in (1, 2):
        return canon.number(Fraction(1, 8))
    if t == 3:
        if ep == "aware" and race == "count":
            return canon.number(Fraction(1, 8))
        return None
    if t == 4:
        if ep == "aware" and race == "count":
            return canon.number(Fraction(1, 16))
        return None
    if t == 5:
        if ep == "aware" and race == "count":
            return canon.make([canon.ZERO], [canon.down_star()])
        return None
    if t == 6:
        return canon.make([canon.ZERO, canon.STAR], [canon.DOWN])
    if t == 7:
        if ep == "aware" and race == "count":
            return canon.make([canon.ZERO], [canon.make([canon.ZERO], [canon.integer(-1)])])
        return None
    if t == 8:
        if ep in ("off", "textbook"):
            if race in ("count", "mover"):
                return canon.nimber(2)
            if race == "opponent":
                return canon.ZERO
        if ep == "aware" and race == "count":
            left = canon.make([canon.integer(3)], [canon.integer(1)])
            right = canon.make([canon.integer(-1)], [canon.integer(-3)])
            return canon.make([left], [right])
        return None
    if t == 9:
        if ep == "aware" and race == "count":
            return canon.nimber(2)
        return None
    return None


def main():
    rows = []
    tsv_path = os.path.join(OUT, "targets.tsv")
    with open(tsv_path, "w") as f:
        f.write("target\tsetting\tV_own\tequals_V_cyl\tequals_claim\tseconds\n")
    for (tnum, files, ranks, wrap, pos_str) in TARGETS:
        for ep_treat in ("off", "textbook", "aware"):
            for race in ("count", "mover", "opponent"):
                setting_name = f"{ep_treat}/{race}"
                P.RACE_RULE = race
                P.PASSED_RESPECTS_EP = (ep_treat != "textbook")
                ep_flag = (ep_treat != "off")
                board = P.Board(files, ranks, wrap, ep_flag)
                pos = P.Pos.parse(pos_str)
                P._value.cache_clear()
                canon.clear_caches()
                canon.clear_pawn_caches()
                t0 = time.time()
                v_own = None
                v_cyl = None
                own_err = None
                cyl_err = None
                try:
                    v_own = canon.pawn_value(board, pos)
                except Exception as e:
                    own_err = f"{type(e).__name__}: {e}"
                try:
                    cg = P.value(board, pos)
                    v_cyl = convert(cg)
                except P.RaceError as e:
                    cyl_err = "RaceError"
                except Exception as e:
                    cyl_err = f"{type(e).__name__}: {e}"
                dt = time.time() - t0

                if own_err is not None:
                    own_str = f"ERROR {own_err}"
                    eq_cyl = "no"
                else:
                    own_str = canon.show(v_own)
                    if cyl_err is not None:
                        eq_cyl = "RaceError" if cyl_err == "RaceError" else "no"
                    else:
                        eq_cyl = "yes" if (v_own is v_cyl) else "no"
                if cyl_err is not None:
                    cyl_str = cyl_err
                else:
                    cyl_str = canon.show(v_cyl)

                cl = claim(tnum, ep_treat, race)
                if cl is None:
                    eq_claim = "no claim"
                else:
                    if own_err is not None:
                        eq_claim = "no"
                    else:
                        eq_claim = "yes" if (v_own is cl) else "no"

                row = (tnum, setting_name, own_str, eq_cyl, eq_claim, f"{dt:.2f}")
                rows.append(row)
                with open(tsv_path, "a") as f:
                    f.write("\t".join(str(x) for x in row) + "\n")
                print(f"T{tnum} {setting_name}: own={own_str} cyl={cyl_str} eq_cyl={eq_cyl} eq_claim={eq_claim} t={dt:.2f}", flush=True)

    with open(os.path.join(OUT, "rows.json"), "w") as f:
        json.dump([list(r) for r in rows], f, indent=2)


if __name__ == "__main__":
    main()
