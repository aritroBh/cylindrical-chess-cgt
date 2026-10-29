#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
./scripts/run_conf.sh no7x6 cyl:7x6 cf/nearover_cyl_7x6.txt 40 over
./scripts/run_conf.sh no8x6 cyl:8x6 cf/nearover_cyl_8x6.txt 40 over
./scripts/run_conf.sh nu7x6 cyl:7x6 cf/nearunder_cyl_7x6.txt 40 under
./scripts/run_conf.sh nu8x6 cyl:8x6 cf/nearunder_cyl_8x6.txt 40 under
./scripts/run_conf.sh no8x8 cyl:8x8 cf/nearover_cyl_8x8.txt 20 over
./scripts/run_conf.sh nu8x8 cyl:8x8 cf/nearunder_cyl_8x8.txt 20 under
./scripts/run_conf.sh no7x7 cyl:7x7 cf/nearover_cyl_7x7.txt 20 over
./scripts/run_conf.sh no8x7 cyl:8x7 cf/nearover_cyl_8x7.txt 20 over
echo finished > cf/near.done
