#!/bin/zsh
# K60 referee: Z_O and H10 beside T_0..T_6, under_D and -1 with the K56/K57 pass-game program pr57 (K56's own move
# generator, not the K56 referee's generator used by vgsum and aux60). Binary built in the session scratchpad: $1.
cd "$(dirname $0)"
BIN=$1
../../../heavy.sh /usr/bin/time -l $BIN/pr57 --board cyl:10x6 --root "Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5" --shuttle g6 --sum logs/TN_pr57.txt --probe logs/probes_H10.txt > logs/pr57_H10.out 2> logs/pr57_H10.err
../../../heavy.sh /usr/bin/time -l $BIN/pr57 --board cyl:8x6 --root "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5" --shuttle d5 --sum logs/TN_pr57.txt --probe logs/probes_ZO.txt > logs/pr57_ZO.out 2> logs/pr57_ZO.err
