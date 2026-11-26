"""K75: positions for one group of in/groups48.txt beside every context of at most n + n pawns on one context file.
(Adapted from kings/delegate/out/K72/src/gen.py: same position order, same context enumeration; groups read from
in/groups48.txt instead of a fixed table.)

Usage (repository root):
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K75/src/gen.py G F NN   -> in/G_F_NN.pos, .names
     G group name, F context file letter (must be a context file of G), NN = 11, 22 or 33 (at most n + n pawns)
  ... gen.py G F NN split   the same contexts in two problems separated by a blank line (both solvers clear their
     tables there): first every context with no White pawn above a Black pawn, then the others.  Pawns on one file
     never pass each other, so the two problems reach about two thirds of the configurations each (used where one
     problem would pass 2 GB).
All contexts of one run form ONE problem (no blank lines), so a solver solves the union of their configurations once.
Positions per context, in this order (8 lines):  A b, A w, B b, B w, qA b, qA w, qB b, qB w
A = root with the first Black king square, B = the second; qA, qB = after White's freeze at A, at B.  No group of the
48 has an e.p. right at a q (no Black pawn beside a double-stepped freezing pawn; checked in groups.py), and context
pawns stand two or more files from every group pawn.  Contexts: every placement of at most n White and n Black pawns
on ranks 2-7 of the file (K63's enumeration: White pawns first, then Black, each by increasing rank).
"""
import itertools, sys

V = "kings/delegate/out/K75"

def load():
    G = {}
    for l in open(f"{V}/in/groups48.txt"):
        if l.startswith("#"): continue
        r = l.rstrip("\n").split("|")
        G[r[0]] = dict(men=int(r[1]), cls=r[2], WK=r[3], kA=r[4], kB=r[5], wp=r[6].split(","), bp=r[7].split(","),
                       fA=r[8], fB=r[9], epA=r[10], epB=r[11], FZ=r[12], ctx=r[13])
    return G

def positions(g, ctx):
    out = []
    for bk in (g["kA"], g["kB"]):
        pcs = [f"K{g['WK']}", f"k{bk}"] + [f"P{s}" for s in g["wp"]] + [f"p{s}" for s in g["bp"]] + ctx
        out += [" ".join(pcs) + " b -", " ".join(pcs) + " w -"]
    for bk, fz, ep in ((g["kA"], g["fA"], g["epA"]), (g["kB"], g["fB"], g["epB"])):
        wp = sorted([fz[2:]] + [s for s in g["wp"] if s != fz[:2]])
        assert len(wp) == len(g["wp"])
        pcs = [f"K{g['WK']}", f"k{bk}"] + [f"P{s}" for s in wp] + [f"p{s}" for s in g["bp"]] + ctx
        out += [" ".join(pcs) + f" b {ep}", " ".join(pcs) + " w -"]
    return out

def contexts(n):
    sq = range(2, 8)
    for nw in range(n + 1):
        for ws in itertools.combinations(sq, nw):
            rest = [r for r in sq if r not in ws]
            for nb in range(n + 1):
                for bs in itertools.combinations(rest, nb):
                    yield ws, bs

def ctxname(f, ws, bs):
    return " ".join([f"P{f}{r}" for r in ws] + [f"p{f}{r}" for r in bs]) or "empty"

if __name__ == "__main__":
    G = load()
    gn, f, nn = sys.argv[1], sys.argv[2], sys.argv[3]
    n = int(nn) // 11
    g = G[gn]
    assert f in g["ctx"], (gn, f, g["ctx"])
    split = len(sys.argv) > 4 and sys.argv[4] == "split"
    cl = list(contexts(n))
    if split:
        above = lambda ws, bs: bool(ws) and bool(bs) and max(ws) > min(bs)
        cl = [c for c in cl if not above(*c)] + [c for c in cl if above(*c)]
        nfirst = sum(1 for c in cl if not above(*c))
    names = []
    with open(f"{V}/in/{gn}_{f}_{nn}.pos", "w") as fh:
        for i, (ws, bs) in enumerate(cl):
            if split and i == nfirst: fh.write("\n")
            ctx = [f"P{f}{r}" for r in ws] + [f"p{f}{r}" for r in bs]
            fh.write("\n".join(positions(g, ctx)) + "\n")
            names.append(ctxname(f, ws, bs))
    open(f"{V}/in/{gn}_{f}_{nn}.names", "w").write("\n".join(names) + "\n")
    print(len(names), "contexts", file=sys.stderr)
