#!/bin/zsh
# regenerate the small fsig aggregates that were deleted by mistake (same commands as run_all.sh / run_flat.sh)
D=$(cd "$(dirname "$0")/.." && pwd)
cd $D
for spec in "6 m0" "6 m1" "6 m2" "7 m2"; do set -- ${=spec}
  bin/kg44 --board cyl:${1}x6 --cfgfile cfg/cyl${1}x6_w6_$2.txt --fsig logs/fsig_new_${1}_$2.txt > /dev/null 2>&1; done
bin/kg44 --board cyl:6x6 --maxpairs 2 --fsig logs/fsig_base_6_free.txt > /dev/null 2>&1
for W in 6 7 8 9 10; do for m in 0 1 2; do
  [ -f logs/fsig_base_${W}_m$m.txt.xz ] || bin/kg44 --board cyl:${W}x6 --maxpairs 2 --margin $m --fsig logs/fsig_base_${W}_m$m.txt > /dev/null 2>&1
done; done
for W in 6 7 8; do bin/kg44 --board flat:${W}x6 --maxpairs 2 --margin 0 --fsig logs/fsig_baseflat_${W}_m0.txt > /dev/null 2>&1; done
echo done > logs/regen.done
