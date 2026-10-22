#!/bin/sh
cd "$(dirname "$0")"
while [ ! -f batchC.done ]; do sleep 30; done
i=400
for cfg in "cyl:7x6 0,1,2 5" "cyl:7x5 0,1,2 4" "flat:6x6 0,1,2 5" "cyl:7x6 4,5,6 5" "flat:6x6 2,3,4 5"; do
  set -- $cfg
  i=$((i+1))
  nice -n 10 python3 tr.py $i 5000 $1 $2 D$i $3 2>&1 | grep -v "^Y " >> batchD.log
done
echo done > batchD.done
