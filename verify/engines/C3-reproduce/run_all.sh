#!/bin/sh
# From project root. Reruns the worker's reproduce step for base/NMP/SHALLOW with my rebuilt binaries
# (byte-identical to the worker's), plus my independent raw runner.
V=verify/engines/C3-reproduce
( for v in base NMP SHALLOW; do .venv/bin/python $V/run_ablation_redirect.py --depth 16 --timeout 300 --bin "$v=$V/sf/bin/sf_$v"; done ) > $V/run_ablation.out 2>&1 &
( for v in base NMP SHALLOW; do .venv/bin/python $V/raw_runner.py $v $V/sf/bin/sf_$v 16; done ) > $V/raw_runner.out 2>&1 &
wait
echo ALL DONE >> $V/run_ablation.out
