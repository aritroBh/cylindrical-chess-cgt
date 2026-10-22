#!/usr/bin/env python3
"""merge_chunks.py DIR : sum the '#summary' lines of DIR/c*of*.tsv and list all hits (nimber>=2)."""
import sys, glob, re, collections
d = sys.argv[1]
tot = collections.Counter(); hits = []; files = sorted(glob.glob(d + "/c*of*.tsv")); done = 0
for f in files:
    ok = False
    for line in open(f):
        if line.startswith("#summary"):
            ok = True
            for k, v in re.findall(r"(\w+)=([0-9]+)", line):
                if k not in ("cpu",): tot[k] += int(v)
        elif not line.startswith("#"):
            p = line.rstrip("\n").split("\t"); hits.append((int(p[4]), p[0], p[3], p[2]))
    done += ok
print(f"{d}: chunks finished {done}/{len(files)}  " + " ".join(f"{k}={v}" for k, v in sorted(tot.items())))
by = collections.Counter(h[0] for h in hits)
print("hits by nimber:", dict(sorted(by.items())))
for h in sorted(hits, reverse=True):
    if h[0] >= 3: print("NIM%d\t%s\toutcome=%s\tpawns=%s" % h)
