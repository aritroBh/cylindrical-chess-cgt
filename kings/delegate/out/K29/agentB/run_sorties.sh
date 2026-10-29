#!/bin/zsh
# agentB/run_sorties.sh : sortie tables (agentB/sortie_table.py) of all class representatives, 10 enumeration configurations.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29
cd $D
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
for x in "cyl7x6_f3 cyl:7x6 0 3" "cyl7x6_f4 cyl:7x6 0 4" "cyl8x6_f3 cyl:8x6 0 3" "cyl8x6_f4 cyl:8x6 0 4" "flat7x6_f3_z0 flat:7x6 0 3" "flat7x6_f4_z0 flat:7x6 0 4" "flat7x6_f3_z2 flat:7x6 2 3" "flat8x6_f3_z0 flat:8x6 0 3" "flat8x6_f4_z0 flat:8x6 0 4" "flat8x6_f3_z2 flat:8x6 2 3"; do
  set -- ${=x}
  $PY agentB/sortie_table.py $2 $3 $4 data/rep_$1.txt agentB/sorties_$1.txt
done
echo "sorties done $(date +%H:%M)" >> agentB/progress.txt
