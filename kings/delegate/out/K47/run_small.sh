#!/bin/zsh
# K47: small test set, both implementations, both conventions (one heavy slot, sequential)
cd "$(dirname $0)"
for c in N C; do
  ./za_k47 8 6 roots8.txt tests_small.txt $c > logs/small_A_$c.out 2> logs/small_A_$c.err
  ./zb_k47 8 6 roots8.txt tests_small.txt $c > logs/small_B_$c.out 2> logs/small_B_$c.err
done
echo done > logs/small.done
