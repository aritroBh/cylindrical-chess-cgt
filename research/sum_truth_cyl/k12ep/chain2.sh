#!/bin/bash
echo $$ > chain2.pid
cd /Users/aritro/Downloads/Research/Chessendgames/research/sum_truth_cyl/k12ep
for b in 6x6 8x6 7x6; do
  nice -n 15 /usr/bin/time -l ../../../kings/kpsolve --board cyl:$b --frozen --cap 1 --threads 2 < ep_${b}_in.txt > ep_${b}_out.txt 2> ep_${b}_kp.err
done
