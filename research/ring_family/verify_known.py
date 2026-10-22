import sys, time, resource
sys.path.insert(0, "research/ring_family")
from rf import *
from known import KNOWN
maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 5
for n in range(3, maxn + 1):
    seen = set()
    for t in KNOWN[n]:
        c = canon_pos(t, n)
        if c in seen: continue
        seen.add(c)
        t0 = time.time()
        g = val(c, n, whole=False)
        t1 = time.time()
        print(f"C{n} {c} -> {sh(g)}   ({t1-t0:.1f}s, rss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20:.2f} GB)", flush=True)
