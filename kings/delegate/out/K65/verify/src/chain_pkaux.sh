#!/bin/zsh
# K65 referee: pk_sum -aux (Aux, Buchi) at every non-shuttle Black root move of the listed groups; stops at logs/STOP.
cd "$(dirname $0)/.."
for nm in "$@"; do
  [[ -f logs/STOP ]] && { echo "STOP before $nm"; exit 1; }
  IN=in/xm_$nm.txt zsh src/run.sh pk/aux_$nm bin/pk_sum -aux
  echo "$nm $(cat logs/pk/aux_$nm.rc) $(grep -E 'maximum resident' logs/pk/aux_$nm.err)"
done
