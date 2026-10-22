#!/bin/bash
# K5b: exact commands.  Usage (from anywhere):   bash kings/delegate/out/K5b/run.sh     (about 4-5 minutes)
#
# FROM SCRATCH: this script deletes results.jsonl first, so every number is recomputed (identities.py `run` is
# resumable and would otherwise skip every cached item).  One Python process at a time, each under nice -n 10.
#
# Logs:
#   run.log        stdout+stderr of every stage, with a header and the elapsed seconds of each stage
#   spotcheck.txt  output of spotcheck.py alone
#   time.log       `/usr/bin/time -l` over THE WHOLE of this script (all stages, so it is the real wall-clock
#                  time; "maximum resident set size" is the largest single child process, i.e. the peak RSS)
set -euo pipefail

OUT=kings/delegate/out/K5b
if [ -z "${K5B_TIMED:-}" ]; then
  SELF="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  cd /Users/aritro/Downloads/Research/Chessendgames
  echo "command timed below: bash $OUT/run.sh   (the whole script, all stages)" > $OUT/time.log
  K5B_TIMED=1 exec /usr/bin/time -l -a -o $OUT/time.log bash "$SELF"
fi

cd /Users/aritro/Downloads/Research/Chessendgames
export PYTHONPATH=.
PY=.venv/bin/python
LOG=$OUT/run.log

rm -f $OUT/results.jsonl                       # recompute everything
: > $LOG

stage () {                                     # stage <name> <command...>: header, tee into run.log, elapsed seconds
  local name=$1; shift
  local t0=$SECONDS
  echo "### [$name] $*" | tee -a $LOG
  "$@" 2>&1 | tee -a $LOG
  echo "### [$name] done in $((SECONDS - t0)) s" | tee -a $LOG
}

stage sanity    nice -n 10 $PY $OUT/identities.py sanity      # -> sanity.txt; exits 1 (and stops here) on failure
stage guardtest nice -n 10 $PY $OUT/identities.py guardtest   # -> guardtest.txt (watchdog self-test)
stage run       nice -n 10 $PY $OUT/identities.py run 40      # -> results.jsonl; 40-minute budget for this stage
stage tables    nice -n 10 $PY $OUT/identities.py tables      # -> claims.tsv, claims_literal_up2star.tsv, cylcgt.tsv, summary.json
stage controls  nice -n 10 $PY $OUT/identities.py controls    # -> controls.tsv (non-vacuity: G - V' for decoy values V')

# spotcheck.py is stand-alone (does not import identities.py): hand-built cells, output also kept in spotcheck.txt
echo "### [spotcheck] nice -n 10 $PY $OUT/spotcheck.py" | tee -a $LOG
t0=$SECONDS
nice -n 10 $PY $OUT/spotcheck.py 2>&1 | tee $OUT/spotcheck.txt | tee -a $LOG
echo "### [spotcheck] done in $((SECONDS - t0)) s" | tee -a $LOG
echo "### ALL STAGES FINISHED" | tee -a $LOG
