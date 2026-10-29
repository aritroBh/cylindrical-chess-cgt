#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
cd $D
for c in "cyl:7x6 cyl7x6_f4 0 4" "cyl:8x6 cyl8x6_f4 0 4" "flat7x6 flat7x6_f4_z0 0 4" "flat8x6 flat8x6_f4_z0 0 4"; do
  set -- ${=c}
  $H $PY me/src/enum_own.py $1 $2 $3 $4 me/enum_own_$2.txt > logs/me_enum_$2.out 2>&1
  $PY me/src/cmp_enum_own.py me/enum_own_$2.txt ../data/enum_$2.txt >> logs/me_enum_$2.out 2>&1
done
echo done > logs/me_enum_f4.done
