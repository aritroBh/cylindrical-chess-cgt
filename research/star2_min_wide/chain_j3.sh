#!/bin/bash
# connected rows (every file occupied) for widths 1..4 and p = 2..6, all splits, cylcgt vs scanner, every row
cd "$(dirname "$0")"
for W in 1 2 3 4; do for P in 2 3 4 5 6; do [ $W -le $P ] || continue; for NW in $(seq 1 $((P-1))); do
  ./run_conn.sh $W $P $NW 0 99999999
done; done; done
