"""Paper Proposition 6 (h = 1, boards with >= 6 ranks): in a chess-legal context with no passed pawn, no pawn stands on the
penultimate rank, hence the defender cannot promote in one move.  Exhaustive over small boards, e.p.-aware test, with every
e.p. right that a legal last double step can leave.  Also prints the H = 5 counterexample (the repository's 'H >= 5').
Run: python3 notes/proof_audit2/checks/prop6_check.py
"""
import itertools, sys
sys.path.insert(0, "notes/proof_audit2/checks")
import indep_sum_model as M

def check(files, ranks, wrap, maxp, aware):
    M.configure(files, ranks, wrap, True, "count", aware)
    sq = [(f, r) for f in range(files) for r in range(2, ranks)]    # chess-legal pawn squares (ranks 2..ranks-1)
    bad = []; n = 0
    for nw in range(0, maxp + 1):
        for nb in range(0, maxp + 1):
            if nw + nb == 0: continue
            for W in itertools.combinations(sq, nw):
                for B in itertools.combinations([s for s in sq if s not in W], nb):
                    Wf, Bf = frozenset(W), frozenset(B)
                    # candidate e.p. rights: a pawn that has just double-stepped (landing rank 4 for W, ranks-3 for B)
                    rights = [None]
                    for (f, r) in W:
                        if r == 4 and (f, 3) not in Wf | Bf: rights.append(((f, 3), (f, 4), 'B'))
                    for (f, r) in B:
                        if r == ranks - 3 and (f, ranks - 2) not in Wf | Bf: rights.append(((f, ranks - 2), (f, r), 'W'))
                    for ep in rights:
                        n += 1
                        if M.passed(Wf, Bf, ep, 'W') or M.passed(Wf, Bf, ep, 'B'):
                            continue
                        pen_w = [p for p in W if p[1] == ranks - 1]
                        pen_b = [p for p in B if p[1] == 2]
                        if pen_w or pen_b:
                            bad.append((sorted(W), sorted(B), ep))
    return n, bad

for ranks in (5, 6, 7):
    for aware in (True, False):
        n, bad = check(4, ranks, False, 2, aware)
        print(f"flat 4 files, {ranks} ranks, e.p.-aware={aware}: {n} (position, right) pairs, "
              f"violations of Prop.6 = {len(bad)}", ("e.g. " + str(bad[0])) if bad else "")
