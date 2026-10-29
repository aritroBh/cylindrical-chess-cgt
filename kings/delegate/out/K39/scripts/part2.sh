#!/bin/zsh
# K39 part 2: Z_B (flat 7x6) beside context H, chess at cap 1 with the capture refinement, both bounds, two solvers
# (own39p, kp39p); P values (kpp --pmodel, ref3m); the parked comparison H + Ka1 ka6 in chess (both solvers).
# usage: part2.sh ID...
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39
cd $D
for id in "$@"; do
  echo $id > in/ctx/c$id.ids
  python3 -I -B scripts/ctx.py make in/ctx/c$id.ids in/ctx/c$id
  scripts/hrun.sh c${id}_own_b0 1180 in/ctx/c$id.zh.in bin/own39p 7 6 0 0 1 1
  scripts/hrun.sh c${id}_own_b1 1180 in/ctx/c$id.zh.in bin/own39p 7 6 0 1 1 1
  scripts/hrun.sh c${id}_kp_A 1180 in/ctx/c$id.zh.in bin/kp39p --board flat:7x6 --cap 1 --refine --bound A --moves --threads 2
  scripts/hrun.sh c${id}_kp_B 1180 in/ctx/c$id.zh.in bin/kp39p --board flat:7x6 --cap 1 --refine --bound B --moves --threads 2
  bin/kpp --board flat:7x6 --ep on --pmodel --cap 0 < in/ctx/c$id.zh.in > logs/r/c${id}_kpp.out 2> logs/r/c${id}_kpp.err
  bin/ref3m --board pln:7x6 < in/ctx/c$id.zh.in > logs/r/c${id}_ref3m.out 2> logs/r/c${id}_ref3m.err
  bin/kp39p --board flat:7x6 --cap 1 --refine --moves < in/ctx/c$id.park.in > logs/r/c${id}_park_kp.out 2> logs/r/c${id}_park_kp.err
  for B in 0 1; do bin/own39p 7 6 0 $B 1 1 < in/ctx/c$id.park.in > logs/r/c${id}_park_own_b$B.out 2> logs/r/c${id}_park_own_b$B.err; done
done
