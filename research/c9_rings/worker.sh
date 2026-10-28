#!/bin/bash
# worker.sh JOBFILE -- run the jobs of JOBFILE one after the other (one rg pipeline at a time, all under nice 15).
# A job line:  N P NW NB I K OUTPREFIX   [extra drive.py args]
# Several workers (at most 2 at a time on this machine) may share one JOBFILE: a job is claimed with an atomic
# mkdir OUTPREFIX.claim, finished jobs leave OUTPREFIX.done and are skipped.  After a crash remove stale *.claim
# directories by hand (only if no worker is running).
cd "$(dirname "$0")" || exit 1
JOBS="$1"
while read -r N P NW NB I K OUT EXTRA; do
  [ -z "$N" ] && continue
  case "$N" in \#*) continue;; esac
  [ -e "$OUT.done" ] && continue
  mkdir -p "$(dirname "$OUT")"
  mkdir "$OUT.claim" 2>/dev/null || continue
  nice -n 15 python3 -I drive.py "$N" "$P" "$NW" "$NB" "$OUT" --chunk "$I" "$K" $EXTRA 2> "$OUT.err"
  rc=$?
  if [ $rc -eq 0 ]; then touch "$OUT.done"; rmdir "$OUT.claim"; echo "$(date +%H:%M:%S) done $OUT" >> "$(dirname "$OUT")/progress.txt"
  else echo "$(date +%H:%M:%S) FAILED rc=$rc $OUT" >> "$(dirname "$OUT")/progress.txt"; fi
done < "$JOBS"
