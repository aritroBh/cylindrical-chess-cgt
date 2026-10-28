#!/bin/zsh
# ES: 25 plain-only king sorties of the 1+1 groups x 125 small contexts (4 pawns in all), P model; a few CPU-seconds each
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
for i in $(seq 0 24); do
  bin/kpp --board cyl:8x6 --ep on --pmodel --promote Q --cap 0 --threads 1 < logs/ES/in_$i.txt > logs/ES/out_$i.txt 2> logs/ES/err_$i.txt
done
echo done > logs/ES_done
