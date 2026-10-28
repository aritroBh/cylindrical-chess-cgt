#!/bin/zsh
# ES7: the same experiment on cyl:7x6 (context files e, f): 25 plain-only king sorties of the 1+1 groups x 59 small contexts
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
for i in $(seq 0 24); do
  bin/kpp --board cyl:7x6 --ep on --pmodel --promote Q --cap 0 --threads 1 < logs/ES7/in_$i.txt > logs/ES7/out_$i.txt 2> logs/ES7/err_$i.txt
done
echo done > logs/ES7_done
