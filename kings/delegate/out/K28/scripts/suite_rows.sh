#!/bin/zsh
# suite_rows.sh : restricted-bound second check of rows 1-4 with kq3 (one heavy.sh job, solvers under watch2.sh).
#   L claims (Black wins): bound A with Black restricted to ONE officer, a queen (A' >= A >= true, so A' = L proves L).
#   W claims (White wins): bound B with White restricted to ONE officer, a queen (B' <= B <= true, so B' = W proves W).
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K28
cd $D; mkdir -p logs/rows
step() {  # step NAME IN CMD...
  n=$1; in=$2; shift 2
  # guard: never more than 2 of my solver processes at once (the shared lock has been seen to lose a slot under load)
  while [ $(ps -eo command | grep -cE '^bin/(kq3|kp|kp28|ownref|ownchess) ') -ge 2 ]; do sleep 20; done
  echo "$$ suite_rows $n $(date +%H:%M:%S)" >> $D/pids.log
  zsh $D/scripts/watch2.sh $D/logs/rows/$n.pid 3000000 5400 "$@" < $in > $D/logs/rows/$n.out 2> $D/logs/rows/$n.err
}
step L_A_restr  logs/rows_L.in bin/kq3 --cap 2 --capw 1 --capb 1 --promb Q --bound A --refine --moves --threads 3
step W_B_restr  logs/rows_W.in bin/kq3 --cap 2 --capw 1 --capb 1 --promw Q --bound B --refine --moves --threads 3
echo done > $D/logs/rows/suite.done
