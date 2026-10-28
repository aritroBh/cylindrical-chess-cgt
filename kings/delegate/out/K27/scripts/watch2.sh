#!/bin/zsh
# watch2.sh PIDFILE LIMIT_KB WALL_S CMD...   like watch.sh plus a wall-clock limit; kills ONLY its own child PID.
pidfile=$1; lim=$2; wall=$3; shift 3
"$@" &
pid=$!
echo $pid > $pidfile
peak=0; t0=$SECONDS
while kill -0 $pid 2>/dev/null; do
  r=$(ps -o rss= -p $pid 2>/dev/null | tr -d ' ')
  if [[ -n $r ]]; then
    (( r > peak )) && peak=$r
    if (( r > lim )); then echo "WATCHDOG: rss ${r} KB > ${lim} KB, killing own pid $pid" >&2; kill $pid; break; fi
  fi
  if (( SECONDS - t0 > wall )); then echo "WATCHDOG: wall ${wall}s exceeded, killing own pid $pid" >&2; kill $pid; break; fi
  sleep 2
done
wait $pid
echo "exit status $?  polled peak rss ${peak} KB  wall $((SECONDS-t0)) s" >&2
