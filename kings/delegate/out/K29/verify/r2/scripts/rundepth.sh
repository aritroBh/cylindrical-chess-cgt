#!/bin/zsh
R=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify/r2
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/data
( echo start $(date +%T); python3 $R/scripts/depthcmp.py cyl:7x6 $D/enum_cyl7x6_f3.txt 30; python3 $R/scripts/depthcmp.py cyl:8x6 $D/enum_cyl8x6_f3.txt 20; python3 $R/scripts/depthcmp.py flat:7x6 $D/enum_flat7x6_f3_z0.txt 15; python3 $R/scripts/depthcmp.py cyl:7x6 $D/enum_cyl7x6_f4.txt 25; echo end $(date +%T) ) > $R/logs/depth.out 2>&1
