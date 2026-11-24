#!/bin/zsh
# K57 referee: smallest input first (a 1 + 1 group on cyl:10x6), through heavy.sh, memory measured.
cd "$(dirname $0)"
../../../heavy.sh /usr/bin/time -l ./vgsum --board cyl:10x6 --root "Kg4 kf6 Pe2 pe5" --shuttle g6 --tests logs/T_h10.txt > logs/small.out 2> logs/small.err &
P=$!; echo "$P heavy.sh time vgsum small $(date)" >> pids.log; wait $P
