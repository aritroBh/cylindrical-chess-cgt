#!/bin/zsh
W=$1; H=$2
for w in 0 1 2 3; do
  for b in 0 1 2 3; do
    if [ $w -eq 0 ] && [ $b -eq 0 ]; then continue; fi
    echo "=== W=$W H=$H 3 files w=$w b=$b ==="
    PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames nice -n 10 /Users/aritro/.venv/bin/python search.py $W $H 3 $w $b
  done
done
