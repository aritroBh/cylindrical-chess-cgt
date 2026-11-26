#!/bin/zsh
# K77 referee: run one command through kings/delegate/heavy.sh under /usr/bin/time -l, with a watchdog on the
# solver's own PID (the child of /usr/bin/time, found from the PIDs this script started): polls every 0.15 s,
# kills that one PID at 2.0 GB RSS and writes verify/tmp/STOP.  Refuses to start while STOP exists.
# usage: zsh wd77.sh <log stem> <cmd> [args...]   (stdin passes through)
V=${0:A:h:h}
R=${V:h:h:h:h:h}
stem=$1; shift
[[ -e $V/tmp/STOP ]] && { print "STOP exists, not starting" >&2; exit 9 }
$R/kings/delegate/heavy.sh /usr/bin/time -l "$@" > $stem.out 2> $stem.err &
hp=$!
print "$(date '+%F %T') heavy.sh pid $hp: ${*:t} -> ${stem:t}" >> $V/pids.log
sp=""; tp=""; peak=0
while kill -0 $hp 2>/dev/null; do
  if [[ -z $sp ]]; then
    tp=$(pgrep -P $hp 2>/dev/null | head -1)
    [[ -n $tp ]] && sp=$(pgrep -P $tp 2>/dev/null | head -1)
    [[ -n $sp ]] && print "$(date '+%F %T')   time pid $tp, solver pid $sp" >> $V/pids.log
  fi
  if [[ -n $sp ]]; then
    rss=$(ps -o rss= -p $sp 2>/dev/null | tr -d ' ')
    if [[ -n $rss ]]; then
      (( rss > peak )) && peak=$rss
      if (( rss > 2000000 )); then
        kill $sp; print "$(date '+%F %T') WATCHDOG killed solver pid $sp at $rss KB" >> $V/pids.log; touch $V/tmp/STOP
      fi
    fi
  fi
  sleep 0.15
done
wait $hp; rc=$?
print "$(date '+%F %T') heavy.sh pid $hp rc=$rc, watchdog peak RSS $peak KB" >> $V/pids.log
exit $rc
