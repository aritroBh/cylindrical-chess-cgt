#!/bin/zsh
# K76 referee: a chain of p74 runs, one at a time, each under run76.sh (time -l, watchdog on the solver's own PID).
# Usage (repository root):  zsh kings/delegate/out/K75/verify/src/chain76.sh direct|heavy LISTFILE
#   LISTFILE lines: TAG G F N [a|b]   (mk76.py pos G F N [a|b] gives the input; output logs/runs/TAG.out)
# direct: only for inputs measured under 30 s and 0.6 GB; the chain stops if a run takes 30 s or more.
# heavy:  each run through kings/delegate/heavy.sh (one slot at a time), 5 s gap between runs.
# The chain stops on any non-zero exit and if a watchdog kill has been recorded.
V=kings/delegate/out/K75/verify
MODE=$1; LIST=$2
while read TAG G F N H; do
  [[ -z $TAG || $TAG == \#* ]] && continue
  [[ -e $V/logs/WATCHDOG_KILLED ]] && { echo "watchdog kill recorded; chain stopped"; exit 2; }
  [[ -s $V/logs/runs/$TAG.out ]] && { echo "$TAG exists, skipped"; continue; }
  python3 -I $V/src/mk76.py pos $G $F $N $H > $V/tmp/$TAG.in || exit 1
  t0=$SECONDS
  if [[ $MODE == heavy ]]; then
    kings/delegate/heavy.sh zsh $V/src/run76.sh $TAG $V/tmp/$TAG.in $V/tmp/$TAG.part || { echo "$TAG failed"; exit 3; }
  else
    zsh $V/src/run76.sh $TAG $V/tmp/$TAG.in $V/tmp/$TAG.part || { echo "$TAG failed"; exit 3; }
  fi
  mv $V/tmp/$TAG.part $V/logs/runs/$TAG.out
  rm -f $V/tmp/$TAG.in
  echo "$(date +%H:%M:%S) $TAG done in $((SECONDS - t0)) s"
  if [[ $MODE == direct ]] && (( SECONDS - t0 >= 30 )); then echo "$TAG took 30 s or more; chain stopped"; exit 4; fi
  [[ $MODE == heavy ]] && sleep 5
done < $LIST
echo "chain $LIST done"
