"""K72: the five chess-exact over groups (K65/K66) and their contexts on one separated file.

Usage (repository root):
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K72/src/gen.py alone        -> in/alone.pos
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K72/src/gen.py ctx G F N    -> in/G_F_N.pos
     G group name, F context file letter, N = 11 (at most 1 + 1 pawns) or 22 (at most 2 + 2)
     All contexts of one run form ONE problem (no blank or # lines between them), so each solver solves the union of
     their configurations once; the context names, in input order, go to in/G_F_N.names (8 input lines each).

Positions per context, in this order (8 lines):
  A b, A w, B b, B w, qA b, qA w, qB b, qB w
A = root with the first Black king square, B = the second; qA, qB = after White's freeze at A, at B (K66 table 4).
No e.p. square is written at the q's: the freezing pawn's neighbours hold no Black pawn, and the context pawns stand
two or more files away, so no e.p. capture exists.  Contexts: every placement of at most n White and n Black pawns
on ranks 2-7 of the file (K63's enumeration: White pawns first, then Black, each by increasing rank).
"""
import itertools, sys

V = "kings/delegate/out/K72"
# name: (White king, other White pawns, Black pawns, (kA, freeze-A pawn after), (kB, freeze-B pawn after), freezing pawn)
GROUPS = {
    "C125_05": ("d4", ["b6", "c5"], ["b7", "c6"], ("b4", "c4"), ("b5", "c3"), "c2"),
    "C125_08": ("e5", ["b6", "f6"], ["b7", "f7"], ("c5", "b3"), ("c6", "b4"), "b2"),
    "C125_10": ("c5", ["b6", "f6"], ["b7", "f7"], ("e5", "f3"), ("e6", "f4"), "f2"),
    "C145_07": ("g4", ["e6", "f5"], ["e7", "f6"], ("e4", "f4"), ("e5", "f3"), "f2"),
    "C145_09": ("d4", ["e5", "f6"], ["e6", "f7"], ("f4", "e4"), ("f5", "e3"), "e2"),
}
# context files: distance >= 2 from the arc F_Z spanned by kings (both root squares) and pawns (Definition 2.1)
FILES = {"C125_05": "fgh", "C125_08": "h", "C125_10": "h", "C145_07": "abc", "C145_09": "abh"}


def positions(g, ctx):
    K, wp, bp, (ka, fa), (kb, fb), fr = GROUPS[g]
    out = []
    for bk, frz in ((ka, fa), (kb, fb)):
        pcs = [f"K{K}", f"k{bk}"] + [f"P{s}" for s in sorted(wp + [fr])] + [f"p{s}" for s in bp] + ctx
        out += [" ".join(pcs) + " b -", " ".join(pcs) + " w -"]
    for bk, frz in ((ka, fa), (kb, fb)):
        pcs = [f"K{K}", f"k{bk}"] + [f"P{s}" for s in sorted(wp + [frz])] + [f"p{s}" for s in bp] + ctx
        out.append((pcs, bk))
    res = out[:4]
    for pcs, _ in out[4:]:
        res += [" ".join(pcs) + " b -", " ".join(pcs) + " w -"]
    return res


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


def ctxkey(ws, bs):
    """file-free key used by the predictor (h stands for any file)"""
    return ctxname("h", ws, bs)


if __name__ == "__main__":
    if sys.argv[1] == "alone":
        with open(f"{V}/in/alone.pos", "w") as fh:
            for g in GROUPS:
                fh.write("\n".join(positions(g, [])) + "\n\n")
    elif sys.argv[1] == "ctx":
        g, f, n = sys.argv[2], sys.argv[3], int(sys.argv[4]) // 11
        assert f in FILES[g]
        k = 0; names = []
        with open(f"{V}/in/{g}_{f}_{n}{n}.pos", "w") as fh:
            for ws, bs in contexts(n):
                ctx = [f"P{f}{r}" for r in ws] + [f"p{f}{r}" for r in bs]
                fh.write("\n".join(positions(g, ctx)) + "\n")
                names.append(ctxname(f, ws, bs))
                k += 1
        open(f"{V}/in/{g}_{f}_{n}{n}.names", "w").write("\n".join(names) + "\n")
        print(k, "contexts", file=sys.stderr)
