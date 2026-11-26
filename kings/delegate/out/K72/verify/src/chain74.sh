#!/bin/zsh
# K74 referee: the 2 + 2 runs, one after another, each through kings/delegate/heavy.sh and run74.sh (watchdog).
# Usage (repository root):  zsh kings/delegate/out/K72/verify/src/chain74.sh G:F [G:F ...]
# Stops at once if a watchdog kill is recorded or p74 exits non-zero.
V=kings/delegate/out/K72/verify
for gf in "$@"; do
  G=${gf%%:*}; F=${gf##*:}; T=${G}_${F}_22
  [[ -e $V/logs/WATCHDOG_KILLED ]] && { echo "watchdog kill recorded; chain stopped"; exit 2; }
  python3 -I $V/src/mk74.py pos $G $F 2 > $V/tmp/${G}_${F}_2.in || exit 1
  kings/delegate/heavy.sh zsh $V/src/run74.sh $T $V/tmp/${G}_${F}_2.in $V/logs/${T}_p74.out
  st=$?
  (( st != 0 )) && { echo "$T exit $st; chain stopped"; exit 3; }
  echo "$(date +%Y-%m-%dT%H:%M:%S) $T finished"
done
echo "chain done"
