#!/usr/bin/env python3
"""Analyze all TSV scan results and generate summary table."""

import os
import re
from collections import defaultdict
from pathlib import Path

OUT_DIR = Path("research/star3_hunt")

# Setting names corresponding to the 9 columns in TSV
SETTINGS = [
    "count/epon",
    "count/epoff",
    "count/epon/aware",
    "mover/epon",
    "mover/epoff",
    "mover/epon/aware",
    "opponent/epon",
    "opponent/epoff",
    "opponent/epon/aware",
]

# Short names for the table
SHORT_SETTINGS = [
    "C/T", "C/off", "C/aware",
    "M/T", "M/off", "M/aware",
    "O/T", "O/off", "O/aware",
]

# Scan groups as defined in the task
SCAN_GROUPS = [
    ("Flat width 4, 8 pawns", "flat_w4p8"),
    ("Flat width 4, 9 pawns", "flat_w4p9"),
    ("Flat width 5, 9 pawns", "flat_w5p9"),
    ("Flat width 6, 7 pawns", "flat_w6p7"),
    ("Flat width 6, 8 pawns", "flat_w6p8"),
    ("Cylinder C3, 6-8 pawns", "cylinder_w3p"),
    ("Cylinder C4, 6-8 pawns", "cylinder_w4p"),
    ("Cylinder C5, 7-9 pawns", "cylinder_w5p"),
    ("Cylinder C6, 7-8 pawns", "cylinder_w6p"),
]

def parse_tsv(tsv_path):
    """Parse a TSV file and return counts for each setting."""
    counts = {s: {"roots": 0, "star2": 0, "star3plus": 0, "max_nimber": 0} for s in SETTINGS}
    total_roots = 0
    
    with open(tsv_path) as f:
        header = f.readline().strip().split('\t')
        # Find the setting columns (indices 3-11)
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 12:
                continue
            total_roots += 1
            for i, setting in enumerate(SETTINGS):
                val = parts[3 + i]
                if val.startswith('N,'):
                    # Nimber
                    nimber = int(val.split(',')[1])
                    if nimber == 2:
                        counts[setting]["star2"] += 1
                    elif nimber >= 3:
                        counts[setting]["star3plus"] += 1
                    if nimber > counts[setting]["max_nimber"]:
                        counts[setting]["max_nimber"] = nimber
                elif val.startswith('*'):
                    # Handle any other star notation
                    pass
    counts["_total_roots"] = total_roots
    return counts

def aggregate_scan_group(group_name, prefix):
    """Aggregate results for all splits in a scan group."""
    # Find all TSV files matching the prefix
    tsv_files = sorted(OUT_DIR.glob(f"{prefix}_*.tsv"))
    
    # Aggregate across splits
    agg = {s: {"roots": 0, "star2": 0, "star3plus": 0, "max_nimber": 0} for s in SETTINGS}
    total_roots = 0
    
    for tsv_file in tsv_files:
        # Skip pilot files
        if "pilot" in tsv_file.name:
            continue
        counts = parse_tsv(tsv_file)
        total_roots += counts.get("_total_roots", 0)
        for s in SETTINGS:
            agg[s]["roots"] += counts[s]["roots"]
            agg[s]["star2"] += counts[s]["star2"]
            agg[s]["star3plus"] += counts[s]["star3plus"]
            if counts[s]["max_nimber"] > agg[s]["max_nimber"]:
                agg[s]["max_nimber"] = counts[s]["max_nimber"]
    
    return {
        "group": group_name,
        "prefix": prefix,
        "total_roots": total_roots,
        "settings": agg,
        "tsv_files": [f.name for f in tsv_files if "pilot" not in f.name],
    }

def main():
    print("Analyzing scan results...")
    print()
    
    all_results = []
    for group_name, prefix in SCAN_GROUPS:
        result = aggregate_scan_group(group_name, prefix)
        all_results.append(result)
        
        print(f"=== {group_name} ===")
        print(f"  Total roots: {result['total_roots']:,}")
        print(f"  Splits: {len(result['tsv_files'])}")
        print(f"  Files: {', '.join(result['tsv_files'])}")
        print()
        print(f"  {'Setting':>12} {'Roots':>12} {'*2':>6} {'*3+':>6} {'Max *':>6}")
        print(f"  {'-'*12} {'-'*12} {'-'*6} {'-'*6} {'-'*6}")
        for i, setting in enumerate(SETTINGS):
            s = result['settings'][setting]
            print(f"  {SHORT_SETTINGS[i]:>12} {s['roots']:>12,} {s['star2']:>6} {s['star3plus']:>6} {s['max_nimber']:>6}")
        print()
    
    # Print summary table in markdown format
    print("## Summary Table")
    print()
    print("| Scan | Total Roots | " + " | ".join([f"{s} (*2/*3+/max)" for s in SHORT_SETTINGS]) + " |")
    print("|" + "---|" * (2 + len(SHORT_SETTINGS)))
    
    for result in all_results:
        row = f"| {result['group']} | {result['total_roots']:,} |"
        for i, setting in enumerate(SETTINGS):
            s = result['settings'][setting]
            row += f" {s['star2']}/{s['star3plus']}/{s['max_nimber']} |"
        print(row)
    
    # Collect all *3+ positions for verification
    print("\n## *3+ Positions Found (for verification)")
    print()
    for result in all_results:
        for tsv_file in result['tsv_files']:
            tsv_path = OUT_DIR / tsv_file
            with open(tsv_path) as f:
                header = f.readline().strip().split('\t')
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) < 12:
                        continue
                    pos = parts[0]
                    for i, setting in enumerate(SETTINGS):
                        val = parts[3 + i]
                        if val.startswith('N,'):
                            nimber = int(val.split(',')[1])
                            if nimber >= 3:
                                print(f"  {result['group']} | {tsv_file} | {pos} | {SHORT_SETTINGS[i]} | *{nimber}")
    
    # Collect all *2 positions for cylinder minimum analysis
    print("\n## *2 Positions on Cylinders (for minimum analysis)")
    print()
    cylinder_groups = [r for r in all_results if r['group'].startswith("Cylinder")]
    for result in cylinder_groups:
        print(f"\n### {result['group']} - count/epon/aware (C/aware)")
        for tsv_file in result['tsv_files']:
            tsv_path = OUT_DIR / tsv_file
            with open(tsv_path) as f:
                header = f.readline().strip().split('\t')
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) < 12:
                        continue
                    pos = parts[0]
                    val = parts[3 + 2]  # C/aware column
                    if val.startswith('N,2'):
                        print(f"  {tsv_file} | {pos}")

if __name__ == "__main__":
    main()