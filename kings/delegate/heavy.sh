#!/bin/zsh
# Run one heavy command (kpsolve batch, big enumeration) under a 2-slot lock shared by every kings/ job,
# so that all kings/ agents together never run more than 2 heavy processes. nice -n 15.
# Usage: kings/delegate/heavy.sh <cmd> [args...]   (stdin and stdout pass through)
L=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/locks
mkdir -p $L
while true; do
  for s in 1 2; do
    if mkdir $L/slot$s 2>/dev/null; then
      echo $$ > $L/slot$s/pid
      trap "rm -rf $L/slot$s" EXIT INT TERM
      nice -n 15 "$@"
      exit $?
    fi
  done
  # free a slot whose owner died without cleaning up (its recorded PID no longer exists)
  for s in 1 2; do
    p=$(cat $L/slot$s/pid 2>/dev/null)
    [[ -n $p ]] && ! ps -p $p >/dev/null 2>&1 && rm -rf $L/slot$s
  done
  sleep 5
done
