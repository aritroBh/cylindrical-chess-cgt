#!/bin/zsh
# exhaustive sim sweeps that are individually below one CPU-minute (run directly, nice 15): all five boards at <= 2+2
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
S=$D/scripts
for b in cyl:6x6 cyl:7x6 cyl:8x6 flat:6x6 flat:7x6; do
  t=${b//[:x]/}
  nice -n 15 $S/bundle_ex.sh $b 2 2 1 0 0 EXD_${t}_22
done
for b in cyl:6x6 cyl:7x6; do
  t=${b//[:x]/}
  nice -n 15 $S/bundle_ex.sh $b 3 2 1 0 0 EXD_${t}_32
  nice -n 15 $S/bundle_ex.sh $b 2 3 1 0 0 EXD_${t}_23
done
