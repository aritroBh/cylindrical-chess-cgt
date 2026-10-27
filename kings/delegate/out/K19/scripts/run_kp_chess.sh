#!/bin/zsh
# kp (chess, cap 1, exact when both bounds agree) on the position lists, each run through heavy.sh.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K19
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
run() {
  $H $D/kp --board $2 --ep on --promote QRBN --cap 1 --threads 2 --moves < $D/logs/in_$1.txt > $D/logs/kp_$1.txt 2> $D/logs/kp_$1.err
  echo done $1 $(date +%T)
}
run s55 cyl:8x6; run s52a cyl:7x6; run s51 cyl:8x8; run s52 cyl:8x8; run s52f flat:8x8; run s52h cyl:7x6
echo ALLDONE
