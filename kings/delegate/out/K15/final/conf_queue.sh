#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/final
./run_conf.sh zb7 cyl:7x6 cf/g_zb.txt
./run_conf.sh zb8 cyl:8x6 cf/g_zb.txt
./run_conf.sh e7x6 cyl:7x6 runs/dud_groups_7x6.tsv
./run_conf.sh e8x6 cyl:8x6 runs/dud_groups_8x6.tsv
echo finished > cf/queue.done
