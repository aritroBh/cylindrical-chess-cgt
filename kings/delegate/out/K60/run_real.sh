#!/bin/zsh
# K60: Aux test (aux60, own) and T_N sums (K57 referee's vgsum) on H10 and Z_O, through heavy.sh under time -l.
# Binaries are built in the session scratchpad (BIN), not in the repository.
cd "$(dirname $0)"
BIN=$1
r() { name=$1; shift
  ../../heavy.sh /usr/bin/time -l "$@" > logs/$name.out 2> logs/$name.err; }
r aux_H10 $BIN/aux60 --board cyl:10x6 --root "Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5" --shuttle g6
r aux_ZO_cyl86 $BIN/aux60 --board cyl:8x6 --root "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5" --shuttle d5
r TN_ZO_cyl86 $BIN/vgsum --board cyl:8x6 --root "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5" --shuttle d5 --tests logs/T_N.txt
