#!/bin/zsh
# K65 referee: pk_sum beside -1 ((B1)) at every non-shuttle Black root move of the listed groups; stops at logs/STOP.
cd "$(dirname $0)/.."
for nm in "$@"; do
  [[ -f logs/STOP ]] && { echo "STOP before $nm"; exit 1; }
  IN=in/xm_$nm.txt zsh src/run.sh pk/B1_$nm bin/pk_sum -T "2|/;/0"
  echo "$nm $(cat logs/pk/B1_$nm.rc) $(grep -E 'maximum resident' logs/pk/B1_$nm.err)"
done
