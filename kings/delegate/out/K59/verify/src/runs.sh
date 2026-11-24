#!/bin/zsh
# K59 referee runs (from kings/delegate/out/K59/verify). Build: clang++ -O2 -std=c++17 -o $BIN/kref src/kref.cpp
# BIN = a scratch directory outside the repository.
H=../../../heavy.sh
r(){ n=$1; shift; /usr/bin/time -l $H $BIN/kref "$@" > logs/$n.out 2> logs/$n.time; }
r F2_check check flat:8x7 "Ka4 kc4 Pb2 Pf5 pb6 pf6" c4 c5
r H10_check check cyl:10x6 "Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5" f6 g6
r ZO_check check cyl:8x6 "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5" d4 d5
r F1_check check flat:8x7 "Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6" c4 c5
r F4_check check flat:8x7 "Kc4 ke4 Pb5 Pf2 Pf5 pb6 pf6" e4 e5
r F3_check check flat:8x7 "Ke4 kc4 Pb2 Pb5 Pf5 pb6 pf6" c4 c5
r F5_check check flat:8x7 "Ka4 kc4 Pb2 Pe5 Pf4 pb6 pe6 pf5" c4 c5
r F2_sumT sum flat:8x7 "Ka4 kc4 Pb2 Pf5 pb6 pf6" c4 c5 ../in/T_h10.txt
r F4_sumT sum flat:8x7 "Kc4 ke4 Pb5 Pf2 Pf5 pb6 pf6" e4 e5 ../in/T_h10.txt
r ZO_star sum cyl:8x6 "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5" d4 d5 src/T_star.txt
r F2_sumR sum flat:8x7 "Ka4 kc4 Pb2 Pf5 pb6 pf6" c4 c5 ../in/rnd_all.txt
# vgsum59 regression (BIN/vgsum59 built from ../src/vgsum59.cpp), run from kings/delegate/out/K59:
# ../../heavy.sh $BIN/vgsum59 --lowmem --board cyl:10x6 --root "Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5" --shuttle g6 <six --query as in ../src/run_regress.sh> --tests in/T_h10.txt
