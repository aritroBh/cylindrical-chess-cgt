#!/bin/zsh
# K59 part 2 step 1: Definition 4.8 on flat 8x7 for the cyl:8x7 groups and their translates, ref3m then kp_p.
cd "$(dirname $0)/.."
python3 src/groups59.py ref3m flat87 > logs/p2a_ref3m.txt 2>&1
python3 src/groups59.py kpp flat87 > logs/p2a_kpp.txt 2>&1
