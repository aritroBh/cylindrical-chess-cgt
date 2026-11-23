#!/bin/bash
# Validation 2: R = 8 controls against documented lines (RESULTS.md, research/star4_hunt/REPORT.md).  Run from research/tall_boards.
T=$(pwd); O=results/control; mkdir -p $O
run() { # name F wrap R nw nb extra...
  n=$1; shift; echo "## $n $*" >> $O/control.out; nice -n 15 ./tw --scan "$@" --maxtab 25 >> $O/control.out; echo $! > /dev/null; }
# (a) C3, 10 pawns, all splits, colours not exchanged: documented 741,110 rings, two *2 (twins)
for nw in 1 2 3 4 5 6 7 8 9; do run c3p10 3 1 8 $nw $((10-nw)) --nocolsym; done
# (b) C6, 9 pawns: documented exactly six *2 = three positions + colour-reversed twins; nw<nb splits give one of each twin
for nw in 1 2 3 4; do run c6p9 6 1 8 $nw $((9-nw)); done
# (c) flat 4 files, 11 pawns: documented 48,649,934 roots, 9 *2, 1 *3, 0 >= *4 (splits 2+9..5+6)
for nw in 1 2 3 4 5; do run f4p11 4 0 8 $nw $((11-nw)); done
echo finished >> $O/control.out
