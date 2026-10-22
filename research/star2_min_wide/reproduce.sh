#!/bin/bash
# T40 reproduce script (documentation of the exact commands; each step is independent).  Run from research/star2_min_wide.
#   nice -n 15 everywhere; at most 2 heavy processes at once.  Python = project .venv, PYTHONPATH = project root.
set -u
cd "$(dirname "$0")"
PY="../../.venv/bin/python"; export PYTHONPATH=../..

# 0. build (nothing is installed; scan_fixed2 is a plain compile of the fixed2 source and gives byte-identical output to
#    ../star26_rings/frontier_split1_fixed2)
cc -O2 -o scan_fixed2 ../star26_rings/frontier_split1_fixed2.c
cc -O2 -o count_roots count_roots.c; cc -O2 -o count_connected count_connected.c; cc -O2 -o emit_roots emit_roots.c

# 1. which positions does the scanner enumerate?  independent re-implementation of the rule; must reproduce stored TOTALs
#    (w6p7 3_4 = 1564495, w4p8 4_4 = 1501971, w5p8 3_5 = 3675495 ...).   (root_counts.txt = all widths 1..8, p = 2..7)
for w in 1 2 3 4 5 6 7 8; do for p in 2 3 4 5 6 7; do nice -n 15 ./count_roots $w $p; done; done > root_counts.txt

# 2. the full scan: flat widths 1..8, 2..7 pawns, every split, default setting (count, e.p. on, e.p.-aware = --only-setting 2)
./run_chain.sh 1 2 3 4 5 6 &     # per split: scan_fixed2 --flat --width W --min P --max P --nw NW --nb NB --only-setting 2
./run_chain.sh 7 8 &  wait       #   | python3 -I filt.py scan/wWpP_NW_NB   (summary + every nimber>=2 row)
python3 -I tabulate.py           # table + check that the row count of every split equals the independent counter
python3 -I twin_check.py         # colour-reversal consistency of all 96 twin split pairs

# 3. regression against the stored scans (row by row, setting count/epon/aware)
for nw in 2 3 4 5; do nb=$((7-nw)); nice -n 15 ./scan_fixed2 --flat --width 6 --min 7 --max 7 --nw $nw --nb $nb --only-setting 2 2>/dev/null \
   | python3 -I regress.py ../star3_hunt/flat_w6p7_${nw}_${nb}.tsv.zst; done          # regress_w6p7.txt, regress_other.txt

# 4. the hits, verified with cylcgt (components / whole-board; 4 and 8 files) and the Codex solver
(cd ../.. && $PY research/star2_min_wide/verify_hits.py)                                 # verify_hits.out

# 5. parts (maximal runs of occupied files) and exact sums, any width (part b)
$PY parts.py 5                   # parts_k2..k5.tsv (connected no-passer roots, cylcgt values)
$PY sums.py > sums_out.txt       # which sums of parts equal 0, *1, *2, *3
$PY sums_hits.py > sums_hits.out # the (3,4) sums equal to *2/*3
$PY check_parts_codex.py K [LO HI]   # Codex solver vs cylcgt on every part (chain_j4.sh)

# 6. scanner (whole-board) versus cylcgt
./chain_j1.sh; ./chain_j2.sh; ./chain_j3.sh; ./chain_j5.sh   # connected rows: cylcgt value of the whole position vs scanner, per split (conn/*.out)
./run_gapped.sh 3 4 5 6 7 8 ; python3 -I aggregate_gapped.py # gapped rows: scanner vs sum of cylcgt part values (gapped/*.out)

# 7. e.p. variant: real-chess expiry (any move clears all e.p. rights) vs per-component persistence
cc -O2 -Wno-unused -o scan_R scan_R.c ; $PY cmp_SR.py W P NW     # S versus R scan, row by row

# 8. width 9 (the only 7-pawn shape needing 9 files is (2,2,3) with spans (2,2,3)): 128-bit-mask copy of the scanner
python3 make_wide.py && cc -O2 -o scan_wide scan_wide.c                 # wide_regress.txt: byte-identical to fixed2 on widths <= 8
python3 make_wide_R.py && cc -O2 -Wno-unused -o scan_wide_R scan_wide_R.c   # variant R of the wide scanner
for NW in 2 3 4 5; do NB=$((7-NW)); nice -n 15 ./scan_wide --flat --width 9 --min 7 --max 7 --nw $NW --nb $NB --only-setting 2 --max-entries 33554432 2>/dev/null | python3 -I filt.py wide/w9p7_${NW}_${NB}; done

# 9. Codex solver vs cylcgt on every part; arbitration of the 166 differing 5-pawn parts by the naive definition of equality
./chain_j4.sh                                                            # codex_parts_k*.out
$PY arbitrate_codex_diffs.py codex_parts_k5_6200.out codex_parts_k5_12400.out codex_parts_k5_18600.out > arbitrate_codex.out

# 10. 7-pawn connected roots (samples), cylcgt whole-board and default; R-variant rows vs cylcgt whole-board
./chain_j5.sh ; ./chain_j7.sh ; $PY check_SR_rows.py ; ./final_tables.sh
