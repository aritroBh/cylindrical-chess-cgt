#!/bin/zsh
# K67: run one program through kings/delegate/heavy.sh under /usr/bin/time -l with src/wd.sh on the tree; record PIDs; wait.
# usage: [IN=<stdin file>] src/run.sh <name> <binary> [args...]  -> logs/<name>.out, .err, .rc ; refuses to start if logs/STOP exists.
cd "$(dirname $0)/.."
[[ -f logs/STOP ]] && { echo "STOP present, not running $1"; exit 99; }
name=$1; shift; mkdir -p logs/$(dirname $name)
../../heavy.sh /usr/bin/time -l "$@" < ${IN:-/dev/null} > logs/$name.out 2> logs/$name.err &
P=$!; echo "$P heavy.sh $name $(date +%H:%M:%S)" >> pids.log
zsh src/wd.sh $P ${name//\//_} &
W=$!; echo "$W wd.sh $name" >> pids.log
wait $P; rc=$?; wait $W
echo "rc=$rc $(date +%H:%M:%S)" > logs/$name.rc
