#!/bin/zsh
# K75: pk_sum slack runs, one group per run (inputs tmp/sl/gNN.pos = the groups of in/slack.pos, split at blank lines).
# Usage (repository root):  zsh kings/delegate/out/K75/src/slack.sh MODE NN [NN ...]    MODE direct | heavy
V=kings/delegate/out/K75
T="18|/;/0;/1;/2;/3;/4;/5;/6;/7;/;9/;10/;11/;12/;13/;14/;15/;16/"
MODE=$1; shift
echo "$(date +%Y-%m-%dT%H:%M:%S) slack.sh $MODE pid $$ : $*" >> $V/pids.log
for n in "$@"; do
  [[ -e $V/logs/WATCHDOG_KILLED ]] && { echo "watchdog kill recorded; chain stopped"; exit 2; }
  if [[ $MODE == heavy ]]; then
    kings/delegate/heavy.sh zsh $V/src/watch.sh slack_g$n $V/tmp/sl/g$n.pos $V/tmp/sl/g$n.out $V/bin/pk_sum -T $T
  else
    zsh $V/src/watch.sh slack_g$n $V/tmp/sl/g$n.pos $V/tmp/sl/g$n.out $V/bin/pk_sum -T $T
  fi
  st=$?; (( st != 0 )) && { echo "g$n exit $st; chain stopped"; exit 3; }
  echo "g$n done"
done
echo "chain done"
