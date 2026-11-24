#!/usr/bin/env python3
"""Aggregate scan results from summary files."""

import os
import glob

TMP_DIR = "research/star3_hunt/analysis_tmp"

SETTINGS = ["C/T", "C/off", "C/aware", "M/T", "M/off", "M/aware", "O/T", "O/off", "O/aware"]

GROUPS = [
    ("Flat width 4, 8 pawns", "flat_w4p8_"),
    ("Flat width 4, 9 pawns", "flat_w4p9_"),
    ("Flat width 5, 9 pawns (4+5,5+4 skipped)", "flat_w5p9_"),
    ("Flat width 6, 7 pawns", "flat_w6p7_"),
    ("Flat width 6, 8 pawns", "flat_w6p8_"),
    ("Cylinder C3, 6-8 pawns", "cylinder_w3p"),
    ("Cylinder C4, 6-8 pawns", "cylinder_w4p"),
    ("Cylinder C5, 7-9 pawns (4+5 for 9 skipped)", "cylinder_w5p"),
    ("Cylinder C6, 7-8 pawns", "cylinder_w6p"),
]

def aggregate_group(pattern):
    """Aggregate all summary files matching pattern."""
    total_roots = 0
    star2 = {s: 0 for s in SETTINGS}
    star3plus = {s: 0 for s in SETTINGS}
    max_nimber = {s: 0 for s in SETTINGS}
    
    files = glob.glob(os.path.join(TMP_DIR, f"{pattern}*.summary"))
    for f in files:
        with open(f) as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                if '=' not in line:
                    continue
                key, value = line.split('=', 1)
                if key == "TOTAL":
                    total_roots += int(value)
                elif key in SETTINGS:
                    s2, s3p, mn = map(int, value.split(','))
                    star2[key] += s2
                    star3plus[key] += s3p
                    if mn > max_nimber[key]:
                        max_nimber[key] = mn
    
    return {
        "total_roots": total_roots,
        "star2": star2,
        "star3plus": star3plus,
        "max_nimber": max_nimber,
    }

def print_group_details(name, pattern):
    result = aggregate_group(pattern)
    print(f"=== {name} ===")
    print(f"Total roots: {result['total_roots']:,}")
    print(f"{'Setting':<10} {'Roots':>12} {'*2':>6} {'*3+':>6} {'Max*':>6}")
    print(f"{'-'*10} {'-'*12} {'-'*6} {'-'*6} {'-'*6}")
    for s in SETTINGS:
        print(f"{s:<10} {result['total_roots']:>12,} {result['star2'][s]:>6} {result['star3plus'][s]:>6} {result['max_nimber'][s]:>6}")
    print()

def main():
    # Markdown summary table
    print("## Summary Table")
    print()
    header = "| Scan | Total Roots | " + " | ".join([f"{s} (*2/*3+/max)" for s in SETTINGS]) + " |"
    print(header)
    print("|" + "---|" * (2 + len(SETTINGS)))
    
    for name, pattern in GROUPS:
        result = aggregate_group(pattern)
        row = f"| {name} | {result['total_roots']:,} |"
        for s in SETTINGS:
            row += f" {result['star2'][s]}/{result['star3plus'][s]}/{result['max_nimber'][s]} |"
        print(row)
    
    print()
    print("## Detailed per-scan breakdown")
    print()
    
    for name, pattern in GROUPS:
        print_group_details(name, pattern)

if __name__ == "__main__":
    main()