#!/bin/zsh
# cylcgt (independent Python solver) on family members; one process at a time, nice 15
cd /Users/aritro/Downloads/Research/Chessendgames
export PYTHONPATH=.
for spec in "even 6" "odd 5" "odd 11" "even 10" "even 12"; do
  set -- ${=spec}
  c=$(.venv/bin/python -c "import sys;sys.path.insert(0,'research/ring_family');from family import *;print(cstr($1($2)))")
  echo "### $1 n=$2: $c"
  nice -n 15 .venv/bin/python research/ring_family/cyl_run.py "$c"
done
echo ALLDONE
