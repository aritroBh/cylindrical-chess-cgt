#!/bin/zsh
# K39 validation: kpsolve and kp39 --refine against own39 (bounds A, B; refine 0 and 1), random positions, cap 1, --moves.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39
cd $D
for b in cyl:7x6 cyl:8x6 flat:7x6; do
  t=${b/:/_}; wh=${b#*:}; W=${wh%x*}; c=0; [[ $b == cyl* ]] && c=1
  scripts/hrun.sh val_kp_$t 1100 in/rand_$t.in bin/kp --board $b --ep on --promote QRBN --cap 1 --moves
  scripts/hrun.sh val_kp39_$t 1100 in/rand_$t.in bin/kp39 --board $b --ep on --promote QRBN --cap 1 --refine --moves
  for B in 0 1; do for R in 0 1; do
    scripts/hrun.sh val_own_${t}_b${B}_r${R} 1100 in/rand_$t.in bin/own39 $W 6 $c $B $R 1
  done; done
done
