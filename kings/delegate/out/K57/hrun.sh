#!/bin/zsh
# K57: run one solver command through heavy.sh under /usr/bin/time -l, record the PID, wait for it.
# usage: hrun.sh <logname> <cmd> [args...]   (run from kings/delegate/out/K57)
cd "$(dirname $0)"
name=$1; shift
../../heavy.sh /usr/bin/time -l "$@" > logs/$name.out 2> logs/$name.err &
P=$!; echo "$P heavy.sh /usr/bin/time -l $* ($name) $(date)" >> pids.log
wait $P
