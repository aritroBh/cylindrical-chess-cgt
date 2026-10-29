#!/bin/zsh
# runshard.sh TAG BOARD FILES MW MB LO HI "PARK0" "PARK1" GROUPFILE [nokpp]  -> logs/TAG.out (one heavy.sh call)
R=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify/r2
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
TAG=$1; shift
( echo "start $(date +%T)"; $H python3 $R/scripts/drive.py $TAG "$@"; echo "end $(date +%T)" ) > $R/logs/$TAG.out 2>&1
