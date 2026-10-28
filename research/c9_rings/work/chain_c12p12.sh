#!/bin/bash
# Start the C12 twelve-pawn scan (2 workers) once the C10 eleven-pawn scan has finished all 2700 jobs.
cd "$(dirname "$0")/.." || exit 1
until [ "$(grep -c done work/c10p11/progress.txt 2>/dev/null)" -ge 2700 ]; do
  grep -q FAILED work/c10p11/progress.txt 2>/dev/null && { echo "c10p11 has FAILED jobs; not starting" > work/chain_c12p12.log; exit 1; }
  sleep 120
done
mkdir -p work/c12p12
nohup ./worker.sh work/jobs_c12p12.txt > /dev/null 2>&1 & echo $! > work/c12p12_workers.pid
sleep 1
nohup ./worker.sh work/jobs_c12p12.txt > /dev/null 2>&1 & echo $! >> work/c12p12_workers.pid
echo "started $(date +%H:%M) $(tr '\n' ' ' < work/c12p12_workers.pid)" > work/chain_c12p12.log
