#!/bin/zsh
# short kpsolve runs (well under one CPU-minute each when the machine is idle): run directly at nice 15, RSS reported by time -l
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K24
cd $D
/usr/bin/time -l nice -n 15 ./kp --board cyl:7x6 --ep on --promote QRBN --cap 1 --moves < pos_7x6.txt > logs/kpsolve_cyl7x6.txt 2> logs/kpsolve_cyl7x6.err
/usr/bin/time -l nice -n 15 ./kp --board cyl:8x8 --ep on --promote QRBN --cap 1 --moves < pos_8x8.txt > logs/kpsolve_cyl8x8.txt 2> logs/kpsolve_cyl8x8.err
/usr/bin/time -l nice -n 15 ./kp --board flat:8x8 --ep on --promote QRBN --cap 1 --moves < pos_8x8.txt > logs/kpsolve_flat8x8.txt 2> logs/kpsolve_flat8x8.err
echo done > logs/direct.done
