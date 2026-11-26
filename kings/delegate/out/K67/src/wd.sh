#!/bin/zsh
# K67 watchdog for ONE process tree started by this agent.  usage: src/wd.sh <pid of my heavy.sh or def48.py> <name>
# Every 0.1 s: one ps snapshot; the descendants of the recorded root PID are found through ppid links; each new one is
# recorded in pids.log; any descendant whose RSS passes 2,000,000 KB (2.0 GB) is killed (that one PID only), the kill
# is logged, and logs/STOP is written so that every chain of runs stops.  Never signals any other process.
cd "$(dirname $0)/.."
root=$1; name=$2; maxkb=0; lim=${WDKB:-2000000}; typeset -A seen   # WDKB only for the self-test
while ps -p $root >/dev/null 2>&1; do
  ps -A -o pid=,ppid=,rss=,comm= | awk -v r=$root '{pp[$1]=$2; rs[$1]=$3; c[$1]=$4} END {for (p in pp) {q=pp[p]; while (q != "" && q > 1) { if (q == r) { print p, rs[p], c[p]; break } q = pp[q] } }}' > logs/.wd_$name.tmp
  while read p r c; do
    [[ $c == sleep ]] && continue
    [[ -z ${seen[$p]} ]] && { seen[$p]=1; echo "$p descendant-of-$root $name $c" >> pids.log; }
    (( r > maxkb )) && maxkb=$r
    if (( r > lim )); then kill $p; echo "$(date +%H:%M:%S) $name: PID $p ($c) RSS $r KB > $lim KB, killed" >> logs/wd_$name.log; echo "$p watchdog-killed $name" >> pids.log; touch logs/STOP; fi
  done < logs/.wd_$name.tmp
  sleep 0.1
done
rm -f logs/.wd_$name.tmp
echo "$(date +%H:%M:%S) $name: max RSS seen $maxkb KB" >> logs/wd_$name.log
