#!/bin/bash
# run_gapped.sh W1 W2 ... : for each width and p = 4..7 and each split, scanner | cmp_gapped_nim.py -> gapped/w{W}p{P}_{NW}_{NB}.out
cd "$(dirname "$0")"
for W in "$@"; do for P in 4 5 6 7; do for NW in $(seq 1 $((P-1))); do
  NB=$((P-NW)); O=gapped/w${W}p${P}_${NW}_${NB}.out
  [ -s $O ] && continue
  nice -n 15 ./scan_fixed2 --flat --width $W --min $P --max $P --nw $NW --nb $NB --only-setting 2 --max-entries 67108864 2>/dev/null \
    | PYTHONPATH=../.. nice -n 15 ../../.venv/bin/python cmp_gapped_nim.py > $O 2> $O.err
done; done; echo "[$(date +%H:%M:%S)] gapped done w=$W"; done
