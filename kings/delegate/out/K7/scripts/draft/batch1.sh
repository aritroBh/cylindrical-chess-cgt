#!/bin/sh
cd "$(dirname "$0")"
for cfg in "11 1500 7 6 cyl c76a 4" "12 1500 7 5 cyl c75a 4" "13 1500 6 6 flat f66a 4" "14 1500 8 6 cyl c86a 4" "15 1500 7 7 cyl c77a 4" "16 1500 7 6 cyl c76b 5"; do
  set -- $cfg
  nice -n 10 python3 run_win.py $1 $2 $3 $4 $5 $6 $7 > log_$6.txt 2>&1
done
echo finished > batch1.done
