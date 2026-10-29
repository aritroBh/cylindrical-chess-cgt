#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K28/verify
H=scripts/hrun.sh
$H c1_kp 5400 logs/children5.in bin/kp --board flat:7x6 --ep on --promote QRBN --cap 1 --moves
$H c1_kq3 5400 logs/children5.in bin/kq3 --cap 1 --bound AB --refine --moves
for b in 0 1; do for r in 0 1; do $H own_b${b}_r${r} 5400 logs/children5.in bin/ownref 7 6 $b $r; done; done
$H r5_kq3_cap2 5400 logs/r5.in bin/kq3 --cap 2 --bound AB --moves --threads 3
$H r5_kp28_B 5400 logs/r5.in bin/kp28 --board flat:7x6 --ep on --promote QRBN --promw Q --capw 1 --cap 2 --threads 3 --moves
