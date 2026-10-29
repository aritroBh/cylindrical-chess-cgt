#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
./scripts/run_conf2.sh no7x6 cyl:7x6 cf/nearover_cyl_7x6.txt 40 over 60
./scripts/run_conf2.sh nu7x6 cyl:7x6 cf/nearunder_cyl_7x6.txt 40 under 60
./scripts/run_conf2.sh no7x7 cyl:7x7 cf/nearover_cyl_7x7.txt 20 over 60
./scripts/run_conf2.sh no8x7 cyl:8x7 cf/nearover_cyl_8x7.txt 20 over 60
echo finished > cf/queueA2.done
