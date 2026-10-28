#!/usr/bin/env python3
"""ring_counter.py -- independent count of the root rings on the pawn cylinder C_N (ranks 2..7), per colour split.

Written without reading enum_rings.c's search; it uses a different method:

  * labelled rings (cyclic sequences of N per-file configurations, no dihedral quotient) are counted with a transfer
    matrix on compressed states, summed over all closed walks (trace of T^N);
  * the number of rings up to the dihedral group D_N (2N elements, colours NOT exchanged) comes from Burnside's lemma,
    the fixed-point counts of the non-identity elements being found by a direct brute-force search over the orbits of
    the files under the element;
  * a brute-force mode (explicit enumeration, literal passed-pawn test on the expanded board, canonical form under
    all 2N images) validates both parts on small cases.

Definition used (taken from the task text, not from the enumerator): a root ring has pawns on ranks 2..7 only, no
square with two pawns, at least one pawn on every file, no passed pawn; a white pawn on (f,r) is passed iff no black
pawn stands on files f-1,f,f+1 (mod N) with rank > r; a black pawn on (f,r) is passed iff no white pawn stands on
files f-1,f,f+1 with rank < r.  No pre-filtering of rank 7 white / rank 2 black pawns is done (the definition removes
them by itself).

usage:
  ring_counter.py orbits N P          Burnside count per split (also prints the labelled count and fixed points)
  ring_counter.py brute N P           brute-force orbit count (small N,P only) per split, with literal definition
  ring_counter.py labelled N P        only the labelled count per split
"""
import sys, time, itertools
import numpy as np

NONE_HI = 0      # "no pawn" for a highest rank
NONE_LO = 99     # "no pawn" for a lowest rank


def make_classes():
    cl = []
    for wm in range(64):
        for bm in range(64):
            if (wm & bm) or (wm | bm) == 0:
                continue
            W = [r for r in range(2, 8) if wm >> (r - 2) & 1]
            B = [r for r in range(2, 8) if bm >> (r - 2) & 1]
            cl.append(dict(W=tuple(W), B=tuple(B), cw=len(W), cb=len(B),
                           hiW=max(W) if W else NONE_HI, loW=min(W) if W else NONE_LO,
                           hiB=max(B) if B else NONE_HI, loB=min(B) if B else NONE_LO))
    return cl


CLASSES = make_classes()          # 728 = 3^6 - 1 file configurations


def file_ok(c, a, d):
    """file with configuration c (class dict) and neighbour classes a, d has no passed pawn."""
    M = max(a['hiB'], c['hiB'], d['hiB'])
    m = min(a['loW'], c['loW'], d['loW'])
    if c['cw'] and c['hiW'] >= M:
        return False
    if c['cb'] and c['loB'] <= m:
        return False
    return True


def literal_ok(files, N):
    """literal definition on explicit pawn lists: files[f] = (whites, blacks)."""
    for f in range(N):
        nb = [(f - 1) % N, f, (f + 1) % N]
        for r in files[f][0]:
            if not any(q > r for g in nb for q in files[g][1]):
                return False
        for r in files[f][1]:
            if not any(q < r for g in nb for q in files[g][0]):
                return False
    return True


# ---------------------------------------------------------------- labelled count: transfer matrix
def build_transfer(Amax, Emax):
    """compressed states s = (sup_next, m, u) with sup = (hiB, loW) of the newest file, m = max hiB and u = min loW of
    the newest two files.  A transition chooses the supply of the next file and sums over the configurations of the
    newest file (whose test is then decided).  Returns the groups {(cw, e): (src, udst, starts, coef)}."""
    sups = sorted({(c['hiB'], c['loW']) for c in CLASSES})
    by_sup = {}
    for c in CLASSES:
        by_sup.setdefault((c['hiB'], c['loW']), []).append(c)
    states = set()
    for s1 in sups:
        for s2 in sups:
            states.add((s2, max(s1[0], s2[0]), min(s1[1], s2[1])))
    states = sorted(states)
    sid = {s: i for i, s in enumerate(states)}
    trans = {}      # (da, de) -> {(src, dst): count}
    for s in states:
        s1, m, u = s
        for s2 in sups:
            dst = sid[(s2, max(s1[0], s2[0]), min(s1[1], s2[1]))]
            M = max(m, s2[0])
            mm = min(u, s2[1])
            for c in by_sup[s1]:
                if c['cw'] and c['hiW'] >= M:
                    continue
                if c['cb'] and c['loB'] <= mm:
                    continue
                e = c['cw'] + c['cb'] - 1
                if e > Emax or c['cw'] > Amax:
                    continue
                d = trans.setdefault((c['cw'], e), {})
                d[(sid[s], dst)] = d.get((sid[s], dst), 0) + 1
    groups = {}
    for key, d in trans.items():
        items = sorted(d.items(), key=lambda kv: (kv[0][1], kv[0][0]))
        src = np.array([k[0] for k, _ in items], dtype=np.int64)
        dst = np.array([k[1] for k, _ in items], dtype=np.int64)
        coef = np.array([v for _, v in items], dtype=np.int64)
        starts = np.flatnonzero(np.r_[True, dst[1:] != dst[:-1]])
        groups[key] = (src, dst[starts], starts, coef)
    return len(states), groups


def labelled_counts(N, P, block=24, verbose=True):
    """returns dict nw -> number of labelled rings (cyclic sequences) with nw white and P-nw black pawns."""
    Emax = P - N                       # every file carries a pawn: at most P-N pawns beyond the first on a file
    Amax = P - 1                       # at least one black pawn
    S, groups = build_transfer(Amax, Emax)
    A, E = Amax + 1, Emax + 1
    if verbose:
        print("  transfer: %d states, %d weight classes, %d transitions" %
              (S, len(groups), sum(len(g[0]) for g in groups.values())), flush=True)
    total = np.zeros((A, E), dtype=np.int64)
    t0 = time.time()
    for b0 in range(0, S, block):
        starts_s0 = list(range(b0, min(S, b0 + block)))
        B = len(starts_s0)
        V = np.zeros((S, B, A, E), dtype=np.int64)
        for i, s0 in enumerate(starts_s0):
            V[s0, i, 0, 0] = 1
        for _ in range(N):
            Vn = np.zeros_like(V)
            for (da, de), (src, udst, st, coef) in groups.items():
                part = V[src][:, :, :A - da, :E - de] * coef[:, None, None, None]
                red = np.add.reduceat(part, st, axis=0)
                Vn[udst, :, da:, de:] += red
            V = Vn
        for i, s0 in enumerate(starts_s0):
            total += V[s0, i]
        if verbose and (b0 // block) % 5 == 0:
            print("  starts %d/%d  %.0fs" % (b0 + B, S, time.time() - t0), flush=True)
    return {nw: int(total[nw, Emax]) for nw in range(1, P) if total[nw, Emax]}, total


# ---------------------------------------------------------------- fixed points by direct search
def perm_orbits(perm):
    N = len(perm)
    seen = [False] * N
    orbs = []
    for i in range(N):
        if seen[i]:
            continue
        o = []
        j = i
        while not seen[j]:
            seen[j] = True
            o.append(j)
            j = perm[j]
        orbs.append(sorted(o))
    return sorted(orbs)


def fixed_points(N, P, perm):
    """number of labelled rings (all file configs, P pawns) with c[perm[i]] == c[i] for all i, by nw."""
    orbs = perm_orbits(perm)
    k = len(orbs)
    orb_of = {}
    for idx, o in enumerate(orbs):
        for f in o:
            orb_of[f] = idx
    mult = [len(o) for o in orbs]
    suffix_min = [0] * (k + 1)
    for i in range(k - 1, -1, -1):
        suffix_min[i] = suffix_min[i + 1] + mult[i]
    # files to test right after orbit idx is assigned
    check_after = [[] for _ in range(k)]
    for f in range(N):
        need = max(orb_of[(f - 1) % N], orb_of[f], orb_of[(f + 1) % N])
        check_after[need].append(f)
    cls_small = [c for c in CLASSES if c['cw'] + c['cb'] <= P]
    cfg_of_file = [None] * N
    res = {}

    def rec(idx, nw, nb):
        if idx == k:
            if nw + nb == P:
                res[nw] = res.get(nw, 0) + 1
            return
        for c in cls_small:
            m = mult[idx]
            tw, tb = nw + m * c['cw'], nb + m * c['cb']
            if tw + tb + suffix_min[idx + 1] > P:
                continue
            for f in orbs[idx]:
                cfg_of_file[f] = c
            good = True
            for f in check_after[idx]:
                if not file_ok(cfg_of_file[f], cfg_of_file[(f - 1) % N], cfg_of_file[(f + 1) % N]):
                    good = False
                    break
            if good:
                rec(idx + 1, tw, tb)
        for f in orbs[idx]:
            cfg_of_file[f] = None

    rec(0, 0, 0)
    return res


def dihedral(N):
    els = []
    for t in range(N):
        els.append(("rot%d" % t, [(i + t) % N for i in range(N)]))
    for t in range(N):
        els.append(("ref%d" % t, [(t - i) % N for i in range(N)]))
    return els


def orbit_counts(N, P, verbose=True):
    lab, _ = labelled_counts(N, P, verbose=verbose)
    fixsum = {}
    detail = []
    for name, perm in dihedral(N)[1:]:
        fx = fixed_points(N, P, perm)
        if fx:
            detail.append((name, fx))
        for nw, v in fx.items():
            fixsum[nw] = fixsum.get(nw, 0) + v
    out = {}
    for nw in sorted(set(lab) | set(fixsum)):
        tot = lab.get(nw, 0) + fixsum.get(nw, 0)
        if tot % (2 * N):
            raise SystemExit("Burnside sum not divisible by %d: nw=%d lab=%d fix=%d" % (2 * N, nw, lab.get(nw, 0), fixsum.get(nw, 0)))
        out[nw] = tot // (2 * N)
    return out, lab, fixsum, detail


# ---------------------------------------------------------------- brute force with literal definition
def brute_orbits(N, P):
    """explicit enumeration of all labelled rings with the literal test, canonical form over the 2N images."""
    cls = [c for c in CLASSES if c['cw'] + c['cb'] <= P - (N - 1)]
    files_lit = [(c['W'], c['B']) for c in cls]
    n = len(cls)
    ring = [0] * N
    canon = {}
    nlab = {}

    def lit_file(f, ids):
        a, c, d = files_lit[ids[(f - 1) % N]], files_lit[ids[f]], files_lit[ids[(f + 1) % N]]
        for r in c[0]:
            if not any(q > r for g in (a, c, d) for q in g[1]):
                return False
        for r in c[1]:
            if not any(q < r for g in (a, c, d) for q in g[0]):
                return False
        return True

    def rec(f, nw, nb):
        if f == N:
            if nw + nb != P:
                return
            if not (lit_file(N - 1, ring) and lit_file(0, ring)):
                return
            if not literal_ok([files_lit[i] for i in ring], N):     # full literal test on the expanded board
                return
            nlab[nw] = nlab.get(nw, 0) + 1
            best = None
            for t in range(N):
                for refl in (0, 1):
                    img = tuple(ring[(t - i) % N] if refl else ring[(i + t) % N] for i in range(N))
                    if best is None or img < best:
                        best = img
            canon[best] = nw
            return
        rem = N - f - 1
        for i in range(n):
            c = cls[i]
            tw, tb = nw + c['cw'], nb + c['cb']
            if tw + tb + rem > P:
                continue
            ring[f] = i
            if f >= 2 and not lit_file(f - 1, ring):
                continue
            rec(f + 1, tw, tb)

    rec(0, 0, 0)
    orb = {}
    for _, nw in canon.items():
        orb[nw] = orb.get(nw, 0) + 1
    return orb, nlab


def main():
    a = sys.argv[1:]
    if len(a) < 3:
        print(__doc__)
        return 2
    mode, N, P = a[0], int(a[1]), int(a[2])
    t0 = time.time()
    if mode == "labelled":
        lab, _ = labelled_counts(N, P)
        for nw in range(1, P):
            print("N=%d P=%d split %d+%d labelled %d" % (N, P, nw, P - nw, lab.get(nw, 0)))
    elif mode == "orbits":
        out, lab, fix, detail = orbit_counts(N, P)
        for nw in range(1, P):
            print("N=%d P=%d split %d+%d labelled %d fixedsum %d orbits %d" %
                  (N, P, nw, P - nw, lab.get(nw, 0), fix.get(nw, 0), out.get(nw, 0)))
        for name, fx in detail:
            print("  fixed by %s: %s" % (name, fx))
    elif mode == "brute":
        orb, nlab = brute_orbits(N, P)
        for nw in range(1, P):
            print("N=%d P=%d split %d+%d labelled %d orbits %d" % (N, P, nw, P - nw, nlab.get(nw, 0), orb.get(nw, 0)))
    else:
        print(__doc__)
        return 2
    print("  (%.1fs)" % (time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
