#!/bin/zsh
# hrun.sh NAME WALL_S IN CMD... : CMD through kings/delegate/heavy.sh (2-slot lock, nice 15) under watch2.sh (3 GB RSS cap, WALL_S s);
# stdin IN, stdout logs/NAME.out, stderr logs/NAME.err; wrapper PID and solver PID to pids.log. Run from kings/delegate/out/K48.
cd "$(dirname $0)/.."
name=$1; wall=$2; in=$3; shift 3
echo "$$ hrun $name $(date +%H:%M:%S)" >> pids.log
../../heavy.sh /bin/zsh scripts/watch2.sh logs/$name.pid 3000000 $wall "$@" < $in > logs/$name.out 2> logs/$name.err
echo "done $(date +%H:%M:%S)" > logs/$name.done
echo "$(cat logs/$name.pid 2>/dev/null) solver $name" >> pids.log
