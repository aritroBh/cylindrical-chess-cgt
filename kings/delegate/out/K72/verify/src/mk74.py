"""K74 referee: inputs for p74 (own enumeration of the K72 contexts), and the D-sum prediction.

Usage (repository root):
  python3 -I kings/delegate/out/K72/verify/src/mk74.py pos G F N   > positions (8 lines per context, in context order)
  python3 -I kings/delegate/out/K72/verify/src/mk74.py pred N      > prediction per context pattern (file-free)
G: group name, F: context file letter, N: 1 (at most 1 + 1 pawns) or 2 (at most 2 + 2).
Positions per context: A b, A w, B b, B w, qA b, qA w, qB b, qB w (A, B = the two Black king squares of the root;
qA, qB = after White's freeze there).  Contexts: White pawn ranks (increasing), then Black pawn ranks (increasing),
on ranks 2-7, pairwise distinct; named "Ph2 ph3" etc.
"""
import itertools, sys
from functools import lru_cache

# White king, Black king squares (A, B), White pawns, Black pawns, freeze at A (from, to), freeze at B (from, to)
# (LOOPY.md Corollary 4.17, K65 paragraph; freezes as in K72 findings section 1, checked with p74 -m)
G = {
    "C125_05": ("d4", ("b4", "b5"), ["b6", "c2", "c5"], ["b7", "c6"], ("c2", "c4"), ("c2", "c3")),
    "C125_08": ("e5", ("c5", "c6"), ["b2", "b6", "f6"], ["b7", "f7"], ("b2", "b3"), ("b2", "b4")),
    "C125_10": ("c5", ("e5", "e6"), ["b6", "f2", "f6"], ["b7", "f7"], ("f2", "f3"), ("f2", "f4")),
    "C145_07": ("g4", ("e4", "e5"), ["e6", "f2", "f5"], ["e7", "f6"], ("f2", "f4"), ("f2", "f3")),
    "C145_09": ("d4", ("f4", "f5"), ["e2", "e5", "f6"], ["e6", "f7"], ("e2", "e4"), ("e2", "e3")),
}


def contexts(n):
    """n = 1, 2: at most n + n pawns; n = 6: every context; n = 9: the extension 3 + 0, 0 + 3, 3 + 1, 1 + 3"""
    if n == 9:
        return [c for c in contexts(3) if max(len(c[0]), len(c[1])) == 3 and len(c[0]) + len(c[1]) <= 4]
    out = []
    for nw in range(n + 1):
        for ws in itertools.combinations(range(2, 8), nw):
            for nb in range(n + 1):
                for bs in itertools.combinations([r for r in range(2, 8) if r not in ws], nb):
                    out.append((ws, bs))
    return out


def name(f, ws, bs):
    return " ".join([f"P{f}{r}" for r in ws] + [f"p{f}{r}" for r in bs]) or "empty"


def positions(g, f, ws, bs):
    K, (ka, kb), wp, bp, fa, fb = G[g]
    ctx = [f"P{f}{r}" for r in ws] + [f"p{f}{r}" for r in bs]
    res = []
    roots = []
    for k in (ka, kb):
        s = " ".join([f"K{K}", f"k{k}"] + [f"P{x}" for x in wp] + [f"p{x}" for x in bp] + ctx)
        roots += [s + " b -", s + " w -"]
    qs = []
    for k, (a, b) in ((ka, fa), (kb, fb)):
        wq = [b if x == a else x for x in wp]
        s = " ".join([f"K{K}", f"k{k}"] + [f"P{x}" for x in wq] + [f"p{x}" for x in bp] + ctx)
        qs += [s + " b -", s + " w -"]
    return roots + qs


# ---- prediction: X = D-game of pawns on one file (pushes and double steps, promotion a terminal win, a side with no
# move loses, Definition 1.3).  omega: Black may pass (omega -> omega), White may freeze once (omega -> 0).
@lru_cache(maxsize=None)
def r(ws, bs, om, s):
    """result (W/L) of (omega if om else 0) + X, s to move ('w'/'b'); X short, so no draws."""
    occ = set(ws) | set(bs)
    opts = []
    if s == "w":
        if om:
            opts.append(("pos", ws, bs, False))
        for p in ws:
            if p + 1 not in occ:
                if p + 1 == 8:
                    return "W"
                opts.append(("pos", tuple(sorted(set(ws) - {p} | {p + 1})), bs, om))
                if p == 2 and 4 not in occ:
                    opts.append(("pos", tuple(sorted(set(ws) - {p} | {4})), bs, om))
        if not opts:
            return "L"
        return "W" if any(r(o[1], o[2], o[3], "b") == "W" for o in opts) else "L"
    else:
        if om:
            opts.append(("pos", ws, bs, True))
        for p in bs:
            if p - 1 not in occ:
                if p - 1 == 1:
                    return "L"
                opts.append(("pos", ws, tuple(sorted(set(bs) - {p} | {p - 1})), om))
                if p == 7 and 5 not in occ:
                    opts.append(("pos", ws, tuple(sorted(set(bs) - {p} | {5})), om))
        if not opts:
            return "W"
        return "L" if any(r(o[1], o[2], o[3], "w") == "L" for o in opts) else "W"


def pred(ws, bs):
    ws, bs = tuple(ws), tuple(bs)
    root = [r(ws, bs, True, "b"), r(ws, bs, True, "w")]
    q = [r(ws, bs, False, "b"), r(ws, bs, False, "w")]
    return root + root + q + q          # A b, A w, B b, B w, qA b, qA w, qB b, qB w


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    if sys.argv[1] == "pos":
        g, f, n = sys.argv[2], sys.argv[3], int(sys.argv[4])
        for ws, bs in contexts(n):
            print("\n".join(positions(g, f, ws, bs)))
    elif sys.argv[1] == "pred":
        for ws, bs in contexts(int(sys.argv[2])):
            print(f"{name('h', ws, bs):22s} " + " ".join(pred(ws, bs)))
