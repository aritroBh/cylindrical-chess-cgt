#!/bin/zsh
# K59: vgsum59 must reproduce the K57 referee's vgsum outputs (H10 with its 63 tests and queries; Z_O flat 8x6).
cd "$(dirname $0)/.."
src/hrun.sh reg_h10 bin/vgsum59 --board cyl:10x6 --root "Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5" --shuttle g6 \
  --query "Kg4 kf6 Pb3 Pe2 pa3 pb4 pe5 w a4" --query "Kg4 kf6 Pb3 Pe2 pa3 pb4 pe5 w -" \
  --query "Kg4 kg6 Pb3 Pe2 pa3 pb4 pe5 w a4" --query "Kg4 kg6 Pb3 Pe2 pa3 pb4 pe5 w -" \
  --query "Kg4 kf6 Pa4 Pe2 pb4 pe5 b -" --query "Kg4 kg6 Pa4 Pe2 pb4 pe5 b -" --tests in/T_h10.txt
src/hrun.sh reg_zoflat bin/vgsum59 --board flat:8x6 --root "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5" --shuttle d5
