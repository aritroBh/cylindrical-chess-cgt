#!/usr/bin/env python3
"""Aggregate results/*.mob1.out (all chunks of an (n, P) job must be present and C1 == C2) into
results/summary.tsv, results/histograms.tsv and results/hits_all.txt.  Run in research/mobius_rings."""
import glob, re, collections, os, subprocess
jobs = collections.defaultdict(lambda: {"chunks": {}, "K": None})
for f in sorted(glob.glob("results/n*_p*_c*of*.mob1.out")):
    m = re.match(r"results/n(\d+)_p(\d+)_c(\d+)of(\d+)\.mob1\.out", f)
    n, p, i, k = map(int, m.groups())
    c2 = f.replace("mob1", "mob2")
    def ck(path): return subprocess.run("zstd -dc -q %s | cksum" % path, shell=True, capture_output=True, text=True).stdout
    agree = (os.path.exists(c2) and os.path.exists(f.replace(".out", ".done")) and os.path.exists(c2.replace(".out", ".done"))
             and open(f).read() == open(c2).read() and ck(f.replace(".out", ".sig.zst")) == ck(c2.replace(".out", ".sig.zst")))
    J = jobs[(n, p)]; J["K"] = k; J["chunks"][i] = (f, agree)

def kappa_orbit_split(ring):
    """number of {id, mirror}-orbits (colours not exchanged) inside the {id, mirror, kappa, mirror*kappa}-orbit of a ring"""
    toks = ring.split()
    def parse(t):
        w = re.search(r"W(\d+)", t); b = re.search(r"B(\d+)", t)
        return (frozenset(int(x) for x in (w.group(1) if w else "")), frozenset(int(x) for x in (b.group(1) if b else "")))
    cfg = [parse(t) for t in toks]
    kap = [(frozenset(9 - r for r in b), frozenset(9 - r for r in w)) for (w, b) in cfg]
    return 1 if (kap == cfg or kap == cfg[::-1]) else 2

hist_rows, summ_rows, all_hits = [], [], []
for (n, p), J in sorted(jobs.items()):
    if len(J["chunks"]) != J["K"]: continue
    hist = collections.Counter(); hits = []; rings = 0; ok = True
    for i, (f, agree) in sorted(J["chunks"].items()):
        ok &= agree
        for line in open(f):
            a = line.split(None, 2)
            if a[0] == "HIST": hist[a[1]] += int(a[2])
            elif a[0] == "RINGS": rings += int(a[1])
            elif a[0] == "HIT": hits.append((a[1], a[2].strip()))
    s2 = [r for s, r in hits if s == "NNPN"]; s3 = [r for s, r in hits if s == "NNNP"]
    summ_rows.append((n, p, rings, len(s2), len(s3), sum(kappa_orbit_split(r) for r in s2), sum(kappa_orbit_split(r) for r in s3),
                      "C1=C2" if ok else "C1 only"))
    for sg, c in sorted(hist.items(), key=lambda x: -x[1]): hist_rows.append((n, p, sg, c))
    for s, r in hits: all_hits.append((n, p, s, r))
with open("results/summary.tsv", "w") as o:
    o.write("n\tpawns\trings(orbits)\tstar2_orbits\tstar3_orbits\tstar2_colour-distinct\tstar3_colour-distinct\tlabel\n")
    for r in summ_rows: o.write("\t".join(map(str, r)) + "\n")
with open("results/histograms.tsv", "w") as o:
    o.write("n\tpawns\tsignature(h=0..3)\trings\n")
    for r in hist_rows: o.write("\t".join(map(str, r)) + "\n")
with open("results/hits_all.txt", "w") as o:
    for n, p, s, r in all_hits:
        w = sum(len(x) for x in re.findall(r"W(\d+)", r)); b = sum(len(x) for x in re.findall(r"B(\d+)", r))
        o.write("n=%d pawns=%d split=%d+%d %s %s\n" % (n, p, w, b, s, r))
print(open("results/summary.tsv").read())
