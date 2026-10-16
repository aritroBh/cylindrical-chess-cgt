#!/bin/sh
# Atoms (every file occupied) recomputed under all race rules, e.p. on and off.
# Run from the project root:  sh atlas/cylinder/run_sensitivity.sh
set -e
OUT=atlas/cylinder/parts_sens
PY=".venv/bin/python"
export PYTHONPATH=.
$PY atlas/cylinder/atlas_run.py --mode atoms --boards flat --widths 1,2,3,4 --minpawns 2 --maxpawns 4 \
    --rules count,mover,opponent --ep 1,0 --jobs 6 --outdir $OUT
$PY atlas/cylinder/atlas_run.py --mode atoms --boards cyl --widths 3,4 --minpawns 2 --maxpawns 4 \
    --rules count,mover,opponent --ep 1,0 --jobs 6 --outdir $OUT
$PY atlas/cylinder/atlas_run.py --mode atoms --boards cyl --widths 3,4,5 --minpawns 5 --maxpawns 5 \
    --rules count,mover,opponent --ep 1,0 --jobs 6 --outdir $OUT
# All positions with w+b <= 4 on widths 3..8, both boards, under the five alternative rule sets
# (count/e.p.-on is the main atlas in parts/).
$PY atlas/cylinder/atlas_run.py --mode all --boards cyl,flat --widths 3,4,5,6,7,8 --minpawns 2 --maxpawns 4 \
    --rules count,mover,opponent --ep 1,0 --jobs 6 --outdir atlas/cylinder/parts_sens_all
