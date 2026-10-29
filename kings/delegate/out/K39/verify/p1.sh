#!/bin/zsh
# referee part 1: rf39 on Z_B (3 boards) and Z_C (cyl:8x6) roots + drawing children
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
cd $D/verify
run() { n=$1; shift; i=$1; shift; /usr/bin/time -l $H ./rf39 "$@" < in/$i.in > out/$n.out 2> out/$n.err; }
for B in A B; do
  run ZB_cyl_7x6_${B}_r1 ZB_cyl_7x6 7 6 1 $B 1 1 1 QRBN QRBN 1
  run ZB_cyl_8x6_${B}_r1 ZB_cyl_8x6 8 6 1 $B 1 1 1 QRBN QRBN 1
  run ZB_flat_7x6_${B}_r1 ZB_flat_7x6 7 6 0 $B 1 1 1 QRBN QRBN 1
  run ZC_cyl_8x6_${B}_r1 ZC_cyl_8x6 8 6 1 $B 1 1 1 QRBN QRBN 1
done
run ZC_c2_Ap ZC_cyl_8x6 8 6 1 A 2 1 1 QRBN Q 0
run ZC_c2_Bp ZC_cyl_8x6 8 6 1 B 2 1 1 Q QRBN 0
for B in A B; do
  run ZB_cyl_8x6_${B}_r0 ZB_cyl_8x6 8 6 1 $B 1 1 1 QRBN QRBN 0
  run ZC_cyl_8x6_${B}_r0 ZC_cyl_8x6 8 6 1 $B 1 1 1 QRBN QRBN 0
done
echo done > out/p1.done
