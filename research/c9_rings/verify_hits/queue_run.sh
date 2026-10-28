#!/bin/bash
# queue_run.sh QUEUEFILE  -- run "MODE<TAB>LABEL<TAB>RING" lines one after the other (one cylcgt process at a time, nice 15).
# Run from the project root.  Results are appended to research/c9_rings/verify_hits/cyl_results.tsv by cyl_solve.py.
V=research/c9_rings/verify_hits
while IFS=$'\t' read -r MODE LABEL RING; do
  [ -z "$MODE" ] && continue
  case "$MODE" in \#*) continue;; esac
  echo "$(date +%H:%M:%S) start $LABEL $MODE $RING" >> $V/logs/queue_progress.txt
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. nice -n 15 .venv/bin/python -B $V/cyl_solve.py "$MODE" "$RING" $V/cyl_results.tsv > $V/logs/${LABEL}_${MODE}.log 2>&1
  echo "$(date +%H:%M:%S) end   $LABEL $MODE rc=$?" >> $V/logs/queue_progress.txt
done < "$1"
