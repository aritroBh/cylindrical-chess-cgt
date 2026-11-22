#!/bin/bash
cd /Users/aritro/Downloads/Research/Chessendgames/research/sum_whole_census
exec nice -n 15 ../../.venv/bin/python census_cyl.py $1 $2 $3 $4 > logs/c_cyl$1_n$2_s$3of$4.log 2>&1
