#!/bin/zsh
# K39 validation of own2 at cap 2 (replaces the cap-2 part of val2.sh, whose 3-pawn sets were too large for kpsolve at cap 2):
# random positions with at most 2 pawns; unrestricted cap 2 (kpsolve vs own2), restricted A' and B' (kp39 vs own2).
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39
cd $D
for b in cyl:8x6 flat:7x6; do
  t=${b/:/_}; wh=${b#*:}; W=${wh%x*}; c=0; [[ $b == cyl* ]] && c=1
  scripts/hrun.sh val3_kp39Ap_$t 1100 in/rand3_$t.in bin/kp39 --board $b --cap 2 --capw 1 --capb 1 --promb Q --bound A --moves --threads 2
  scripts/hrun.sh val3_own2Ap_$t 1100 in/rand3_$t.in bin/own2 $W 6 $c 0 2 1 1 QRBN Q 1
  scripts/hrun.sh val3_kp39Bp_$t 1100 in/rand3_$t.in bin/kp39 --board $b --cap 2 --capw 1 --capb 1 --promw Q --bound B --moves --threads 2
  scripts/hrun.sh val3_own2Bp_$t 1100 in/rand3_$t.in bin/own2 $W 6 $c 1 2 1 1 Q QRBN 1
  scripts/hrun.sh val3_kpc2_$t 1100 in/rand3_$t.in bin/kp --board $b --cap 2 --moves --threads 2
  for B in 0 1; do scripts/hrun.sh val3_own2c2_${t}_b$B 1100 in/rand3_$t.in bin/own2 $W 6 $c $B 2 2 2 QRBN QRBN 1; done
done
