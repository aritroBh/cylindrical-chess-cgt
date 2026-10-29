#!/bin/zsh
# referee part 2: rf39 on context 1 (Pe2 / pe4) of Z_B on flat 7x6, cap 1 with refinement, both bounds; parked H
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
cd $D/verify
run() { n=$1; shift; i=$1; shift; /usr/bin/time -l $H ./rf39 "$@" < in/$i.in > out/$n.out 2> out/$n.err; }
for B in B; do
  run c1_park_$B c1.park 7 6 0 $B 1 1 1 QRBN QRBN 1
  run c1_$B c1.zh 7 6 0 $B 1 1 1 QRBN QRBN 1
done
echo done > out/p2b.done
