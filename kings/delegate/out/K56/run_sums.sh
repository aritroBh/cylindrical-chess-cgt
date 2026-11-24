#!/bin/zsh
# K56: D-sum results of the 2 + 3 group (H10) and of Z_O beside test games, for comparison with over (src/over56.py).
cd "$(dirname $0)"
./hrun.sh S_rnd_ZO  src/pr56c --board cyl:8x6  --root "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5" --shuttle d5 --sum tests/rnd_all.txt
./hrun.sh S_rnd_H10 src/pr56c --board cyl:10x6 --root "Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5" --shuttle g6 --sum tests/rnd_all.txt
./hrun.sh S_k47_H10 src/pr56c --board cyl:10x6 --root "Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5" --shuttle g6 --sum tests/k47_le30.txt
./hrun.sh S_k55_H10 src/pr56c --board cyl:10x6 --root "Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5" --shuttle g6 --sum tests/k55_le30.txt
