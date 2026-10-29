#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29
cd $D
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
while read name board zs fz res rep ns; do
  [[ -s logs/wsym_${name}.txt ]] && continue
  $H /usr/bin/time -l zsh scripts/wsym_run.sh $name $board $zs $fz $res $rep $ns > logs/S_${name}.out 2> logs/S_${name}.err
  echo "S $name done $(date +%H:%M)" >> logs/progress.txt
done <<L
cyl7x6_f3 cyl:7x6 0 3 R_cyl7x6_f3.txt cyl7x6_f3 10
cyl8x6_f3 cyl:8x6 0 3 R_cyl8x6_f3_A.txt cyl8x6_f3 10
cyl7x6_f4 cyl:7x6 0 4 R_cyl7x6_f4_A.txt cyl7x6_f4 10
cyl8x6_f4 cyl:8x6 0 4 R_cyl8x6_f4_A.txt cyl8x6_f4 10
flat7x6_f3_z0 flat:7x6 0 3 R_flat7x6_f3_z0_A.txt flat7x6_f3_z0 10
flat7x6_f3_z2 flat:7x6 2 3 R_flat7x6_f3_z2_A.txt flat7x6_f3_z2 10
flat7x6_f4_z0 flat:7x6 0 4 R_flat7x6_f4_z0_A.txt flat7x6_f4_z0 10
flat8x6_f3_z0 flat:8x6 0 3 R_flat8x6_f3_z0_A.txt flat8x6_f3_z0 10
flat8x6_f3_z2 flat:8x6 2 3 R_flat8x6_f3_z2_A.txt flat8x6_f3_z2 10
flat8x6_f4_z0 flat:8x6 0 4 R_flat8x6_f4_z0_A.txt flat8x6_f4_z0 10
L
