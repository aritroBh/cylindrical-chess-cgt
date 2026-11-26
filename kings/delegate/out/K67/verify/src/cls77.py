"""K77 referee: classification of exact over groups with s77 (own sum solver).  For each group and each non-shuttle Black
root move m: x_m beside -1 (White to move; (B1) = W), Aux(x_m) (W or L), and, where Aux is lost or asked for, the
ladder values x_m + u_0 of T_N (White to move) and both roots + u_0 of T_N (Black to move).
usage (repository root): python cls77.py <group file: name|Kxx kz0 pawns|z0|z1 per line> <maxN for ladders> [direct|heavy]
  ladders are computed for every group with an Aux loss, and for groups listed with a '+' after the name.
"""
import os, subprocess, sys

V = "kings/delegate/out/K67/verify"
S77 = V + "/tmp/s77"
LOG = V + "/logs/cls77"
os.makedirs(LOG, exist_ok=True)
groups = [l.strip().split("|") for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
MAXN = int(sys.argv[2])
MODE = sys.argv[3] if len(sys.argv) > 3 else "direct"


def run(name, T, positions):
    stem = f"{LOG}/{name}_{T}"
    with open(stem + ".in", "w") as f:
        f.write("\n".join(positions) + "\n")
    runner = V + ("/src/run77.sh" if MODE == "direct" else "/src/wd77.sh")
    with open(stem + ".in") as fin:
        r = subprocess.run(["zsh", runner, stem, S77, "-t", T, "-m"], stdin=fin)
    if r.returncode:
        sys.exit("s77 failed: %s %s rc %d" % (name, T, r.returncode))
    res, cur = {}, None
    for line in open(stem + ".out"):
        if not line.startswith("   "):
            t, v = line.rstrip("\n").rsplit("  ", 1)
            cur = t.strip(); res[cur] = (v.split("=")[1], {})
        else:
            m, v = line.split(); res[cur][1][m] = v
    tm = [l for l in open(stem + ".err") if "real" in l or "maximum resident" in l]
    print("   [%s %s: %s]" % (name, T, " ".join(x.split()[0] for x in tm)), file=sys.stderr)
    return res


def roots(g):
    name, men, z0, z1 = g
    toks = men.split()
    base = [t for t in toks if t[0] != "k"]
    pos = {}
    for z, o in ((z0, z1), (z1, z0)):
        pos[z] = (" ".join(base[:1] + ["k" + z] + base[1:]) + " b -", "K%s-%s" % (z, o))
    return pos


for g in groups:
    name = g[0].rstrip("+")
    want_ladder = g[0].endswith("+")
    R = roots(g)
    P = [p for p, _ in R.values()]
    m1 = run(name, "minus1", P)
    ax = run(name, "aux", P)
    rows, lost = [], []
    for z, (p, sh) in R.items():
        for m, v in m1[p][1].items():
            if m in (sh, "T-move"):
                continue
            a = ax[p][1][m]
            rows.append((z, m, v, a))
            if a != "W":
                lost.append((z, m))
    nb1 = [r for r in rows if r[2] != "W"]
    print("%s: %d bad moves; (B1) fails at %s; Aux lost at %s" % (
        name, len(rows), ", ".join("%s (%s, -1: %s, Aux %s)" % (m, z, v, a) for z, m, v, a in nb1) or "none",
        ", ".join("%s (%s)" % (m, z) for z, m in lost) or "none"))
    for z, m, v, a in rows:
        print("     root %s  %-9s beside -1: %s   Aux: %s" % (z, m, v, a))
    if lost or want_ladder:
        targets = lost if lost else [(z, m) for z, m, v, a in nb1]
        for N in range(MAXN + 1):
            L = run(name, "ladder%d" % N, P)
            print("     T_%d: roots (Black to move) %s; %s" % (
                N, ", ".join("%s %s" % (z, L[p][0]) for z, (p, _) in R.items()),
                ", ".join("x_m %s (%s) %s" % (m, z, L[R[z][0]][1][m]) for z, m in targets)))
    sys.stdout.flush()
