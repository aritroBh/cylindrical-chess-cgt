#!/bin/zsh
# usage: runone.sh BOARD nW nB   (own enumerator + ref3m; TMAX=2 so totals 0,1,2 are complete)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/verify
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
tag=$(echo $1 | tr ':' '_')_$2$3
rm -rf work/$tag; CHUNK=60000 nice -n 15 $PY scripts/ref_enum.py gen $1 $2 $3 work/$tag
TMAX=2 TAG=$tag nice -n 15 $PY scripts/ref_enum.py run $1 $2 $3 work/$tag 2>/dev/null | grep -v "^stage2 total" > logs/own_$tag.txt
cat logs/own_$tag.txt
