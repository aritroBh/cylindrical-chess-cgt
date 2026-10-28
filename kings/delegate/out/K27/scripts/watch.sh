#!/bin/zsh
# watch.sh PIDFILE LIMIT_KB CMD...   run CMD directly, record its PID in PIDFILE, poll its RSS every second, report the polled
# peak at the end, and kill ONLY that PID if RSS passes LIMIT_KB.  (stdin/stdout pass through.)
pidfile=$1; lim=$2; shift 2
"$@" &
pid=$!
echo $pid > $pidfile
peak=0
while kill -0 $pid 2>/dev/null; do
  r=$(ps -o rss= -p $pid 2>/dev/null | tr -d ' ')
  if [[ -n $r ]]; then
    (( r > peak )) && peak=$r
    if (( r > lim )); then echo "WATCHDOG: rss ${r} KB > ${lim} KB, killing own pid $pid" >&2; kill $pid; break; fi
  fi
  sleep 1
done
wait $pid
echo "exit status $?  polled peak rss ${peak} KB" >&2
