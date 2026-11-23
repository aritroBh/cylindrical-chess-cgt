#!/bin/zsh
cd "$(dirname $0)"
{
for W in 8 9; do for s in ref3m kpp; do
 python3 verify_hit.py $s $W 1 "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5 b -" d5
 python3 verify_hit.py $s $W 0 "Kd2 kf2 Pa3 Pb2 Pe2 pb3 pb5 pe5 w -" d3
 python3 verify_hit.py $s $W 1 "Ke5 kg4 Pa2 Pa4 Pf2 pb4 pa5 pf5 b -" g5
 python3 verify_hit.py $s $W 0 "Kg2 ke2 Pa2 Pb3 Pf2 pa3 pa5 pf5 w -" g3
done; done
} > verify_hits_W8_W9.txt 2>&1
echo done > logs/verify2.done
