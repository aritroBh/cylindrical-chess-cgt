#!/bin/sh
# K6 driver. Run from the project root:  nohup sh kings/delegate/out/K6/run_all.sh BOARD... > kings/delegate/out/K6/driver.log 2>&1 &
# One board at a time: gafni.py (check 1 against kpsolve, signatures, difference tests), then tempo_scan.py,
# then tempo_detail.py (per-placement profiles; asserts agreement with tempo_scan.py).
# runlim.py stops OUR job at 3 GB RSS (single process) or 20 minutes and the board is skipped.
# A check 1 failure (gafni.py exit 2) stops the whole run.
cd "$(dirname "$0")/../../../.." || exit 1
export PYTHONPATH=.
K6=kings/delegate/out/K6
PY=".venv/bin/python"
for b in "$@"; do
  tag=$(echo "$b" | tr ':' '_')
  echo "=== $b start $(date +%T)"
  nice -n 10 $PY $K6/runlim.py "gafni $b" 1200 3000 $K6/runs.jsonl -- nice -n 10 $PY $K6/gafni.py "$b" > "$K6/log_gafni_$tag.txt" 2>&1
  rc=$?
  tail -n 3 "$K6/log_gafni_$tag.txt" | cut -c1-600
  if [ $rc -eq 2 ]; then echo "CHECK 1 FAILED on $b: stopping"; exit 2; fi
  if [ $rc -ne 0 ]; then echo "SKIPPED $b (gafni rc=$rc)"; continue; fi
  nice -n 10 $PY $K6/runlim.py "tempo_scan $b" 1200 3000 $K6/runs.jsonl -- sh -c "nice -n 10 $PY $K6/tempo_scan.py $b >> $K6/tempo_scan.jsonl"
  rc=$?
  if [ $rc -ne 0 ]; then echo "tempo_scan SKIPPED/FAILED $b rc=$rc"; continue; fi
  nice -n 10 $PY $K6/runlim.py "tempo_detail $b" 1200 3000 $K6/runs.jsonl -- nice -n 10 $PY $K6/tempo_detail.py "$b" > "$K6/log_detail_$tag.txt" 2>&1
  rc=$?
  tail -n 2 "$K6/log_detail_$tag.txt" | cut -c1-500
  if [ $rc -ne 0 ]; then echo "tempo_detail FAILED $b rc=$rc"; fi
  echo "=== $b done $(date +%T)"
done
echo ALL-DONE
