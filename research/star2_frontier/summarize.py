#!/usr/bin/env python3
"""Summarize nimber hits from frontier TSV or TSV.gz output."""
import argparse
import collections
import csv
import gzip

SETTING = ("C/T", "C/off", "C/aware", "M/T", "M/off", "M/aware", "O/T", "O/off", "O/aware")


def fits_trabuchet(position):
    files = [ord(sq[0]) - ord("a") for sq in position.replace("W:", "").replace("B:", "").split()
             if len(sq) >= 2 and sq[0].isalpha() and sq[1].isdigit()]
    return bool(files) and max(files) - min(files) <= 4


assert fits_trabuchet("W: a2 / B: e7")
assert not fits_trabuchet("W: a2 / B: f7")


def summarize(path):
    opener = gzip.open if path.endswith(".gz") else open
    hits = collections.defaultdict(set)
    rows, maxnim = 0, -1
    with opener(path, "rt", newline="") as stream:
        for row in csv.reader(stream, delimiter="\t"):
            if not row or row[0].startswith("#"):
                continue
            rows += 1
            for setting, field in enumerate(row[3:12]):
                k = int(field.split(",", 1)[1])
                maxnim = max(maxnim, k)
                if k >= 2:
                    hits[(k, int(row[2]), int(row[1]), row[0])].add(setting)
    print(f"{path}: roots={rows}, maximum nimber seen={maxnim}")
    for k in sorted({hit[0] for hit in hits}):
        rows_k = [hit for hit in sorted(hits) if hit[0] == k]
        robust = sum(len(hits[hit]) == 9 for hit in rows_k)
        print(f"*{k}: {len(rows_k)} positions; robust across all 9 settings={robust}")
        for _, pawns, width, position in rows_k:
            names = ",".join(SETTING[i] for i in sorted(hits[(k, pawns, width, position)]))
            print(f"  {pawns} pawns; settings={names}; trébuchet-fit={'yes' if fits_trabuchet(position) else 'no'}; {position}")
    print(f"total *k>=2 position-setting hits={sum(map(len, hits.values()))}; *3={sum(k == 3 for k, *_ in hits)}; *4={sum(k == 4 for k, *_ in hits)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    for filename in parser.parse_args().files:
        summarize(filename)
