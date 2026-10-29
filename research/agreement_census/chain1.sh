#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/research/agreement_census
g() { python3 -I guard.py "$@"; }
g work/cyl_5x5 cyl:5x5 Q 2 F --frozen
g work/cyl_4x4 cyl:4x4 Q 2 F --frozen
g work/cyl_4x4 cyl:4x4 QRBN 2 QRBN2
g work/flat_5x6 flat:5x6 Q 2 Q2
g work/flat_5x6 flat:5x6 Q 2 F --frozen
g work/flat_5x6 flat:5x6 QRBN 2 QRBN2
g work/cyl_5x5 cyl:5x5 QRBN 2 QRBN2
g work/cyl_6x6 cyl:6x6 Q 2 F --frozen
g work/cyl_6x6 cyl:6x6 Q 2 Q2
echo chain1 done > logs/chain1.done
