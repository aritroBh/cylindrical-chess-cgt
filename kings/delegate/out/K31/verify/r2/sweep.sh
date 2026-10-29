#!/bin/zsh
# sweep.sh Hmin Hmax Wmin Wmax out : own LK3 classification of every single pair (file a, rank r=2..H-2), cylinder, free board
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/verify/r2
out=$5; : > $out
for H in {$1..$2}; do for W in {$3..$4}; do for r in {2..$((H-2))}; do
  ./bin/lk3 cls cyl $W $H a$r dump >> $out
done; done; done
echo DONE >> $out
