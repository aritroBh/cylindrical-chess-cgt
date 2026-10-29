#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/f3
( ulimit -t 110; /usr/bin/time -l nice -n 15 ./grp --tempo --W 8 --H 6 --F 3 --wmax 3 --bmax 3 --out runs/tp_8x6_f3_33 > runs/tp_8x6_f3_33.json 2> runs/tp_8x6_f3_33.err )
echo "done tp_8x6_f3_33 exit=$? $(date +%T) rss=$(grep 'maximum resident' runs/tp_8x6_f3_33.err | awk '{print $1}')" >> runs/tp.log
