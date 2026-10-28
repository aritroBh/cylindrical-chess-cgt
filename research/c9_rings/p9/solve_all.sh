#!/bin/bash
# solve every 9-pawn ring on C9 (enum_rings.c set and pyenum.py set) with the original rg and with rg_copy; sequential, one rg at a time
cd "$(dirname "$0")"
for set in c py; do
  for sp in 3_6 4_5 5_4 6_3; do
    f=$set/${set}_rings_$sp.txt
    nice -n 15 /usr/bin/python3 -I solve_rings.py $f solve/orig_${set}_$sp --rg original >> solve/orig_${set}_$sp.log 2>&1
  done
  if [ "$set" = c ]; then
    for sp in 3_6 4_5 5_4 6_3; do
      nice -n 15 /usr/bin/python3 -I solve_rings.py $set/${set}_rings_$sp.txt solve/copy_${set}_$sp --rg copy >> solve/copy_${set}_$sp.log 2>&1
    done
  fi
done
echo ALLDONE > solve/ALLDONE
