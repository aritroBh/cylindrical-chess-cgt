"""K77 referee: Definition 4.8 (exact over group) checked directly with p74 (the K74 referee's P solver, a program that
shares no code with p45a, r48, ref3m, kp_p, ax65 or pk_sum), for the 13 hits of {a,b,e} and {a,d,e} and for 30 near
misses (same pawns; White king, or the Black shuttle pair, moved by one square) that are not hits.

Over group (colour mirror of Definition 4.8): Black king shuttles on z = {z0, z1}, White king on w0.
 K1: no White pawn attacks z0 or z1, no Black pawn attacks w0.  K2: king distance >= 2 from w0 to z0 and to z1.
 (O1) at both Black-to-move roots the shuttle is legal and every other Black move is a White win in P;
 (O2) at both White-to-move roots White has a move that is not a loss (a freeze); no freeze may be a promotion;
 (O3) after each freeze, q with Black to move (e.p. right if a double step): Black has a move and every Black move is a White win;
 (O4) q with White to move (no right): legal (Black not in check), White has a move and every White move is a White loss.
usage (from the repository root): python def77.py   (writes verify/logs/def77/ and prints a table)
"""
import os, subprocess, sys

V = "kings/delegate/out/K67/verify"
sys.path.insert(0, V + "/src")
import recount77 as rc  # noqa: E402

P74 = V + "/tmp/p74"
LOG = V + "/logs/def77"
os.makedirs(LOG, exist_ok=True)


def nm(s):
    return "abcdefgh"[s[0]] + str(s[1])


def katt(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= 1


def wpatt(W, s):  # is square s attacked by a White pawn
    return any((p[0] - s[0]) in (-1, 1) and s[1] == p[1] + 1 for p in W)


def bpatt(B, s):
    return any((p[0] - s[0]) in (-1, 1) and s[1] == p[1] - 1 for p in B)


def postext(wk, bk, W, B, stm, ep=None):
    return "K%s k%s %s %s %s" % (nm(wk), nm(bk), " ".join(["P" + nm(s) for s in sorted(W)] + ["p" + nm(s) for s in sorted(B)]),
                                 stm, nm(ep) if ep else "-")


def run_p74(positions, stem):
    path = f"{LOG}/{stem}.in"
    with open(path, "w") as f:
        f.write("\n".join(positions) + "\n")
    with open(path) as fin:  # size first (p74 -c counts configs only): direct runs only below 60,000 configs (about 20 s, 0.2 GB)
        c = subprocess.run([P74, "-c"], stdin=fin, capture_output=True, text=True)
    ncfg = int(c.stderr.split(" configs")[0].split()[-1])
    print("[%s: %d configs]" % (stem, ncfg), file=sys.stderr)
    if ncfg > 60000:
        sys.exit("too large for a direct run: %s" % stem)
    with open(path) as fin:
        r = subprocess.run(["zsh", V + "/src/run77.sh", f"{LOG}/{stem}", P74, "-m"], stdin=fin)
    if r.returncode != 0:
        sys.exit("p74 failed on %s (rc %d)" % (stem, r.returncode))
    res, cur = {}, None
    for line in open(f"{LOG}/{stem}.out"):
        if not line.startswith("   "):
            t, v = line.rstrip("\n").rsplit("  P=", 1)
            cur = t.strip()
            res[cur] = (v, [])
        else:
            mv, v = line.split()
            res[cur][1].append((mv, v))
    return res


def apply(wk, bk, W, B, mv):
    """apply a White move given in p74's notation; return (wk, W, B, ep for Black, is promotion)"""
    if mv.endswith("="):
        return None
    if mv[0] == "K":
        to = rc.sq(mv[4:6])
        return to, W, B - {to}, None
    fr, to = rc.sq(mv[0:2]), rc.sq(mv[3:5])
    W2 = (W - {fr}) | {to}
    B2 = B - {to}
    ep = (fr[0], fr[1] + 1) if to[1] - fr[1] == 2 else None
    return wk, W2, B2, ep


def check(groups, stem):
    """groups: list of (label, (wk, z, W, B)); returns list of (label, group, exact?, notes, details)"""
    pre = []
    roots = []
    for lab, g in groups:
        wk, z, W, B = g
        z0, z1 = sorted(z, key=lambda s: (s[1], s[0]))
        bad = []
        if katt(z0, z1) is False or z0 == z1:
            bad.append("z not adjacent")
        if any(wpatt(W, s) for s in (z0, z1)) or bpatt(B, wk):
            bad.append("K1 fails")
        if katt(wk, z0) or katt(wk, z1):
            bad.append("K2 fails")
        occ = W | B
        if wk in occ or z0 in occ or z1 in occ or wk in (z0, z1):
            bad.append("occupied")
        pre.append((lab, g, z0, z1, bad))
        if not bad:
            for zz in (z0, z1):
                roots += [postext(wk, zz, W, B, "b"), postext(wk, zz, W, B, "w")]
    R = run_p74(sorted(set(roots)), stem + "_roots")
    qs, plan = [], []
    for lab, g, z0, z1, bad in pre:
        if bad:
            plan.append((lab, g, z0, z1, bad, None))
            continue
        wk, z, W, B = g
        info = {}
        for zz, oth in ((z0, z1), (z1, z0)):
            vb, mb = R[postext(wk, zz, W, B, "b")]
            vw, mw = R[postext(wk, zz, W, B, "w")]
            sh = "K%s-%s" % (nm(zz), nm(oth))
            frz = [(m, v) for m, v in mw if v != "L"]
            qlist = []
            for m, v in frz:
                a = apply(wk, zz, W, B, m)
                if a is None:
                    qlist.append((m, None, None, "promotion"))
                    continue
                wk2, W2, B2, ep = a
                qb = postext(wk2, zz, W2, B2, "b", ep)
                legal_w = not wpatt(W2, zz)
                qw = postext(wk2, zz, W2, B2, "w") if legal_w else None
                qs.append(qb)
                if qw:
                    qs.append(qw)
                qlist.append((m, qb, qw, ""))
            info[nm(zz)] = dict(vb=vb, vw=vw, shuttle=any(m == sh for m, _ in mb),
                                badB=[(m, v) for m, v in mb if m != sh], frz=qlist, nmovesW=len(mw))
        plan.append((lab, g, z0, z1, bad, info))
    Q = run_p74(sorted(set(qs)), stem + "_qs") if qs else {}
    out = []
    for lab, g, z0, z1, bad, info in plan:
        notes = list(bad)
        if info:
            for r, d in info.items():
                if not d["shuttle"]:
                    notes.append("O1: no shuttle at %s" % r)
                nl = [m for m, v in d["badB"] if v != "W"]
                if nl:
                    notes.append("O1 fails at %s: %s" % (r, ",".join(nl)))
                if not d["frz"]:
                    notes.append("O2: no freeze at %s" % r)
                for m, qb, qw, why in d["frz"]:
                    if why:
                        notes.append("freeze %s at %s is a %s" % (m, r, why))
                        continue
                    v, ml = Q[qb]
                    if not ml or any(x != "W" for _, x in ml):
                        notes.append("O3 fails after %s (%s): %s" % (m, r, ",".join(a for a, x in ml if x != "W") or "no move"))
                    if qw is None:
                        notes.append("O4: q after %s (%s) with White to move illegal (check)" % (m, r))
                    else:
                        v2, ml2 = Q[qw]
                        if not ml2 or any(x != "L" for _, x in ml2):
                            notes.append("O4 fails after %s (%s): %s" % (m, r, ",".join(a for a, x in ml2 if x != "L") or "no move"))
        out.append((lab, g, not notes, notes, info, Q))
    return out


def describe(info, Q):
    s = []
    for r, d in info.items():
        fz = []
        for m, qb, qw, why in d["frz"]:
            if why:
                fz.append(m + "(" + why + ")")
            else:
                fz.append("%s: q b %s, q w %s" % (m, Q[qb][0], Q[qw][0] if qw else "illegal"))
        s.append("root %s: B to move %s, W to move %s; %d bad Black moves (%s); freezes [%s]" % (
            r, d["vb"], d["vw"], len(d["badB"]), " ".join(m + "=" + v for m, v in d["badB"]), "; ".join(fz)))
    return s


def main():
    sets = {}
    for cname, a, r, _ in rc.CLASSES:
        sets[cname] = {rc.grpA(l) for l in rc.read(a) if l.startswith("HIT sh=1")}
    allhits = set().union(*sets.values())
    hits = sorted(sets["{a,b,e}"] | sets["{a,d,e}"], key=rc.show)
    res = check([(rc.show(g), g) for g in hits], "hits")
    print("== 13 hits of {a,b,e} and {a,d,e}")
    for lab, g, ex, notes, info, Q in res:
        print("%-44s %s%s" % (lab, "EXACT" if ex else "NOT EXACT", "" if ex else "  " + "; ".join(notes)))
        for l in describe(info, Q):
            print("     " + l)
    # near misses: same pawns, one king moved by one square; K1, K2 and empty squares, not a hit of any class
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    cands = []
    for i, g in enumerate(hits):
        wk, z, W, B = g
        got = []
        for k, (df, dr) in enumerate(dirs):
            for kind in ("K", "z"):
                if kind == "K":
                    ng = ((wk[0] + df, wk[1] + dr), z, W, B)
                else:
                    ng = (wk, frozenset((s[0] + df, s[1] + dr) for s in z), W, B)
                sqs = [ng[0]] + list(ng[1])
                if not all(0 <= s[0] < 8 and 1 <= s[1] <= 8 for s in sqs):
                    continue
                zz = sorted(ng[1])
                if wpatt(W, zz[0]) or wpatt(W, zz[1]) or bpatt(B, ng[0]) or katt(ng[0], zz[0]) or katt(ng[0], zz[1]):
                    continue
                if any(s in (W | B) for s in sqs) or ng in allhits:
                    continue
                got.append(("%s %s%+d%+d" % (rc.show(ng), kind, df, dr), ng))
        want = 3 if i < 4 else 2
        # take one White-king move and one shuttle-pair move first, then the rest in order
        ks = [x for x in got if " K" in x[0][-7:]]
        zs = [x for x in got if " z" in x[0][-7:]]
        pick = (ks[:1] + zs[:1] + [x for x in got if x not in ks[:1] + zs[:1]])[:want]
        cands += pick
    res2 = check(cands, "near")
    print("== %d near misses" % len(res2))
    nex = 0
    for lab, g, ex, notes, info, Q in res2:
        nex += ex
        print("%-52s %s  %s" % (lab, "EXACT (!)" if ex else "not exact", "; ".join(notes[:3]) + (" ..." if len(notes) > 3 else "")))
    print("hits exact: %d of %d; near misses exact: %d of %d" % (sum(x[2] for x in res), len(res), nex, len(res2)))


if __name__ == "__main__":
    main()
