#!/bin/zsh
# Run the cylcgt check on every line of hits_batch1.tsv ("N<TAB>position"), three at a time, sum model.
cd "${0:A:h}/../../.."
while IFS=$'\t' read -r n p; do
  [[ -s delegate/checks/c7p10/h${n}_sum.txt ]] && continue
  while (( $(pgrep -f 'c7p10/check.py' | wc -l) >= 3 )); do sleep 10; done
  nice -n 15 .venv/bin/python -I delegate/checks/c7p10/check.py "$p" h$n sum > /dev/null 2> delegate/checks/c7p10/h${n}_sum.err &!
  sleep 1
done < delegate/checks/c7p10/hits_batch1.tsv
