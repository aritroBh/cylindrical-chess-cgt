#!/bin/zsh
# K48 part 1: Z_O (the K45 over group) on cyl:8x6 in chess, cap 1, roots and the two freeze positions q (both sides to move), with move lists.
cd "$(dirname $0)/.."
B=cyl:8x6; I=in/ZO_cyl_8x6.in
scripts/hrun.sh ZO_kp 3000 $I ../../../kpsolve --board $B --ep on --promote QRBN --cap 1 --moves
scripts/hrun.sh ZO_kp39r 3000 $I bin/kp39 --board $B --ep on --promote QRBN --cap 1 --refine --moves
for b in 0 1; do scripts/hrun.sh ZO_own_b${b}_r1 3000 $I bin/own39 8 6 1 $b 1 1; done
for b in A B; do scripts/hrun.sh ZO_rf_${b}_r1 3000 $I bin/rf39 8 6 1 $b 1 1 1 QRBN QRBN 1; done
echo done > logs/p1_cap1.done
