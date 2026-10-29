#!/bin/zsh
# waits for chain2.sh, then P-model confirmation of the dud_D-type groups on cyl:7x6 (kp_p build kpp15), through the lock, 1100 s alarm per batch
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/v2
while kill -0 $(cat chain2.pid) 2>/dev/null; do sleep 30; done
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
for b in conf7/b?_00; do
  $H perl -e 'alarm 1100; exec @ARGV' ./kpp15 --board cyl:7x6 --ep on --cap 1 --pmodel < $b > $b.out 2> $b.err
  echo "done $b exit=$? lines=$(wc -l < $b.out)" >> runs/chain.log
done
echo "chain3 finished" >> runs/chain.log
