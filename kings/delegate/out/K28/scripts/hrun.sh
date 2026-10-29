#!/bin/zsh
# hrun.sh NAME WALL_S IN CMD... : run CMD through the shared 2-slot lock (heavy.sh, nice 15) under watch2.sh (3 GB RSS cap = 3000000 KB,
# WALL_S seconds), stdin from IN, stdout to logs/r/NAME.out, stderr to logs/r/NAME.err. The wrapper PID goes to pids.log,
# the solver PID (written by watch2.sh) to logs/r/NAME.pid.
K=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate
D=$K/out/K28
name=$1; wall=$2; in=$3; shift 3
echo "$$ hrun $name $(date +%H:%M:%S)" >> $D/pids.log
cd $D
$K/heavy.sh /bin/zsh $D/scripts/watch2.sh $D/logs/r/$name.pid 3000000 $wall "$@" < $in > $D/logs/r/$name.out 2> $D/logs/r/$name.err
echo "done $(date +%H:%M:%S)" > $D/logs/r/$name.done
