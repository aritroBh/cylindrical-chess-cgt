#!/usr/bin/env python3
"""coverage.py : table of every scan in scans/ (single-component roots) and the totals of le8/ (<= 8 pawns, all roots)."""
import glob, re, os, collections
rows = []
for d in sorted(glob.glob("scans/*")):
    tot = collections.Counter(); chunks = 0; done = 0
    for f in glob.glob(d + "/c*of*.tsv"):
        chunks += 1
        for line in open(f):
            if line.startswith("#summary"):
                done += 1
                for k, v in re.findall(r"(\w+)=([0-9]+)", line):
                    if k != "cpu": tot[k] += int(v)
    rows.append((os.path.basename(d), f"{done}/{chunks}", tot["roots"], tot["states"], tot["nim1"], tot["nim2"], tot["nim3"] + sum(tot[f"nim{k}"] for k in range(4, 9))))
print("scan\tchunks\troots\tstates\t*1\t*2\t*3+")
for r in rows: print("\t".join(map(str, r)))
tot = collections.Counter(); n = 0
for f in glob.glob("le8/*.tsv"):
    for line in open(f):
        if line.startswith("#summary"):
            n += 1
            for k, v in re.findall(r"(\w+)=([0-9]+)", line):
                if k != "cpu": tot[k] += int(v)
print(f"le8 (<=8 pawns, flat widths 1-8 + rings C3-C8, nw<=nb)\t{n} runs\t{tot['roots']}\t{tot['states']}\t{tot['nim1']}\t{tot['nim2']}\t{sum(tot[f'nim{k}'] for k in range(3,9))}")
