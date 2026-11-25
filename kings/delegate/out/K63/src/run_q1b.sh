#!/bin/zsh
# K63 question 1 for F1, F3, F4 on flat 8x8: own39 bounds A and B (refinement), then kp39 --refine under a 2.2 GB
# RSS watchdog for my own child only (stopped and reported if it would go over).
cd "$(dirname $0)/.."
for f in F1 F3 F4; do
  I=in/${f}_88_chess.in
  [[ -s logs/${f}_own_A.out ]] || zsh src/hrun.sh ${f}_own_A $I bin/own39 8 8 0 0 1 1
  zsh src/hrun.sh ${f}_own_B $I bin/own39 8 8 0 1 1 1
done
for f in F1 F3 F4; do
  zsh src/hrun.sh ${f}_kp39r in/${f}_88_chess.in zsh src/watch2.sh 2200000 bin/kp39 --board flat:8x8 --ep on --promote QRBN --cap 1 --refine --moves
  grep -q WATCHDOG logs/${f}_kp39r.err && break
done
echo done > logs/q1b.done
