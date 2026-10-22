#!/bin/sh
# Reproduce every K8 result from the project root:
#     nohup sh kings/delegate/out/K8/run.sh > kings/delegate/out/K8/run.log 2>&1 &
# One heavy process at a time, each under `nice -n 10`, <= 20 min and <= 3 GB RSS per job (runlim.py), <= 2 h in total
# (K8_START below; every job's time limit is cut to what is left of the two hours).  Needs only .venv/bin/python (stdlib) and cc.
# Each job is started by runlim.py, which signals only its own process group.  Nothing here kills anything else.
cd "$(dirname "$0")/../../../.." || exit 1
export PYTHONPATH=.
K8=kings/delegate/out/K8
PY=.venv/bin/python

# Start clean inside this task's output directory; the scripts stay.
mkdir -p "$K8/check1"
rm -f "$K8"/flat_*.jsonl "$K8"/cyl_*.jsonl "$K8"/tempo_scan.jsonl \
  "$K8"/chess_tempo_*.jsonl "$K8"/runs.jsonl "$K8"/meta_*.json "$K8"/summary.json \
  "$K8"/tempo_detail_*.json "$K8"/log_*.txt "$K8"/FAILED*.json "$K8"/check1/*.gz \
  "$K8"/ablation_*.json "$K8"/compare_rules.json "$K8"/candidates.json "$K8"/offclass_*.json \
  "$K8"/explain_*.json "$K8"/asym_*.json "$K8"/audit.log

# kpsolve, the independent C solver that check 1 compares with
nice -n 10 cc -O2 -o "$K8/kp" kings/kpsolve.c || exit $?
export K8_START=$(date +%s)

# job LABEL CAP_SECONDS LOGFILE COMMAND...   runs COMMAND under runlim (3000 MB RSS), appending its output to LOGFILE
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
  tail -n 2 "$logf" | cut -c1-300
  return $rc
}

# Task 1: normal play (as in K6).  Required boards, smallest first; a failure stops the run.
sh "$K8/run_all.sh" cyl:5x4 cyl:3x7 cyl:5x7 cyl:3x8 cyl:4x7 cyl:4x8 flat:4x6 flat:3x7 || exit $?

# Task 2: chess stalemate rule.  chess_scan.py runs check 1 (T = 0 against kpsolve) before any scan and
# stops on a difference.
# (the last four are not in the brief: boards whose chess-rule mutual-zugzwang count is small or zero, run as an extra test)
for b in flat:3x4 flat:4x4 cyl:4x4 cyl:4x6 flat:5x6 cyl:3x6 cyl:5x6 cyl:6x5 cyl:7x5 cyl:3x7 cyl:3x8 cyl:2x6 cyl:2x8; do
  tag=$(echo "$b" | tr ':' '_')
  job "chess $b" 1200 "$K8/log_chess_$tag.txt" "$PY" "$K8/chess_scan.py" "$b" || { echo "chess board failed/skipped: $b rc=$?"; exit 1; }
done

# Optional Task 1 boards ("if time allows"): the 2-file cylinders and cyl:6x7.  A failure here does not stop the run.
sh "$K8/run_all.sh" cyl:2x6 cyl:2x8 cyl:6x7 || echo "an optional board failed or was skipped (see runs.jsonl)"

# Direct count of the White-stalemated placements (= the off / off+* class), every board
for b in cyl:5x4 cyl:3x7 cyl:5x7 cyl:3x8 cyl:4x7 cyl:4x8 flat:4x6 flat:3x7 cyl:2x6 cyl:2x8 cyl:6x7 \
         flat:3x4 flat:4x4 cyl:4x4 cyl:4x6 flat:5x6 cyl:3x6 cyl:5x6 cyl:6x5 cyl:7x5; do
  job "offclass $b" 600 "$K8/log_offclass.txt" "$PY" "$K8/offclass.py" "$b" || echo "offclass failed: $b"
done

# Where is a spare move spent?  (mask tests and principal variations, chess rule)
for b in flat:3x4 flat:4x4 cyl:4x4 cyl:4x6 flat:5x6 cyl:3x6 cyl:5x6 cyl:6x5 cyl:7x5 cyl:3x7 cyl:3x8 cyl:2x6 cyl:2x8; do
  job "explain $b" 1200 "$K8/log_explain.txt" "$PY" "$K8/explain.py" "$b" || echo "explain failed: $b"
done

# Whose stalemate rule matters?  Four stalemate rules (White draws / loses x Black draws / loses) on the same placements
for b in flat:3x4 flat:4x4 cyl:4x4 cyl:4x6 flat:5x6 cyl:3x6 cyl:5x6 cyl:6x5 cyl:7x5 cyl:3x7 cyl:3x8 cyl:2x6 cyl:2x8 \
         cyl:4x7 cyl:4x8 flat:4x6 flat:3x7; do
  job "asym $b" 1200 "$K8/log_asym.txt" "$PY" "$K8/asym.py" "$b" || echo "asym failed: $b"
done

# Ablation: which part of the chess rule gives the parity tails?  (experiment, not a rule of the task)
for b in flat:3x4 flat:4x4 cyl:4x4 cyl:4x6 flat:5x6 cyl:3x6 cyl:5x6 cyl:6x5 cyl:7x5; do
  job "ablation $b" 1200 "$K8/log_ablation.txt" "$PY" "$K8/ablation.py" "$b" || echo "ablation failed: $b"
done

# Normal rule against chess rule on the same placements
nice -n 10 "$PY" "$K8/compare_rules.py" > "$K8/compare_rules.json" || echo "compare_rules failed"

# Internal cross-check of the product solver for x (+) n (naive fixed-point solver, no shared code)
for b in flat:3x4 cyl:4x4 flat:4x4 cyl:3x6 cyl:5x4 cyl:4x6; do
  job "naive $b" 900 "$K8/log_naive.txt" "$PY" "$K8/check_naive.py" "$b" || echo "naive check failed: $b"
done

nice -n 10 "$PY" "$K8/summarize.py" > "$K8/summary.json" || exit $?
# Re-derive every headline number from the per-placement files and the gzipped kpsolve inputs/outputs
nice -n 10 "$PY" "$K8/audit.py" > "$K8/audit.log" 2>&1
echo "audit exit code $? (0 = every check passed); see $K8/audit.log"
echo "K8 complete: $K8/summary.json"
