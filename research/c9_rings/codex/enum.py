"""Independent enumerator of root rings on C_n: one pawn per file, no passed pawn, modulo dihedral group."""
import sys, os, itertools, time

RANKS = range(2, 8)


def images(seq, n):
    out = []
    for t in range(n):
        out.append(tuple(seq[(i + t) % n] for i in range(n)))
        out.append(tuple(seq[(t - i) % n] for i in range(n)))
    return out


def passed_any_general(ring, n):
    W = {(f, r) for f, (c, r) in enumerate(ring) if c == 'W'}
    B = {(f, r) for f, (c, r) in enumerate(ring) if c == 'B'}
    for (f, r) in W:
        if not any((g % n, q) in B for g in (f - 1, f, f + 1) for q in range(r + 1, 9)):
            return True
    for (f, r) in B:
        if not any((g % n, q) in W for g in (f - 1, f, f + 1) for q in range(1, r)):
            return True
    return False


def stabiliser(p, n):
    S = []
    for t in range(n):
        for refl in (0, 1):
            perm = [((t - i) % n) if refl else ((i + t) % n) for i in range(n)]
            if all(p[perm[i]] == p[i] for i in range(n)):
                S.append(perm)
    return S


def pattern_classes(n, nw):
    reps = {}
    for ones in itertools.combinations(range(n), nw):
        p = tuple(1 if i in ones else 0 for i in range(n))
        key = min(images(p, n))
        reps[key] = reps.get(key, 0) + 1
    return reps


def rank_assignments(p, n):
    out = []
    r = [0] * n

    def good(f, g):
        if p[f] == p[g]:
            return False
        return (r[f] < r[g]) if p[f] == 1 else (r[g] < r[f])

    def rec(f, sat_prev):
        if f == n:
            wrap = good(n - 1, 0)
            if not (good(n - 2, n - 1) or wrap):
                return
            if not (wrap or good(0, 1)):
                return
            out.append(tuple(r))
            return
        for q in RANKS:
            r[f] = q
            if f >= 1:
                e = good(f - 1, f)
                if f >= 2 and not (sat_prev or e):
                    continue
                rec(f + 1, e)
            else:
                rec(1, False)

    rec(0, False)
    return out


def fast(n, outdir=None, regen=False):
    res = {}
    t0 = time.time()
    for nw in range(1, n):
        nb = n - nw
        classes = pattern_classes(n, nw)
        orbits = 0
        rings = []
        for p, size in sorted(classes.items()):
            S = stabiliser(p, n)
            A = rank_assignments(p, n)
            reps = [a for a in A if all(tuple(a[perm[i]] for i in range(n)) >= a for perm in S)]
            orbits += len(reps)
            for a in reps:
                rings.append(tuple(('W' if p[i] else 'B', a[i]) for i in range(n)))
        if regen:
            bad = sum(1 for ring in rings if passed_any_general(ring, n))
            assert bad == 0, (nw, bad)
        res[nw] = (nw, nb, len(classes), len(rings), rings)
        if outdir and rings:
            with open(os.path.join(outdir, "rings_%d_%d.txt" % (nw, nb)), "w") as f:
                for ring in rings:
                    f.write(" ".join(c + str(rk) for c, rk in ring) + "\n")
        print("n=%d split %d+%d: classes=%d orbits=%d [%.1fs]" % (n, nw, nb, len(classes), len(rings), time.time() - t0), flush=True)
    if outdir:
        with open(os.path.join(outdir, "counts.txt"), "w") as f:
            f.write("n\tnw\tnb\tpattern_classes\torbits\n")
            for nw in range(1, n):
                _, nb, classes, orbits, _ = res[nw]
                f.write("%d\t%d\t%d\t%d\t%d\n" % (n, nw, nb, classes, orbits))
    return res


def selftest():
    ok = True
    for n in (4, 5, 6):
        # brute force orbits
        codes = [(c, r) for c in 'WB' for r in RANKS]
        brute_orbits = {}
        for ring in itertools.product(codes, repeat=n):
            if passed_any_general(ring, n):
                continue
            nw = sum(1 for c, r in ring if c == 'W')
            brute_orbits.setdefault(nw, set()).add(min(images(ring, n)))
        fr = fast(n, regen=True)
        for nw in range(1, n):
            fs = set(min(images(r, n)) for r in fr[nw][4])
            same = (fs == brute_orbits.get(nw, set()))
            print("selftest n=%d nw=%d fast=%d brute=%d sets_equal=%s" % (n, nw, len(fs), len(brute_orbits.get(nw, set())), same))
            if not same:
                ok = False
    print("SELFTEST", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


def main():
    a = sys.argv[1:]
    if a and a[0] == "selftest":
        return selftest()
    n = int(a[0])
    outdir = a[1]
    os.makedirs(outdir, exist_ok=True)
    fast(n, outdir=outdir, regen="--regen-check" in a)
    return 0

if __name__ == "__main__":
    sys.exit(main())
