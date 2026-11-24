#!/bin/zsh
# K57: the cyl:8x7 groups T1, T2, T4 beside K56's 600 random D-games (Lemma prediction: equal to over).
cd "$(dirname $0)"
./hrun.sh S_rnd_T2 src/pr57 --board cyl:8x7 --root "Kd4 kf4 Pb3 Pb5 Pe2 pb4 pb6 pe6" --shuttle f5 --sum tests/rnd_all.txt
./hrun.sh S_rnd_T4 src/pr57 --board cyl:8x7 --root "Kc4 ka4 Pb2 Pe3 Pe5 pb6 pe4 pe6" --shuttle a5 --sum tests/rnd_all.txt
./hrun.sh S_rnd_T1 src/pr57 --board cyl:8x7 --root "Kd4 kf4 Pa4 Pb5 Pe2 pa5 pb6 pe6" --shuttle f5 --sum tests/rnd_all.txt
