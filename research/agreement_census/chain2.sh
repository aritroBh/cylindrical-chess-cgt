#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/research/agreement_census
while [ ! -f logs/chain1.done ]; do sleep 10; done
g() { python3 -I guard.py "$@"; }
g work/flat_5x6_x3 flat:5x6 Q 2 F --frozen
g work/flat_5x6_x3 flat:5x6 Q 2 Q2
g work/cyl_6x6_x3 cyl:6x6 Q 2 F --frozen
g work/cyl_6x6_x3 cyl:6x6 Q 2 Q2
g work/cyl_5x5_x3 cyl:5x5 Q 1 F --frozen
g work/cyl_5x5_x3 cyl:5x5 Q 1 Q1
g work/cyl_5x5 cyl:5x5 QRBN 1 QRBN1
g work/flat_5x6 flat:5x6 QRBN 1 QRBN1
echo chain2 done > logs/chain2.done
