#!/bin/zsh
# K65 referee watchdog.  usage: src/wd.sh <pid of my heavy.sh> <solver binary basename> <name>
# Finds the solver's own PID (a descendant of the recorded heavy.sh whose command name ends in the binary name),
# records it in pids.log, then polls ITS RSS every 0.1 s and kills that one PID at 2.0 GB (2,000,000 KB).
# A kill writes logs/STOP so that every chain of runs stops.  Never signals any other process.
cd "$(dirname $0)/.."
root=$1; bin=$2; name=$3; spid=""; maxkb=0
while ps -p $root >/dev/null 2>&1 && [[ -z $spid ]]; do
  for c in $(ps -A -o pid=,ppid=,comm= | awk -v b="$bin" '$3 ~ ("/" b "$") || $3==b {print $1" "$2}' | while read p pp; do
       q=$pp; while [[ -n $q && $q != 1 && $q != 0 ]]; do [[ $q == $root ]] && { echo $p; break; }; q=$(ps -o ppid= -p $q 2>/dev/null | tr -d ' '); done; done); do
    spid=$c; echo "$spid solver $bin $name (child of my heavy.sh $root)" >> pids.log; break
  done
  [[ -z $spid ]] && sleep 0.1
done
[[ -z $spid ]] && { echo "$name: no solver seen" >> logs/wd_$name.log; exit 0; }
while true; do
  r=$(ps -o rss= -p $spid 2>/dev/null | tr -d ' '); [[ -z $r ]] && break
  (( r > maxkb )) && maxkb=$r
  if (( r > 2000000 )); then kill $spid; echo "$(date +%H:%M:%S) $name: PID $spid RSS $r KB > 2.0 GB, killed" >> logs/wd_$name.log; echo "$spid watchdog-killed $name" >> pids.log; touch logs/STOP; break; fi
  sleep 0.1
done
echo "$(date +%H:%M:%S) $name: max RSS seen $maxkb KB" >> logs/wd_$name.log
