# K63 referee: run one solver command through kings/delegate/heavy.sh under /usr/bin/time -l, with a watchdog.
# Usage (repository root):  zsh kings/delegate/out/K63/verify/src/hrun.sh TAG INFILE OUTFILE CMD [ARGS...]
# Records every PID it starts in verify/pids.log; kills only the recorded solver PID if its RSS passes 2.2 GB.
V=kings/delegate/out/K63/verify
TAG=$1; IN=$2; OUT=$3; shift 3
LIMIT_KB=2306867   # 2.2 GB
kings/delegate/heavy.sh /usr/bin/time -l "$@" < $IN > $OUT 2> $V/logs/$TAG.time &
H=$!
echo "$(date +%Y-%m-%dT%H:%M:%S) $TAG heavy.sh wrapper pid $H : ${1:t} ${@:2}" >> $V/pids.log
SOLVER=""; PEAK=0
while kill -0 $H 2>/dev/null; do
  if [[ -z $SOLVER ]]; then
    # the solver is the deepest descendant of the wrapper (heavy.sh -> time -> solver)
    T=$(ps -A -o pid=,ppid= | awk -v h=$H '{p[$1]=$2} END{for (x in p){y=x; while (y in p && y!=h && y>1) y=p[y]; if (y==h && x!=h) print x}}')
    for x in ${(f)T}; do
      c=$(ps -o comm= -p $x 2>/dev/null)
      if [[ -n $c && ${c:t} == ${1:t} ]]; then SOLVER=$x; echo "$(date +%Y-%m-%dT%H:%M:%S) $TAG solver pid $SOLVER (${c:t})" >> $V/pids.log; fi
    done
  fi
  if [[ -n $SOLVER ]]; then
    r=$(ps -o rss= -p $SOLVER 2>/dev/null | tr -d ' ')
    [[ -z $r ]] && SOLVER=""   # solver gone (or not yet started): look again
    if [[ -n $r ]]; then
      (( r > PEAK )) && PEAK=$r
      if (( r > LIMIT_KB )); then
        echo "$(date +%Y-%m-%dT%H:%M:%S) $TAG WATCHDOG kill $SOLVER at rss ${r} kB" >> $V/pids.log
        kill $SOLVER
      fi
    fi
  fi
  sleep 1
done
wait $H
echo "$(date +%Y-%m-%dT%H:%M:%S) $TAG done, exit $?, watchdog peak rss ${PEAK} kB" >> $V/pids.log
