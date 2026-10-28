#!/bin/zsh
S=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/scripts
$S/run_rand.sh cyl:6x6 3 3 net 6 100000 1000 RN_c66
$S/run_rand.sh flat:6x6 3 3 net 6 100000 1300 RN_f66
$S/run_rand.sh cyl:7x6 3 3 net 6 100000 1100 RN_c76
$S/run_rand.sh flat:7x6 3 3 net 4 100000 1400 RN_f76
$S/run_rand.sh cyl:8x6 3 3 net 4 100000 1200 RN_c86
$S/run_rand.sh cyl:6x6 3 3 scene 5 100000 2000 RS_c66
$S/run_rand.sh flat:6x6 3 3 scene 5 100000 2100 RS_f66
$S/run_rand.sh cyl:7x6 3 3 scene 5 100000 2200 RS_c76
$S/run_rand.sh cyl:8x6 3 3 scene 4 100000 2300 RS_c86
$S/run_rand.sh flat:7x6 3 3 scene 4 100000 2400 RS_f76
$S/run_rand.sh cyl:6x6 3 3 uniform 5 150000 3000 RU_c66
$S/run_rand.sh flat:6x6 3 3 uniform 5 150000 3100 RU_f66
$S/run_rand.sh cyl:7x6 3 3 uniform 5 150000 3200 RU_c76
$S/run_rand.sh cyl:8x6 3 3 uniform 4 150000 3300 RU_c86
$S/run_rand.sh flat:7x6 3 3 uniform 4 150000 3400 RU_f76
