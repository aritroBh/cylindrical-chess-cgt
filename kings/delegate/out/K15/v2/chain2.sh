#!/bin/zsh
# waits for chain.sh, then one exact-chess kpsolve attempt on the bare Z_B^cyl roots (cyl:7x6, cap 1, 2 threads), through the lock, 1100 s alarm
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/v2
while kill -0 $(cat chain.pid) 2>/dev/null; do sleep 30; done
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
head -2 chk/zb.in > chk/zb_chess_2.in
/usr/bin/time -l $H perl -e 'alarm 1100; exec @ARGV' ./kp15 --board cyl:7x6 --cap 1 --threads 2 < chk/zb_chess_2.in > chk/zb_chess_7x6.out 2> chk/zb_chess_7x6.err
echo "done chess exit=$?" >> runs/chain.log
