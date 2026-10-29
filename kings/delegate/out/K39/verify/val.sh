#!/bin/zsh
# referee validation: rf39 on the investigator's random positions, cap 1, bounds A/B, refine 0/1
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
cd $D/verify
for t in cyl_7x6 cyl_8x6 flat_7x6; do
  W=${${t#*_}%x6}; c=0; [[ $t == cyl* ]] && c=1
  for B in A B; do for r in 0 1; do
    /usr/bin/time -l $H ./rf39 $W 6 $c $B 1 1 1 QRBN QRBN $r < $D/in/rand_$t.in > out/val_${t}_${B}_r$r.out 2> out/val_${t}_${B}_r$r.err
  done; done
done
echo done > out/val.done
