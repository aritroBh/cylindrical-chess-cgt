#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22
OUT=$D/logs/scan_C.txt
: > $OUT
scan() { kind=$1; W=$2; H=$3; lo=$4; hi=$5; wm=$6; bm=$7
  for f in $(seq $lo $hi); do for safe in "" "--safe"; do
    nice -n 15 $D/local --board $kind $W $H --fz $lo $hi $safe enum --f $f --wmax $wm --bmax $bm --ep --ex 0 | grep -E 'SUMMARY|VIOLATION' >> $OUT
  done; done; }
# 4-rank boards (SPEC allows H = 4), then 4+4 pawns on the smallest boards
for dims in "3 4" "4 4" "5 4" "6 4"; do scan flat ${=dims} 0 $((${dims% *}-1)) 3 3; done
for dims in "4 4" "5 4"; do scan cyl ${=dims} 0 $((${dims% *}-1)) 3 3; done
for dims in "3 5" "3 6" "4 5" "4 6" "5 5"; do scan flat ${=dims} 0 $((${dims% *}-1)) 4 4; done
echo ALLDONE >> $OUT
