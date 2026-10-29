#!/bin/zsh
# K15 r3: kpsolve (chess) cap 1 on Z* alone, one heavy.sh call, own watchdog (3 GB, 1100 s)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/r3
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
$H ../fin2/scripts/wd.sh logs/chess_zstar.pid 3000000 1100 bin/kp --board cyl:8x6 --cap 1 --threads 2 < data/zstar.in > logs/chess_zstar_c1.out 2> logs/chess_zstar_c1.err
echo "exit=$? $(date +%T)" > logs/chess_zstar_c1.done
