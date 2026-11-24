#!/bin/zsh
# K48: the four exact over groups found by A on cyl:8x7 (files a, b, e), checked from ref3m and kp_p --pmodel move values only
cd "$(dirname $0)/.."
export K48_H=7
for s in ref3m kpp; do
  python3 scripts/verify_hit48.py $s cyl 8 1 "Kd4 kf4 Pa4 Pb5 Pe2 pa5 pb6 pe6 b -" f5
  python3 scripts/verify_hit48.py $s cyl 8 1 "Kd4 kf4 Pb3 Pb5 Pe2 pb4 pb6 pe6 b -" f5
  python3 scripts/verify_hit48.py $s cyl 8 1 "Kc4 ka4 Pb2 Pe3 Pe5 pb6 pe4 pe6 b -" a5
  python3 scripts/verify_hit48.py $s cyl 8 1 "Kd4 kf4 Pb3 Pb5 Pe2 pa5 pb6 pe6 b -" f5
done
