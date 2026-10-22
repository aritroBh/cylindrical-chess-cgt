#!/bin/sh
# Second stage.  Run it AFTER run.sh has finished (it needs chess_tempo_*.jsonl, summary.json's inputs and the check1 files):
#     nohup sh kings/delegate/out/K8/run_extra.sh > kings/delegate/out/K8/run_extra.log 2>&1 &
# pv_stats.py: where the spare move is spent and how the win ends, normal play against the chess rule.  Then summary.json is
# rebuilt (it now includes the pvstats section) and audit.py re-derives the headline numbers again.
# Same limits as run.sh: one heavy process at a time, nice -n 10, <= 20 min and <= 3 GB RSS per job (runlim.py), <= 2 h.
cd "$(dirname "$0")/../../../.." || exit 1
export PYTHONPATH=.
K8=kings/delegate/out/K8
PY=.venv/bin/python
rm -f "$K8"/pvstats_*.json "$K8"/log_pvstats.txt "$K8"/audit.log
K8_START=$(date +%s)

job() {
  label=$1; cap=$2; logf=$3; shift 3
  now=$(date +%s)
  remaining=$((7200 - now + K8_START))
  if [ "$remaining" -le 0 ]; then echo "2-hour limit reached before $label"; return 99; fi
  limit=$cap
  if [ "$remaining" -lt "$limit" ]; then limit=$remaining; fi
  echo "=== $label start $(date +%T) limit=${limit}s"
  nice -n 10 "$PY" "$K8/runlim.py" "$label" "$limit" 3000 "$K8/runs.jsonl" -- nice -n 10 "$@" >> "$logf" 2>&1
  rc=$?
  tail -n 1 "$logf" | cut -c1-300
  return $rc
}

for b in flat:3x4 flat:4x4 cyl:4x4 cyl:4x6 flat:5x6 cyl:3x6 cyl:5x6 cyl:6x5 cyl:7x5 cyl:3x7 cyl:3x8 cyl:2x6 cyl:2x8 \
         cyl:4x7 cyl:4x8 flat:4x6 flat:3x7; do
  job "pvstats $b" 1200 "$K8/log_pvstats.txt" "$PY" "$K8/pv_stats.py" "$b" || echo "pvstats failed: $b"
done

nice -n 10 "$PY" "$K8/summarize.py" > "$K8/summary.json" || exit $?
nice -n 10 "$PY" "$K8/audit.py" > "$K8/audit.log" 2>&1
echo "audit exit code $? (0 = every check passed); see $K8/audit.log"
echo "K8 stage 2 complete"
