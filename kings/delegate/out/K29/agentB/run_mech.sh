#!/bin/zsh
# agentB/run_mech.sh : mechanism classification (scripts/mech2.py, K29 session 2's tool, unchanged) of the first failing context of every
# Phase A class representative, all 13 configurations.  One heavy.sh call.  Output agentB/mech_NAME.txt.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29
cd $D
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
grep -v '^#' scripts/configs.txt | while read name board zs fz dmin rep; do
  src=data/A_$name.txt; [[ $name == cyl7x6_f3 ]] && src=data/screen_cyl7x6_f3.txt
  $PY scripts/mech2.py $board $zs $fz $src > agentB/mech_$name.txt
done
echo "mech done $(date +%H:%M)" >> agentB/progress.txt
