#!/usr/bin/env python3
"""pyenum.py -- independent enumerator of root rings with ONE pawn on every file of the cylinder C_n (n files, n pawns).

No code shared with research/c9_rings/enum_rings.c; different method.

Definition (same game): white pawns and black pawns on ranks 2..7, one pawn per file (a ring with n pawns on n files has
exactly one pawn per file), no passed pawn.  A white pawn on (f,r) is passed iff no black pawn stands on files
f-1,f,f+1 (mod n) with rank > r; a black pawn on (f,r) is passed iff no white pawn stands on f-1,f,f+1 with rank < r.
Rings are counted up to the dihedral group of the cylinder (rotations f -> f+t, reflection f -> -f; 2n elements), colours NOT
exchanged.

Method (colour pattern first):
  1. every colour pattern (a cyclic 0/1 word, 1 = white) is put into its dihedral class; one representative p per class;
  2. for the representative, DFS over rank assignments r[0..n-1] (2..7), using the reduction "with one pawn per file a pawn is
     blocked iff a neighbouring file holds an opposite-colour pawn in front of it": the edge (f,f+1) is GOOD iff the colours
     differ and (white rank) < (black rank); every pawn needs a good edge;
  3. two rank assignments for the same representative pattern are in the same dihedral orbit iff they differ by an element
     of the stabiliser of the pattern, so the orbit representatives are the assignments that are lexicographically
     smallest under the stabiliser.
The reduction in 2 is NOT trusted: (a) `selftest` compares this fast method against a brute-force of ALL 12^n labelled
sequences tested by the general definition (n = 3..6, orbits canonicalised by the full dihedral group), (b) every ring emitted
for the real n is re-tested by the general definition (`--regen-check`), (c) Burnside's lemma is evaluated separately.

usage:  pyenum.py selftest
        pyenum.py N OUTDIR [--regen-check]       writes OUTDIR/py_rings_<nw>_<nb>.txt and OUTDIR/py_counts.txt
"""
import sys, os, itertools, json, time

RANKS = range(2, 8)


def images(seq, n):
    """the 2n dihedral images of a sequence (list/tuple of length n)"""
    out = []
    for t in range(n):
        out.append(tuple(seq[(i + t) % n] for i in range(n)))
        out.append(tuple(seq[(t - i) % n] for i in range(n)))
    return out


# ---------------------------------------------------------------- general definition (used by brute force and re-check)
def passed_any_general(ring, n):
    """ring: list of (colour, rank), colour 'W' or 'B', one pawn per file.  True iff some pawn is passed (general definition
    on sets of squares, no one-pawn-per-file shortcut)."""
    W = {(f, r) for f, (c, r) in enumerate(ring) if c == 'W'}
    B = {(f, r) for f, (c, r) in enumerate(ring) if c == 'B'}
    for (f, r) in W:
        if not any((g % n, q) in B for g in (f - 1, f, f + 1) for q in range(r + 1, 9)):
            return True
    for (f, r) in B:
        if not any((g % n, q) in W for g in (f - 1, f, f + 1) for q in range(1, r)):
            return True
    return False


def brute(n):
    """all labelled valid rings by the general definition; returns (labelled_count, set of canonical orbit reps) with the
    full dihedral group, and the per-(nw) counts"""
    codes = [(c, r) for c in 'WB' for r in RANKS]
    lab = {}
    orb = {}
    for ring in itertools.product(codes, repeat=n):
        if passed_any_general(ring, n):
            continue
        nw = sum(1 for c, r in ring if c == 'W')
        lab[nw] = lab.get(nw, 0) + 1
        orb.setdefault(nw, set()).add(min(images(ring, n)))
    return lab, {k: len(v) for k, v in orb.items()}, orb


# ---------------------------------------------------------------- fast method
def stabiliser(p, n):
    """list of dihedral elements (as permutations of file indices: image[i] = old index) fixing the colour pattern p"""
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
        reps.setdefault(min(images(p, n)), 0)
        reps[min(images(p, n))] += 1
    return reps            # representative -> number of patterns in the class


def rank_assignments(p, n):
    """all rank assignments (list of tuples) for pattern p with no passed pawn, by the good-edge reduction.
    p[f] = 1 for white, 0 for black."""
    out = []
    r = [0] * n

    def good(f, g):       # edge between files f and g (adjacent): opposite colours, white rank < black rank
        if p[f] == p[g]:
            return False
        return (r[f] < r[g]) if p[f] == 1 else (r[g] < r[f])

    def rec(f, sat_prev):
        # sat_prev: pawn f-1 already satisfied by the edge (f-2, f-1) (for f >= 2)
        if f == n:
            # pawn n-1 and pawn 0 are decided with the wrap edge (n-1, 0)
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


def fast(n, regen=False, outdir=None):
    res = {}
    t0 = time.time()
    for nw in range(1, n):
        nb = n - nw
        classes = pattern_classes(n, nw)
        lab_total = 0               # labelled valid rings (all patterns with nw whites)
        orbits = 0
        burn_total = 0              # sum over classes of (1/|S|) sum_g fix(g) -> must be an integer = orbit reps
        rings = []
        for p, size in sorted(classes.items()):
            S = stabiliser(p, n)
            A = rank_assignments(p, n)
            lab_total += size * len(A)
            # orbit representatives: lexicographically smallest under S
            reps = [a for a in A if all(tuple(a[perm[i]] for i in range(n)) >= a for perm in S)]
            orbits += len(reps)
            # Burnside inside the stabiliser, independent of the lexicographic selection
            aset = set(A)
            fixsum = 0
            for perm in S:
                fixsum += sum(1 for a in A if all(a[perm[i]] == a[i] for i in range(n)))
            assert fixsum % len(S) == 0, "Burnside sum not divisible"
            burn_total += fixsum // len(S)
            for a in reps:
                rings.append(tuple(('W' if p[i] else 'B', a[i]) for i in range(n)))
        assert burn_total == orbits, ("Burnside mismatch", nw, burn_total, orbits)
        if regen:
            bad = sum(1 for ring in rings if passed_any_general(ring, n))
            assert bad == 0, "emitted ring has a passed pawn by the general definition"
        res[nw] = dict(nw=nw, nb=nb, labelled=lab_total, orbits=orbits, burnside=burn_total,
                       n_pattern_classes=len(classes), rings=rings)
        if outdir:
            with open(os.path.join(outdir, "py_rings_%d_%d.txt" % (nw, nb)), "w") as f:
                for ring in rings:
                    f.write(" ".join(c + str(rk) for c, rk in ring) + "\n")
        print("n=%d split %d+%d: pattern classes %d, labelled valid rings %d, dihedral orbits %d (Burnside %d) [%.0fs]"
              % (n, nw, nb, len(classes), lab_total, orbits, burn_total, time.time() - t0), flush=True)
    return res


def selftest():
    ok = True
    for n in (3, 4, 5, 6):
        t0 = time.time()
        lab_b, orb_b, orbsets = brute(n)
        fr = fast(n, regen=True)
        for nw in range(1, n):
            lf = fr[nw]["labelled"]; of = fr[nw]["orbits"]
            lb = lab_b.get(nw, 0); ob = orb_b.get(nw, 0)
            # compare orbit SETS (canonicalised under the full group) as well as counts
            fs = set(min(images(r, n)) for r in fr[nw]["rings"])
            same = (fs == orbsets.get(nw, set())) and len(fs) == len(fr[nw]["rings"])
            line = "selftest n=%d nw=%d: labelled fast %d brute %d | orbits fast %d brute %d | orbit sets equal: %s" % (
                n, nw, lf, lb, of, ob, same)
            print(line)
            if not (lf == lb and of == ob and same):
                ok = False
        print("n=%d brute+fast %.0fs" % (n, time.time() - t0), flush=True)
    print("SELFTEST", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


def main():
    a = sys.argv[1:]
    if a and a[0] == "selftest":
        return selftest()
    n = int(a[0]); outdir = a[1]
    os.makedirs(outdir, exist_ok=True)
    res = fast(n, regen="--regen-check" in a, outdir=outdir)
    with open(os.path.join(outdir, "py_counts.txt"), "w") as f:
        f.write("n\tnw\tnb\tpattern_classes\tlabelled_valid\torbits\tburnside\n")
        for nw in range(1, n):
            r = res[nw]
            f.write("%d\t%d\t%d\t%d\t%d\t%d\t%d\n" % (n, nw, r["nb"], r["n_pattern_classes"], r["labelled"], r["orbits"], r["burnside"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
