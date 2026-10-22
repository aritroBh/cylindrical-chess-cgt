#!/bin/bash
# run_chain.sh W1 W2 ... : runs run_scans.sh for each width in the list, p = 2..7
cd "$(dirname "$0")"
for W in "$@"; do for P in 2 3 4 5 6 7; do
  echo "[$(date +%H:%M:%S)] start w=$W p=$P"; ./run_scans.sh $W $P; done; done
echo "[$(date +%H:%M:%S)] chain done: $*"
