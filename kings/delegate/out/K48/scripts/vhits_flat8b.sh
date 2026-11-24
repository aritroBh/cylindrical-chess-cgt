#!/bin/zsh
# K48: the two further flat 8x6 hits (translates of Z_O by one and two files) checked from ref3m and kp_p --pmodel move values only
cd "$(dirname $0)/.."
for s in ref3m kpp; do
  python3 scripts/verify_hit48.py $s flat 8 1 "Kg5 ke4 Pc2 Pc4 Pf2 pb4 pc5 pf5 b -" e5
  python3 scripts/verify_hit48.py $s flat 8 1 "Ka5 kc4 Pb2 Pe2 Pe4 pb5 pe5 pf4 b -" c5
done
