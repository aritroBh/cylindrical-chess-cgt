#!/usr/bin/env python3
"""K15 confirmation harness.

  gen   : build kpsolve input (group + small context, both sides to move) and the D-model predictions
  cmp   : compare kpsolve output with the predictions

D-model prediction: G (+) Z_D with Z_D in {dud, over, under, on, off, zero}; G is a set of context pawns
(pushes and double steps only; contexts are chosen so that no pawn ever attacks another, so no captures and no
e.p.).  A promotion is a decisive event: win for the promoter (model P).  A side with no move loses (normal play).
Infinite play is a draw.  Results are from White's point of view.
"""
import sys, json, itertools

FILES = "abcdefgh"


def sq(s):
    return (FILES.index(s[0]), int(s[1:]))


def name(f, r):
    return f"{FILES[f]}{r}"


# ---- D-model solver -------------------------------------------------------------------------------------------
ZSTR = {
    # name -> {state: (left_options, right_options)}
    "dud": {"w": (["w"], ["w"])},
    "on": {"w": (["w"], [])},
    "off": {"w": ([], ["w"])},
    "over": {"w": (["0"], ["w"]), "0": ([], [])},
    "under": {"w": (["w"], ["0"]), "0": ([], [])},
    "zero": {"w": ([], [])},
}


def pawn_moves(H, wp, bp, side):
    """list of (new_wp, new_bp, promotes) for the context game (pushes and double steps only)."""
    occ = set(wp) | set(bp)
    mine = wp if side == "W" else bp
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else H - 1
    last = H if side == "W" else 1
    out = []
    for (f, r) in mine:
        r1 = r + d
        if (f, r1) in occ:
            continue
        if r1 == last:
            out.append((None, None, True))
            continue
        for (t, dbl) in [((f, r1), False)] + ([((f, r + 2 * d), True)] if r == start and (f, r + 2 * d) not in occ else []):
            nm = (mine - {(f, r)}) | {t}
            out.append((nm, None, False) if side == "W" else (None, nm, False))
    return out


def solve_d(H, wp, bp, zname):
    """returns (value with White to move, value with Black to move), values in {'W','D','L'}."""
    Z = ZSTR[zname]
    start = (frozenset(wp), frozenset(bp), "w")
    # explore reachable states (g, z, stm)
    states = {}
    stack = [(start[0], start[1], "w", "W")]
    # state = (wp, bp, z, stm)
    def moves(st):
        wpp, bpp, z, stm = st
        side = stm
        res = []  # (next_state or 'WIN')
        for (nw, nb, prom) in pawn_moves(H, wpp, bpp, side):
            if prom:
                res.append("WIN")
            else:
                res.append((nw if nw is not None else wpp, nb if nb is not None else bpp, z, "B" if stm == "W" else "W"))
        lo, ro = Z[z]
        for z2 in (lo if side == "W" else ro):
            res.append((wpp, bpp, z2, "B" if stm == "W" else "W"))
        return res

    init = [(frozenset(wp), frozenset(bp), "w", "W"), (frozenset(wp), frozenset(bp), "w", "B")]
    seen = {}
    todo = list(init)
    while todo:
        s = todo.pop()
        if s in seen:
            continue
        seen[s] = moves(s)
        for m in seen[s]:
            if m != "WIN" and m not in seen:
                todo.append(m)
    val = {s: 0 for s in seen}  # 0 unknown(draw), 1 win for mover, 2 loss for mover
    changed = True
    while changed:
        changed = False
        for s, ms in seen.items():
            if val[s]:
                continue
            if any(m == "WIN" or val[m] == 2 for m in ms):
                val[s] = 1
                changed = True
            elif all(m != "WIN" and val[m] == 1 for m in ms):  # includes no moves: loss
                val[s] = 2
                changed = True

    def pov(s):
        v = val[s]
        if v == 0:
            return "D"
        win_for_mover = v == 1
        mover_white = s[3] == "W"
        return "W" if win_for_mover == mover_white else "L"

    return pov(init[0]), pov(init[1])


# ---- contexts -------------------------------------------------------------------------------------------------
def contexts(board):
    W, H = board
    if W == 8:
        return {
            "C0_empty": ([], []),
            "C1_blocked_f3f4": (["f3"], ["f4"]),
            "C2_onemove_f3f5": (["f3"], ["f5"]),
            "C3_gap2_f2f5": (["f2"], ["f5"]),
            "C4_race_e2_g5": (["e2"], ["g5"]),
            "C5_two_onemoves_e3e5_g2g4": (["e3", "g2"], ["e5", "g4"]),
        }
    else:  # 7 files, group on a-c, buffer d and g, context e,f (adjacent: same-file pairs only)
        return {
            "C0_empty": ([], []),
            "C1_blocked_e3e4": (["e3"], ["e4"]),
            "C2_onemove_e3e5": (["e3"], ["e5"]),
            "C3_gap2_e2e5": (["e2"], ["e5"]),
        }


def parse_group(pos):
    toks = pos.split()
    # drop trailing 'w -'
    toks = [t for t in toks if t[0] in "KkPp" and len(t) >= 3]
    return toks


def cmd_gen(args):
    # args: board(8x6) candfile outprefix zname
    bd, candfile, outp = args[0], args[1], args[2]
    W, H = map(int, bd.split("x"))
    ctxs = contexts((W, H))
    rows = []
    lines = []
    for ln in open(candfile):
        ln = ln.rstrip("\n")
        if not ln or ln.startswith("#"):
            continue
        cls, pos, zname = ln.split("\t")[:3]
        toks = parse_group(pos)
        for cname, (cw, cb) in ctxs.items():
            wp = [sq(t[1:]) for t in toks if t[0] == "P"]
            bp = [sq(t[1:]) for t in toks if t[0] == "p"]
            cwp = [sq(x) for x in cw]
            cbp = [sq(x) for x in cb]
            pred_w, pred_b = solve_d(H, cwp, cbp, zname)
            ctoks = [f"P{x}" for x in cw] + [f"p{x}" for x in cb]
            for stm, pred in (("w", pred_w), ("b", pred_b)):
                p = " ".join(toks + ctoks) + f" {stm} -"
                lines.append(p)
                rows.append({"cls": cls, "group": " ".join(toks), "ctx": cname, "stm": stm, "pos": p, "z": zname, "pred": pred})
    open(outp + ".in", "w").write("\n".join(lines) + "\n")
    json.dump(rows, open(outp + ".rows.json", "w"))
    print(len(rows), "positions written to", outp + ".in")


ORD = {"L": 0, "D": 1, "W": 2}


def cmd_cmp(args):
    outp, kpout = args[0], args[1]
    rows = json.load(open(outp + ".rows.json"))
    res = [l.rstrip("\n") for l in open(kpout) if l.strip() and not l.startswith("#")]
    assert len(res) == len(rows), (len(res), len(rows))
    summ = {}
    table = []
    for r, l in zip(rows, res):
        pos, ab = l.split(" | ")
        A, B = ab.split()
        assert pos.strip() == r["pos"], (pos, r["pos"])
        if A == B:
            status = "agree" if A == r["pred"] else "DISAGREE"
        else:
            status = "inexact-consistent" if ORD[B] <= ORD[r["pred"]] <= ORD[A] else "inexact-DISAGREE"
        r.update({"A": A, "B": B, "status": status})
        key = (r["cls"], r["ctx"])
        summ.setdefault(r["cls"], {}).setdefault(status, 0)
        summ[r["cls"]][status] += 1
        table.append(r)
    json.dump(table, open(outp + ".table.json", "w"), indent=0)
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    {"gen": cmd_gen, "cmp": cmd_cmp}[sys.argv[1]](sys.argv[2:])
