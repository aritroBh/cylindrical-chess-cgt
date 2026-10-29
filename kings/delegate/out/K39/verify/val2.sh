#!/bin/zsh
# referee validation 2: rf39 with refinement, bound A, on the first 40 random cyl:8x6 positions of K39
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
cd $D/verify
/usr/bin/time -l $H ./rf39 8 6 1 A 1 1 1 QRBN QRBN 1 < in/rand40_cyl_8x6.in > out/val_cyl_8x6_A_r1.out 2> out/val_cyl_8x6_A_r1.err
echo done > out/val2.done
