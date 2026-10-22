#!/bin/bash
# run_queue.sh JOBSFILE [MAXJOBS]
#
# Each line of JOBSFILE is "W NW NB MODE [BIN] [ONLY] [CHUNK_I CHUNK_N] [PROGRESS]".
#   MODE = pilot | full
#   BIN  = frontier_split (default; all nine settings) | frontier_split1
#   ONLY = setting index 0..8 for frontier_split1 (2 = count/epon/aware)
# Runs at most MAXJOBS scans at the same time (each scan is niced inside scan.sh).
set -u
JOBS=$1
MAX=${2:-3}
i=0
while read -r W NW NB MODE BIN ONLY CH_I CH_N PROG; do
    [ -z "${W:-}" ] && continue
    case "$W" in \#*) continue;; esac
    BIN=${BIN:-frontier_split}; ONLY=${ONLY:-2}; CH_I=${CH_I:-0}; CH_N=${CH_N:-1}; PROG=${PROG:-0}
    i=$((i+1))
    ./scan.sh "$W" "$NW" "$NB" "$MODE" "$BIN" "$ONLY" "$CH_I" "$CH_N" "$PROG" &
    while [ "$(jobs -rp | wc -l | tr -d ' ')" -ge "$MAX" ]; do sleep 1; done
done < "$JOBS"
wait
echo "QUEUE COMPLETE: $i jobs"
