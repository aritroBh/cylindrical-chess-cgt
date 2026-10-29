#!/bin/zsh
# K15 r3: exhaustive single-file contexts (3^(H-2) assignments, both sides to move) for the surviving near-over candidate, through the lock.
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/r3
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
P=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
S=../fin2/scripts/ctx_exh.py
for spec in "cyl:8x6 f" "cyl:8x6 g" "cyl:7x6 e" "cyl:7x6 f"; do
  set -- ${=spec}
  $H $P $S $1 over $2 "Kd5 kb5 Pa3 Pb2 Pd2 pa4 pc5 pd4" >> logs/ctxexh_surv.txt 2>&1
  echo "done $spec $(date +%T)" >> logs/ctxexh_surv.log
done
echo finished >> logs/ctxexh_surv.log
