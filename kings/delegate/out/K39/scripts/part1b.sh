#!/bin/zsh
# K39 part 1b: Z_C roots with own2 (restricted cap 2, second implementation); children of the drawing deviations.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39
cd $D
scripts/hrun.sh ZC_own2_Ap 1150 in/ZC_roots_cyl_8x6.in bin/own2 8 6 1 0 2 1 1 QRBN Q 1
scripts/hrun.sh ZC_own2_Bp 1150 in/ZC_roots_cyl_8x6.in bin/own2 8 6 1 1 2 1 1 Q QRBN 1
scripts/hrun.sh ZCk_kp39_Ap 1150 in/ZC_kids_cyl_8x6.in bin/kp39 --board cyl:8x6 --cap 2 --capw 1 --capb 1 --promb Q --bound A --refine --moves --threads 2
scripts/hrun.sh ZCk_kp39_Bp 1150 in/ZC_kids_cyl_8x6.in bin/kp39 --board cyl:8x6 --cap 2 --capw 1 --capb 1 --promw Q --bound B --refine --moves --threads 2
scripts/hrun.sh ZCk_own2_Ap 1150 in/ZC_kids_cyl_8x6.in bin/own2 8 6 1 0 2 1 1 QRBN Q 1
scripts/hrun.sh ZCk_own2_Bp 1150 in/ZC_kids_cyl_8x6.in bin/own2 8 6 1 1 2 1 1 Q QRBN 1
for t in cyl_7x6 cyl_8x6; do W=${${t#cyl_}%x6}
  scripts/hrun.sh ZBk_kp39_$t 1150 in/ZB_kids_$t.in bin/kp39 --board cyl:${W}x6 --cap 1 --refine --moves
  for B in 0 1; do scripts/hrun.sh ZBk_own_${t}_b$B 1150 in/ZB_kids_$t.in bin/own39p $W 6 1 $B 1 1; done
done
