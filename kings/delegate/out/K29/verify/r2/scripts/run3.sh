#!/bin/zsh
# run3.sh TAG CTXFILE GROUPFILE CHUNK  (one heavy.sh call; ref3 only, cyl:7x6, parking Ka1 ka6)
R=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify/r2
( echo "start $(date +%T)"; /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh python3 $R/scripts/drive_ctx.py $1 cyl:7x6 $R/data/$2 "Ka1 ka6" $R/data/$3 $4; echo "end $(date +%T)" ) > $R/logs/$1.out 2>&1
