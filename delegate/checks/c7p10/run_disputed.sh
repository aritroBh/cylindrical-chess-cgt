#!/bin/zsh
# cylcgt (sum and whole-board) on the five C7 scanner hits that T43's independent solver says are not *2.
cd "${0:A:h}/../../.."
while IFS=$'\t' read -r tag p m; do
  [[ -s delegate/checks/c7p10/${tag}_$m.txt ]] && continue
  while (( $(pgrep -f 'c7p10/check.py' | wc -l) >= 3 )); do sleep 10; done
  nice -n 15 .venv/bin/python -I delegate/checks/c7p10/check.py "$p" $tag $m > /dev/null 2> delegate/checks/c7p10/${tag}_$m.err &!
  sleep 1
done < delegate/checks/c7p10/disputed.tsv
