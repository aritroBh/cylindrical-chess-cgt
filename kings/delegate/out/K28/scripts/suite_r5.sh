#!/bin/zsh
# suite_r5.sh : row 5 child, White barred from promoting (--capw 0), Black free (Black has only two pawns, so cap 2 never binds for Black).
#   bound A: a White promotion is a White win (generous to White; with --refine resolved by Black's capture of the new piece when possible)
#   bound B: a White promotion is a Black win (generous to Black).  true value is in [B, A].  One heavy.sh job, solvers under watch2.sh.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K28
cd $D; mkdir -p logs/r5
step() {
  n=$1; in=$2; shift 2
  echo "$$ suite_r5 $n $(date +%H:%M:%S)" >> $D/pids.log
  zsh $D/scripts/watch2.sh $D/logs/r5/$n.pid 3000000 5400 "$@" < $in > $D/logs/r5/$n.out 2> $D/logs/r5/$n.err
}
step R5_B_w0      logs/r5.in bin/kq3 --cap 2 --capw 0 --bound B --moves --threads 3
step R5_A_w0_ref  logs/r5.in bin/kq3 --cap 2 --capw 0 --bound A --refine --moves --threads 3
echo done > $D/logs/r5/suite.done
