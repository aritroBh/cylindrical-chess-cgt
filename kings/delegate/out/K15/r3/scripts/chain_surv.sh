#!/bin/zsh
# K15 r3: more tests of the surviving near-over candidate Z* = Kd5 kb5 Pa3 Pb2 Pd2 pa4 pc5 pd4 (unlocked chunks of <= 58 CPU-s, one process at a time)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/r3
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
Z="Kd5 kb5 Pa3 Pb2 Pd2 pa4 pc5 pd4"
python3 scripts/ctxexh_chunked.py cyl:8x6 over f "$Z" logs/ctxexh_surv_chunked.txt 4 3 > logs/surv_f.out 2>&1
python3 scripts/ctxexh_chunked.py cyl:7x6 over f "$Z" logs/ctxexh_surv_chunked.txt 4 3 > logs/surv_7f.out 2>&1
echo finished > logs/surv_chain.done
