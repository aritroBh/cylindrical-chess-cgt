"""Independent check that no 2-component position with <= 5 pawns (2+2 or 2+3;
a lone pawn is always passed) has a nimber value *k, k >= 2, under a given
setting.  Uses the exact sum-model solver of indep_scan.py on a flat strip
A | empty file | B.  (Cylinder non-ring components are flat segments, so this
also covers cylinders.)

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python -I verify/cylatlas/C5-reproduce/indep_pairs.py count/1
"""
import os, sys, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_scan as S

def atoms_list(maxw, npawns):
    out = []
    for n in range(1, maxw + 1):
        S.CFG.clear(); S.CFG.update(n=n, wrap=False, ep=True, rule="count")
        for W, B in S.atoms(n, False, npawns):
            Wf, Bf = frozenset(W), frozenset(B)
            if S.has_passer("W", Wf, Bf) or S.has_passer("B", Wf, Bf):
                continue
            out.append((n, W, B))
    return out

if __name__ == "__main__":
    rule, ep = sys.argv[1].split("/"); ep = ep == "1"
    A2 = atoms_list(2, 2)
    A3 = atoms_list(3, 3)
    t0 = time.time(); tested = 0; hits = []
    for (na, Wa, Ba) in A2:
        for (nb, Wb, Bb) in A2 + A3:
            n = na + 1 + nb
            S.CFG.clear(); S.CFG.update(n=n, wrap=False, ep=ep, rule=rule)
            for f in (S.comp_children, S.can_produce, S.wins):
                f.cache_clear()
            sh = na + 1
            ca = S.comp_key(Wa, Ba, None)
            cb = S.comp_key([(f + sh, r) for f, r in Wb], [(f + sh, r) for f, r in Bb], None)
            comps = tuple(sorted((ca, cb)))
            lf, rf = S.wins(comps, 0, S.ZERO, "W"), S.wins(comps, 0, S.ZERO, "B")
            tested += 1
            if lf and rf:
                for k in range(2, 6):
                    X = S.NIMS[k]
                    if not S.wins(comps, 0, X, "W") and not S.wins(comps, 0, X, "B"):
                        hits.append((k, S.fmt(Wa, Ba), S.fmt(Wb, Bb)))
    print(f"{rule}/ep{int(ep)}: 1v1 atoms={len(A2)}, 3-pawn atoms={len(A3)}, pairs tested={tested}, "
          f"nimber k>=2 hits={hits} ({time.time()-t0:.0f}s)")
