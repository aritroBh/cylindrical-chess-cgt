#!/bin/zsh
# K72: run one solver under /usr/bin/time -l with a watchdog on the solver's own PID.
# Usage (repository root):  zsh kings/delegate/out/K72/src/watch.sh TAG INFILE OUTFILE CMD [ARGS...]
#   heavy runs:             kings/delegate/heavy.sh zsh kings/delegate/out/K72/src/watch.sh TAG ...
# The solver is started as the child of /usr/bin/time (started here); its PID is read from the process table as the
# child of that recorded PID and written to pids.log.  Polls 5 times a second; kills ONLY that recorded PID if its RSS
# passes 2.0 GB, and then writes logs/WATCHDOG_KILLED so that every driver stops.
unsetopt BG_NICE
V=kings/delegate/out/K72
TAG=$1; IN=$2; OUT=$3; shift 3
LIMIT_KB=1953125   # 2.0 GB (2.0e9 bytes)
/usr/bin/time -l "$@" < $IN > $OUT 2> $V/logs/$TAG.time &
T=$!
echo "$(date +%Y-%m-%dT%H:%M:%S) $TAG watch.sh pid $$, time pid $T : ${1:t} ${@:2}" >> $V/pids.log
S=""; PEAK=0; t0=$SECONDS
while kill -0 $T 2>/dev/null; do
  if [[ -z $S ]]; then
    S=$(ps -A -o pid=,ppid= | awk -v t=$T '$2==t {print $1; exit}')
    [[ -n $S ]] && echo "$(date +%Y-%m-%dT%H:%M:%S) $TAG solver pid $S ($(ps -o comm= -p $S 2>/dev/null))" >> $V/pids.log
  fi
  if [[ -n $S ]]; then
    r=$(ps -o rss= -p $S 2>/dev/null | tr -d ' ')
    if [[ -n $r ]]; then
      (( r > PEAK )) && PEAK=$r
      if (( r > LIMIT_KB )); then
        echo "$(date +%Y-%m-%dT%H:%M:%S) $TAG WATCHDOG kill $S at rss $r kB" >> $V/pids.log
        echo "$TAG $S $r" >> $V/logs/WATCHDOG_KILLED
        kill $S
      fi
    fi
  fi
  sleep 0.2
done
wait $T; st=$?
echo "$(date +%Y-%m-%dT%H:%M:%S) $TAG done, exit $st, polled peak rss $PEAK kB, wall $((SECONDS-t0)) s" >> $V/pids.log
exit $st
