#!/bin/zsh
# K59 part 2 step 2 (end): Definition 4.8 for the cyl:8x7 groups' translates on flat 9x7, and on flat 8x8 (as placed and
# one rank up), each with ref3m and kp_p (def48.py; every solver call goes through heavy.sh).
cd "$(dirname $0)/.."
for s in flat97 flat88; do
  python3 src/groups59.py ref3m $s > logs/p2b_${s}_ref3m.txt 2>&1
  python3 src/groups59.py kpp $s > logs/p2b_${s}_kpp.txt 2>&1
done
