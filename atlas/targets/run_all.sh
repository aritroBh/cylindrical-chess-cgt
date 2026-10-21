#!/bin/sh
# Workstream A3-targets: the whole pipeline, in order. Run from the project root:
#   sh atlas/targets/run_all.sh
# Total compute on a 14-core machine shared with other sessions (load 70-160): about 10 CPU-min of C,
# about 15-25 CPU-min of Python analysis; wall time about 40 min.
set -e
T=atlas/targets
PY=".venv/bin/python"
mkdir -p $T/work
cc -O2 -o $T/pcgt $T/pcgt.c

# ---- 1. validation of the C engine against cylcgt databases
PYTHONPATH=. $PY -c "
import json
recs=[json.loads(l) for l in open('atlas/flat8/rerun/values.jsonl')]
recs.sort(key=lambda r:(r['width'], r['nw']+r['nb']))
open('$T/work/db_positions.tsv','w').write(''.join(f\"{r['position']}\t{r['width']}\t0\n\" for r in recs))"
$T/pcgt --printlimit 1000000000 < $T/work/db_positions.tsv > $T/work/pcgt_flat_textbook_count_epon.tsv
$T/pcgt --aware 1 --printlimit 1000000000 < $T/work/db_positions.tsv > $T/work/pcgt_flat_aware_count_epon.tsv
$PY $T/check_db.py atlas/flat8/rerun/values.jsonl $T/work/pcgt_flat_textbook_count_epon.tsv
$PY $T/check_db.py atlas/flat8/values_aware.jsonl.gz $T/work/pcgt_flat_aware_count_epon.tsv
$PY $T/check_cyl.py prepare
$T/pcgt --printlimit 1000000000 < $T/work/cyl_atlas_positions.tsv > $T/work/pcgt_cyl_atlas.tsv
$PY $T/check_cyl.py compare
mkdir -p $T/work/sens && (cd $T/work/sens && tar xzf ../../../cylinder/parts_sens.tar.gz)
$PY $T/check_sens.py

# ---- 2. exact values: 15 settings x (flat, cylinder of the same width)
$PY $T/runs.py db
$PY $T/runs.py w5
$PY $T/runs.py n7 --split 5
$PY $T/runs.py w5n7 --split 5

# ---- 3. analyses
for s in db w5 n7 w5n7; do
  for c in classify matrix targets hot stats; do PYTHONPATH=. $PY $T/analyze.py $c $s > /dev/null; done
done
for s in db w5; do
  PYTHONPATH=. $PY $T/analyze.py cylinder $s > /dev/null
  PYTHONPATH=. $PY $T/analyze.py matrix-cyl $s > /dev/null
done
PYTHONPATH=. $PY $T/summarize.py > /dev/null

# ---- 4. independent checks
PYTHONPATH=. $PY $T/crosscheck.py db          # A2 worker's nimscan --test, 15 settings per target
PYTHONPATH=. $PY $T/crosscheck.py n7
cc -O2 -o $T/work/nimscan_copy $T/work/nimscan_copy.c    # copy of atlas/flat8/rerun/nimscan.c + 1 bound patch
$T/work/nimscan_copy --max 7 > $T/work/nimscan_census_max7.tsv
PYTHONPATH=. $PY $T/crosscheck_census.py
PYTHONPATH= $PY $T/validate_sample.py db 60 20261016
PYTHONPATH= $PY $T/validate_sample.py w5 25 20261016
PYTHONPATH= $PY $T/cylcgt_confirm.py --race count --ep 1 "W: a4 b3 d2 d3 / B: a7 b7 c5" 4 "W: a5 b2 b3 d2 / B: b7 c5 d7" 4
PYTHONPATH= $PY $T/cylcgt_confirm.py --race count --ep 1 --textbook "W: a4 b3 d2 d3 / B: a7 b7 c5" 4 "W: a5 b2 b3 d2 / B: b7 c5 d7" 4
PYTHONPATH= $PY $T/races.py > $T/races_star2_7pawn.out

# ---- 5. headline table, 8x8 freeze/legality, tests
PYTHONPATH=. $PY $T/headline.py $T/work/headline_extra.json > /dev/null
PYTHONPATH=. $PY $T/freeze.py --json $T/work/freeze_w5_in.json --out $T/freeze_w5.json
PYTHONPATH=. $PY -m pytest -q -p no:cacheprovider $T/test_targets.py
