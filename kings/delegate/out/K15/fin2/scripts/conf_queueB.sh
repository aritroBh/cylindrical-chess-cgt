#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
./scripts/run_conf2.sh c8x6 cyl:8x6 cf/g_cyl_8x6.txt 24 dud 480
./scripts/run_conf2.sh no8x6 cyl:8x6 cf/nearover_cyl_8x6.txt 40 over 60
./scripts/run_conf2.sh nu8x6 cyl:8x6 cf/nearunder_cyl_8x6.txt 40 under 60
echo finished > cf/queueB.done
