#!/bin/zsh
# T22b left 100 census7 width-4 chunks running at once (its brief allowed 3). Keep at most N running and
# SIGSTOP the rest, resuming them as running ones finish, so no chunk loses its progress.
#   zsh delegate/checks/throttle_census7.sh [N]      (default 4)
N=${1:-4}
pat='census7[.]py --width 4'
while true; do
  pids=($(pgrep -f "$pat"))
  (( ${#pids} == 0 )) && { echo "[$(date +%H:%M)] all width-4 chunks finished"; break; }
  running=(); stopped=()
  for p in $pids; do
    st=$(ps -o state= -p $p 2>/dev/null)
    [[ -z $st ]] && continue
    [[ $st == T* ]] && stopped+=($p) || running+=($p)
  done
  if (( ${#running} > N )); then kill -STOP ${running[$((N+1)),-1]} 2>/dev/null; fi
  free=$(( N - ${#running} ))
  if (( free > 0 && ${#stopped} > 0 )); then kill -CONT ${stopped[1,$free]} 2>/dev/null; fi
  sleep 30
done
