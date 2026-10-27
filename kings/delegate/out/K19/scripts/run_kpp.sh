#!/bin/zsh
# kp_p (P model) on the position lists of fullboard.py. Small runs (seconds), no heavy.sh needed.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K19
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
run() {
  $PY $D/scripts/fullboard.py list $1 > $D/logs/in_$1.txt
  ( time timeout 100 $D/kp_p --board $2 --ep on --promote QRBN --cap 1 --pmodel --threads 1 < $D/logs/in_$1.txt > $D/logs/kpp_$1.txt 2> $D/logs/kpp_$1.err ) 2>&1 | grep real
  head -c 300 $D/logs/kpp_$1.err
}
run s51 cyl:8x8; run s52 cyl:8x8; run s52f flat:8x8; run s52a cyl:7x6; run s55 cyl:8x6
