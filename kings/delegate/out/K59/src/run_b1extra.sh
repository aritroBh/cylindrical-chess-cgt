#!/bin/zsh
# K59: (B1) with vgsum59 and pr57 for the placements of F2..F5 that are exact on flat 9x7 and 8x8 (def48, two solvers).
cd "$(dirname $0)/.."
b1() { tag=$1; B=$2; G=$3; z=$4
  src/hrun.sh ${tag}_vgsum bin/vgsum59 --lowmem --board flat:$B --root "$G" --shuttle $z
  src/hrun.sh ${tag}_pr57 bin/pr57 --board flat:$B --root "$G" --shuttle $z --orient over; }
b1 X97_F2 9x7 "Ka4 kc4 Pb2 Pf5 pb6 pf6" c5
b1 X97_F3 9x7 "Ke4 kc4 Pb2 Pb5 Pf5 pb6 pf6" c5
b1 X97_F3t1 9x7 "Kf4 kd4 Pc2 Pc5 Pg5 pc6 pg6" d5
b1 X97_F3t2 9x7 "Kg4 ke4 Pd2 Pd5 Ph5 pd6 ph6" e5
b1 X97_F4 9x7 "Kc4 ke4 Pb5 Pf2 Pf5 pb6 pf6" e5
b1 X97_F4t1 9x7 "Kd4 kf4 Pc5 Pg2 Pg5 pc6 pg6" f5
b1 X97_F4t2 9x7 "Ke4 kg4 Pd5 Ph2 Ph5 pd6 ph6" g5
b1 X97_F5 9x7 "Ka4 kc4 Pb2 Pe5 Pf4 pb6 pe6 pf5" c5
b1 X88_F2 8x8 "Ka4 kc4 Pb2 Pf5 pb6 pf6" c5
b1 X88_F3 8x8 "Ke4 kc4 Pb2 Pb5 Pf5 pb6 pf6" c5
b1 X88_F3t1 8x8 "Kf4 kd4 Pc2 Pc5 Pg5 pc6 pg6" d5
b1 X88_F4 8x8 "Kc4 ke4 Pb5 Pf2 Pf5 pb6 pf6" e5
b1 X88_F4t1 8x8 "Kd4 kf4 Pc5 Pg2 Pg5 pc6 pg6" f5
