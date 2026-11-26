#!/bin/zsh
# K77 referee: run one small command (measured < 30 s and < 0.6 GB) directly, under /usr/bin/time -l, and record its PID.
# usage: zsh run77.sh <log stem> <cmd> [args...]   (stdin passes through; stdout to <stem>.out, stderr to <stem>.err)
V=${0:A:h:h}
stem=$1; shift
/usr/bin/time -l "$@" > $stem.out 2> $stem.err &
pid=$!
print "$(date '+%F %T') pid $pid (/usr/bin/time of: ${*:t}) -> ${stem:t}" >> $V/pids.log
wait $pid
rc=$?
print "$(date '+%F %T') pid $pid rc=$rc" >> $V/pids.log
exit $rc
