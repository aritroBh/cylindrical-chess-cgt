#!/bin/zsh
# K65 referee: pk_sum beside T_N (u_0 = T-state 1) for the listed group:N pairs; stops at logs/STOP.
cd "$(dirname $0)/.."
for gn in "$@"; do
  nm=${gn%%:*}; N=${gn##*:}
  [[ -f logs/STOP ]] && { echo "STOP before $gn"; exit 1; }
  IN=in/lad_$nm.txt zsh src/run.sh pk/lad_${nm}_T$N bin/pk_sum -ladder $N
  echo "$nm T_$N $(cat logs/pk/lad_${nm}_T$N.rc) $(grep -E 'maximum resident' logs/pk/lad_${nm}_T$N.err)"; cat logs/pk/lad_${nm}_T$N.out
done
