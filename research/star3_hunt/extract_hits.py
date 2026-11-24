#!/usr/bin/env python3
"""Extract *3+ positions and *2 cylinder positions for verification."""

import os
import glob

OUT_DIR = "research/star3_hunt"

SETTINGS = [
    "count/epon", "count/epoff", "count/epon/aware",
    "mover/epon", "mover/epoff", "mover/epon/aware",
    "opponent/epon", "opponent/epoff", "opponent/epon/aware",
]

SHORT_SETTINGS = [
    "C/T", "C/off", "C/aware",
    "M/T", "M/off", "M/aware",
    "O/T", "O/off", "O/aware",
]

def extract_star3plus():
    """Extract all *3+ positions across all scans."""
    print("## *3+ Positions Found (for verification)")
    print()
    print("| Scan | Split | Position | Setting | Nimber |")
    print("|---|---|---|---|---|")
    
    tsv_files = sorted(glob.glob(os.path.join(OUT_DIR, "*.tsv")))
    for tsv_file in tsv_files:
        name = os.path.basename(tsv_file)
        if "pilot" in name:
            continue
        if os.path.getsize(tsv_file) == 0:
            continue
        
        with open(tsv_file) as f:
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
                            print(f"| {name} | {pos} | {SHORT_SETTINGS[i]} | *{nimber} |")

def extract_cylinder_star2_aware():
    """Extract *2 positions on cylinders under C/aware (count/epon/aware)."""
    print("\n## *2 Positions on Cylinders (C/aware = count/epon/aware)")
    print()
    print("| Scan | Split | Position |")
    print("|---|---|---|")
    
    cylinder_files = sorted(glob.glob(os.path.join(OUT_DIR, "cylinder_w*p*.tsv")))
    for tsv_file in cylinder_files:
        name = os.path.basename(tsv_file)
        if "pilot" in name:
            continue
        if os.path.getsize(tsv_file) == 0:
            continue
        
        with open(tsv_file) as f:
            header = f.readline().strip().split('\t')
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) < 12:
                    continue
                pos = parts[0]
                # C/aware is index 2 (3rd setting, column 6 in TSV)
                val = parts[3 + 2]  # C/aware
                if val == 'N,2':
                    print(f"| {name} | {pos} |")

def extract_opponent_star3():
    """Extract *3+ positions under opponent rule."""
    print("\n## *3+ Positions under Opponent Race Rule")
    print()
    print("| Scan | Split | Position | Setting | Nimber |")
    print("|---|---|---|---|---|")
    
    tsv_files = sorted(glob.glob(os.path.join(OUT_DIR, "*.tsv")))
    for tsv_file in tsv_files:
        name = os.path.basename(tsv_file)
        if "pilot" in name:
            continue
        if os.path.getsize(tsv_file) == 0:
            continue
        
        with open(tsv_file) as f:
            header = f.readline().strip().split('\t')
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) < 12:
                    continue
                pos = parts[0]
                # Opponent settings: indices 6, 7, 8
                for idx in [6, 7, 8]:
                    val = parts[3 + idx]
                    if val.startswith('N,'):
                        nimber = int(val.split(',')[1])
                        if nimber >= 3:
                            print(f"| {name} | {pos} | {SHORT_SETTINGS[idx]} | *{nimber} |")

if __name__ == "__main__":
    extract_star3plus()
    extract_cylinder_star2_aware()
    extract_opponent_star3()