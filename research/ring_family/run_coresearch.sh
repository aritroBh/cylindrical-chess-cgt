#!/bin/zsh
# exhaustive core + alternating chain searches; output logs/coresearch_c<c>.txt
cd "${0:A:h}"
for spec in "3 6 7" "4 7 6"; do
  set -- ${=spec}; c=$1; npc=$2; Lmax=$3
  out=logs/coresearch_c${c}.txt; : > $out
  for r in 2 3; do for start in W B; do for ((L=1; L<=Lmax; L++)); do
    res=$(nice -n 15 ./coresearch --c $c --npc $npc --r $r --start $start --L $L --max-entries 16777216 2> logs/cs_tmp.err)
    n=$(echo -n "$res" | grep -c '^W:')
    echo "# c=$c npc=$npc r=$r start=$start L=$L (ring width $((c+L)), pawns $((npc+L))): $n hits  [$(tail -1 logs/cs_tmp.err)]" >> $out
    [[ -n "$res" ]] && echo "$res" | sed 's/^/    /' >> $out
  done; done; done
done
echo ALLDONE >> logs/coresearch_c4.txt
