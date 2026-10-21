#!/bin/bash
# Launch the e.p.-aware evaluations (run from the project root): bash verify/cylatlas/C3-theory/ep_launch.sh
EPWT=/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt
D=verify/cylatlas/C3-theory/ep
mkdir -p $D
for spec in "flat 1 2 5" "flat 2 2 5" "flat 3 2 4" "flat 3 5 5" "flat 4 2 5" "flat 5 2 5" "ring 3 2 5" "ring 4 2 5" "ring 5 2 5"; do
  set -- $spec
  nohup env PYTHONPATH=$EPWT:. PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verify/cylatlas/C3-theory/ep_run.py $1 $2 $3 $4 $D/$1$2_p$3-$4.jsonl > $D/$1$2_p$3-$4.log 2>&1 &
done
