import sys, glob, re, collections
d = sys.argv[1]
rows = 0; roots = 0; states = 0; hits = []; hist = collections.Counter(); s2 = s3 = dh = 0; mx = -1
files = sorted(glob.glob(d + "/c*of*.summary.txt"), key=lambda f: int(re.search(r"/c(\d+)of", f).group(1)))
for f in files:
    for line in open(f):
        p = line.rstrip("\n").split("\t")
        if p[0] == "rows" and len(p) > 1 and p[1] != "": rows += int(p[1])
        elif p[0] == "default_star2": s2 += int(p[1])
        elif p[0] == "default_star3plus": s3 += int(p[1])
        elif p[0] == "default_setting_hits": dh += int(p[1])
        elif p[0] == "set":
            m = re.search(r"max_nimber=(-?\d+)", line); mx = max(mx, int(m.group(1)))
        elif p[0] == "outcome_hist_default":
            for tok in (p[1].split() if len(p) > 1 else []):
                k, v = tok.split(":"); hist[k] += int(v)
    base = f[:-len(".summary.txt")]
    hits += [l.rstrip("\n") for l in open(base + ".hits.tsv")]
    for l in open(base + ".log"):
        m = re.search(r"roots=(\d+) sampled=\d+ states=(\d+)", l)
        if m: roots += int(m.group(1)); states += int(m.group(2))
print("subchunks", len(files), "rows", rows, "roots(log)", roots, "states_sum", states)
print("default_setting_hits", dh, "default_star2", s2, "default_star3plus", s3, "max_nimber", mx)
print("outcome_hist_default", " ".join("%s:%d" % kv for kv in sorted(hist.items())))
print("hits", len(hits))
for h in hits: print(h)
