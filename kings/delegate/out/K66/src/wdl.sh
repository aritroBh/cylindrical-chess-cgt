#!/bin/zsh
# Light runs (expected under a minute): k66 directly under /usr/bin/time -l, same watchdog (own PID, 0.2 s polls,
# kill at 2.0 GB) plus a 60 s limit, after which the run is killed and must be redone through src/wd.sh.
tag=$1; shift
BIN=${K66_BIN:?set K66_BIN}
pf=logs/$tag.pid; rm -f $pf
K66_PIDFILE=$pf /usr/bin/time -l $BIN "$@" > logs/$tag.out 2> logs/$tag.err &
w=$!
pid=""; t=0
while kill -0 $w 2>/dev/null; do
  if [[ -z $pid && -s $pf ]]; then pid=$(cat $pf); echo "$(date +%FT%T) $tag solver pid $pid (light)" >> pids.log; fi
  if [[ -n $pid ]]; then
    rss=$(ps -o rss= -p $pid 2>/dev/null | tr -d ' ')
    if [[ -n $rss && $rss -gt 2097152 ]]; then kill $pid; echo "$tag killed at rss ${rss} KB" > logs/WDKILL; echo "$(date +%FT%T) $tag WATCHDOG KILL $pid" >> pids.log; fi
    if (( t > 300 )); then kill $pid; echo "$(date +%FT%T) $tag stopped at 60 s (light limit) $pid" >> pids.log; fi
  fi
  sleep 0.2; t=$((t+1))
done
wait $w
rm -f $pf
