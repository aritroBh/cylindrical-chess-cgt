#!/bin/zsh
# chainW.sh: witness verification (two solvers each side of the comparison) for the failing groups of phase A (first failing context of each),
# one heavy.sh call per configuration.  Lines "name board zs H" below.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29
cd $D
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
while read name board zs hh; do
  [[ -s logs/witness_${name}_A.txt ]] && continue
  $PY scripts/mkR.py ${name}_A A_${name}.txt
  $H /usr/bin/time -l zsh scripts/verify_witness2.sh ${name}_A $board $zs $hh > logs/W_${name}.out 2> logs/W_${name}.err
  echo "W $name done $(date +%H:%M)" >> logs/progress.txt
done <<L
cyl7x6_f4 cyl:7x6 0 6
cyl8x6_f3 cyl:8x6 0 6
cyl8x6_f3_d3 cyl:8x6 0 6
cyl8x6_f4 cyl:8x6 0 6
flat7x6_f3_z0 flat:7x6 0 6
flat7x6_f3_z0_d3 flat:7x6 0 6
flat7x6_f3_z2 flat:7x6 2 6
flat7x6_f4_z0 flat:7x6 0 6
flat8x6_f3_z0 flat:8x6 0 6
flat8x6_f3_z0_d3 flat:8x6 0 6
flat8x6_f3_z2 flat:8x6 2 6
flat8x6_f4_z0 flat:8x6 0 6
L
