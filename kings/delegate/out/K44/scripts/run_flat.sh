#!/bin/zsh
D=$(cd "$(dirname "$0")/.." && pwd)
cd $D
rm -f logs/fsig_baseflat_*.txt
for W in 6 7 8; do
  bin/kg44 --board flat:${W}x6 --maxpairs 2 --fsig logs/fsig_baseflat_${W}_free.txt > logs/baseflat_${W}_free.log 2>&1
  for m in 0 1 2; do
    bin/kg44 --board flat:${W}x6 --maxpairs 2 --margin $m --fsig logs/fsig_baseflat_${W}_m$m.txt > logs/baseflat_${W}_m$m.log 2>&1
  done
done
echo done > logs/run_flat.done
