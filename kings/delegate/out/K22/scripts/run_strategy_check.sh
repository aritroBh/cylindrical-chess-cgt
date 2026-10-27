#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
cd $D; OUT=logs/strategy_check.txt; : > $OUT
# a random sample of 2500 roots with at most one attacked s-bar pawn; kings anywhere legal; s king on f above the front pawn
for args in "flat 4 5 0 3 1 3 3" "flat 4 5 0 3 2 3 3" "flat 4 6 0 3 1 3 3" "flat 5 5 0 4 2 3 3" "flat 3 5 0 2 1 3 3" "flat 3 6 0 2 1 3 3" "cyl 4 6 0 3 1 3 3" "cyl 5 5 0 4 2 3 3" "cyl 7 6 0 2 0 2 3" "cyl 7 6 0 2 1 2 3" "cyl 7 6 0 2 2 2 3" "flat 5 6 0 4 2 2 3" "flat 4 4 0 3 1 3 3" "flat 3 4 0 2 1 3 3"; do
  nice -n 10 $PY scripts/strategy_check.py ${=args} 2500 1 ep >> $OUT 2>&1
done
echo ALLDONE >> $OUT
