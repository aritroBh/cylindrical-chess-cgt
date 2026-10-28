"""Solve every enumerated 9-pawn C9 root ring with the independent engine."""
import os, time, collections

BASE = "research/c9_rings/codex/enumerated"
OUT = "research/c9_rings/codex/solved"
os.makedirs(OUT, exist_ok=True)

from engine import parse_ring, make_engine

SPLITS = [("3_6", "rings_3_6.txt"),
          ("4_5", "rings_4_5.txt"),
          ("5_4", "rings_5_4.txt"),
          ("6_3", "rings_6_3.txt")]

eng = make_engine(9, True)
t_global = time.time()
grand = collections.Counter()

for split, fname in SPLITS:
    path = os.path.join(BASE, fname)
    out_sig = os.path.join(OUT, "sigs_%s.tsv" % split)
    out_hits = os.path.join(OUT, "hits_%s.txt" % split)
    lines = open(path).read().splitlines()
    hist = collections.Counter()
    hits2 = []
    hits3 = []
    buf = []
    t0 = time.time()
    n = len(lines)
    with open(out_sig, "w") as fsig, open(out_hits, "w") as fhit:
        for i, ring in enumerate(lines, 1):
            pos = parse_ring(ring.split(), 9)
            sig = eng["signature"](pos, 4)
            eng["wins"].cache_clear()
            eng["passers"].cache_clear()
            eng["terminal_winner"].cache_clear()
            hist[sig] += 1
            grand[sig] += 1
            if sig == "NNPN":
                hits2.append(ring)
            if sig == "NNNP":
                hits3.append(ring)
            buf.append("%s\t%s\n" % (ring, sig))
            if len(buf) >= 5000:
                fsig.writelines(buf)
                buf.clear()
            if i % 10000 == 0 or i == n:
                fsig.flush()
                elapsed = time.time() - t0
                rate = i / elapsed if elapsed else 0
                print("split %s %d/%d sigs=%s elapsed=%.1f rate=%.1f/s" %
                      (split, i, n, dict(hist), elapsed, rate), flush=True)
        if buf:
            fsig.writelines(buf)
            buf.clear()
        # write hits
        fhit.write("NNPN (*2) count: %d\n" % len(hits2))
        for r in hits2:
            fhit.write(r + "\n")
        fhit.write("NNNP (*3) count: %d\n" % len(hits3))
        for r in hits3:
            fhit.write(r + "\n")
    # summary file
    with open(os.path.join(OUT, "summary_%s.txt" % split), "w") as f:
        f.write("split=%s rings=%d wall_seconds=%.1f\n" % (split, n, time.time() - t0))
        for sig, c in sorted(hist.items(), key=lambda x: (-x[1], x[0])):
            f.write("%s\t%d\n" % (sig, c))
    print("split %s done: %s" % (split, dict(hist)), flush=True)

with open(os.path.join(OUT, "grand_summary.txt"), "w") as f:
    f.write("total_rings=%d wall_seconds=%.1f\n" % (sum(1 for _ in []), time.time() - t_global))
    # recompute total
    total = sum(grand.values())
    f.write("total_rings=%d wall_seconds=%.1f\n" % (total, time.time() - t_global))
    for sig, c in sorted(grand.items(), key=lambda x: (-x[1], x[0])):
        f.write("%s\t%d\n" % (sig, c))
print("GRAND", dict(grand), "elapsed", time.time() - t_global)
