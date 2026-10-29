#!/bin/zsh
# K39: Z_C (cyl:8x6) roots in chess at cap 2, restricted runs (valid one-sided bounds; see FINDINGS):
#  A' (upper bound): Black held to one queen (--capb 1 --promb Q), White one officer of any type (a second one counts as a White win), refine
#  B' (lower bound): White held to one queen, Black one officer of any type, refine
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39
cd $D
scripts/hrun.sh ZC_c2_Ap 1150 in/ZC_roots_cyl_8x6.in bin/kp39 --board cyl:8x6 --ep on --cap 2 --capw 1 --capb 1 --promb Q --bound A --refine --moves --threads 2
scripts/hrun.sh ZC_c2_Bp 1150 in/ZC_roots_cyl_8x6.in bin/kp39 --board cyl:8x6 --ep on --cap 2 --capw 1 --capb 1 --promw Q --bound B --refine --moves --threads 2
