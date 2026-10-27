#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K24
cd $D
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
$H ./kp --board cyl:7x6 --ep on --promote QRBN --cap 1 --moves < pos_7x6.txt > logs/kpsolve_cyl7x6.txt 2>&1
$H ./kp --board cyl:8x8 --ep on --promote QRBN --cap 1 --moves < pos_8x8.txt > logs/kpsolve_cyl8x8.txt 2>&1
$H ./kp --board flat:8x8 --ep on --promote QRBN --cap 1 --moves < pos_8x8.txt > logs/kpsolve_flat8x8.txt 2>&1
echo done > logs/batch2.done
