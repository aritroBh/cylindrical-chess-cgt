#!/bin/zsh
# Exhaustive scans of the local game; every run is a few CPU-seconds (measured), so no lock is needed.
# Roots: s-bar (White) pawns on file f only (1..WMAX), s (Black) pawns on any F_Z file (0..BMAX), s king on f in front,
# s-bar king anywhere on F_Z, s to move, with and without an e.p. right of a White double step.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22
OUT=$D/logs/scan_all.txt
: > $OUT
scan() { # kind W H lo hi wmax bmax
  kind=$1; W=$2; H=$3; lo=$4; hi=$5; wm=$6; bm=$7
  for f in $(seq $lo $hi); do
    for safe in "" "--safe"; do
      nice -n 15 $D/local --board $kind $W $H --fz $lo $hi $safe enum --f $f --wmax $wm --bmax $bm --ep --ex 0 | grep -E 'SUMMARY|VIOLATION' >> $OUT
    done
  done
}
for dims in "3 5" "3 6" "3 7" "4 5" "4 6" "4 7" "5 5" "5 6" "5 7" "6 5" "6 6"; do scan flat ${=dims} 0 $((${dims% *}-1)) 3 3; done
for dims in "4 5" "4 6" "5 5" "5 6" "6 6"; do scan cyl ${=dims} 0 $((${dims% *}-1)) 3 3; done
scan cyl 7 6 0 2 3 3
scan cyl 7 6 0 3 3 3
scan cyl 8 6 0 2 3 3
scan cyl 8 6 0 4 2 3
scan cyl 7 7 0 2 3 3
for dims in "3 5" "3 6" "4 5" "4 6" "5 5"; do scan flat ${=dims} 0 $((${dims% *}-1)) 4 4; done
echo ALLDONE >> $OUT
