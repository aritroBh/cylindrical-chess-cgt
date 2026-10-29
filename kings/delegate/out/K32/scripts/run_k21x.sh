#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K32
export PYTHONDONTWRITEBYTECODE=1
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh sh -c "$PY $D/scripts/crosscheck_k21.py 4 $D/data/B_4.txt $D/data/classes_4.txt 20 > $D/logs/k21x_N4_stride20.txt 2>&1"
echo "k21x done $(date +%T)" >> $D/logs/k21x.log
