#!/bin/zsh
# K39 part 1: the 8 roots of Z_B (cyl:7x6, cyl:8x6, flat:7x6) and Z_C (cyl:8x6), chess, cap 1, with move lists:
# kpsolve; kp39 --refine; own39 bounds A and B with refine.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39
cd $D
for gb in ZB:cyl:7x6 ZB:cyl:8x6 ZC:cyl:8x6 ZB:flat:7x6; do
  g=${gb%%:*}; b=${gb#*:}; t=${b/:/_}; wh=${b#*:}; W=${wh%x*}; c=0; [[ $b == cyl* ]] && c=1
  scripts/hrun.sh ${g}_kp_$t 1150 in/${g}_roots_$t.in bin/kp --board $b --ep on --promote QRBN --cap 1 --moves
  scripts/hrun.sh ${g}_kp39_$t 1150 in/${g}_roots_$t.in bin/kp39 --board $b --ep on --promote QRBN --cap 1 --refine --moves
  for B in 0 1; do scripts/hrun.sh ${g}_own_${t}_b${B}_r1 1150 in/${g}_roots_$t.in bin/own39 $W 6 $c $B 1 1; done
done
