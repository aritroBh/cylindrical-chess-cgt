#!/bin/zsh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K24/verify
for b in cyl:8x8 flat:8x8; do for m in p ww bb; do echo "== $m $b"; $PY psolve.py $b $m --moves < pos.txt; done; done
