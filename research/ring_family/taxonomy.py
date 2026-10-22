import sys, subprocess
sys.path.insert(0, "research/ring_family")
from ringlib import *
from known import KNOWN
from touched import touched
def analyse(ring):
    n = len(ring)
    p = subprocess.run(["nice", "-n", "15", "research/ring_family/ringeval_w", "--width", str(n), "--reduced", "/tmp/tax.tsv", "--no-solve", "--max-entries", "1048576", "--rg-cap", "300000"],
                       input=to_text(ring) + "\n", capture_output=True, text=True)
    last = p.stdout.strip().split("\n")[-1]
    edges = [l.rstrip("\n").split("\t") for l in open("/tmp/tax.tsv")]
    t, m = touched(edges)
    nodes = int(last.split("nodes=")[1].split()[0])
    return t, nodes, "OVERFLOW" in last
for n in (5, 6, 7):
    seen = []
    for t in KNOWN[n]:
        c = canon(to_ring(t, n))
        if c not in seen: seen.append(c)
    for c in seen:
        res = evaluate([c])[0]
        if res[:2] != ("N", 2): continue
        t, nodes, ov = analyse(c)
        toks = cstr(c).split()
        print(f"C{n} nodes={nodes}{'+' if ov else ''} frozen files={n-len(t)}: " + " ".join((f"[{toks[i]}]" if i in t else toks[i]) for i in range(n)))
