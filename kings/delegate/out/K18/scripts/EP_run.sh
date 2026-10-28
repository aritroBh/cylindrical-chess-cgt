#!/bin/zsh
# EP: 25 plain-only king sorties (1+1 groups) x the 5 promotion-free zero contexts (2+2 pawns, shared-gap tempo pairs)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
for i in $(seq 0 24); do
  bin/kpp --board cyl:8x6 --ep on --pmodel --promote Q --cap 0 --threads 1 < logs/EP/in_$i.txt > logs/EP/out_$i.txt 2> logs/EP/err_$i.txt
done
echo done > logs/EP_done
