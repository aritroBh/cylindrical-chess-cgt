#!/bin/zsh
# second small worker for the E1 module contexts (about 1 CPU-second per sortie), highest indices first
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
for i in $(seq 31 -1 10); do
  bin/kpp --board cyl:8x6 --ep on --pmodel --promote Q --cap 0 < logs/E1/in_$i.txt > logs/E1b/out_$i.txt 2>/dev/null
done
echo done > logs/E1b_done
