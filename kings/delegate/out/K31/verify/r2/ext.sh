#!/bin/zsh
# outside K31's grid: H=13,14 with W=4..12 (all ranks), W=27..34 with H=4..6 (all ranks)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/verify/r2
for H in 13 14; do for W in {4..12}; do for r in {2..$((H-2))}; do ./bin/lk3 cls cyl $W $H a$r dump; done; done; done
for H in 4 5 6; do for W in {27..34}; do for r in {2..$((H-2))}; do ./bin/lk3 cls cyl $W $H a$r dump; done; done; done
echo DONE
