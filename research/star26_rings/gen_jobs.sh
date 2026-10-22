#!/bin/bash
# gen_jobs.sh > JOBSFILE
# Emits the scan queue: every split nw+nb=p for the cylinders in scope.
#
# Binary choice:
#   frontier_split      -- all nine settings (used where the split is cheap)
#   frontier_split1 2   -- default setting only (count/epon/aware), used for the
#                          splits whose full nine-setting run would exceed the
#                          45-minute single-job limit
set -u
emit() {  # emit W nw nb mode bin only
    echo "$1 $2 $3 $4 $5 $6 0 1 0"
}
# --- C6, p=9 (the n+3 prediction) ------------------------------------------
for nw in 4 5 3 6; do emit 6 $nw $((9-nw)) full frontier_split1 2; done
for nw in 2 7 1 8; do emit 6 $nw $((9-nw)) full frontier_split 2; done
# --- C4, p=8,9 -------------------------------------------------------------
for nw in 4 5 3 6; do emit 4 $nw $((9-nw)) full frontier_split1 2; done
for nw in 4 3 5; do emit 4 $nw $((8-nw)) full frontier_split 2; done
for nw in 2 6 1 7; do emit 4 $nw $((8-nw)) full frontier_split 2; done
for nw in 2 7 1 8; do emit 4 $nw $((9-nw)) full frontier_split 2; done
# --- C3, p=7,8,9,10 -------------------------------------------------------
for p in 10 9 8 7; do
    for nw in $(seq 1 $((p-1))); do emit 3 $nw $((p-nw)) full frontier_split 2; done
done
