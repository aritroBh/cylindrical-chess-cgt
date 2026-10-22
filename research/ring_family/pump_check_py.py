import sys
sys.path.insert(0, "research/ring_family")
import pump_check as pc
from reduced_py import reduced_edges
name = sys.argv[1]; kmin, kmax = int(sys.argv[2]), int(sys.argv[3])
prev = None
for k in range(kmin, kmax + 1):
    ring = pc.fam(name, k)
    edges = sorted(reduced_edges(ring))
    if prev is not None:
        n = len(ring); p = n // 2 - 1; inter = {}
        for f in (p, p + 1):
            a, b = ring[f]; inter[f] = ("W", a[0]) if a else ("B", b[0])
        img = pc.image([list(e) for e in edges], inter, n)
        ok = img == set(prev)
        print(f"[python/cylcgt] {name}: k{k} (C{n}) --delete files {p},{p+1}--> equals reduced graph of k{k-1}? {ok}  ({len(edges)} edges)", flush=True)
    prev = [tuple(e) for e in edges]
