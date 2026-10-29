#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
cd $D
$PY me/src/gen3.py hi 60 101 > me/c3_hi60.txt 2>/dev/null
$PY me/src/gen3.py t4 80 202 > me/c3_t4_80.txt 2>/dev/null
split -l 20 me/c3_hi60.txt me/c3_hi60_part_
for z in "Kb3 Pa2 Pc2 kb1 pa3 pc3" "Kb1 Pa2 Pb3 ka3 pb2 pc5"; do
  tag=$(echo $z | tr -d ' ')
  for p in me/c3_hi60_part_*; do
    $H $PY me/src/ctxcheck.py cyl:7x6 cyl:7x6 a1 a6 "$z" $p >> logs/me_c3_$tag.txt 2>&1
  done
  $H $PY me/src/ctxcheck.py cyl:7x6 cyl:7x6 a1 a6 "$z" me/c3_t4_80.txt >> logs/me_c3_$tag.txt 2>&1
done
echo done > logs/me_c3.done
