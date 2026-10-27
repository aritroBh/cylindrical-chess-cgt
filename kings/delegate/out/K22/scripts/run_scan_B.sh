#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22
OUT=$D/logs/scan_B.txt
: > $OUT
scan() { kind=$1; W=$2; H=$3; lo=$4; hi=$5; wm=$6; bm=$7
  for f in $(seq $lo $hi); do for safe in "" "--safe"; do
    nice -n 15 $D/local --board $kind $W $H --fz $lo $hi $safe enum --f $f --wmax $wm --bmax $bm --ep --ex 0 | grep -E 'SUMMARY|VIOLATION' >> $OUT
  done; done; }
scan cyl 7 6 0 2 3 3
scan cyl 8 6 0 2 3 3
for dims in "4 5" "4 6" "5 5" "5 6"; do scan cyl ${=dims} 0 $((${dims% *}-1)) 3 3; done
scan cyl 7 6 0 3 3 3
scan cyl 7 7 0 2 3 3
scan cyl 8 6 0 4 2 3
scan cyl 6 6 0 5 3 3
echo ALLDONE >> $OUT
