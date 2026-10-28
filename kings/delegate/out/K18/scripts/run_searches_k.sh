#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
run() { nice -n 15 bin/lg --board $1 --fz $2 --maxw $3 --maxb $4 --kmax 6 --search > logs/searchk_$5.out 2> logs/searchk_$5.err; }
run cyl:8x6 0:3 2 2 c8x6_f3_22
run cyl:7x6 0:3 2 2 c7x6_f3_22
run cyl:8x6 0:3 3 2 c8x6_f3_32
echo done > logs/searchesk_done
