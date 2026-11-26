"""K75: the 48 exact over groups of flat 8x8 (K65's 38, K67's 10) with roots, freezes, q's, class, context files.

Usage (repository root):
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K75/src/groups.py LOGDIR65 LOGDIR67
    LOGDIR65: the ax65 logs g/ of the K65 referee (untarred from kings/delegate/out/K65/verify/logs/groups_logs.tar.xz)
    LOGDIR67: kings/delegate/out/K67/logs/g
  -> in/groups48.txt, one line per group:
     name|men|class|WK|kA|kB|White pawns (root)|Black pawns|freeze at A|freeze at B|ep at qA|ep at qB|F_Z|context files
Freezes and q's are read from ax65's Definition 4.8 log of each group ("freeze Pxxyy at z -> q = ...").
Class (K65 referee VERIFY.md table 1; K67 findings 1c): B1 = (B1) at every bad move; AUXW = (B1) fails, Aux won at
every failing move (Theorem 4.18); AUXL = Aux lost at one bad move (N* finite).
Context files (Definition 2.1): files at distance >= 2 from every file of F_Z, F_Z = the files of the White king, both
shuttle squares and every group pawn (roots and q's).
"""
import re, sys, os

V = "kings/delegate/out/K75"
AUXW = {"C125_09", "C125_13", "C125_22", "C125_23", "C145_16", "C145_24", "C145_25", "C014_04", "C014_09"}
AUXL = {"C125_14": 2, "C125_15": 3, "C125_16": 2, "C145_19": 2, "C014_08": 2}
PROVISIONAL = {"C014_01", "C014_04", "C014_05", "C014_06", "C014_08", "C014_09", "C014_10", "C034_01", "C034_02",
               "C034_03"}

def parse(path):
    t = open(path).read()
    head = t.splitlines()[0]
    m = re.match(r"ax65 flat:8x8\s+(.*?)\s+shuttle (\w\d)-(\w\d)", head)
    pcs, za, zb = m.group(1).split(), m.group(2), m.group(3)
    fr = re.findall(r"freeze P(\w\d)(\w\d) at (\w\d) ->", t)
    assert len(fr) == 2, (path, fr)
    assert "exact (0 failures)" in t, path
    frz = {z: (a, b) for a, b, z in fr}
    WK = [p[1:] for p in pcs if p[0] == "K"][0]
    wp = sorted(p[1:] for p in pcs if p[0] == "P")
    bp = sorted(p[1:] for p in pcs if p[0] == "p")
    return WK, za, zb, wp, bp, frz[za], frz[zb]

def epsq(frm, to, bp):
    """e.p. target after a White double step frm->to if a Black pawn can take e.p."""
    if int(to[1]) - int(frm[1]) != 2: return "-"
    f = ord(to[0])
    for d in (-1, 1):
        if 0 <= f + d - 97 < 8 and chr(f + d) + to[1] in bp: return to[0] + str(int(frm[1]) + 1)
    return "-"

if __name__ == "__main__":
    d65, d67 = sys.argv[1], sys.argv[2]
    rows = []
    for d in (d65, d67):
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".out"): continue
            nm = fn[:-4]
            if d == d67 and nm == "C125_15": continue    # K67's validation rerun of a K65 group
            WK, za, zb, wp, bp, fa, fb = parse(os.path.join(d, fn))
            cls = "AUXL" if nm in AUXL else ("AUXW" if nm in AUXW else "B1")
            sq = [WK, za, zb] + wp + bp + [fa[1], fb[1]]
            fz = sorted({s[0] for s in sq})
            ctx = [f for f in "abcdefgh" if all(abs(ord(f) - ord(g)) >= 2 for g in fz)]
            men = 2 + len(wp) + len(bp)
            rows.append((nm, men, cls + ("*" if nm in PROVISIONAL else ""), WK, za, zb, ",".join(wp), ",".join(bp),
                         fa[0] + fa[1], fb[0] + fb[1], epsq(*fa, bp), epsq(*fb, bp), "".join(fz), "".join(ctx)))
    assert len(rows) == 48, len(rows)
    with open(f"{V}/in/groups48.txt", "w") as fh:
        fh.write("# name|men|class (* = K67, search by one program)|WK|kA|kB|White pawns|Black pawns|freeze A|freeze B|"
                 "ep qA|ep qB|F_Z|context files\n")
        for r in rows: fh.write("|".join(map(str, r)) + "\n")
    print(sum(len(r[-1]) for r in rows), "pairs;", sum(1 for r in rows if r[-1]), "groups with a context file",
          file=sys.stderr)
