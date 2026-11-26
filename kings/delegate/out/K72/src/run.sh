#!/bin/zsh
# K72 driver.  Usage (repository root):  zsh kings/delegate/out/K72/src/run.sh MODE NN G:F [G:F ...]
#   MODE direct: each solver run (under a minute, measured) is started by watch.sh here;
#   MODE heavy:  each solver run goes through kings/delegate/heavy.sh (2-slot lock) and watch.sh.
# For each group G and context file F: generate in/G_F_NN.pos, solve it with pk and with ref3m, compare.
# Stops the whole chain if a watchdog kill is recorded (logs/WATCHDOG_KILLED) or a solver exits non-zero.
V=kings/delegate/out/K72
MODE=$1; NN=$2; shift 2
for gf in "$@"; do
  G=${gf%%:*}; F=${gf##*:}; T=${G}_${F}_${NN}
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python $V/src/gen.py ctx $G $F $NN || exit 1
  for S in pk ref3m; do
    [[ -e $V/logs/WATCHDOG_KILLED ]] && { echo "watchdog kill recorded; chain stopped"; exit 2; }
    if [[ $S == pk ]]; then CMD=($V/bin/pk); else CMD=($V/bin/ref3m --board pln:8x8); fi
    if [[ $MODE == heavy ]]; then
      kings/delegate/heavy.sh zsh $V/src/watch.sh ${T}_$S $V/in/$T.pos $V/logs/${T}_$S.out $CMD
    else
      zsh $V/src/watch.sh ${T}_$S $V/in/$T.pos $V/logs/${T}_$S.out $CMD
    fi
    st=$?
    (( st != 0 )) && { echo "$T $S exit $st; chain stopped"; exit 3; }
    [[ -e $V/logs/WATCHDOG_KILLED ]] && { echo "watchdog kill recorded; chain stopped"; exit 2; }
  done
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python $V/src/cmp.py $G $F $NN >> $V/logs/summary_$NN.txt
done
echo "chain done"
