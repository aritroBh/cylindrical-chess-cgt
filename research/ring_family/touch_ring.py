import sys, subprocess, re
sys.path.insert(0, "research/ring_family")
from ringlib import *
from touched import touched
def edges_of(ring, path="/tmp/tr.tsv"):
    n = len(ring)
    p = subprocess.run(["research/ring_family/ringeval_w", "--width", str(n), "--reduced", path, "--max-entries", "4194304", "--rg-cap", "200000"], input=to_text(ring) + "\n", capture_output=True, text=True)
    last = p.stdout.strip().split("\n")[-1]
    return [l.rstrip("\n").split("\t") for l in open(path)], last
for c in sys.argv[1:]:
    ring = from_cstr(c)
    edges, last = edges_of(ring)
    t, m = touched(edges)
    toks = cstr(ring).split()
    print(f"C{len(ring)} {c}")
    print("   ", last)
    print("    touched:", " ".join((f"[{toks[i]}]" if i in t else toks[i]) for i in range(len(ring))))
