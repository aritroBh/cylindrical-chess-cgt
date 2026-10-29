#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K40
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
HV=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
for b in "8 6 4" "5 8 6" "6 8 4" "7 8 2" "8 8 2"; do
  $HV /usr/bin/time -l $PY scripts/cross2.py ${=b}
done
