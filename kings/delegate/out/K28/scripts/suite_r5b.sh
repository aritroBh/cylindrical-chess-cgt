#!/bin/zsh
# suite_r5b.sh : row 5 child with one side restricted, the other free (cap 2 total).  One heavy.sh job, solvers under watch2.sh.
#   B' : White restricted to ONE queen (--capw 1 --promw Q), Black free, bound B (Black's capped promotions are Black wins).  B' <= true.
#   A' : Black restricted to ONE queen (--capb 1 --promb Q), White free, bound A (capped promotions are White wins, White's resolved by
#        Black's capture of the new piece with --refine).  A' >= true.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K28
cd $D; mkdir -p logs/r5
step() {
  n=$1; in=$2; shift 2
  # guard: never more than 2 of my solver processes at once (the shared lock has been seen to lose a slot under load)
  while [ $(ps -eo command | grep -cE '^bin/(kq3|kp|kp28|ownref|ownchess) ') -ge 2 ]; do sleep 20; done
  echo "$$ suite_r5b $n $(date +%H:%M:%S)" >> $D/pids.log
  zsh $D/scripts/watch2.sh $D/logs/r5/$n.pid 3000000 5400 "$@" < $in > $D/logs/r5/$n.out 2> $D/logs/r5/$n.err
}
step R5_B_w1Q      logs/r5.in bin/kq3 --cap 2 --capw 1 --promw Q --bound B --moves --threads 3
step R5_A_b1Q_ref  logs/r5.in bin/kq3 --cap 2 --capb 1 --promb Q --bound A --refine --moves --threads 3
echo done > $D/logs/r5/suiteb.done
