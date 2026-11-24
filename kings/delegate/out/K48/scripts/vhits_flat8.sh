#!/bin/zsh
# K48: the flat 8x6 hits checked from ref3m and kp_p --pmodel move values only (verify_hit48.py)
cd "$(dirname $0)/.."
for s in ref3m kpp; do
  python3 scripts/verify_hit48.py $s flat 8 1 "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5 b -" d5
  python3 scripts/verify_hit48.py $s flat 8 0 "Kd2 kf2 Pa3 Pb2 Pe2 pb3 pb5 pe5 w -" d3
done
