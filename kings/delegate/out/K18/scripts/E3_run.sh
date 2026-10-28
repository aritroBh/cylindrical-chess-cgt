#!/bin/zsh
# E3: reduced context family (159 contexts) for 12 sorties; ~10 CPU-seconds per sortie, two small workers (even / odd)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
for i in "$@"; do
  bin/kpp --board cyl:8x6 --ep on --pmodel --promote Q --cap 0 --threads 1 < logs/E3/in_$i.txt > logs/E3/out_$i.txt 2> logs/E3/err_$i.txt
done
