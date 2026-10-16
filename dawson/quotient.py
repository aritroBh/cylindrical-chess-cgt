"""Partial misere quotients Q_n of Dawson's chess (octal 0.137), computed from scratch.

Q_n is the misere quotient (Plambeck-Siegel) of the set A_n of all sums of strips of length
<= n. This is an independent re-implementation of the MisereSolver strategy described in
Plambeck & Siegel, "Misere quotients for impartial games", supplementary material
(arXiv:0705.2404, Appendix C):
  * verification: P-verification (their Fact C.1) and the N-verification traversal of A_n in
    lexicographic order with subsumption pruning (their Algorithm 1);
  * recalibration: free the generators of the least failure into <t | t^(m+k) = t^m>, guess
    outcomes of lexicographically least representatives, and reduce.
Only the final answer matters for correctness: a candidate (Q, P, Phi) is accepted only when
both verifications find no failure, which proves that Phi predicts the misere outcome of
every position of A_n (by induction on positions) and hence, because Q is reduced and Phi is
onto, that (Q, P) is the misere quotient of A_n. As an extra, independent check, the result
is compared against the exhaustive outcome table of dawson/misere.c.

Strips of length 2 are identical game trees to strips of length 1, so the generators are the
strip lengths 1, 3, 4, ..., n. Note Q_n(0.137) = Q_{n+1}(0.07) (Dawson's Kayles), since a
0.137 heap of n is the same game tree as a 0.07 heap of n + 1.

Run from the project root:
    PYTHONPATH=. .venv/bin/python -m dawson.quotient 32
"""
import sys
import time
from collections import defaultdict
from itertools import combinations

from dawson.octal import heap_moves, octal_options

sys.setrecursionlimit(100000)
MV = octal_options("0.137")
M_EXP, K_EXP = 4, 2           # the new generator is freed into <t | t^(M+K) = t^M>
OLD_M, OLD_K = 2, 2           # older generators, when freed, go to <t | t^4 = t^2>
LIMIT = 400_000                # largest expanded monoid Q* we are willing to build


def canon_heap(h):
    return 1 if h == 2 else h


def heap_option_tuples(h):
    """Options of a single strip h, each as a tuple of canonical generator sizes."""
    out = set()
    for rest in heap_moves(MV, h):
        out.add(tuple(sorted(canon_heap(x) for x in rest if x > 0)))
    return sorted(out)


class Quotient:
    """A finite commutative monoid with identity 0, given by its full multiplication table,
    a P-portion, and images phi[h] of the generators (strip lengths)."""

    def __init__(self, mult, P, phi, gens):
        self.mult = mult            # list of lists
        self.P = P                  # list of bool
        self.phi = dict(phi)        # strip length -> element
        self.gens = list(gens)      # increasing strip lengths
        self.N = len(mult)
        self.Pmask = sum(1 << i for i in range(self.N) if P[i])
        self._ms = {}

    def img(self, heaps):
        x = 0
        for h in heaps:
            x = self.mult[x][self.phi[h]]
        return x

    def mulset(self, E, h):
        """{e * h : e in E} for a bitmask E and element h."""
        key = (E, h)
        r = self._ms.get(key)
        if r is not None:
            return r
        r = 0
        row = self.mult
        e = E
        while e:
            low = e & -e
            i = low.bit_length() - 1
            r |= 1 << row[i][h]
            e ^= low
        if len(self._ms) < 2_000_000:
            self._ms[key] = r
        return r

    def opts_mask(self, h):
        m = 0
        for t in heap_option_tuples(h):
            m |= 1 << self.img(t)
        return m

    # ---- lexicographically least representatives (largest generator counts most) ----
    def lexleast(self, gens=None):
        gens = self.gens if gens is None else gens
        reps = {0: ()}            # element -> key tuple (count of largest gen first)
        for g in gens:
            pw = [0]
            seen = {0: 0}
            while True:
                nxt = self.mult[pw[-1]][self.phi[g]]
                if nxt in seen:
                    break
                seen[nxt] = len(pw)
                pw.append(nxt)
            new = {}
            for c, p in enumerate(pw):
                for s, key in reps.items():
                    x = self.mult[p][s]
                    cand = (c,) + key
                    old = new.get(x)
                    if old is None or cand < old:
                        new[x] = cand
            reps = new
        return reps   # key tuples are aligned with reversed(gens)

    # ---------------------------------- verification ----------------------------------
    def verify(self, record=True):
        """Return (least failure or None, records). A failure is a count vector (dict)."""
        gens = self.gens
        G = len(gens)
        mult, P = self.mult, self.P
        phis = [self.phi[g] for g in gens]
        omasks = [self.opts_mask(g) for g in gens]
        fails = []
        # P-verification (Plambeck-Siegel Fact C.1)
        reps = self.lexleast()
        for i, g in enumerate(gens):
            hi = phis[i]
            opt_imgs = [self.img(t) for t in heap_option_tuples(g)]
            for x in range(self.N):
                if P[mult[x][hi]] and any(P[mult[x][y]] for y in opt_imgs):
                    key = list(reps[x])                 # aligned with reversed(gens)
                    key[G - 1 - i] += 1
                    fails.append(tuple(key))
        # N-verification (Algorithm 1 with subsumption; records every visited (x, E))
        records = defaultdict(list)
        counts = [0] * G

        def subsumed(x, E):
            for D in records[x]:
                if D & ~E == 0:
                    return True
            return False

        def add_record(x, E):
            lst = records[x]
            for D in lst:
                if D & ~E == 0:
                    return
            lst[:] = [D for D in lst if E & ~D != 0] + [E]

        def rec(d, x, E, nonzero):
            if d == 0:
                if not nonzero:
                    return None
                if not P[x] and (E & self.Pmask) == 0:
                    return tuple(reversed(counts))
                add_record(x, E)
                return None
            i = d - 1
            h, om = phis[i], omasks[i]
            c0 = counts[i]
            while True:
                r = rec(d - 1, x, E, nonzero)
                if r is not None:
                    counts[i] = c0
                    return r
                E = self.mulset(E, h) | self.mulset(om, x)
                x = mult[x][h]
                nonzero = True
                counts[i] += 1
                if subsumed(x, E):
                    counts[i] = c0
                    return None

        nf = rec(G, 0, 0, False)
        if nf is not None:
            fails.append(nf)
        least = min(fails) if fails else None
        return least, records

    # ---------------------------------- recalibration ---------------------------------
    def recalibrate(self, J, exps=None):
        """Free the generators in J (strip lengths): generator g is sent to the free element t_g
        of <t | t^(m+k) = t^m> with (m, k) = exps[g] (default (M_EXP, K_EXP)).
        Returns a new reduced Quotient."""
        gens = self.gens
        J = [g for g in gens if g in J]
        nonJ = [g for g in gens if g not in J]
        exps = exps or {}
        MK = [exps.get(g, (M_EXP, K_EXP)) for g in J]
        Rs = [m + k for (m, k) in MK]
        # Q^- : submonoid generated by the non-J generators
        qm = [0]
        seen = {0}
        frontier = [0]
        while frontier:
            nf = []
            for q in frontier:
                for g in nonJ:
                    y = self.mult[q][self.phi[g]]
                    if y not in seen:
                        seen.add(y)
                        qm.append(y)
                        nf.append(y)
            frontier = nf
        qpos = {q: i for i, q in enumerate(qm)}
        nJ = len(J)
        size = len(qm)
        for r in Rs:
            size *= r

        def enc(q, es):
            v = qpos[q]
            for e, r in zip(es, Rs):
                v = v * r + e
            return v

        def dec(v):
            es = []
            for r in reversed(Rs):
                es.append(v % r)
                v //= r
            return qm[v], tuple(reversed(es))

        def wrap1(s, mk):
            m, k = mk
            return s if s < m + k else m + (s - m) % k

        def wrap(es):
            return tuple(wrap1(s, mk) for s, mk in zip(es, MK))

        elems = [dec(v) for v in range(size)]

        def mulstar(a, b):
            (qa, ea), (qb, eb) = elems[a], elems[b]
            return enc(self.mult[qa][qb], wrap([x + y for x, y in zip(ea, eb)]))

        gstar = {}
        for g in gens:
            if g in J:
                es = [0] * nJ
                es[J.index(g)] = 1
                gstar[g] = enc(0, tuple(es))
            else:
                gstar[g] = enc(self.phi[g], (0,) * nJ)
        # generator action tables on Q*
        act = {}
        for g in gens:
            hq, he = elems[gstar[g]]
            tab = [0] * size
            for v in range(size):
                q, es = elems[v]
                tab[v] = enc(self.mult[q][hq], wrap([x + y for x, y in zip(es, he)]))
            act[g] = tab
        # lex-least representatives: J counts = exponents, non-J part = lex-least in Q^-
        sub = Quotient(self.mult, self.P, self.phi, nonJ)
        repm = sub.lexleast(nonJ)          # q -> key aligned with reversed(nonJ)

        def full_counts(v):
            q, es = elems[v]
            cnt = dict(zip(reversed(nonJ), repm[q]))
            for g, e in zip(J, es):
                cnt[g] = e
            return cnt

        order = sorted(range(size), key=lambda v: tuple(full_counts(v).get(g, 0) for g in reversed(gens)))
        Pstar = [None] * size
        hopts = {g: heap_option_tuples(g) for g in gens}

        def img_counts(cnt):
            v = enc(0, (0,) * nJ)
            for g, c in cnt.items():
                for _ in range(c):
                    v = act[g][v]
            return v

        for v in order:
            cnt = full_counts(v)
            if all(c == 0 for c in cnt.values()):
                Pstar[v] = False
                continue
            isP = True
            for g, c in cnt.items():
                if c == 0 or not isP:
                    continue
                base_cnt = dict(cnt)
                base_cnt[g] -= 1
                base = img_counts(base_cnt)
                for t in hopts[g]:
                    w = base
                    for h in t:
                        w = act[h][w]
                    if Pstar[w] is None:
                        raise RuntimeError("option processed out of order")
                    if Pstar[w]:
                        isP = False
                        break
            Pstar[v] = isP
        # reduction: coarsest congruence refining the P-partition (Moore minimisation)
        cls = [1 if p else 0 for p in Pstar]
        ncls = len(set(cls))
        while True:
            sig = {}
            new = [0] * size
            for v in range(size):
                key = (cls[v],) + tuple(cls[act[g][v]] for g in gens)
                if key not in sig:
                    sig[key] = len(sig)
                new[v] = sig[key]
            if len(sig) == ncls:
                cls = new
                break
            cls, ncls = new, len(sig)
        # renumber so that the identity is class 0
        ident = enc(0, (0,) * nJ)
        perm = {cls[ident]: 0}
        for v in range(size):
            if cls[v] not in perm:
                perm[cls[v]] = len(perm)
        cls = [perm[c] for c in cls]
        rep = {}
        for v in range(size):
            rep.setdefault(cls[v], v)
        n = len(rep)
        mult = [[0] * n for _ in range(n)]
        for a in range(n):
            ra = rep[a]
            for b in range(a, n):
                c = cls[mulstar(ra, rep[b])]
                mult[a][b] = c
                mult[b][a] = c
        Pn = [bool(Pstar[rep[c]]) for c in range(n)]
        phin = {g: cls[gstar[g]] for g in gens}
        return Quotient(mult, Pn, phin, gens)

    def qminus_size(self, J):
        seen = {0}
        frontier = [0]
        gl = [self.phi[g] for g in self.gens if g not in J]
        while frontier:
            nf = []
            for q in frontier:
                for y0 in gl:
                    y = self.mult[q][y0]
                    if y not in seen:
                        seen.add(y)
                        nf.append(y)
            frontier = nf
        return len(seen)

    def meximal(self):
        Z = []
        for x in range(self.N):
            m = 0
            for z in range(self.N):
                if self.P[self.mult[x][z]]:
                    m |= 1 << z
            Z.append(m)
        Mx = []
        for x in range(self.N):
            m = 0
            for y in range(self.N):
                if Z[x] & Z[y] == 0:
                    m |= 1 << y
            Mx.append(m)
        return Mx


def extend(Qc, records, h, log):
    """Given the verified quotient Qc of A_{n-1} (with the transition records of its
    verification), return the verified quotient of A_n (n = h, the new strip length)."""
    gens = Qc.gens + [h]
    E = 0
    for t in heap_option_tuples(h):
        E |= 1 << Qc.img(t)
    Mx = Qc.meximal()
    cands = [x for x in range(Qc.N) if E & ~Mx[x] == 0]
    # Mex Interpolation Principle (Plambeck-Siegel Cor. 5.6): a lower bound (x, D) with D <= E <= M_x
    for x in cands:
        if any(D & ~E == 0 for D in records.get(x, ())):
            phi = dict(Qc.phi)
            phi[h] = x
            log(f"  strip {h}: Phi = element {x} by mex interpolation (|Q| = {Qc.N})")
            return Quotient(Qc.mult, Qc.P, phi, gens), records, "interpolated"
    for x in cands:
        phi = dict(Qc.phi)
        phi[h] = x
        trial = Quotient(Qc.mult, Qc.P, phi, gens)
        fail, rec = trial.verify()
        if fail is None:
            log(f"  strip {h}: Phi = existing element {x} after verification (|Q| = {Qc.N}); "
                f"{len(cands)} candidate(s)")
            return trial, rec, "verified"
    # the quotient grows: free the new generator first
    phi = dict(Qc.phi)
    phi[h] = 0
    cur = Quotient(Qc.mult, Qc.P, phi, gens).recalibrate({h}, {h: (M_EXP, K_EXP)})
    fail, rec = cur.verify()
    rounds = 1
    while fail is not None:
        failc = dict(zip(reversed(gens), fail))
        involved = sorted((g for g in gens if failc.get(g, 0) > 0), reverse=True)
        log(f"    candidate |Q| = {cur.N}: least failure "
            f"{dict((g, c) for g, c in failc.items() if c)}")
        top, others = involved[0], involved[1:]
        trials = []
        for r in range(0, len(others) + 1):
            for combo in combinations(others, r):
                trials.append({top, *combo})
        accepted = False
        for bump in (0, 2, 4):
            for J in trials:
                exps = {}
                for g in J:
                    base = M_EXP if g == h else OLD_M
                    exps[g] = (max(base, failc.get(g, 0)) + bump, K_EXP if g == h else OLD_K)
                est = cur.qminus_size(J)
                for g in J:
                    est *= sum(exps[g])
                if est > LIMIT:
                    continue
                cand = cur.recalibrate(J, exps)
                f2, r2 = cand.verify()
                if f2 is None or f2 > fail:
                    log(f"    freed {sorted(J)} with (m,k) {[exps[g] for g in sorted(J)]} (|Q*| = {est})"
                        f" -> candidate |Q| = {cand.N}")
                    cur, fail, rec = cand, f2, r2
                    accepted = True
                    break
            if accepted:
                break
        if not accepted:
            raise RuntimeError(f"no recalibration within size limit made progress at strip {h}")
        rounds += 1
        if rounds > 200:
            raise RuntimeError("recalibration does not converge")
    log(f"  strip {h}: quotient grows to |Q| = {cur.N} ({rounds} recalibration round(s))")
    return cur, rec, "grew"


def presentation_summary(Q):
    return f"|Q| = {Q.N}, |P| = {sum(Q.P)}"


def main(nmax=20, out=None):
    def log(s):
        print(s, flush=True)
        if out:
            out.write(s + "\n")
            out.flush()

    # A_0 = {0}: trivial quotient
    Q = Quotient([[0]], [False], {}, [])
    records = {}
    sizes = {}
    t0 = time.time()
    for h in range(1, nmax + 1):
        if h == 2:
            sizes[2] = (Q.N, sum(Q.P))
            log(f"n = 2: strip 2 is identical to strip 1; |Q_2| = {Q.N}, |P| = {sum(Q.P)}")
            continue
        Q, records, how = extend(Q, records, h, log)
        sizes[h] = (Q.N, sum(Q.P))
        log(f"n = {h}: {presentation_summary(Q)}   [{how}]  ({time.time() - t0:.1f}s)")
    fail, _ = Q.verify()
    log(f"final full verification of Q_{nmax}: least failure = {fail}  ({time.time() - t0:.1f}s)")
    log("Phi(strip n): " + " ".join(f"{g}:{Q.phi[g]}" for g in Q.gens))
    return Q, sizes


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    with open(f"dawson/quotient_run_{n}.txt", "w") as f:
        Q, sizes = main(n, f)
    import pickle
    with open(f"dawson/quotient_Q{n}.pkl", "wb") as f:
        pickle.dump({"mult": Q.mult, "P": Q.P, "phi": Q.phi, "gens": Q.gens}, f)


def resume(pkl, nmax, logpath):
    """Continue from a saved verified quotient (e.g. dawson/quotient_Q32.pkl) up to strip nmax."""
    import pickle
    d = pickle.load(open(pkl, "rb"))
    Q = Quotient(d["mult"], d["P"], d["phi"], d["gens"])
    out = open(logpath, "w")

    def log(s):
        print(s, flush=True)
        out.write(s + "\n")
        out.flush()

    t0 = time.time()
    fail, records = Q.verify()
    log(f"loaded {pkl}: |Q| = {Q.N}, |P| = {sum(Q.P)}, re-verification least failure = {fail}")
    for h in range(max(Q.gens) + 1, nmax + 1):
        Q, records, how = extend(Q, records, h, log)
        log(f"n = {h}: {presentation_summary(Q)}   [{how}]  ({time.time() - t0:.1f}s)")
        with open(f"dawson/quotient_Q{h}.pkl", "wb") as f:
            pickle.dump({"mult": Q.mult, "P": Q.P, "phi": Q.phi, "gens": Q.gens}, f)
    return Q
