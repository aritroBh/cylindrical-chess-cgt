#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/verify
while [[ ! -f mine_sweep_done.txt ]]; do sleep 20; done
/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh ./sweep_ext_mine.sh mine_ext.txt
echo DONE > mine_ext_done.txt
