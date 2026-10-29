#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
./scripts/run_conf.sh c7x6 cyl:7x6 cf/g_cyl_7x6.txt 24
./scripts/run_conf.sh c8x6 cyl:8x6 cf/g_cyl_8x6.txt 24
./scripts/run_conf.sh c8x8 cyl:8x8 cf/g_cyl_8x8.txt 8
echo finished > cf/queue.done
