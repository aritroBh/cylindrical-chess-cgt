#!/bin/sh
# K8 normal-play scan. One whole board is one runlim job (20 min, 3 GB RSS).
cd "$(dirname "$0")/../../../.." || exit 1
export PYTHONPATH=.
K8=kings/delegate/out/K8
PY=.venv/bin/python
K8_START=${K8_START:-$(date +%s)}
export K8_START

for b in "$@"; do
  now=$(date +%s)
  remaining=$((7200 - now + K8_START))
  if [ "$remaining" -le 0 ]; then echo "2-hour limit reached before $b"; exit 99; fi
  limit=1200
  if [ "$remaining" -lt "$limit" ]; then limit=$remaining; fi
  tag=$(echo "$b" | tr ':' '_')
  echo "=== normal $b start $(date +%T) limit=${limit}s"
  nice -n 10 "$PY" "$K8/runlim.py" "normal $b" "$limit" 3000 "$K8/runs.jsonl" -- \
    nice -n 10 "$PY" "$K8/run_board.py" "$b" > "$K8/log_board_$tag.txt" 2>&1
  rc=$?
  tail -n 6 "$K8/log_board_$tag.txt" | cut -c1-700
  if [ "$rc" -ne 0 ]; then echo "normal board failed/skipped: $b rc=$rc"; exit "$rc"; fi
  echo "=== normal $b done $(date +%T)"
done
