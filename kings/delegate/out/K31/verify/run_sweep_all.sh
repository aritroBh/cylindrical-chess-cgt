#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/verify
for H in 4 5 6 7 8 9 10 11 12; do
  /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh ./sweep_mine.sh 3 26 $H $H mine_H$H.txt
done
echo DONE > mine_sweep_done.txt
