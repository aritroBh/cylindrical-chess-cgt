#!/bin/zsh
# task 3: lead profiles with N = 30 spare moves for eight configurations (leads_set.py prints the set of leads).
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
while read b p; do
  /usr/bin/time -l nice -n 15 $D/bin/tempo profile $b $p free 30 2> $D/logs/prof_tmp.time | $PY $D/scripts/leads_set.py
  echo "   [$b $p] $(egrep 'real|maximum resident' $D/logs/prof_tmp.time | tr -s ' ' | tr '\n' ' ')"
done <<'LIST'
cyl:6x6 a2
cyl:6x6 a3
cyl:8x6 a3
cyl:10x6 a3
cyl:12x8 a4
flat:6x6 a2,c4
cyl:8x6 a2,d3
cyl:7x6 a2,c3
LIST
