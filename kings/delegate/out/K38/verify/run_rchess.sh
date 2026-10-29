#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K38/verify
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
for w in 1 0; do for b in A B; do
  echo "== rchess 7x6 wrap=$w bound $b cap 1"
  /usr/bin/time -l $H zsh -c "ulimit -v 3000000 2>/dev/null; ulimit -t 1200; ./bin/rchess 7 6 $w $b < pos.txt"
done; done > logs/rchess.log 2>&1
