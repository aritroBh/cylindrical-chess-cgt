#!/bin/zsh
# K65: run one tool through kings/delegate/heavy.sh under /usr/bin/time -l with the RSS watchdog; record the PIDs; wait.
# usage: src/hrunw.sh <name> <binary> [args...]   -> logs/<name>.out, logs/<name>.err, logs/watch_<name>.log
cd "$(dirname $0)/.."
name=$1; shift
mkdir -p logs/$(dirname $name)
../../heavy.sh /usr/bin/time -l "$@" > logs/$name.out 2> logs/$name.err &
P=$!; echo "$P heavy.sh $name $(date +%H:%M:%S)" >> pids.log
zsh src/watch.sh $P ${name//\//_} &
Wd=$!; echo "$Wd watch.sh $name" >> pids.log
wait $P; rc=$?; wait $Wd
echo "rc=$rc $(date +%H:%M:%S)" > logs/$name.done
