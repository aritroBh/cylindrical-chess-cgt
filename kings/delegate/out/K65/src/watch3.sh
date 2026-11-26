#!/bin/zsh
# K65 (v3: polls every 0.2 s, after v2 let fast-allocating runs reach 3.5 GB between 2 s polls; skips the sleep children of heavy.sh while it waits for a slot): RSS watchdog for ONE process tree started by this agent.  usage: src/watch.sh <pid of my heavy.sh> <name>
# Every 2 s: walk the descendants of that recorded PID (ps ppid links), record each new one in pids.log, check its RSS;
# if one passes 2,200,000 KB (2.2 GB), kill that one recorded PID (and log it).  Never signals anything else.
cd "$(dirname $0)/.."
root=$1; name=$2; maxkb=0; typeset -A seen
while ps -p $root >/dev/null 2>&1; do
  kids=($root); all=()
  while (( ${#kids} )); do
    next=()
    for k in $kids; do for c in $(ps -A -o pid=,ppid= | awk -v p=$k '$2==p{print $1}'); do next+=$c; all+=$c; done; done
    kids=($next)
  done
  for c in $all; do
    cm=$(ps -o comm= -p $c 2>/dev/null); [[ $cm == sleep ]] && continue; [[ -z ${seen[$c]} ]] && { seen[$c]=1; echo "$c child-of-$root $name $cm" >> pids.log; }
    r=$(ps -o rss= -p $c 2>/dev/null | tr -d ' '); [[ -z $r ]] && continue
    (( r > maxkb )) && maxkb=$r
    if (( r > 2200000 )); then echo "$(date +%H:%M:%S) $name: PID $c RSS $r KB over 2.2 GB, killed" >> logs/watch_$name.log; echo "$c watchdog-killed $name" >> pids.log; kill $c; fi
  done
  sleep 0.2
done
echo "$(date +%H:%M:%S) $name: max RSS seen $maxkb KB" >> logs/watch_$name.log
