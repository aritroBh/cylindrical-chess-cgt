"""fverify.py NAME m_lo m_hi : reduced graph (rgraph.py of research/mobius_rings_proof) of a candidate *3 family on
the strip, per m: nodes / K-edges / T-moves, flagged nodes, nodes with a passer, zone, signature h=0..4; for each step
m-1 -> m the insertion test ins_c(R_{m-1}) = R_m for every cut c with files c, c+1 in the block, and the
Lemma-3-admissible cuts (arc c-4..c+5 inside the block, a chart interval, disjoint from the zone)."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mobius_rings_proof'))
sys.setrecursionlimit(1000000)
import rgraph
from fgame import FBoard
rgraph.Board = FBoard
from rgraph import reduced, solve, stats, iso, ins
FAMS = {
  'TT':  (lambda m: 'B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2' + ' B4 W2' * m, lambda m: (10, 2 * m)),
  'SS':  (lambda m: 'B6 W3' + ' W2 B4' * m + ' W6B7 W3 B7 B6 W3 W2 B6 W2 B4', lambda m: (2, 2 * m)),
  'E2':  (lambda m: 'B5 W3' + ' W2 B4' * m + ' W2 W4 B7 B7 W3 W2 W2B7 B7', lambda m: (2, 2 * m + 1)),
  'H2':  (lambda m: 'B5 W3' + ' W2 B4' * m + ' W4 B7 B7 W3 W2 W2B7 B7', lambda m: (2, 2 * m)),
  'H4':  (lambda m: 'B5 W3 W4 B7' + ' W2 B4' * m + ' B7 W3 W2 W2B7 B7', lambda m: (4, 2 * m)),
  # name: (ring(m), block(m) = (first file, length))
  'G6':  (lambda m: 'B7 W4 W23 B5 W3B7 W4B7' + ' W2 B4' * m, lambda m: (6, 2 * m)),
  'G6b': (lambda m: 'B7 W4 W23 B5 W3B7 W4B7' + ' W3 B5' * m, lambda m: (6, 2 * m)),
  'G5':  (lambda m: 'B67 W4 W2B6 W2B5' + ' B6 W4' * m + ' W5B7', lambda m: (4, 2 * m)),
  'G5b': (lambda m: 'B67 W4 W2B6 W2B5 W5B7' + ' W4 B6' * m, lambda m: (5, 2 * m)),
}
def main():
    name, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    R, BL = FAMS[name]; prev = None
    for m in range(lo, hi + 1):
        t = time.time(); ring = R(m)
        B, root, nodes = reduced(ring)
        st = stats(nodes, root); sig = solve(nodes, root, 4)
        npass = sum(1 for p in nodes if B.passers(p, 0) or B.passers(p, 1))
        b0, bl = BL(m); n = len(root[0])
        print('m=%d n=%d ring=[%s] nodes=%d Kedges=%d Tmoves=%d flagged=%d passer_nodes=%d zone=%s sig=%s (%.1fs)'
              % (m, n, ring, st['nodes'], st['K'], st['T'], st['flagged'], npass, st['zone'], sig, time.time() - t), flush=True)
        if prev is not None:
            pm, pnodes, proot, pst, pb0, pbl = prev
            ok, bad = [], []
            for c in range(pb0, pb0 + pbl - 1):
                if ins(proot, c) != root: continue
                r, why = iso(pnodes, proot, nodes, root, c)
                (ok if r else bad).append(c if r else (c, why))
            adm = [c for c in range(pb0 + 4, pb0 + pbl - 5) if c - 4 >= 0 and c + 5 <= len(proot[0]) - 1
                   and not set(range(c - 4, c + 6)) & set(pst['zone'])]
            print('  step %d->%d: iso for c in %s; fails %s; Lemma-3-admissible cuts (at m=%d) %s' % (pm, m, ok, bad, pm, adm), flush=True)
        prev = (m, nodes, root, st, b0, bl)
main()
