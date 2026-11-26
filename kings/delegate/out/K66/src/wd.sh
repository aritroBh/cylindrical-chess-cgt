#!/bin/zsh
# Usage: zsh src/wd.sh <tag> <args to k66...>   (run from kings/delegate/out/K66)
# Runs k66 through kings/delegate/heavy.sh under /usr/bin/time -l; the solver writes its own PID to a file;
# this watchdog records that PID in pids.log, polls its RSS five times a second and kills it (that PID only)
# at 2.0 GB, leaving logs/WDKILL. Output: logs/<tag>.out, logs/<tag>.err.
tag=$1; shift
BIN=${K66_BIN:?set K66_BIN}
ROOT=../../../..
pf=logs/$tag.pid; rm -f $pf
K66_PIDFILE=$pf $ROOT/kings/delegate/heavy.sh /usr/bin/time -l $BIN "$@" > logs/$tag.out 2> logs/$tag.err &
w=$!
pid=""
while kill -0 $w 2>/dev/null; do
  if [[ -z $pid && -s $pf ]]; then pid=$(cat $pf); echo "$(date +%FT%T) $tag solver pid $pid" >> pids.log; fi
  if [[ -n $pid ]]; then
    rss=$(ps -o rss= -p $pid 2>/dev/null | tr -d ' ')
    if [[ -n $rss && $rss -gt 2097152 ]]; then kill $pid; echo "$tag killed at rss ${rss} KB" > logs/WDKILL; echo "$(date +%FT%T) $tag WATCHDOG KILL $pid" >> pids.log; fi
  fi
  sleep 0.2
done
wait $w
rm -f $pf
