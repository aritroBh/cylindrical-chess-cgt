"""K77 referee: own recount of the exact over groups of the four file classes on flat 8x8, from the raw outputs.

Written for K77 without reading K67's census.py or K65's recount.py/hits.py logic (only the output line formats).
p45a prints over-frame hits 'HIT sh=1 <men> b -  shuttle <z0><z1>'.  r48 prints under-frame hits
'HIT under: shuttle <z0>-<z1>, Black king <sq>, <pawns>'; these are colour-mirrored (rank r -> 9 - r, colours swapped).
Also compares the six counters of the two programs per class.
usage (from the repository root): python recount77.py
"""
import lzma, re, sys

O = "kings/delegate/out"
CLASSES = [  # name, p45a output, r48 output, in K65?
    ("{a,b,e}", f"{O}/K67/logs/search/A88_f0_1_4.out.xz", f"{O}/K67/logs/search/R88_f0_1_4.out", False),
    ("{a,d,e}", f"{O}/K67/logs/search/A88_f0_3_4.out.xz", f"{O}/K67/logs/search/R88_f0_3_4.out", False),
    ("{b,c,f}", f"{O}/K65/logs/search/A88_f1_2_5.out.xz", f"{O}/K65/logs/search/R88_f1_2_5.out", True),
    ("{b,e,f}", f"{O}/K65/logs/search/A88_f1_4_5.out.xz", f"{O}/K65/verify/logs/R88_f1_4_5.out", True),
]


def read(p):
    return (lzma.open(p, "rt") if p.endswith(".xz") else open(p)).read().splitlines()


def sq(s):
    return (ord(s[0]) - 97, int(s[1]))


def name(s):
    return "abcdefgh"[s[0]] + str(s[1])


def mir(s):
    return (s[0], 9 - s[1])


def grpA(line):
    m = re.match(r"HIT sh=1 (.+?) b -\s+shuttle ([a-h]\d)([a-h]\d)\s*$", line)
    toks = m.group(1).split()
    wk = [sq(t[1:]) for t in toks if t[0] == "K"]
    bk = [sq(t[1:]) for t in toks if t[0] == "k"]
    z = (sq(m.group(2)), sq(m.group(3)))
    assert len(wk) == 1 and bk == [z[0]], line
    W = frozenset(sq(t[1:]) for t in toks if t[0] == "P")
    B = frozenset(sq(t[1:]) for t in toks if t[0] == "p")
    return (wk[0], frozenset(z), W, B)


def grpR(line):
    m = re.match(r"HIT under: shuttle ([a-h]\d)-([a-h]\d), Black king ([a-h]\d),(.*)$", line)
    z = frozenset([mir(sq(m.group(1))), mir(sq(m.group(2)))])
    wk = mir(sq(m.group(3)))
    toks = m.group(4).split()
    W = frozenset(mir(sq(t[1:])) for t in toks if t[0] == "p")  # Black pawns of the under frame become White
    B = frozenset(mir(sq(t[1:])) for t in toks if t[0] == "P")
    return (wk, z, W, B)


def ctrA(lines):
    r = [l for l in lines if l.startswith("RESULT")]
    assert len(r) == 1
    l = r[0]
    g = lambda k: int(re.search(re.escape(k) + r"=(\d+)", l).group(1))
    return (g("placements"), g("F1(U1 at both shuttler roots)"), g("promoFreeze"), g("F2(U2)"), g("F3(U3 loose)"), g("F4(exact U4)"))


def ctrR(lines):
    r = [l for l in lines if l.startswith("SUMMARY")]
    assert len(r) == 1
    l = r[0]
    g = lambda k: int(re.search(r"\b" + re.escape(k) + r" (\d+)", l).group(1))
    return (g("placements"), g("U1"), g("promoFreeze"), g("U1+U2"), g("loose"), g("exact"))


def canon(g):
    wk, z, W, B = g
    best = None
    for refl in (False, True):
        f = (lambda s: (7 - s[0], s[1])) if refl else (lambda s: s)
        items = [("K", f(wk))] + [("z", f(s)) for s in z] + [("P", f(s)) for s in W] + [("p", f(s)) for s in B]
        lo = min(s[0] for _, s in items)
        t = tuple(sorted((c, (s[0] - lo, s[1])) for c, s in items))
        if best is None or t < best:
            best = t
    return best


def show(g):
    wk, z, W, B = g
    z0, z1 = sorted(z, key=lambda s: (s[1], s[0]))
    return "K%s k%s/k%s %s" % (name(wk), name(z0), name(z1),
                               " ".join(["P" + name(s) for s in sorted(W)] + ["p" + name(s) for s in sorted(B)]))


def men(g):
    return 2 + len(g[2]) + len(g[3])


def main():
    sets = {}
    ok = True
    for cname, a, r, _ in CLASSES:
        la, lr = read(a), read(r)
        ca, cr = ctrA(la), ctrR(lr)
        ha = [grpA(l) for l in la if l.startswith("HIT sh=1")]
        hr = [grpR(l) for l in lr if l.startswith("HIT under")]
        same = set(ha) == set(hr) and len(ha) == len(set(ha)) and len(hr) == len(set(hr))
        print("%s  p45a %s\n         r48  %s  counters %s; hits p45a %d, r48 %d, %s" % (
            cname, ca, cr, "EQUAL" if ca == cr else "DIFFER", len(ha), len(hr), "same set" if same else "DIFFERENT SETS"))
        ok &= ca == cr and same
        sets[cname] = set(ha)
    old = sets["{b,c,f}"] | sets["{b,e,f}"]
    new = sets["{a,b,e}"] | sets["{a,d,e}"]
    allg = old | new
    shapes = {}
    for g in allg:
        shapes.setdefault(canon(g), []).append(g)
    oldshapes = {canon(g) for g in old}
    print("K65 classes: %d distinct, %d shapes" % (len(old), len(oldshapes)))
    print("K67 classes: %d distinct; %d not among K65's; in both K67 classes %d" % (
        len(new), len(new - old), len(sets["{a,b,e}"] & sets["{a,d,e}"])))
    print("four classes: %d distinct, %d up to reflection and file translation" % (len(allg), len(shapes)))
    for m in (6, 7, 8):
        gs = [g for g in allg if men(g) == m]
        print("  %d men: %d groups, %d shapes; new groups %d, new shapes %d" % (
            m, len(gs), len({canon(g) for g in gs}), len([g for g in gs if g not in old]),
            len({canon(g) for g in gs if canon(g) not in oldshapes})))
    for cname in sets:
        others = set().union(*[sets[c] for c in sets if c != cname])
        print("  %s: %d, also in another class %d" % (cname, len(sets[cname]), len(sets[cname] & others)))
    print("new groups (not in K65's 38):")
    for g in sorted(new - old, key=show):
        cl = ",".join(c for c in sets if g in sets[c])
        sh = "NEW SHAPE" if canon(g) not in oldshapes else "known shape: " + "; ".join(sorted(show(h) for h in shapes[canon(g)] if h in old))
        print("  %-44s men %d pawns %d+%d  %s  %s" % (show(g), men(g), len(g[2]), len(g[3]), cl, sh))
    print("K67 hits already in K65:")
    for g in sorted(new & old, key=show):
        print("  %s" % show(g))
    print("2+2 or 3+1 etc. (6 men) groups:")
    for g in sorted(allg, key=show):
        if men(g) == 6:
            print("  %s  shape-mates %d" % (show(g), len(shapes[canon(g)])))
    print("ALL CHECKS", "OK" if ok else "FAILED")


if __name__ == "__main__":
    main()
