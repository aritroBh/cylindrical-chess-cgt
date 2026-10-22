#!/bin/sh
cd "$(dirname "$0")"
while [ ! -f batchE.done ]; do sleep 30; done
i=600
for cfg in "cyl:8x8 7,0,1 7" "cyl:8x7 7,0,1 6" "flat:8x8 0,1,2 7" "cyl:8x8 3,4,5 7"; do
  set -- $cfg
  i=$((i+1))
  nice -n 10 python3 hunt3.py $i 1500 $1 $2 G$i $3 0.3 3 2>&1 | grep -v "^gen" >> batchF.log
done
echo done > batchF.done
