#!/usr/bin/env python3
import sys

# Column indices (0-based): 4=count/epon, 5=count/epoff, 7=mover/epon, 8=mover/epoff
TARGET_COLS = [3, 4, 6, 7]
SETTING_NAMES = ["count/epon", "count/epoff", "mover/epon", "mover/epoff"]

print("position\twidth\tnpawns\tsetting\toutcome\tnimber\tsource_file")

for filepath in sys.argv[1:]:
    with open(filepath) as f:
        for line_num, line in enumerate(f):
            if line_num == 0:
                continue  # skip header
            parts = line.rstrip('\n').split('\t')
            if len(parts) < 12:
                continue
            pos, width, npawns = parts[0], parts[1], parts[2]
            for col_idx, setting in zip(TARGET_COLS, SETTING_NAMES):
                val = parts[col_idx]
                if ',' in val:
                    outcome, nimber_str = val.split(',', 1)
                    try:
                        nimber = int(nimber_str)
                        if nimber >= 3:
                            print(f"{pos}\t{width}\t{npawns}\t{setting}\t{outcome}\t{nimber}\t{filepath}")
                    except ValueError:
                        pass

