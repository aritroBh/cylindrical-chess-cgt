#!/bin/zsh
# K59 part 1b: check the --lowmem build against earlier outputs (H10 of K57, T4 of run_p1), then T3 with --lowmem.
cd "$(dirname $0)/.."
src/hrun.sh reg_h10_lowmem bin/vgsum59 --lowmem --board cyl:10x6 --root "Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5" --shuttle g6 \
  --query "Kg4 kf6 Pb3 Pe2 pa3 pb4 pe5 w a4" --query "Kg4 kf6 Pb3 Pe2 pa3 pb4 pe5 w -" \
  --query "Kg4 kg6 Pb3 Pe2 pa3 pb4 pe5 w a4" --query "Kg4 kg6 Pb3 Pe2 pa3 pb4 pe5 w -" \
  --query "Kg4 kf6 Pa4 Pe2 pb4 pe5 b -" --query "Kg4 kg6 Pa4 Pe2 pb4 pe5 b -" --tests in/T_h10.txt
src/hrun.sh reg_T4_lowmem bin/vgsum59 --lowmem --board cyl:8x7 --root "Kc4 ka4 Pb2 Pe3 Pe5 pb6 pe4 pe6" --shuttle a5
