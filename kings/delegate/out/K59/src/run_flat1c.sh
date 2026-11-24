#!/bin/zsh
# K59: F1 = Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6 as placed on flat 9x7 and flat 8x8: (B1) and direct sums with vgsum59 and pr57.
cd "$(dirname $0)/.."
for b in 9x7 8x8; do
  src/hrun.sh F1_${b}_vgsum bin/vgsum59 --lowmem --board flat:$b --root "Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6" --shuttle c5 --tests in/T_h10.txt
  src/hrun.sh F1_${b}_pr57 bin/pr57 --board flat:$b --root "Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6" --shuttle c5 --orient over
  src/hrun.sh F1_${b}_pr57sum bin/pr57 --board flat:$b --root "Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6" --shuttle c5 --orient over --sum in/rnd_all.txt
done
