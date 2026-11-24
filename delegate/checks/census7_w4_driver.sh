#!/bin/zsh
# Runs the width-4 census7 chunks (0..99 of 100) that have no .done file, N at a time, under nice.
# Replaces the 100-at-once launch T22b made (killed 2026-10-22 00:40 to free swap; chunks restart from scratch).
#   zsh delegate/checks/census7_w4_driver.sh [N]     (default 3)
cd "${0:A:h}/../.."
N=${1:-3}; D=research/star2_seven_check/census7
for k in {0..99}; do
  [[ -f $D/w4_c$k.done ]] && continue
  pgrep -f "census7[.]py --width 4 --chunk $k --of 100" >/dev/null && continue
  while (( $(pgrep -f 'census7[.]py --width 4' | wc -l) >= N )); do sleep 30; done
  echo "[$(date +%H:%M)] start chunk $k"
  nice -n 15 .venv/bin/python research/star2_seven_check/census7.py --width 4 --chunk $k --of 100 > $D/w4_c$k.stdout 2>&1 &!
  sleep 2
done
echo "[$(date +%H:%M)] all chunks launched"
