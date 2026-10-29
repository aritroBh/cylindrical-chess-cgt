#!/bin/zsh
# usage: partial_cmp.sh TAG  -> compares whatever chunk outputs exist (missing positions are reported as missing); writes cf/TAGp.* (not cf/TAG.*)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
t=$1
cp cf/$t.rows.json cf/${t}p.rows.json
cat cf/$t.chunk.??.out > cf/${t}p.out 2>/dev/null
$PY conf2.py cmp cf/${t}p cf/${t}p.out > cf/${t}p.cmp.txt
cat cf/${t}p.cmp.txt
