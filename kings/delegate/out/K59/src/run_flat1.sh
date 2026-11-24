#!/bin/zsh
# K59 part 2: the flat 8x7 hit F1 = Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6 (Black shuttles c4-c5): Definition 4.8 with ref3m and kp_p (def48.py),
# (B1) with vgsum59 (sum rule) and pr57 (pass game), direct sums with vgsum59 (63 games) and pr57 (600 random games).
cd "$(dirname $0)/.."
python3 src/def48.py ref3m flat 8 7 b "Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6" c5 F1_ref3m > logs/F1_def48_ref3m.txt 2>&1
python3 src/def48.py kpp flat 8 7 b "Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6" c5 F1_kpp > logs/F1_def48_kpp.txt 2>&1
src/hrun.sh F1_vgsum bin/vgsum59 --lowmem --board flat:8x7 --root "Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6" --shuttle c5 --tests in/T_h10.txt
src/hrun.sh F1_pr57 bin/pr57 --board flat:8x7 --root "Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6" --shuttle c5 --orient over
src/hrun.sh F1_pr57sum bin/pr57 --board flat:8x7 --root "Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6" --shuttle c5 --orient over --sum in/rnd_all.txt
