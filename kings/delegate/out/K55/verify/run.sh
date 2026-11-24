#!/bin/zsh
# K55 referee: run one solver command through heavy.sh under /usr/bin/time -l, log its PIDs, stop only its own
# processes (by recorded PID) if their RSS passes 2.9 GB.  Usage: run.sh <tag> <cmd> [args...]  (stdout -> logs/<tag>.out)
cd "$(dirname $0)"; mkdir -p logs
tag=$1; shift
../../../heavy.sh /usr/bin/time -l "$@" > logs/$tag.out 2> logs/$tag.err &
H=$!; echo "$H heavy.sh for $tag ($*) $(date)" >> pids.log
desc() { local p=$1; for c in $(pgrep -P $p 2>/dev/null); do echo $c; desc $c; done; }
peak=0; seen=""
while kill -0 $H 2>/dev/null; do
  for d in $(desc $H); do
    if [[ " $seen " != *" $d "* ]]; then seen="$seen $d"; echo "$d child of $H for $tag ($(ps -o comm= -p $d 2>/dev/null))" >> pids.log; fi
    r=$(ps -o rss= -p $d 2>/dev/null | tr -d ' ')
    [[ -n $r ]] && (( r > peak )) && peak=$r
    if [[ -n $r ]] && (( r > 2900000 )); then kill $d; echo "watchdog: stopped own PID $d at rss $r KB" >> logs/$tag.err; fi
  done
  sleep 1
done
echo "watchdog peak rss ${peak} KB" >> logs/$tag.err
echo done > logs/$tag.done
