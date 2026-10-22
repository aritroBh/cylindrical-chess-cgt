#!/bin/sh
cd "$(dirname "$0")"
while [ ! -f batchA.done ]; do sleep 30; done
run() {  # geo FZ Tmax nZs nZsb nCs nCsb tag
  nice -n 10 python3 exh.py $1 $2 $3 $4 $5 $6 $7 exh_$8.json 2>/dev/null >> batchB.log
  nice -n 10 python3 pcheck.py $1 exh_$8.json 20000 2>/dev/null >> batchB.log
}
run cyl:7x5 0,1,2 4 1 1 2 2 U1
run cyl:7x5 0,1,2 4 1 2 2 1 U2
run cyl:7x5 0,1 4 1 1 2 2 U3
run flat:6x5 0,1,2 4 1 1 2 2 U4
run cyl:7x6 0,1,2 4 1 1 1 2 U5
run flat:6x6 0,1,2 4 1 1 2 1 U6
echo done > batchB.done
