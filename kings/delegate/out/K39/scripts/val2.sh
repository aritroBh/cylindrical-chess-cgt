#!/bin/zsh
# K39 validation of own2: cap 1 against kpsolve (the random sets of val.sh), cap 2 against kpsolve, restricted cap 2 against kp39.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39
cd $D
for b in cyl:7x6 cyl:8x6 flat:7x6; do
  t=${b/:/_}; wh=${b#*:}; W=${wh%x*}; c=0; [[ $b == cyl* ]] && c=1
  for B in 0 1; do scripts/hrun.sh val2_own2c1_${t}_b$B 1100 in/rand_$t.in bin/own2 $W 6 $c $B 1 2 2 QRBN QRBN 1; done
done
for b in cyl:8x6 flat:7x6; do
  t=${b/:/_}; wh=${b#*:}; W=${wh%x*}; c=0; [[ $b == cyl* ]] && c=1
  scripts/hrun.sh val2_kpc2_$t 1100 in/rand2_$t.in bin/kp --board $b --cap 2 --moves --threads 2
  for B in 0 1; do scripts/hrun.sh val2_own2c2_${t}_b$B 1100 in/rand2_$t.in bin/own2 $W 6 $c $B 2 2 2 QRBN QRBN 1; done
  scripts/hrun.sh val2_kp39Ap_$t 1100 in/rand2_$t.in bin/kp39 --board $b --cap 2 --capw 1 --capb 1 --promb Q --bound A --moves --threads 2
  scripts/hrun.sh val2_own2Ap_$t 1100 in/rand2_$t.in bin/own2 $W 6 $c 0 2 1 1 QRBN Q 1
  scripts/hrun.sh val2_kp39Bp_$t 1100 in/rand2_$t.in bin/kp39 --board $b --cap 2 --capw 1 --capb 1 --promw Q --bound B --moves --threads 2
  scripts/hrun.sh val2_own2Bp_$t 1100 in/rand2_$t.in bin/own2 $W 6 $c 1 2 1 1 Q QRBN 1
done
