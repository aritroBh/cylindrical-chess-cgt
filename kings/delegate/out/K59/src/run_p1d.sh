#!/bin/zsh
# K59 extra for part 1: direct sums of T4, T2, T1 (cyl:8x7) beside the K57 referee's 63 finite D-games, vgsum59 --lowmem.
# (T3 is left out: its graph plus the product states would exceed 2 GB.)
cd "$(dirname $0)/.."
src/hrun.sh sum_T4 bin/vgsum59 --lowmem --board cyl:8x7 --root "Kc4 ka4 Pb2 Pe3 Pe5 pb6 pe4 pe6" --shuttle a5 --tests in/T_h10.txt
src/hrun.sh sum_T2 bin/vgsum59 --lowmem --board cyl:8x7 --root "Kd4 kf4 Pb3 Pb5 Pe2 pb4 pb6 pe6" --shuttle f5 --tests in/T_h10.txt
src/hrun.sh sum_T1 bin/vgsum59 --lowmem --board cyl:8x7 --root "Kd4 kf4 Pa4 Pb5 Pe2 pa5 pb6 pe6" --shuttle f5 --tests in/T_h10.txt
