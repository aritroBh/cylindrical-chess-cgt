"""verify.py FAM m_lo m_hi [--cyl]
For each m: reduced graph R_m of FAM(m) on the Moebius strip (or the cylinder with --cyl, control), its size,
zone, flags, passers, signature (h = 0..4); then for each step m -> m+1 the insertion test ins_c(R_m) = R_{m+1}
for every cut c with files c, c+1 inside the block, and whether c is admissible for Lemma 3 (the arc c-4..c+5
lies inside the block, avoids the zone, and every file of it is an exact pattern file in every node)."""
import sys, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rgraph import FAM, BLOCK, reduced, solve, stats, iso, ins
from mgame import fmt

def main():
    fam, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); twist = '--cyl' not in sys.argv
    print('# family %s  %s  m = %d..%d' % (fam, 'MOEBIUS' if twist else 'CYLINDER (control)', lo, hi), flush=True)
    prev = None
    for m in range(lo, hi + 1):
        t = time.time(); ring = FAM[fam](m)
        B, root, nodes = reduced(ring, twist)
        st = stats(nodes, root); sig = solve(nodes, root, 4)
        npass = sum(1 for p in nodes if B.passers(p, 0) or B.passers(p, 1))
        b0, bl = BLOCK[fam](m); n = len(root[0])
        print('m=%d n=%d ring=[%s] nodes=%d Kedges=%d Tmoves=%d Tpairs=%d flagged=%d passer_nodes=%d zone=%s sig=%s (%.1fs)'
              % (m, n, ring, st['nodes'], st['K'], st['T'], st['Tpairs'], st['flagged'], npass, st['zone'], sig,
                 time.time() - t), flush=True)
        if prev is not None:
            pm, pnodes, proot, pst, pb0, pbl = prev
            ok, bad = [], []
            for c in range(pb0, pb0 + pbl - 1):           # files c, c+1 inside the block of FAM(m-1)
                if ins(proot, c) != root: continue
                r, why = iso(pnodes, proot, nodes, root, c)
                (ok if r else bad).append(c if r else (c, why))
            adm = [c for c in range(pb0 + 4, pb0 + pbl - 5)
                   if not set(range(c - 4, c + 6)) & set(pst['zone'])]
            print('  step %d->%d: ins_c(root)=root and isomorphism for c in %s; fails for %s; Lemma-3-admissible cuts %s'
                  % (pm, m, ok, bad, adm), flush=True)
        prev = (m, nodes, root, st, b0, bl)

if __name__ == '__main__':
    main()
