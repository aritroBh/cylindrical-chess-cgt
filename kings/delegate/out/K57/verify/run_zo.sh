#!/bin/zsh
# K57 referee: (B1) under the sum rule for Z_O (cyl:8x6, flat 8x6) and its two flat translates, through heavy.sh.
cd "$(dirname $0)"
r() { name=$1; shift
  ../../../heavy.sh /usr/bin/time -l ./vgsum "$@" > logs/$name.out 2> logs/$name.err &
  P=$!; echo "$P heavy.sh time vgsum $name $(date)" >> pids.log; wait $P; }
r ZO_cyl86 --board cyl:8x6 --root "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5" --shuttle d5
r ZO_flat86 --board flat:8x6 --root "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5" --shuttle d5
r ZO_flat86_t1 --board flat:8x6 --root "Kg5 ke4 Pc2 Pc4 Pf2 pb4 pc5 pf5" --shuttle e5
r ZO_flat86_t2 --board flat:8x6 --root "Kh5 kf4 Pd2 Pd4 Pg2 pc4 pd5 pg5" --shuttle f5
