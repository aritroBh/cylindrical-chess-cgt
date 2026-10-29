#!/bin/zsh
# light version for the near-over / near-under roots (up to 10 pawns): the four named contexts only, chunks of 8 positions
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
until grep -q finished cf/no7x6.progress 2>/dev/null; do sleep 20; done
./scripts/run_conf2.sh nol7x6 cyl:7x6 cf/nearover_cyl_7x6.txt 4 over 8
./scripts/run_conf2.sh nul7x6 cyl:7x6 cf/nearunder_cyl_7x6.txt 4 under 8
./scripts/run_conf2.sh nol8x6 cyl:8x6 cf/nearover_cyl_8x6.txt 4 over 8
./scripts/run_conf2.sh nul8x6 cyl:8x6 cf/nearunder_cyl_8x6.txt 4 under 8
./scripts/run_conf2.sh nol8x8 cyl:8x8 cf/nearover_cyl_8x8.txt 4 over 8
./scripts/run_conf2.sh nul8x8 cyl:8x8 cf/nearunder_cyl_8x8.txt 4 under 8
./scripts/run_conf2.sh nol7x7 cyl:7x7 cf/nearover_cyl_7x7.txt 4 over 8
./scripts/run_conf2.sh nol8x7 cyl:8x7 cf/nearover_cyl_8x7.txt 4 over 8
echo finished > cf/queueNear.done
