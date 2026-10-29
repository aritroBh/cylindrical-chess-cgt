#!/bin/zsh
# K15 r3: kpsolve (chess) on the shuttle-closure states of D2 and D2m (cyl:7x6), cap 1, --moves; one heavy.sh call, own watchdog (3 GB, 1100 s).
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/r3
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
$H ../fin2/scripts/wd.sh logs/chess_cyl7.pid 3000000 1100 bin/kp --board cyl:7x6 --cap 1 --threads 2 --moves < data/cyl7_states.in > logs/chess_cyl7_c1_mv.out 2> logs/chess_cyl7_c1_mv.err
echo "exit=$? $(date +%T)" > logs/chess_cyl7_c1_mv.done
