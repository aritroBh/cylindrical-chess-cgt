"""Resume solve_all.py after the 2026-10-27 reboot: finish split 4_5 from ring 420001, then 5_4 and 6_3.
Uses the same engine and per-ring loop as solve_all.py; only the start offset differs."""
import os, sys, time, collections
sys.path.insert(0, "research/c9_rings/codex")
from engine import parse_ring, make_engine
BASE, OUT = "research/c9_rings/codex/enumerated", "research/c9_rings/codex/solved"
eng = make_engine(9, True)
for split, start in (("4_5", 420000), ("5_4", 0), ("6_3", 0)):
    lines = open(os.path.join(BASE, "rings_%s.txt" % split)).read().splitlines()
    sigf = os.path.join(OUT, "sigs_%s.tsv" % split)
    if start:
        done = open(sigf).read().splitlines()
        assert len(done) == start and all(d.split("\t")[0] == r for d, r in zip(done, lines)), "prefix mismatch"
    t0, n = time.time(), len(lines)
    with open(sigf, "a" if start else "w") as fsig:
        for i in range(start, n):
            sig = eng["signature"](parse_ring(lines[i].split(), 9), 4)
            eng["wins"].cache_clear(); eng["passers"].cache_clear(); eng["terminal_winner"].cache_clear()
            fsig.write("%s\t%s\n" % (lines[i], sig))
            if (i + 1) % 10000 == 0 or i + 1 == n:
                fsig.flush(); print("split %s %d/%d elapsed=%.1f" % (split, i + 1, n, time.time() - t0), flush=True)
    hist = collections.Counter(l.split("\t")[1] for l in open(sigf).read().splitlines())
    hits2 = [l.split("\t")[0] for l in open(sigf) if l.rstrip().endswith("NNPN")]
    hits3 = [l.split("\t")[0] for l in open(sigf) if l.rstrip().endswith("NNNP")]
    with open(os.path.join(OUT, "hits_%s.txt" % split), "w") as f:
        f.write("NNPN (*2) count: %d\n" % len(hits2)); f.writelines(r + "\n" for r in hits2)
        f.write("NNNP (*3) count: %d\n" % len(hits3)); f.writelines(r + "\n" for r in hits3)
    with open(os.path.join(OUT, "summary_%s.txt" % split), "w") as f:
        f.write("split=%s rings=%d resumed_from=%d wall_seconds=%.1f\n" % (split, n, start, time.time() - t0))
        for s, c in sorted(hist.items(), key=lambda x: (-x[1], x[0])): f.write("%s\t%d\n" % (s, c))
    print("split %s done: %s" % (split, dict(hist)), flush=True)
