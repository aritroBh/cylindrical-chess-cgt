#!/bin/bash
# T49 (*4 hunt): commands that produced the numbers in the report.  Run from research/star4_hunt (project venv not needed
# except for verify1.sh / xcheck_sample.py).  All C runs are single-process, nice 15, table <= 33.5M entries (1.9 GB).
set -u
cc -O2 -o h4 h4.c -lm                        # scanner core of star3_single/s3.c + the modes added here
cc -O2 -DSTRIDE=10 -o ring4 ring4.c -lm      # same core re-laid-out for widths <= 10 (ringeval.c copy with a node budget)
source ./scanlib.sh                          # scan DIR KIND WIDTH NW NB NCHUNKS [flags]; H=./h4 by default
# (1) exhaustive flat 5 files, 10 pawns, single component, all splits (45.1M + 64.8M + 22.3M + 2.7M roots)
./run_scan_w5p10.sh; python3 summarize.py out/w5p10
# (2) extensions of *3 cores by up to 3 pawns (flat widths 4-6); *3 cores + new files; A + new files; *2 cores + new files
./run_ext1.sh; ./run_queue9.sh              # j3, rows, j2, j1a, rows_w5 (see the script for the exact arguments)
# (3) ring tools: C7 primitive *3 rings -> C8/C9 (new files), C7 + 2 pawns
./ring4 --cylinder --width 8 --single --evalbudget 4000000 --extend seeds/c7_prim.txt --k 5 --rot 7 --newonly --rep-nim 3 --near 3
./ring4 --cylinder --width 9 --single --evalbudget 4000000 --extend seeds/c7_prim.txt --k 3 --rot 7 --newonly --rep-nim 3 --near 3
./ring4 --cylinder --width 7 --single --evalbudget 500000  --extend seeds/c7_prim.txt --k 2 --rep-nim 3 --near 3
# (4) dense small-width scans
scan c3p11 cylinder 3 5 6 2; scan c3p12 cylinder 3 6 6 2 --colsym; scan w4p11 flat 4 3 8 8; scan w4p11 flat 4 4 7 32; scan w4p11 flat 4 5 6 48
# (5) structured families
for w in 3 4 5; do ./h4 --flat --width $w --duel; done; ./h4 --cylinder --width 5 --duel
./h4 --flat --width 8 --evalbudget 3000000 --eval seeds/periodic2_w8.txt
# (6) structure tests
python3 decomp.py pairs; python3 decomp.py ring; python3 decomp.py star2; python3 s3_decomp_all.py; python3 additivity.py
# (7) verification of the new *3 positions and the scanner cross-check (from the project root)
bash research/star4_hunt/verify1.sh
PYTHONPATH=. .venv/bin/python research/star4_hunt/xcheck_sample.py
python3 final_stats.py
