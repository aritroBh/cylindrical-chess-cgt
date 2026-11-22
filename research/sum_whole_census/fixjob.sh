#!/bin/bash
cd /Users/aritro/Downloads/Research/Chessendgames/research/sum_whole_census
f=$(basename $1)
exec nice -n 15 ../../.venv/bin/python census_fix.py data/$f data/fixed/$f > logs/fix_$f.log 2>&1
