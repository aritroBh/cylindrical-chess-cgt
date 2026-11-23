#!/bin/zsh
# K47 item 2: all 275 test games, implementation B, convention $1 (N = Definition 1.2 normal play; C = stalemate draws)
cd "$(dirname $0)"
c=$1
/usr/bin/time -l ./zb_k47 8 6 roots8.txt tests.txt $c > logs/full_B_$c.out 2> logs/full_B_$c.err
echo done > logs/full_B_$c.done
