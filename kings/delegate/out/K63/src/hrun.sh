#!/bin/zsh
# K63: run one tool through kings/delegate/heavy.sh under /usr/bin/time -l; record the PID; wait for it.
# usage: src/hrun.sh <name> <stdin file or -> <binary> [args...]   -> logs/<name>.out, logs/<name>.err
cd "$(dirname $0)/.."
name=$1; in=$2; shift 2
[[ $in == - ]] && in=/dev/null
../../heavy.sh /usr/bin/time -l "$@" < $in > logs/$name.out 2> logs/$name.err &
P=$!; echo "$P heavy.sh $name $(date +%H:%M:%S)" >> pids.log; wait $P
