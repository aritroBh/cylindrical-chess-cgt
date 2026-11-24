#!/bin/zsh
# K55: run one solver command with stdout/stderr files, record its PID, stop it (its own recorded PID only) if its RSS
# passes 2.9 GB, log the polled peak RSS and the run time.  usage: capped.sh <out> <err> <cmd> [args...]
cd "$(dirname $0)"
out=$1; err=$2; shift 2
t0=$(date +%s)
"$@" > $out 2> $err &
P=$!; echo "$P $* (child of capped.sh $$) $(date)" >> pids.log
peak=0
while kill -0 $P 2>/dev/null; do
  r=$(ps -o rss= -p $P 2>/dev/null | tr -d ' ')
  [[ -n $r ]] && (( r > peak )) && peak=$r
  if [[ -n $r ]] && (( r > 2900000 )); then echo "stopped at rss ${r} KB" >> $err; kill $P; fi
  sleep 2
done
echo "capped.sh: polled peak rss ${peak} KB, $(( $(date +%s) - t0 )) s" >> $err
