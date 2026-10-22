#!/bin/sh
cd "$(dirname "$0")"
while [ ! -f batchD.done ]; do sleep 30; done
i=500
for cfg in "cyl:7x4 0,1,2 4" "flat:6x4 0,1,2 4" "cyl:5x6 0 5" "cyl:6x6 0,1,2 5" "flat:5x6 0,1 5" "cyl:8x5 0,1,2 4" "cyl:6x5 0,1 4"; do
  set -- $cfg
  i=$((i+1))
  nice -n 10 python3 hunt.py $i 8000 $1 $2 E$i $3 0.5 2>&1 | grep -v "^gen" >> batchE.log
  nice -n 10 python3 hunt2.py $((i+50)) 6000 $1 $2 F$i $3 0.35 2>&1 | grep -v "^gen" >> batchE.log
done
echo done > batchE.done
