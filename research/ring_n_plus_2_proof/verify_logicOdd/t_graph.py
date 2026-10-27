"""C1 with the fresh engine D: reduced graph of R_n / Qo_n, odd n: nodes, K and T counts, flags, passers, zone, 'pattern files 2..n-8 in every node', signature."""
import sys, time
from common import *

def run(fam, n, hs=(0, 1, 2, 3, 4)):
    t0 = time.time()
    start = parse(TOKS[fam](n))
    order, edges = build(start)
    K = sum(len(edges[(nd, s)][1]) for nd in order for s in 'WB')
    T = 0
    for nd in order:
        for s in 'WB':
            T += sum(1 for c, *_ in classify(nd[0], nd[1], s) if c == 'T')
    flagged = sum(1 for nd in order if nd[1] is not None)
    pas = sum(1 for nd in order if passed_list(nd[0], nd[1], 'W') or passed_list(nd[0], nd[1], 'B'))
    zone = sorted({j for nd in order for j in range(n) if nd[0][j] != start[j]})
    patok = all(nd[0][j] == pat(j) for nd in order for j in range(2, n - 7))
    sig = solve_sig(order, edges, hs)
    print(f'{fam}_{n}: nodes={len(order)} K={K} T={T} flagged={flagged} passers={pas} zone={zone} files2..{n-8}_exact_pattern={patok} sig={sig} ({time.time()-t0:.0f}s)', flush=True)
    return order, edges

if __name__ == '__main__':
    fam = sys.argv[1]
    for n in map(int, sys.argv[2:]):
        run(fam, n)
        engineD._cache.clear()
