#!/bin/zsh
# K59: RSS watchdog for ONE process tree started by this agent. usage: src/watch.sh <pid of my heavy.sh> <name>
# Every 2 s: find the descendants of that PID (by walking ps ppid links), sum nothing, check each one's RSS;
# if one exceeds 3,000,000 KB, stop that one PID (it is mine: a descendant of a PID I started) and log it.
cd "$(dirname $0)/.."
root=$1; name=$2; maxkb=0
while ps -p $root >/dev/null 2>&1; do
  kids=($root); all=()
  while (( ${#kids} )); do
    next=()
    for k in $kids; do for c in $(ps -A -o pid=,ppid= | awk -v p=$k '$2==p{print $1}'); do next+=$c; all+=$c; done; done
    kids=($next)
  done
  for c in $all; do
    r=$(ps -o rss= -p $c 2>/dev/null | tr -d ' '); [[ -z $r ]] && continue
    (( r > maxkb )) && maxkb=$r
    if (( r > 3000000 )); then echo "$(date +%H:%M:%S) $name: PID $c RSS $r KB over 3 GB, stopped" >> logs/watch_$name.log; echo "$c watchdog-stopped $name" >> pids.log; kill $c; fi
  done
  sleep 2
done
echo "$(date +%H:%M:%S) $name: max RSS seen $maxkb KB" >> logs/watch_$name.log
