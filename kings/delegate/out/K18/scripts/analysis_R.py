#!/usr/bin/env python3
"""for a plain-game win (variant P or Q): T, the set R of squares the White king can occupy in lines where sbar plays
optimal (n-decreasing) moves, and the (L3_F) test (s always has a Z-pawn move or a king move onto F_Z)."""
import sys
sys.path.insert(0, "scripts")
import kit
lg2 = kit.lg2
def analyse(Qstr, qclause, passing=False):
    root = lg2.parse(Qstr)
    n, nodes, val = lg2.solve(root, passing, qclause, full=True)
    if n >= lg2.INF: return None
    R = set(); l3f = True; seen = set(); stack = [root]
    while stack:
        st = stack.pop()
        if st in seen: continue
        seen.add(st)
        ty, d = nodes[st]
        Wp, Bp, wk, bk, stm, ep = st
        R.add(wk)
        if ty == "A":
            for o in d:
                if o[0] == "win": continue
                if val[o[1]] == val[st] - 1: stack.append(o[1])
        else:
            if d == "mated": continue
            # (L3_F): a Z-pawn move or a king move onto F_Z must exist at this s-turn
            ok = False
            for ns, kd, frm, to in lg2.moves(st, "w", False):
                if frm in Wp and kd != "promo": ok = True           # Z-pawn move (non-promotion)
                if frm == wk and to[0] in lg2.FZFILES: ok = True      # king move onto F_Z
            if not ok: l3f = False
            for o in d: stack.append(o)
    return n, R, l3f
if __name__ == "__main__":
    kit.setboard(sys.argv[1], sys.argv[2])
    for line in sys.stdin:
        r = analyse(line.strip(), qclause=False)
        print(line.strip(), r if r is None else (r[0], sorted(kit.sqn(s) for s in r[1]), r[2]))
