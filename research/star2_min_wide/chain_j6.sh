#!/bin/bash
# variant S (e.p. rights persist per component) vs variant R (real-chess e.p. expiry), row by row, all gapped-capable (w,p,split)
cd "$(dirname "$0")"
for W in 3 4 5 6 7 8; do for P in 4 5 6 7; do for NW in $(seq 1 $((P-1))); do
  O=sr/w${W}p${P}_${NW}_$((P-NW)).out; [ -s $O ] && continue
  PYTHONPATH=../.. ../../.venv/bin/python cmp_SR.py $W $P $NW > $O 2>&1
done; done; echo "[$(date +%H:%M:%S)] SR done w=$W"; done
