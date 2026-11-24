#!/bin/zsh
# K59 part 1: (B1) under the sum's rule (and the pass game) for the four exact groups of cyl:8x7 (K48), with vgsum59.
# Smallest first (T4, 4.1 million nodes), then T1, T2, then T3 (14.3 million nodes) with a capacity hint.
cd "$(dirname $0)/.."
src/hrun.sh p1_T4 bin/vgsum59 --board cyl:8x7 --root "Kc4 ka4 Pb2 Pe3 Pe5 pb6 pe4 pe6" --shuttle a5
src/hrun.sh p1_T1 bin/vgsum59 --board cyl:8x7 --root "Kd4 kf4 Pa4 Pb5 Pe2 pa5 pb6 pe6" --shuttle f5
src/hrun.sh p1_T2 bin/vgsum59 --board cyl:8x7 --root "Kd4 kf4 Pb3 Pb5 Pe2 pb4 pb6 pe6" --shuttle f5
