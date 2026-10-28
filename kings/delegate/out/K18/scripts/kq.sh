#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
nice -n 15 bin/lg --board cyl:8x6 --fz 0:3 --maxw 2 --maxb 2 --kmax 3 --query < logs/k_xcheck_Q.txt > logs/k_xcheck_lg.txt 2> /dev/null
