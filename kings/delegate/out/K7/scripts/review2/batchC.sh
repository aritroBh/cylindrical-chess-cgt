#!/bin/sh
cd "$(dirname "$0")"
while [ ! -f batchB.done ]; do sleep 30; done
i=300
for cfg in "cyl:7x6 0,1,2 5" "cyl:7x5 0,1,2 4" "flat:6x6 0,1,2 5" "flat:6x6 3,4,5 5" "cyl:7x6 5,6,0 5" "cyl:7x5 3,4 4"; do
  set -- $cfg
  i=$((i+1))
  nice -n 10 python3 hunt2.py $i 10000 $1 $2 C$i $3 0.35 2>&1 | grep -v "^gen" >> batchC.log
done
echo done > batchC.done
