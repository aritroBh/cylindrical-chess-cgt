#!/bin/zsh
# K74 referee: solve one (group, file) run in chunks of 10 contexts, each a short direct run of p74 (measured under
# 30 s and 0.6 GB), one at a time, each under run74.sh (time -l, watchdog on the solver's PID).
# Usage (repository root):  zsh kings/delegate/out/K72/verify/src/chunk74.sh G F N TAG
#   N = 2 (at most 2 + 2 pawns) or 6 (every context); output logs/TAG_p74.out in context order.
# Stops if a chunk exits non-zero, takes 30 s or more, or a watchdog kill is recorded.
V=kings/delegate/out/K72/verify
G=$1; F=$2; N=$3; TAG=$4
python3 -I $V/src/mk74.py pos $G $F $N > $V/tmp/$TAG.in || exit 1
rm -f $V/tmp/${TAG}_ck_*(N) $V/tmp/${TAG}_out_*(N)
split -l 80 $V/tmp/$TAG.in $V/tmp/${TAG}_ck_
: > $V/logs/${TAG}_p74.out
for c in $V/tmp/${TAG}_ck_*; do
  k=${c##*_ck_}
  t0=$SECONDS
  zsh $V/src/run74.sh ${TAG}_$k $c $V/tmp/${TAG}_out_$k || { echo "$TAG chunk $k failed"; exit 3; }
  (( SECONDS - t0 >= 30 )) && { echo "$TAG chunk $k took $((SECONDS - t0)) s; stopped"; exit 4; }
  cat $V/tmp/${TAG}_out_$k >> $V/logs/${TAG}_p74.out
done
echo "$TAG done"
