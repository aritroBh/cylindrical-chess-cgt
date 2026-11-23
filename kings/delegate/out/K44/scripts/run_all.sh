#!/bin/zsh
# K44: new window runs (cfgfile) and K20-convention baseline runs (native enumeration, <=2 pairs, files within 4)
D=$(cd "$(dirname "$0")/.." && pwd)
H="$D/../../heavy.sh"
rm -f $D/logs/fsig_*.txt
for W in 6 7 8 9 10; do
  for reg in free m0 m1 m2; do
    $H $D/bin/kg44 --board cyl:${W}x6 --cfgfile $D/cfg/cyl${W}x6_w6_$reg.txt --fsig $D/logs/fsig_new_${W}_$reg.txt > $D/logs/new_${W}_$reg.log 2>&1
  done
  $H $D/bin/kg44 --board cyl:${W}x6 --maxpairs 2 --fsig $D/logs/fsig_base_${W}_free.txt > $D/logs/base_${W}_free.log 2>&1
  for m in 0 1 2; do
    $H $D/bin/kg44 --board cyl:${W}x6 --maxpairs 2 --margin $m --fsig $D/logs/fsig_base_${W}_m$m.txt > $D/logs/base_${W}_m$m.log 2>&1
  done
done
echo done > $D/logs/run_all.done
