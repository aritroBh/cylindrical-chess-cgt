#!/bin/zsh
# chainM.sh: failure-mechanism classification (scripts/mech2.py) of the first failing context of every failing class representative, one heavy.sh call per configuration.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29
cd $D
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
while read name board zs fz src; do
  [[ -s data/M_${name}.txt ]] && continue
  $H /usr/bin/time -l $PY scripts/mech2.py $board $zs $fz data/$src > data/M_${name}.tmp 2> logs/M_${name}.err
  mv data/M_${name}.tmp data/M_${name}.txt
  echo "M $name done $(date +%H:%M)" >> logs/progress.txt
done <<L
cyl7x6_f3 cyl:7x6 0 3 R_cyl7x6_f3.txt
cyl8x6_f3 cyl:8x6 0 3 R_cyl8x6_f3_A.txt
cyl7x6_f4 cyl:7x6 0 4 R_cyl7x6_f4_A.txt
cyl8x6_f4 cyl:8x6 0 4 R_cyl8x6_f4_A.txt
flat7x6_f3_z0 flat:7x6 0 3 R_flat7x6_f3_z0_A.txt
flat7x6_f3_z2 flat:7x6 2 3 R_flat7x6_f3_z2_A.txt
flat7x6_f4_z0 flat:7x6 0 4 R_flat7x6_f4_z0_A.txt
flat8x6_f3_z0 flat:8x6 0 3 R_flat8x6_f3_z0_A.txt
flat8x6_f3_z2 flat:8x6 2 3 R_flat8x6_f3_z2_A.txt
flat8x6_f4_z0 flat:8x6 0 4 R_flat8x6_f4_z0_A.txt
cyl8x6_f3_d3 cyl:8x6 0 3 R_cyl8x6_f3_d3_A.txt
flat7x6_f3_z0_d3 flat:7x6 0 3 R_flat7x6_f3_z0_d3_A.txt
flat8x6_f3_z0_d3 flat:8x6 0 3 R_flat8x6_f3_z0_d3_A.txt
L
