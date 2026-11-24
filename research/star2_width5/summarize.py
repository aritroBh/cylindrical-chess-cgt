#!/usr/bin/env python3
"""Summarize the T21 scope: flat width 5, exactly 8 pawns, all nine settings.

Reads the per-split TSV files produced by frontier_split and prints, per file,
the *k >= 2 hits with their settings, plus the counts of *2 and *3 by setting.
"""
import argparse
import collections
import csv
import gzip
import os
import sys

SETTING = ("C/T", "C/off", "C/aware", "M/T", "M/off", "M/aware", "O/T", "O/off", "O/aware")
# The brief's headline setting: count race rule, e.p. on, e.p.-aware passed test.
HEADLINE = 2  # index into row[3:12]


def fits_trabuchet(position):
    """The brief's geometry test: the pawn-file span must fit files a..e."""
    files = [ord(sq[0]) - ord("a") for sq in position.replace("W:", "").replace("B:", "").split()
             if len(sq) >= 2 and sq[0].isalpha() and sq[1].isdigit()]
    return bool(files) and max(files) - min(files) <= 4


def read_rows(path):
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", newline="") as stream:
        for row in csv.reader(stream, delimiter="\t"):
            if not row or row[0].startswith("#"):
                continue
            yield row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    per_setting = collections.Counter()      # (setting, k) -> count
    hits = collections.defaultdict(set)       # (k, position) -> set of settings
    total_rows = 0
    maxnim = -1
    seen_positions = set()
    for path in args.files:
        rows = 0
        for row in read_rows(path):
            rows += 1
            total_rows += 1
            seen_positions.add(row[0])
            for setting, field in enumerate(row[3:12]):
                k = int(field.split(",", 1)[1])
                maxnim = max(maxnim, k)
                if k >= 2:
                    per_setting[(setting, k)] += 1
                    hits[(k, row[0])].add(setting)
        print(f"{path}: roots={rows}")

    print(f"TOTAL roots={total_rows} distinct positions={len(seen_positions)} maximum nimber seen={maxnim}")
    print("counts by setting (position-setting hits):")
    for setting in range(9):
        c2 = per_setting[(setting, 2)]
        c3 = per_setting[(setting, 3)]
        c4 = sum(v for (s, k), v in per_setting.items() if s == setting and k >= 4)
        print(f"  {SETTING[setting]:8s} *2={c2:4d}  *3={c3:4d}  *k>=4={c4:4d}")

    for k in sorted({key[0] for key in hits}):
        keys = [key for key in sorted(hits) if key[0] == k]
        robust = sum(len(hits[key]) == 9 for key in keys)
        print(f"*{k}: {len(keys)} positions; robust across all 9 settings={robust}")
        for _, position in keys:
            names = ",".join(SETTING[i] for i in sorted(hits[(k, position)]))
            print(f"  settings={names}; trébuchet-fit={'yes' if fits_trabuchet(position) else 'no'}; {position}")

    headline = [(k, p) for (k, p), s in hits.items() if HEADLINE in s]
    print(f"count/e.p.-aware hits with k>=2: {len(headline)}")
    for k, position in sorted(headline):
        print(f"  *{k}: {position}")

    # machine-readable dump for the verification step
    with open(os.path.join(os.path.dirname(os.path.abspath(args.files[0])), "hits.tsv"), "w") as out:
        out.write("k\tsettings\tposition\n")
        for (k, position), settings in sorted(hits.items()):
            out.write(f"{k}\t{','.join(SETTING[i] for i in sorted(settings))}\t{position}\n")


if __name__ == "__main__":
    main()
