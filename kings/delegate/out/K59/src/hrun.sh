#!/bin/zsh
# K59: run one tool through kings/delegate/heavy.sh under /usr/bin/time -l; record the PID; wait for it.
# usage: src/hrun.sh <name> <binary> [args...]   -> logs/<name>.out, logs/<name>.err
cd "$(dirname $0)/.."
name=$1; shift
../../heavy.sh /usr/bin/time -l "$@" > logs/$name.out 2> logs/$name.err &
P=$!; echo "$P heavy.sh $name $(date +%H:%M:%S)" >> pids.log; wait $P
