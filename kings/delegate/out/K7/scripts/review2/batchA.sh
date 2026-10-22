#!/bin/sh
cd "$(dirname "$0")"
i=100
for cfg in "cyl:7x6 0,1,2 5" "cyl:7x6 6,0,1 5" "cyl:7x5 0,1,2 4" "cyl:7x5 2,3 4" "flat:6x6 0,1,2 5" "flat:6x6 2,3 5" "flat:6x6 3,4,5 5" "cyl:6x6 0,1 5" "cyl:8x6 0,1,2 5" "cyl:7x6 0,1 5" "cyl:7x6 2 5" "flat:7x6 0,1,2 5" "cyl:7x7 0,1,2 5"; do
  set -- $cfg
  i=$((i+1))
  nice -n 10 python3 hunt.py $i 12000 $1 $2 A$i $3 0.55 2>&1 | grep -v "^gen" >> batchA.log
done
echo done > batchA.done
