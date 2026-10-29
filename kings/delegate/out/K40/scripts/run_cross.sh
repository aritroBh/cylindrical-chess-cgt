#!/bin/zsh
# K40 cross-check kpsum.c vs ksum2.py on every board (heavy.sh slot, nice 15)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K40
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
HV=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
for b in "3 6 12" "4 6 12" "5 6 12" "6 6 12" "7 6 6" "8 6 4" "3 8 12" "4 8 12" "5 8 6" "6 8 4" "7 8 2" "8 8 2"; do
  $HV $PY scripts/cross2.py ${=b}
done
