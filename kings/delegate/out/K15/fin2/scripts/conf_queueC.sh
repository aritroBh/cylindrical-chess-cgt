#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
./scripts/run_conf2.sh c8x8 cyl:8x8 cf/g_cyl_8x8.txt 8 dud 240
./scripts/run_conf2.sh no8x8 cyl:8x8 cf/nearover_cyl_8x8.txt 20 over 60
./scripts/run_conf2.sh nu8x8 cyl:8x8 cf/nearunder_cyl_8x8.txt 20 under 60
echo finished > cf/queueC.done
