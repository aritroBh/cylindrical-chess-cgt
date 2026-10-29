#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K38
for b in cyl:7x6 flat:7x6; do echo "== kp_p --pmodel $b"; ./bin/kp_p --board $b --pmodel --moves < logs/pos_main.txt; done > logs/kp_p_pmodel.log 2>&1
for b in cyl:7x6 pln:7x6; do echo "== ref3 $b"; ./bin/ref3 --board $b < logs/pos_main.txt; echo "== ref3m $b"; ./bin/ref3m --board $b --moves < logs/pos_main.txt; done > logs/ref3.log 2>&1
echo "== kpsolve cap2 flat:7x6" > logs/kpsolve_cap2_flat.log
./bin/kpsolve --board flat:7x6 --cap 2 --moves < logs/pos_main.txt >> logs/kpsolve_cap2_flat.log 2>&1
