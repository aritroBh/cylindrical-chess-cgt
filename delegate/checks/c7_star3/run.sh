#!/bin/zsh
# Verify the C7 ten-pawn *3 hits of the C scanner (default setting) with two other programs:
#  (1) T43's independent solver (research/c7_independent/c7check.c) extended to test heaps 3-5
#      (delegate/checks/c7_epconv/c7k_persist: persistent e.p. rights, as in the CGT sum);
#  (2) cylcgt with component splitting off (whole-board game) and on (sum model).
cd "${0:A:h}/../../.."
D=delegate/checks/c7_star3
i=0
while read -r p; do
  i=$((i+1))
  [[ -s $D/t43_$i.txt ]] || { echo "$p" > $D/t43_$i.txt; nice -n 15 delegate/checks/c7_epconv/c7k_persist --pos 7 "$p" >> $D/t43_$i.txt 2>&1; }
  for m in nosplit sum; do
    [[ -s delegate/checks/c7p10/s3_${i}_$m.txt ]] && continue
    while (( $(pgrep -f 'c7p10/check.py' | wc -l) >= 2 )); do sleep 10; done
    nice -n 15 .venv/bin/python -I delegate/checks/c7p10/check.py "$p" s3_$i $m > /dev/null 2> $D/s3_${i}_$m.err &!
    sleep 1
  done
done < $D/positions.txt
