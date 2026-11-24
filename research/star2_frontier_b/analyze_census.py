#!/usr/bin/env python3
"""Analyze nimscan census output to validate known results and find *k >= 2."""

import sys
import re

def analyze_census(tsv_path):
    with open(tsv_path) as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    # Header is first line
    header = lines[0]
    data_lines = lines[1:]
    
    print(f"Total data lines: {len(data_lines)}")
    
    # Settings: 9 settings, indices 3-11 in the tab-separated data
    # Format: position \t width \t npawns \t setting0 \t setting1 ... setting8
    # Each setting: outcome,nimber (e.g., "P,0" or "N,2")
    
    settings = [
        "count/epon", "count/epoff", "count/epon/aware",
        "mover/epon", "mover/epoff", "mover/epon/aware",
        "opponent/epon", "opponent/epoff", "opponent/epon/aware"
    ]
    
    # Counters for e.p.-aware count (setting 2)
    zero_count = 0
    star_count = 0
    nimber2_plus = []
    
    for line in data_lines:
        parts = line.split('\t')
        if len(parts) < 12:
            continue
        
        pos = parts[0]
        width = int(parts[1])
        npawns = int(parts[2])
        
        # Check e.p.-aware count (setting index 2, which is parts[5])
        setting_val = parts[5]  # count/epon/aware
        outcome, nim_str = setting_val.split(',')
        nim = int(nim_str)
        
        if nim == 0:
            zero_count += 1
        elif nim == 1:
            star_count += 1
        elif nim >= 2:
            nimber2_plus.append((pos, width, npawns, nim, setting_val))
        
        # Also check all settings for *k >= 2
        for i, setting_name in enumerate(settings):
            setting_val = parts[3 + i]
            outcome, nim_str = setting_val.split(',')
            nim = int(nim_str)
            if nim >= 2:
                print(f"  *{nim} found: {pos} width={width} npawns={npawns} setting={setting_name} outcome={outcome}")
    
    print(f"\nValidation for e.p.-aware count (setting 2):")
    print(f"  Zeros (nim=0): {zero_count}")
    print(f"  Stars (nim=1): {star_count}")
    print(f"  *k>=2: {len(nimber2_plus)}")
    
    if zero_count == 6724 and star_count == 4042 and len(nimber2_plus) == 0:
        print("  ✓ MATCHES known census: 6,724 zeros, 4,042 stars, no *2")
    else:
        print(f"  ✗ MISMATCH: expected 6724 zeros, 4042 stars, 0 *2+")
    
    return nimber2_plus

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_census.py <census.tsv>")
        sys.exit(1)
    analyze_census(sys.argv[1])