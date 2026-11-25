#!/bin/zsh
# K63 copy of the K27/K48 watch2.sh: run CMD as my own child; stop ONLY that child if its RSS exceeds LIMIT_KB.
# usage: watch2.sh LIMIT_KB CMD...   (polled peak and exit status on stderr)
unsetopt BG_NICE
lim=$1; shift
"$@" &
pid=$!
echo "watch2: child pid $pid" >&2
peak=0; t0=$SECONDS
while kill -0 $pid 2>/dev/null; do
  r=$(ps -o rss= -p $pid 2>/dev/null | tr -d ' ')
  if [[ -n $r ]]; then
    (( r > peak )) && peak=$r
    if (( r > lim )); then echo "WATCHDOG: rss ${r} KB > ${lim} KB, stopping own child $pid" >&2; kill $pid; break; fi
  fi
  sleep 2
done
wait $pid
echo "exit status $?  polled peak rss ${peak} KB  wall $((SECONDS-t0)) s" >&2
