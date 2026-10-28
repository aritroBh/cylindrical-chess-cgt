#!/usr/bin/env python3
"""finite pass budget version of lg2.solve (independent of lg.cpp): s may pass at most k times (k = -1: unlimited).
usage: lg2k.py BOARD FZ < lines "<Q position> | k qclause"   -> prints n"""
import sys
sys.path.insert(0, "scripts")
import kit
lg2 = kit.lg2
INF = lg2.INF
def solve_k(root, k, qclause):
    start = (root, k)
    nodes = {}; stack = [start]
    while stack:
        key = stack.pop()
        if key in nodes: continue
        st, kk = key
        Wp, Bp, wk, bk, stm, ep = st
        if stm == "b":
            opts = []
            for ns, kd, frm, to in lg2.moves(st, "b", True):
                if kd == "promo":
                    if not qclause: opts.append(("win",))
                    else:
                        bp2 = Bp - {frm}
                        cap = (to in lg2.king_nbrs(wk)) and (to not in lg2.king_nbrs(bk)) and not lg2.pawn_attacks_square("b", bp2, to)
                        if not cap: opts.append(("win",))
                else:
                    opts.append(("succ", (ns, kk))); stack.append((ns, kk))
            nodes[key] = ("A", opts)
        else:
            ms = lg2.moves(st, "w", False); chk = lg2.pawn_attacks_square("b", Bp, wk)
            if not ms and chk: nodes[key] = ("B", "mated"); continue
            promo = any(kd == "promo" for ns, kd, frm, to in ms)
            opts = [(ns, kk) for ns, kd, frm, to in ms if kd != "promo"]
            if (kk != 0) and not chk:
                opts.append(((Wp, Bp, wk, bk, "b", None), kk if kk < 0 else kk - 1))
            for o in opts: stack.append(o)
            nodes[key] = ("B", "promo" if promo else opts)
    val = {k_: INF for k_ in nodes}
    for k_, (ty, d) in nodes.items():
        if ty == "B" and d == "mated": val[k_] = 0
    ch = True
    while ch:
        ch = False
        for k_, (ty, d) in nodes.items():
            if ty == "A":
                best = INF
                for o in d:
                    if o[0] == "win": best = min(best, 1)
                    elif val[o[1]] < INF: best = min(best, val[o[1]] + 1)
                nv = best
            elif d == "mated": nv = 0
            elif d == "promo": nv = INF
            elif not d: nv = INF
            else: nv = max(val[o] for o in d)
            if nv != val[k_]: val[k_] = nv; ch = True
    return val[start]
if __name__ == "__main__":
    kit.setboard(sys.argv[1], sys.argv[2])
    for line in sys.stdin:
        pos, rest = line.rstrip("\n").split(" | "); k, q = map(int, rest.split())
        v = solve_k(lg2.parse(pos), k, bool(q))
        print(f"{pos} | k={k} q={q} n={'inf' if v >= INF else v}", flush=True)
