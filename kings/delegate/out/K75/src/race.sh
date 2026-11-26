#!/bin/zsh
# K75: pk_sum race runs (race.py), one group per run (inputs tmp/rc/gNN.pos = the groups of in/race.pos, split at blank lines).
# Usage (repository root):  zsh kings/delegate/out/K75/src/race.sh MODE NN [NN ...]    MODE direct | heavy
V=kings/delegate/out/K75
T="25|/;/B;/1;/2;/3;/4;/5;/6;/7;/8;/9;/10;/11;W/;13/;14/;15/;16/;17/;18/;19/;20/;21/;22/;23/"
MODE=$1; shift
echo "$(date +%Y-%m-%dT%H:%M:%S) race.sh $MODE pid $$ : $*" >> $V/pids.log
for n in "$@"; do
  [[ -e $V/logs/WATCHDOG_KILLED ]] && { echo "watchdog kill recorded; chain stopped"; exit 2; }
  if [[ $MODE == heavy ]]; then
    kings/delegate/heavy.sh zsh $V/src/watch.sh race_g$n $V/tmp/rc/g$n.pos $V/tmp/rc/g$n.out $V/bin/pk_sum -T $T
  else
    zsh $V/src/watch.sh race_g$n $V/tmp/rc/g$n.pos $V/tmp/rc/g$n.out $V/bin/pk_sum -T $T
  fi
  st=$?; (( st != 0 )) && { echo "g$n exit $st; chain stopped"; exit 3; }
  echo "g$n done"
done
echo "chain done"
