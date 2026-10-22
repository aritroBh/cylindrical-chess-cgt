#!/bin/zsh
# Re-run the width-3 seven-pawn census with the final census7.py (the old w3 results predate it).
cd "${0:A:h}/../.."
for k in {0..9}; do
  while (( $(pgrep -f 'census7[.]py --width 3' | wc -l) >= 3 )); do sleep 20; done
  nice -n 15 .venv/bin/python research/star2_seven_check/census7.py --width 3 --chunk $k --of 10 \
    > research/star2_seven_check/census7/driver_logs/rerun_w3_c$k.log 2>&1 &!
  sleep 2
done
