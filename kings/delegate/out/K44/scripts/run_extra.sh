#!/bin/zsh
D=$(cd "$(dirname "$0")/.." && pwd)
cd $D
for spec in "10 7" "9 7" "8 7" "7 7" "6 7" "9 8" "8 8" "7 8" "6 8"; do
  set -- ${=spec}
  python3 scripts/lk_extra.py $1 $2 cfg/cyl${1}x${2}_w6_free.txt cyl${1}x${2}_free >> logs/run_extra.out 2>&1
done
echo done >> logs/run_extra.out
