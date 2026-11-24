#!/bin/zsh
# K57 referee: abstract brute force of Lemma 4.15 / Proposition 4.14, four seeds, through heavy.sh.
cd "$(dirname $0)"
for s in 1 2 3 4; do
  ../../../heavy.sh /usr/bin/time -l python3 src/toyref.py $s 2000 200 > logs/toy_$s.out 2> logs/toy_$s.err &
  P=$!; echo "$P heavy.sh time toyref seed $s $(date)" >> pids.log; wait $P
done
