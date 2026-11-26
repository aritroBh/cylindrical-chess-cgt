#!/bin/zsh
# K74 referee: run p74 once under /usr/bin/time -l with a watchdog on the solver's own PID.
# Usage (repository root):  zsh kings/delegate/out/K72/verify/src/run74.sh TAG INFILE OUTFILE [p74 flags]
#   heavy runs:             kings/delegate/heavy.sh zsh kings/delegate/out/K72/verify/src/run74.sh TAG ...
# Records the PID of /usr/bin/time (started here) and of its child, the solver, in pids.log; polls the solver's RSS
# five times a second and kills ONLY that recorded PID above 2.0 GB, then writes logs/WATCHDOG_KILLED.
unsetopt BG_NICE
V=kings/delegate/out/K72/verify
TAG=$1; IN=$2; OUT=$3; shift 3
[[ -e $V/logs/WATCHDOG_KILLED ]] && { echo "watchdog kill recorded earlier; not starting"; exit 2; }
LIMIT_KB=1953125
# "--cmd PROGRAM ARGS" runs another solver (used once: K72's pk, built in tmp/, for the three C125_10 failures)
if [[ $1 == --cmd ]]; then shift; CMD=("$@"); else CMD=($V/tmp/p74 "$@"); fi
/usr/bin/time -l "${CMD[@]}" < $IN > $OUT 2> $V/logs/$TAG.time &
T=$!
echo "$(date +%Y-%m-%dT%H:%M:%S) $TAG run74.sh pid $$, time pid $T, p74 $@" >> $V/pids.log
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
