"""Pump with engine D: graph_{n+2} == ins_c(graph_n) (nodes, K-edges, T-flags) for odd n, with the cut c; also prints which cuts work.
usage: t_pump.py FAM c n_lo n_hi   (n_lo, n_hi odd; steps n -> n+2)"""
import sys, time
from common import *

def graph(fam, n):
    start = parse(TOKS[fam](n))
    order, edges = build(start)
    return start, order, edges

def compare(fam, n, c):
    s1, o1, e1 = graph(fam, n)
    s2, o2, e2 = graph(fam, n + 2)
    ok_start = ins(s1, c) == s2
    img = {nd: ins_nd(nd, c) for nd in o1}
    ok_nodes = set(img.values()) == set(o2) and len(set(img.values())) == len(o1)
    ok_edges = True
    if ok_nodes:
        for nd in o1:
            for s in 'WB':
                hT, ks = e1[(nd, s)]
                hT2, ks2 = e2[(img[nd], s)]
                if hT != hT2 or {img[k] for k in ks} != set(ks2):
                    ok_edges = False
    else:
        ok_edges = False
    return ok_start, ok_nodes, ok_edges, len(o1), len(o2)

if __name__ == '__main__':
    fam, c, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    for n in range(lo, hi + 1, 2):
        t0 = time.time()
        r = compare(fam, n, c)
        print(f'{fam} n={n}->{n+2} cut c={c}: start->start {r[0]}, nodes onto {r[1]} ({r[3]}->{r[4]}), K-edges and T-flags equal {r[2]}  ({time.time()-t0:.0f}s)', flush=True)
        engineD._cache.clear()
