#!/bin/zsh
# K59: F1's translates on flat 8x7 and 9x7 and its versions on flat 8x8, Definition 4.8 with ref3m and kp_p.
cd "$(dirname $0)/.."
for s in F1_87 F1_97 F1_88; do
  python3 src/groups59.py ref3m $s > logs/p2c_${s}_ref3m.txt 2>&1
  python3 src/groups59.py kpp $s > logs/p2c_${s}_kpp.txt 2>&1
done
