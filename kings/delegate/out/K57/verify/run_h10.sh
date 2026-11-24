#!/bin/zsh
# K57 referee: (B1) for H10 under the sum rule beside -1, P values, and direct sums H10 (+) T for the battery
# logs/T_h10.txt; through heavy.sh under time -l.
cd "$(dirname $0)"
../../../heavy.sh /usr/bin/time -l ./vgsum --board cyl:10x6 --root "Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5" --shuttle g6 \
  --query "Kg4 kf6 Pb3 Pe2 pa3 pb4 pe5 w a4" --query "Kg4 kf6 Pb3 Pe2 pa3 pb4 pe5 w -" \
  --query "Kg4 kg6 Pb3 Pe2 pa3 pb4 pe5 w a4" --query "Kg4 kg6 Pb3 Pe2 pa3 pb4 pe5 w -" \
  --query "Kg4 kf6 Pa4 Pe2 pb4 pe5 b -" --query "Kg4 kg6 Pa4 Pe2 pb4 pe5 b -" \
  --tests logs/T_h10.txt > logs/h10.out 2> logs/h10.err &
P=$!; echo "$P heavy.sh time vgsum H10 $(date)" >> pids.log; wait $P
