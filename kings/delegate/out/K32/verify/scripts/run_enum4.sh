#!/bin/zsh
# referee K32: enumerate the 4-node rooted stopper classes in 64 chunks of the outer loop (1024 values of the Left matrix each);
# each chunk is far below one CPU-minute, run at nice -n 15 without the lock
V=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K32/verify
for c in {0..63}; do
  lo=$((c*1024)); hi=$(((c+1)*1024))
  [[ -s $V/logs/enum4/chunk_$c.txt ]] && continue
  nice -n 15 $V/bin/vref_tmp enum4 $lo $hi 3 > $V/logs/enum4/chunk_$c.tmp && mv $V/logs/enum4/chunk_$c.tmp $V/logs/enum4/chunk_$c.txt
done
echo done > $V/logs/enum4/DONE
