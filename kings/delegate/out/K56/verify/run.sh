#!/bin/zsh
# K56 referee: pass-game check of Z_O (cyl:8x6) and H10 (cyl:10x6) with vg, each through heavy.sh under time -l.
cd "$(dirname $0)"
r() { name=$1; shift
  ../../../heavy.sh /usr/bin/time -l ./vg "$@" > logs/$name.out 2> logs/$name.err &
  P=$!; echo "$P heavy.sh time vg $name $(date)" >> pids.log; wait $P; }
r H10 --board cyl:10x6 --root "Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5" --shuttle g6 --sample 400 --seed 7 --samplefile logs/H10.sample
r ZO --board cyl:8x6 --root "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5" --shuttle d5 --sample 400 --seed 11 --samplefile logs/ZO.sample \
  --query "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe4 w -" --query "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe4 b -"
