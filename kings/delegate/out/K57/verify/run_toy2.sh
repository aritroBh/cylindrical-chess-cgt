#!/bin/zsh
# K57 referee: adversarial gadget family, two seeds, through heavy.sh.
cd "$(dirname $0)"
for s in 5 6; do
  ../../../heavy.sh /usr/bin/time -l python3 src/toyref.py $s 2000 200 gadget > logs/toyg_$s.out 2> logs/toyg_$s.err &
  P=$!; echo "$P heavy.sh time toyref gadget seed $s $(date)" >> pids.log; wait $P
done
