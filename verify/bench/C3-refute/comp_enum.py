"""Per-component exhaustive enumeration (verifier C3-refute; own code, imports nothing from the project).

For each library component, enumerate every position reachable by ANY sequence of moves
of either side (as in a sum, where the opponent may move elsewhere), with the game ending
as soon as a passed pawn exists (textbook test). After every double step, record whether
an enemy pawn stands beside the moved pawn (e.p. capture available) and whether the moved
pawn is textbook-passed (then the e.p.-aware test judges the position differently).
Also run with the e.p.-aware terminal rule and compare the reachable sets.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[2] / "bench" / "data"
FILES = "abcdefghijklmnopqrstuvwxyz"


def sq(t):
    return FILES.index(t[0]), int(t[1:])


def parse(text):
    w, b = text.split("/")
    W = frozenset(sq(t) for t in w.split(":")[1].split())
    B = frozenset(sq(t) for t in b.split(":")[1].split())
    return W, B


def adj(f, n, cyl):
    out = []
    for g in (f - 1, f + 1):
        if cyl:
            out.append(g % n)
        elif 0 <= g < n:
            out.append(g)
    return out


def pawn_passed(f, r, white, W, B, n, cyl):
    fs = [f] + adj(f, n, cyl)
    if white:
        return not any((g, s) in B for g in fs for s in range(r + 1, 9))
    return not any((g, s) in W for g in fs for s in range(1, r))


def has_passer(white, W, B, n, cyl, excl=None):
    for (f, r) in (W if white else B):
        if (f, r) == excl:
            continue
        if pawn_passed(f, r, white, W, B, n, cyl):
            return True
    return False


def moves(white, W, B, ep, n, cyl):
    """ep = (f, r, side_that_may_capture) of a pawn that has just double-stepped."""
    me, op = (W, B) if white else (B, W)
    d, home = (1, 2) if white else (-1, 7)
    occ = W | B
    for (f, r) in me:
        t = r + d
        if not 1 <= t <= 8:
            continue
        if (f, t) not in occ:
            yield (f, r), (f, t), None, False
            t2 = r + 2 * d
            if r == home and (f, t2) not in occ:
                yield (f, r), (f, t2), None, True
        for g in adj(f, n, cyl):
            if (g, t) in op:
                yield (f, r), (g, t), (g, t), False
            elif ep and ep[2] == white and ep[0] == g and ep[1] == r and (g, t) not in occ:
                yield (f, r), (g, t), (g, r), False


def enumerate_comp(W0, B0, n, cyl, ep_aware):
    seen = set()
    stack = [(W0, B0, None)]
    stats = {"states": 0, "terminal": 0, "dbl_beside_nonterminal": 0, "dbl_beside_terminal": 0,
             "dbl_beside_passed": 0, "ep_caps": 0}
    terminal_set = set()
    while stack:
        st = stack.pop()
        if st in seen:
            continue
        seen.add(st)
        stats["states"] += 1
        W, B, ep = st
        for white in (True, False):
            for fr, to, cap, dbl in moves(white, W, B, ep, n, cyl):
                me, op = (set(W), set(B)) if white else (set(B), set(W))
                me.discard(fr)
                me.add(to)
                if cap:
                    op.discard(cap)
                    if cap != to:
                        stats["ep_caps"] += 1
                nW, nB = (frozenset(me), frozenset(op)) if white else (frozenset(op), frozenset(me))
                nep, excl, beside = None, None, False
                if dbl:
                    beside = any((g, to[1]) in (nB if white else nW) for g in adj(to[0], n, cyl))
                    if beside:
                        nep = (to[0], to[1], not white)
                        if ep_aware:
                            excl = to
                wp = has_passer(True, nW, nB, n, cyl, excl if white else None)
                bp = has_passer(False, nW, nB, n, cyl, None if white else excl)
                term = wp or bp
                if dbl and beside:
                    stats["dbl_beside_terminal" if term else "dbl_beside_nonterminal"] += 1
                    if pawn_passed(to[0], to[1], white, nW, nB, n, cyl):
                        stats["dbl_beside_passed"] += 1
                if term:
                    terminal_set.add((nW, nB, wp, bp))
                    continue
                stack.append((nW, nB, nep))
    stats["terminal"] = len(terminal_set)
    return stats, seen, terminal_set


def main():
    comps = [json.loads(l) for l in open(DATA / "components.jsonl")]
    agg = {}
    tree_diff = 0
    for c in comps:
        W, B = parse(c["position"])
        n = c["width"]
        st0, seen0, term0 = enumerate_comp(W, B, n, False, False)
        st1, seen1, term1 = enumerate_comp(W, B, n, False, True)
        same = seen0 == seen1 and term0 == term1
        tree_diff += not same
        for k, v in st0.items():
            agg["textbook " + k] = agg.get("textbook " + k, 0) + v
        for k, v in st1.items():
            agg["epaware " + k] = agg.get("epaware " + k, 0) + v
        if st0["dbl_beside_passed"] or st0["dbl_beside_nonterminal"] or not same:
            print("FLAG", c["comp_id"], c["position"], st0, same)
    print(json.dumps({"components": len(comps), "reachable_tree_differs": tree_diff, "totals": agg}, indent=1))


if __name__ == "__main__":
    main()
